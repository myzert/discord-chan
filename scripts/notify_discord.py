#!/usr/bin/env python3
"""
Discord-Chan Custom: Webhook Notifier
Sends rich embeds and release announcements to Discord channels via environment variable.
Secure: Never hardcodes webhook tokens into source code.
"""

import os
import sys
import json
import urllib.request

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK", os.environ.get("DISCORD_WEBHOOK_URL", "")).strip()

def send_announcement(version="2.6.0", webhook_url=None):
    url = webhook_url or WEBHOOK_URL
    if not url:
        print("Notice: No DISCORD_WEBHOOK environment variable provided. Skipping notification.")
        return True

    payload = {
        "username": "Anime Studio (myzert)",
        "embeds": [
            {
                "title": f"🌸 Discord-Chan Studio v{version}: Official Release!",
                "description": "**Universal Anime Theme Customizer, All-Custom Glass UI & Modular Extension Manager for Discord.**",
                "url": "https://github.com/myzert/discord-chan",
                "color": 16745890,
                "fields": [
                    {
                        "name": "👑 Lead Creator",
                        "value": "myzert (zerttcihuy@gmail.com)",
                        "inline": True
                    },
                    {
                        "name": "📦 Version",
                        "value": f"v{version}",
                        "inline": True
                    },
                    {
                        "name": "✨ Key Features",
                        "value": "• 100% Glass Translucent Chat Column (No solid grey)\n• See-Through Window Mode (View apps behind Discord)\n• All-Custom Wallpapers (Kaede to Suzu & Whisper Me a Love Song)\n• UI Corner Radius Slider (0px - 24px)\n• Modular Chrome-Style ZIP Extensions\n• Theme Export & Import (.zip bundles)",
                        "inline": False
                    },
                    {
                        "name": "🐧 1-Command Linux Installation",
                        "value": "```bash\ncurl -fsSL https://raw.githubusercontent.com/myzert/discord-chan/main/install.sh | bash\n```",
                        "inline": False
                    },
                    {
                        "name": "🪟 1-Command Windows Installation",
                        "value": "```powershell\nirm https://raw.githubusercontent.com/myzert/discord-chan/main/install.ps1 | iex\n```",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "Discord-Chan Studio • GPLv3 License • 100% Client-Side Safe (Not a Nitro Mod)"
                }
            }
        ]
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Discord-Chan-Studio-Notifier"
        }
    )

    try:
        with urllib.request.urlopen(req) as resp:
            print(f"Announcement sent successfully! (HTTP {resp.status})")
            return True
    except Exception as e:
        print(f"Error sending announcement: {e}")
        return False

if __name__ == "__main__":
    send_announcement()
