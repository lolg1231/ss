# 🎮 Xbox Autoclaimer Tool

A powerful Python tool for monitoring Xbox gamertag availability and automatically claiming available tags.

## 🌟 Features

✅ Fast multi-threaded gamertag checking  
✅ Residential proxy rotation with health tracking  
✅ Selenium browser automation with stealth  
✅ Discord webhook notifications  
✅ Modern dark-themed GUI  
✅ Real-time statistics and logging  
✅ Persistent hit tracking  
✅ Error recovery and retry logic  

## 📋 Requirements

- Python 3.8+
- Chrome browser
- Active Xbox account(s)
- Residential proxies (recommended)

## 🚀 Quick Start

### 1. Setup

```bash
git clone https://github.com/lolg1231/ss.git
cd ss
mkdir data logs
pip install -r requirements.txt
```

### 2. Configure

Create `data/gamertags.txt`:
```
coolname
epicgamer
legendplayer
```

Create `data/accounts.txt`:
```
email1@outlook.com:Password123
email2@xbox.com:SecurePass456
```

Create `data/proxies.txt` (optional):
```
123.45.67.89:8080
proxy.service.com:3128
```

### 3. Run

**GUI Mode:**
```bash
python main.py
```

**CLI Mode:**
```bash
python main.py --cli
```

## 📁 File Formats

### gamertags.txt
```
gamertag1
gamertag2
gamertag3
```

### accounts.txt
```
email:password
email2:password2
```

### proxies.txt
```
IP:PORT
IP:PORT:USERNAME:PASSWORD
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
CHECK_WORKERS = 20      # Concurrent checkers
CLAIM_WORKERS = 1       # Sequential claiming
USE_PROXIES = True      # Enable proxies
USE_HEADLESS_BROWSER = True  # Headless Chrome
```

## 🔐 Security

- Never share credentials
- Use fresh, verified accounts only
- Respect Xbox Terms of Service
- Follow responsible automation practices

## 📊 Output

- `data/hits.txt` - Successfully claimed gamertags
- `logs/autoclaimer.log` - Execution logs

## 🆘 Troubleshooting

**No proxies:** Create `data/proxies.txt`  
**Login failed:** Check credentials in `data/accounts.txt`  
**Chrome error:** Run `pip install --upgrade webdriver-manager`

## 📝 License

MIT License - See LICENSE file

---

Made with ❤️ for Xbox gamertag hunters
