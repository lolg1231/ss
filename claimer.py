"""
Main Xbox Autoclaimer Core Logic
Orchestrates availability checking and claiming
"""
import threading
import time
from typing import List, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from config import (
    GAMERTAGS_FILE,
    ACCOUNTS_FILE,
    PROXIES_FILE,
    HITS_FILE,
    CHECK_WORKERS,
    BETWEEN_CLAIM_DELAY,
    USE_PROXIES
)

from proxy_manager import ProxyManager
from discord_notifier import DiscordNotifier
from availability_checker import AvailabilityChecker
from browser_claimer import BrowserClaimer


class XboxAutoclaimer:
    """Main orchestrator for gamertag checking and claiming"""
    
    def __init__(self, on_status_update: Optional[Callable] = None):
        self.gamertags: List[str] = []
        self.accounts: List[dict] = []
        self.hits: List[str] = []
        self.available_tags: List[str] = []
        
        self.proxy_manager = ProxyManager() if USE_PROXIES else None
        self.checker = None
        self.notifier = DiscordNotifier()
        
        self.is_running = False
        self.start_time: Optional[float] = None
        self.checked_count = 0
        self.on_status_update = on_status_update
        
        self.lock = threading.Lock()

    def load_gamertags(self) -> bool:
        """Load gamertags from file"""
        try:
            with open(GAMERTAGS_FILE, 'r') as f:
                self.gamertags = [line.strip().lower() for line in f if line.strip() and not line.startswith('#')]
            self._update_status(f"[+] Loaded {len(self.gamertags)} gamertags to check")
            return True
        except FileNotFoundError:
            self._update_status(f"[-] Gamertags file not found: {GAMERTAGS_FILE}")
            return False

    def load_accounts(self) -> bool:
        """Load Xbox accounts from file"""
        try:
            with open(ACCOUNTS_FILE, 'r') as f:
                for line in f:
                    if ':' in line and not line.startswith('#'):
                        email, password = line.strip().split(':', 1)
                        self.accounts.append({'email': email.strip(), 'password': password.strip()})
            self._update_status(f"[+] Loaded {len(self.accounts)} accounts")
            return len(self.accounts) > 0
        except FileNotFoundError:
            self._update_status(f"[-] Accounts file not found: {ACCOUNTS_FILE}")
            return False

    def load_hits(self) -> None:
        """Load previously claimed gamertags"""
        try:
            with open(HITS_FILE, 'r') as f:
                self.hits = [line.strip() for line in f if line.strip()]
            self._update_status(f"[+] Loaded {len(self.hits)} previous hits")
        except FileNotFoundError:
            pass

    def save_hits(self) -> None:
        """Save claimed gamertags to file"""
        try:
            with open(HITS_FILE, 'a') as f:
                for hit in self.hits:
                    f.write(f"{hit}\n")
        except Exception as e:
            self._update_status(f"[-] Error saving hits: {e}")

    def run(self) -> None:
        """Main execution loop"""
        self.is_running = True
        self.start_time = time.time()
        self.checked_count = 0

        if not self.load_gamertags() or not self.load_accounts():
            self._update_status("[-] Failed to load required files")
            return

        self.load_hits()
        self.checker = AvailabilityChecker(self.proxy_manager)

        self._update_status("\\n[*] ===== Xbox Autoclaimer Started =====\"")
        self._update_status(f"[*] Gamertags: {len(self.gamertags)} | Accounts: {len(self.accounts)}")
        
        if self.proxy_manager:
            stats = self.proxy_manager.get_stats()
            self._update_status(f"[*] Proxies: {stats['total_proxies']}")
        
        self._update_status("[*] Phase 1: Checking availability...")
        
        self._check_all_gamertags()
        
        if not self.is_running:
            return
        
        self._update_status(f"[*] Phase 1 Complete: Found {len(self.available_tags)} available tags")
        
        if self.available_tags:
            self._update_status("[*] Phase 2: Claiming available gamertags...")
            self._claim_available_tags()
        
        self.stop()

    def _check_all_gamertags(self) -> None:
        """Check all gamertags for availability"""
        with ThreadPoolExecutor(max_workers=CHECK_WORKERS) as executor:
            futures = {}
            
            for gamertag in self.gamertags:
                if not self.is_running:
                    break
                
                future = executor.submit(self._check_single_gamertag, gamertag)
                futures[future] = gamertag
            
            for future in as_completed(futures):
                if not self.is_running:
                    break
                
                try:
                    future.result()
                except Exception as e:
                    self._update_status(f"[-] Check error: {e}")

    def _check_single_gamertag(self, gamertag: str) -> None:
        """Check a single gamertag"""
        try:
            is_available, error = self.checker.check_availability(gamertag)
            
            with self.lock:
                self.checked_count += 1
            
            if is_available:
                with self.lock:
                    self.available_tags.append(gamertag)
                
                self._update_status(f"[!] AVAILABLE: {gamertag}")
            
            elapsed = time.time() - self.start_time
            rate = self.checked_count / elapsed if elapsed > 0 else 0
            self._update_status(
                f"[*] Checked: {self.checked_count} | "
                f"Rate: {rate:.1f}/sec | "
                f"Available: {len(self.available_tags)}"
            )
        
        except Exception as e:
            self._update_status(f"[-] Error checking {gamertag}: {e}")

    def _claim_available_tags(self) -> None:
        """Attempt to claim all available gamertags"""
        claimer = BrowserClaimer(self.proxy_manager)
        
        for gamertag in self.available_tags:
            if not self.is_running:
                break
            
            if not self.accounts:
                self._update_status("[-] No accounts available for claiming")
                break
            
            account = self.accounts[0]
            
            self._update_status(f"[*] Attempting to claim: {gamertag}")
            success, message = claimer.claim_gamertag(
                account['email'],
                account['password'],
                gamertag
            )
            
            if success:
                with self.lock:
                    self.hits.append(gamertag)
                
                self._update_status(f"[✓] CLAIMED: {gamertag}")
                self.notifier.send_hit_notification(gamertag)
            else:
                self._update_status(f"[-] Failed to claim {gamertag}: {message}")
            
            time.sleep(BETWEEN_CLAIM_DELAY)

    def stop(self) -> None:
        """Stop the autoclaimer"""
        self.is_running = False
        self.save_hits()

        elapsed = time.time() - self.start_time
        hours, remainder = divmod(int(elapsed), 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours}h {minutes}m {seconds}s"

        self._update_status(f"\\n[*] ===== Session Complete =====\"")
        self._update_status(f"[+] Total Checked: {self.checked_count}")
        self._update_status(f"[+] Available Found: {len(self.available_tags)}")
        self._update_status(f"[+] Successfully Claimed: {len(self.hits)}")
        self._update_status(f"[+] Time Elapsed: {time_str}")
        
        if self.checked_count > 0:
            avg_rate = self.checked_count / elapsed
            self._update_status(f"[+] Average Rate: {avg_rate:.2f} checks/sec")
        
        self.notifier.send_completion_notification(
            self.hits,
            self.checked_count,
            time_str
        )

    def _update_status(self, message: str) -> None:
        """Update status message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        print(full_message)
        
        if self.on_status_update:
            self.on_status_update(full_message)
