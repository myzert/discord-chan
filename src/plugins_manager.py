#!/usr/bin/env python3
"""
Discord-Chan Custom: Plugin Manager
Allows 1-click downloading, enabling, and managing popular BetterDiscord plugins.
"""

import os
import urllib.request
import json

HOME = os.path.expanduser("~")
PLUGINS_DIR = os.path.join(HOME, ".config", "BetterDiscord", "plugins")

AVAILABLE_PLUGINS = [
    {
        "id": "ShowHiddenChannels",
        "name": "Show Hidden Channels",
        "author": "JustOptimize",
        "desc": "Displays channels you cannot access and shows information about them.",
        "url": "https://raw.githubusercontent.com/JustOptimize/ShowHiddenChannels/main/ShowHiddenChannels.plugin.js",
        "filename": "ShowHiddenChannels.plugin.js"
    },
    {
        "id": "CompleteTimestamps",
        "name": "Complete Timestamps",
        "author": "DevilBro",
        "desc": "Shows exact timestamps and creation dates in messages and profiles.",
        "url": "https://raw.githubusercontent.com/mwittrien/BetterDiscordAddons/master/Plugins/CompleteTimestamps/CompleteTimestamps.plugin.js",
        "filename": "CompleteTimestamps.plugin.js"
    },
    {
        "id": "ClickableMentions",
        "name": "Clickable Mentions",
        "author": "DevilBro",
        "desc": "Opens user profile or mentions immediately upon clicking.",
        "url": "https://raw.githubusercontent.com/mwittrien/BetterDiscordAddons/master/Plugins/ClickableMentions/ClickableMentions.plugin.js",
        "filename": "ClickableMentions.plugin.js"
    },
    {
        "id": "CharCounter",
        "name": "Character Counter",
        "author": "DevilBro",
        "desc": "Adds a character and word counter to the chat input field.",
        "url": "https://raw.githubusercontent.com/mwittrien/BetterDiscordAddons/master/Plugins/CharCounter/CharCounter.plugin.js",
        "filename": "CharCounter.plugin.js"
    }
]

def get_installed_plugins():
    os.makedirs(PLUGINS_DIR, exist_ok=True)
    installed = []
    for item in AVAILABLE_PLUGINS:
        file_path = os.path.join(PLUGINS_DIR, item["filename"])
        is_installed = os.path.exists(file_path) and os.path.getsize(file_path) > 100
        installed.append({
            **item,
            "installed": is_installed,
            "path": file_path if is_installed else None
        })
    return installed

def install_plugin(plugin_id):
    os.makedirs(PLUGINS_DIR, exist_ok=True)
    target = next((p for p in AVAILABLE_PLUGINS if p["id"] == plugin_id), None)
    if not target:
        return False, f"Plugin {plugin_id} not found"
    
    file_path = os.path.join(PLUGINS_DIR, target["filename"])
    try:
        req = urllib.request.Request(
            target["url"],
            headers={"User-Agent": "Discord-Chan-Plugin-Manager"}
        )
        with urllib.request.urlopen(req, timeout=12) as resp, open(file_path, "wb") as f:
            f.write(resp.read())
        return True, f"Successfully installed {target['name']}"
    except Exception as e:
        return False, f"Failed to download plugin: {e}"

def uninstall_plugin(plugin_id):
    target = next((p for p in AVAILABLE_PLUGINS if p["id"] == plugin_id), None)
    if not target:
        return False, f"Plugin {plugin_id} not found"
    
    file_path = os.path.join(PLUGINS_DIR, target["filename"])
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True, f"Removed {target['name']}"
        return True, "Plugin was not installed"
    except Exception as e:
        return False, f"Failed to remove plugin: {e}"

if __name__ == "__main__":
    print("Installed plugins:", get_installed_plugins())
