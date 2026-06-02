"""
Gamertag Availability Checker
Checks if gamertags are available using multiple methods
"""
import requests
import time
import random
from typing import Optional, Tuple
from config import (
    TIMEOUT,
    REQUEST_DELAY_MIN,
    REQUEST_DELAY_MAX
)
from proxy_manager import ProxyManager
from fake_useragent import UserAgent


class AvailabilityChecker:
    """Check if Xbox gamertags are available"""
    
    def __init__(self, proxy_manager: Optional[ProxyManager] = None):
        self.proxy_manager = proxy_manager
        self.ua = UserAgent()
        self.session = requests.Session()

    def check_availability(self, gamertag: str) -> Tuple[bool, Optional[str]]:
        """
        Check if a gamertag is available
        Returns: (is_available, error_message)
        """
        time.sleep(random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX))
        return self._check_via_web(gamertag)

    def _check_via_web(self, gamertag: str) -> Tuple[bool, Optional[str]]:
        """
        Check availability via web request
        Uses multiple fallback endpoints
        """
        try:
            headers = {
                'User-Agent': self.ua.random,
                'Accept': 'application/json',
                'Referer': 'https://www.xbox.com/'
            }
            
            endpoints = [
                f"https://xboxgamertag.com/api/gamertag/search/{gamertag.lower()}",
                f"https://gamercards.io/api/v1/gamertag/{gamertag.lower()}"
            ]
            
            proxies = self.proxy_manager.get_proxy() if self.proxy_manager else None
            
            for endpoint in endpoints:
                try:
                    response = requests.get(
                        endpoint,
                        headers=headers,
                        proxies=proxies,
                        timeout=TIMEOUT
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if 'available' in data:
                            is_available = data['available']
                        elif 'exists' in data:
                            is_available = not data['exists']
                        else:
                            continue
                        
                        if self.proxy_manager and proxies:
                            proxy_str = proxies.get('http', '')
                            self.proxy_manager.mark_success(proxy_str)
                        
                        return is_available, None
                
                except requests.exceptions.RequestException as e:
                    if self.proxy_manager and proxies:
                        proxy_str = proxies.get('http', '')
                        self.proxy_manager.mark_failure(proxy_str)
                    continue
            
            return False, "Could not verify availability"
        
        except Exception as e:
            return False, f"Web check failed: {str(e)}"
