"""
Browser-based Gamertag Claimer using Selenium
Handles the actual claiming process
"""
import time
from typing import Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from config import (
    USE_HEADLESS_BROWSER,
    BROWSER_TIMEOUT,
    PAGE_LOAD_TIMEOUT
)
from proxy_manager import ProxyManager


class BrowserClaimer:
    """Use Selenium to claim gamertags"""
    
    def __init__(self, proxy_manager: Optional[ProxyManager] = None):
        self.proxy_manager = proxy_manager
        self.driver: Optional[webdriver.Chrome] = None

    def claim_gamertag(self, email: str, password: str, gamertag: str) -> Tuple[bool, str]:
        """
        Attempt to claim a gamertag using browser automation
        Returns: (success, message)
        """
        try:
            self.driver = self._setup_browser()
            
            self.driver.get("https://www.xbox.com/en-US/identity/profile")
            self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
            
            if not self._login(email, password):
                return False, "Login failed"
            
            self.driver.get("https://social.xbox.com/changegamertag")
            time.sleep(2)
            
            if not self._check_and_claim(gamertag):
                return False, "Gamertag unavailable or claim failed"
            
            return True, f"Successfully claimed {gamertag}"
        
        except Exception as e:
            return False, f"Browser error: {str(e)}"
        
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None

    def _setup_browser(self) -> webdriver.Chrome:
        """Setup Selenium WebDriver with options"""
        options = Options()
        
        if USE_HEADLESS_BROWSER:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        if self.proxy_manager:
            proxy = self.proxy_manager.get_proxy()
            if proxy:
                proxy_url = proxy.get('http', '')
                if proxy_url:
                    options.add_argument(f"--proxy-server={proxy_url}")
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=False)
        
        driver.set_script_timeout(BROWSER_TIMEOUT)
        driver.implicitly_wait(5)
        
        return driver

    def _login(self, email: str, password: str) -> bool:
        """Login to Xbox account"""
        try:
            wait = WebDriverWait(self.driver, BROWSER_TIMEOUT)
            
            email_field = wait.until(
                EC.presence_of_element_located((By.ID, "i0116"))
            )
            email_field.clear()
            email_field.send_keys(email)
            
            next_btn = self.driver.find_element(By.ID, "idSIButton9")
            next_btn.click()
            
            time.sleep(1)
            
            password_field = wait.until(
                EC.presence_of_element_located((By.ID, "i0118"))
            )
            password_field.clear()
            password_field.send_keys(password)
            
            signin_btn = self.driver.find_element(By.ID, "idSIButton9")
            signin_btn.click()
            
            time.sleep(3)
            
            return True
        
        except Exception as e:
            print(f"[-] Login error: {e}")
            return False

    def _check_and_claim(self, gamertag: str) -> bool:
        """Check gamertag availability and claim if available"""
        try:
            wait = WebDriverWait(self.driver, BROWSER_TIMEOUT)
            
            gamertag_input = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "gamertag-input"))
            )
            
            gamertag_input.clear()
            gamertag_input.send_keys(gamertag)
            
            check_btn = self.driver.find_element(By.CLASS_NAME, "check-availability-btn")
            check_btn.click()
            
            time.sleep(1)
            
            try:
                available_msg = self.driver.find_element(By.CLASS_NAME, "available-message")
                if not available_msg:
                    return False
            except:
                return False
            
            claim_btn = self.driver.find_element(By.CLASS_NAME, "claim-gamertag-btn")
            claim_btn.click()
            
            time.sleep(2)
            
            try:
                success_msg = self.driver.find_element(By.CLASS_NAME, "success-message")
                return bool(success_msg)
            except:
                return False
        
        except Exception as e:
            print(f"[-] Claim error: {e}")
            return False
