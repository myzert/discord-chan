#!/usr/bin/env python3
"""
Discord-Chan Custom: BetterDiscord Auto-Injector
Detects Discord desktop core and injects BetterDiscord safely.
"""

import os
import glob
import urllib.request
import json
import shutil

HOME = os.path.expanduser("~")
BD_DIR = os.path.join(HOME, ".config", "BetterDiscord")
BD_ASAR = os.path.join(BD_DIR, "data", "betterdiscord.asar")
BD_ASAR_URL = "https://github.com/BetterDiscord/BetterDiscord/releases/latest/download/betterdiscord.asar"

def get_discord_core_paths():
    search_patterns = [
        os.path.join(HOME, ".config", "discord", "app-*", "modules", "discord_desktop_core-*", "discord_desktop_core", "index.js"),
        os.path.join(HOME, ".var", "app", "com.discordapp.Discord", "config", "discord", "app-*", "modules", "discord_desktop_core-*", "discord_desktop_core", "index.js"),
        "/opt/discord/resources/app/discord_desktop_core/index.js",
        "/usr/share/discord/resources/app/discord_desktop_core/index.js"
    ]
    results = []
    for pattern in search_patterns:
        matches = glob.glob(pattern)
        results.extend(matches)
    return results

def ensure_bd_asar():
    os.makedirs(os.path.dirname(BD_ASAR), exist_ok=True)
    if not os.path.exists(BD_ASAR) or os.path.getsize(BD_ASAR) < 100000:
        print("Downloading BetterDiscord asar package...")
        try:
            req = urllib.request.Request(
                BD_ASAR_URL,
                headers={"User-Agent": "Discord-Chan-Custom-Installer"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp, open(BD_ASAR, "wb") as f:
                shutil.copyfileobj(resp, f)
            print(f"Downloaded betterdiscord.asar ({os.path.getsize(BD_ASAR)} bytes)")
        except Exception as e:
            print(f"Download failed: {e}")
            return False
    return os.path.exists(BD_ASAR)

def check_status():
    core_files = get_discord_core_paths()
    if not core_files:
        return {
            "installed": False,
            "injected": False,
            "message": "Discord installation not found"
        }
    
    target_core = core_files[0]
    injected = False
    try:
        with open(target_core, "r", encoding="utf-8") as f:
            content = f.read()
            if "betterdiscord.asar" in content or "BetterDiscord" in content:
                injected = True
    except Exception as e:
        pass

    return {
        "installed": True,
        "injected": injected,
        "core_path": target_core,
        "bd_asar_exists": os.path.exists(BD_ASAR)
    }

def inject():
    core_files = get_discord_core_paths()
    if not core_files:
        return False, "Could not find Discord desktop core index.js"
    
    if not ensure_bd_asar():
        return False, "Failed to obtain betterdiscord.asar"
    
    target_core = core_files[0]
    
    # Backup original if not yet backed up
    backup_file = target_core + ".backup"
    if not os.path.exists(backup_file):
        try:
            shutil.copy2(target_core, backup_file)
        except Exception:
            pass

    injection_code = f'require("{BD_ASAR}");\nmodule.exports = require(\'./core.asar\');\n'
    try:
        with open(target_core, "w", encoding="utf-8") as f:
            f.write(injection_code)
        
        # Ensure BD directories exist
        os.makedirs(os.path.join(BD_DIR, "themes"), exist_ok=True)
        os.makedirs(os.path.join(BD_DIR, "plugins"), exist_ok=True)
        os.makedirs(os.path.join(BD_DIR, "data", "stable"), exist_ok=True)

        return True, f"Successfully injected BetterDiscord into {target_core}"
    except Exception as e:
        return False, f"Injection error: {e}"

def uninject():
    core_files = get_discord_core_paths()
    if not core_files:
        return False, "Discord installation not found"
    
    target_core = core_files[0]
    backup_file = target_core + ".backup"
    try:
        if os.path.exists(backup_file):
            shutil.copy2(backup_file, target_core)
            return True, "Restored original index.js from backup"
        else:
            with open(target_core, "w", encoding="utf-8") as f:
                f.write("module.exports = require('./core.asar');\n")
            return True, "Reset index.js to default"
    except Exception as e:
        return False, f"Uninjection error: {e}"

if __name__ == "__main__":
    st = check_status()
    print("BetterDiscord Status:", st)
    if not st.get("injected"):
        ok, msg = inject()
        print("Inject result:", ok, msg)
