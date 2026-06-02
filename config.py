"""
Configuration settings for Xbox Autoclaimer Tool
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ==================== FILE PATHS ====================
GAMERTAGS_FILE = "data/gamertags.txt"
ACCOUNTS_FILE = "data/accounts.txt"
PROXIES_FILE = "data/proxies.txt"
HITS_FILE = "data/hits.txt"

# ==================== DISCORD ====================
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

# ==================== XBOX LIVE API ====================
XBOX_CLIENT_ID = os.getenv("XBOX_CLIENT_ID", "")
XBOX_CLIENT_SECRET = os.getenv("XBOX_CLIENT_SECRET", "")
XBOX_TENANT_ID = os.getenv("XBOX_TENANT_ID", "")

# API Endpoints
MICROSOFT_OAUTH_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
XBOX_AUTH_URL = "https://user.auth.xboxlive.com/user/authenticate"
XBOX_XSTS_URL = "https://xsts.auth.xboxlive.com/xsts/authorize"
XBOX_GAMERTAG_CHECK_URL = "https://gamertag.xboxlive.com/gamertags/available"
XBOX_GAMERTAG_RESERVE_URL = "https://gamertag.xboxlive.com/gamertags/reserve"

# ==================== CHECKING SETTINGS ====================
CHECK_INTERVAL = 2
TIMEOUT = 15
MAX_RETRIES = 3
BATCH_SIZE = 50

# ==================== PROXY SETTINGS ====================
USE_PROXIES = True
PROXY_TIMEOUT = 10
ROTATE_PROXY_EVERY = 5
PROXY_RANDOMIZE = True

# ==================== THREADING ====================
MAX_WORKERS = 15
CHECK_WORKERS = 20
CLAIM_WORKERS = 1

# ==================== SELENIUM SETTINGS ====================
USE_HEADLESS_BROWSER = True
BROWSER_TIMEOUT = 30
PAGE_LOAD_TIMEOUT = 20

# ==================== RATE LIMITING ====================
REQUEST_DELAY_MIN = 1
REQUEST_DELAY_MAX = 3
BETWEEN_CLAIM_DELAY = 5

# ==================== LOGGING ====================
LOG_LEVEL = "INFO"
LOG_FILE = "logs/autoclaimer.log"

# ==================== USER AGENTS ====================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]
