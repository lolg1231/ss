"""
Discord Webhook Notifications Handler
"""
import requests
import json
from typing import List
from config import DISCORD_WEBHOOK_URL
from datetime import datetime


class DiscordNotifier:
    """Send notifications to Discord webhook"""
    
    def __init__(self, webhook_url: str = DISCORD_WEBHOOK_URL):
        self.webhook_url = webhook_url
        self.enabled = bool(webhook_url)

    def send_completion_notification(self, hits: List[str], total_checked: int, time_elapsed: str) -> bool:
        """Send notification when claiming session is complete"""
        if not self.enabled:
            return False

        hits_text = "\\n".join(hits[:50]) if hits else "None"
        if len(hits) > 50:
            hits_text += f"\\n... and {len(hits) - 50} more"

        embed = {
            "title": "🎮 Xbox Autoclaimer - Session Complete!",
            "color": 3066993,
            "fields": [
                {
                    "name": "Total Checked",
                    "value": f"{total_checked}",
                    "inline": True
                },
                {
                    "name": "Successful Claims",
                    "value": f"{len(hits)}",
                    "inline": True
                },
                {
                    "name": "Time Elapsed",
                    "value": time_elapsed,
                    "inline": True
                },
                {
                    "name": "Claimed Gamertags",
                    "value": hits_text,
                    "inline": False
                }
            ],
            "timestamp": datetime.now().isoformat(),
            "footer": {
                "text": "Xbox Autoclaimer Tool"
            }
        }

        return self._send_embed(embed)

    def send_hit_notification(self, gamertag: str) -> bool:
        """Send notification when a gamertag is successfully claimed"""
        if not self.enabled:
            return False

        embed = {
            "title": "✅ Gamertag Claimed!",
            "color": 65280,
            "fields": [
                {
                    "name": "Gamertag",
                    "value": f"**{gamertag}**",
                    "inline": False
                }
            ],
            "timestamp": datetime.now().isoformat()
        }

        return self._send_embed(embed)

    def _send_embed(self, embed: dict) -> bool:
        """Internal method to send embed to webhook"""
        if not self.webhook_url:
            return False

        payload = {"embeds": [embed]}

        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"[-] Failed to send Discord notification: {e}")
            return False
