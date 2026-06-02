"""
Advanced Proxy Manager with failure handling and rotation
"""
import random
import time
from typing import List, Optional, Dict
from config import PROXIES_FILE, ROTATE_PROXY_EVERY, PROXY_RANDOMIZE


class ProxyManager:
    def __init__(self):
        self.proxies: List[str] = []
        self.proxy_health: Dict[str, dict] = {}
        self.current_index = 0
        self.request_count = 0
        self.load_proxies()

    def load_proxies(self) -> None:
        """Load proxies from file and initialize health tracking"""
        try:
            with open(PROXIES_FILE, 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            for proxy in self.proxies:
                self.proxy_health[proxy] = {
                    'failures': 0,
                    'successes': 0,
                    'last_used': 0
                }
            
            print(f"[+] Loaded {len(self.proxies)} proxies")
        except FileNotFoundError:
            print(f"[!] Proxies file not found: {PROXIES_FILE}")
            self.proxies = []

    def get_proxy(self) -> Optional[dict]:
        """Get next proxy in rotation or random"""
        if not self.proxies:
            return None

        if PROXY_RANDOMIZE:
            proxy = random.choice(self.proxies)
        else:
            proxy = self.proxies[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.proxies)

        self.request_count += 1
        self.proxy_health[proxy]['last_used'] = time.time()

        return self._format_proxy(proxy)

    def _format_proxy(self, proxy: str) -> dict:
        """Format proxy string to requests format"""
        return {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }

    def mark_success(self, proxy: str) -> None:
        """Mark proxy as successful"""
        if proxy in self.proxy_health:
            self.proxy_health[proxy]['successes'] += 1
            self.proxy_health[proxy]['failures'] = 0

    def mark_failure(self, proxy: str) -> None:
        """Mark proxy as failed"""
        if proxy in self.proxy_health:
            self.proxy_health[proxy]['failures'] += 1

    def get_healthy_proxies(self) -> List[str]:
        """Get list of healthy proxies"""
        return [p for p in self.proxies if self.proxy_health[p]['failures'] < 3]

    def reset_health(self) -> None:
        """Reset all proxy health metrics"""
        for proxy in self.proxy_health:
            self.proxy_health[proxy]['failures'] = 0
            self.proxy_health[proxy]['successes'] = 0

    def reload_proxies(self) -> None:
        """Reload proxies from file"""
        self.proxies.clear()
        self.proxy_health.clear()
        self.load_proxies()
        self.current_index = 0
        self.request_count = 0

    def get_stats(self) -> dict:
        """Get proxy statistics"""
        total_success = sum(p['successes'] for p in self.proxy_health.values())
        total_failures = sum(p['failures'] for p in self.proxy_health.values())
        return {
            'total_proxies': len(self.proxies),
            'healthy_proxies': len(self.get_healthy_proxies()),
            'total_success': total_success,
            'total_failures': total_failures
        }
