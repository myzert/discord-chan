#!/usr/bin/env python3
"""
Discord-Chan Custom: BetterDiscord Addon Store & Downloader
Allows direct 1-click download, installation, and management of BetterDiscord
Themes (UI) and Plugins from official community repositories.
Powered by BetterDiscord Engine.
"""

import os
import sys
import shutil
import urllib.request
import urllib.parse

HOME = os.path.expanduser("~")

def get_bd_dirs():
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA", os.path.join(HOME, "AppData", "Roaming"))
        base_dir = os.path.join(appdata, "BetterDiscord")
    else:
        base_dir = os.path.join(HOME, ".config", "BetterDiscord")
    
    themes_dir = os.path.join(base_dir, "themes")
    plugins_dir = os.path.join(base_dir, "plugins")
    os.makedirs(themes_dir, exist_ok=True)
    os.makedirs(plugins_dir, exist_ok=True)
    return base_dir, themes_dir, plugins_dir

# Curated catalog of high quality BetterDiscord community themes and plugins
CURATED_ADDONS = [
    # THEMES (UI)
    {
        "id": "clearvision",
        "name": "ClearVision v6",
        "type": "theme",
        "author": "ClearVision Team",
        "version": "6.9.0",
        "filename": "ClearVision_v6.theme.css",
        "url": "https://raw.githubusercontent.com/ClearVision/ClearVision-v6/master/ClearVision_v6.theme.css",
        "description": "One of the most famous glass and transparent themes for BetterDiscord with vivid accent customization.",
        "tag": "Glass UI"
    },
    {
        "id": "translucence",
        "name": "Translucence",
        "type": "theme",
        "author": "CapnKitten",
        "version": "1.3.4",
        "filename": "Translucence.theme.css",
        "url": "https://raw.githubusercontent.com/CapnKitten/Translucence/master/Translucence.theme.css",
        "description": "Clean, highly readable translucent frosted glass theme with sleek modern styling and customizable acrylic blur.",
        "tag": "Frosted Glass"
    },
    {
        "id": "frostedglass",
        "name": "Frosted Glass",
        "type": "theme",
        "author": "Gibbu",
        "version": "2.0.1",
        "filename": "FrostedGlass.theme.css",
        "url": "https://raw.githubusercontent.com/Gibbu/BetterDiscord-Themes/master/FrostedGlass/FrostedGlass.theme.css",
        "description": "True glassmorphism frosted glass interface for Discord with smooth blurred background support.",
        "tag": "Glassmorphism"
    },
    {
        "id": "darkmatter",
        "name": "Dark Matter",
        "type": "theme",
        "author": "Chippy & Beard",
        "version": "3.1.0",
        "filename": "DarkMatter.theme.css",
        "url": "https://raw.githubusercontent.com/DiscordStyles/DarkMatter/deploy/DarkMatter.theme.css",
        "description": "A dark, modern, and minimalist glass theme inspired by IDE interfaces with clean typography.",
        "tag": "Minimalist Dark"
    },
    {
        "id": "radialstatus",
        "name": "RadialStatus",
        "type": "theme",
        "author": "Gibbu",
        "version": "2.0.4",
        "filename": "RadialStatus.theme.css",
        "url": "https://raw.githubusercontent.com/DiscordStyles/RadialStatus/deploy/RadialStatus.theme.css",
        "description": "Transforms avatar online/offline status indicators into neon circular rings wrapping member profile pictures.",
        "tag": "Avatar Polish"
    },
    {
        "id": "basicbackground",
        "name": "BasicBackground",
        "type": "theme",
        "author": "DevilBro",
        "version": "1.0.8",
        "filename": "BasicBackground.theme.css",
        "url": "https://raw.githubusercontent.com/DevilBro/BetterDiscordStuff/master/Themes/BasicBackground/BasicBackground.theme.css",
        "description": "Lightweight BetterDiscord base theme allowing customizable background images and overlay opacity.",
        "tag": "Base Theme"
    },

    # PLUGINS
    {
        "id": "showhiddenchannels",
        "name": "ShowHiddenChannels",
        "type": "plugin",
        "author": "JustAWumpus",
        "version": "3.1.5",
        "filename": "ShowHiddenChannels.plugin.js",
        "url": "https://raw.githubusercontent.com/JustAWumpus/ShowHiddenChannels/main/ShowHiddenChannels.plugin.js",
        "description": "Displays hidden channels in server lists with permission locks, topic details, and member access requirements.",
        "tag": "Server Utility"
    },
    {
        "id": "betterrolecolors",
        "name": "BetterRoleColors",
        "type": "plugin",
        "author": "DevilBro",
        "version": "1.0.4",
        "filename": "BetterRoleColors.plugin.js",
        "url": "https://raw.githubusercontent.com/DevilBro/BetterDiscordStuff/master/Plugins/BetterRoleColors/BetterRoleColors.plugin.js",
        "description": "Applies role colors to entire usernames in chat, member lists, voice channels, and user mentions.",
        "tag": "Color Enhance"
    },
    {
        "id": "voiceevents",
        "name": "VoiceEvents",
        "type": "plugin",
        "author": "DevilBro",
        "version": "1.1.2",
        "filename": "VoiceEvents.plugin.js",
        "url": "https://raw.githubusercontent.com/DevilBro/BetterDiscordStuff/master/Plugins/VoiceEvents/VoiceEvents.plugin.js",
        "description": "Text-to-Speech audio notifications when someone connects, disconnects, or moves between voice channels.",
        "tag": "Voice Audio"
    },
    {
        "id": "permissionsviewer",
        "name": "PermissionsViewer",
        "type": "plugin",
        "author": "DevilBro",
        "version": "1.0.2",
        "filename": "PermissionsViewer.plugin.js",
        "url": "https://raw.githubusercontent.com/DevilBro/BetterDiscordStuff/master/Plugins/PermissionsViewer/PermissionsViewer.plugin.js",
        "description": "Inspect all server permissions, channel overrides, and roles of any user directly via context menu.",
        "tag": "Moderation"
    },
    {
        "id": "translator",
        "name": "Translator",
        "type": "plugin",
        "author": "DevilBro",
        "version": "1.4.1",
        "filename": "Translator.plugin.js",
        "url": "https://raw.githubusercontent.com/DevilBro/BetterDiscordStuff/master/Plugins/Translator/Translator.plugin.js",
        "description": "Translates incoming and outgoing Discord messages on-the-fly using Google Translate and DeepL engines.",
        "tag": "Productivity"
    },
    {
        "id": "studiohotkey",
        "name": "DiscordChanStudioHotkey",
        "type": "plugin",
        "author": "myzert",
        "version": "2.6.0",
        "filename": "DiscordChanStudioHotkey.plugin.js",
        "url": "local",
        "description": "Official Discord-Chan BetterDiscord plugin that binds Ctrl+Shift+P to open the Studio Control Center instantly.",
        "tag": "Core Studio"
    }
]

def get_installed_addons():
    _, themes_dir, plugins_dir = get_bd_dirs()
    installed = {"theme": set(), "plugin": set()}
    
    if os.path.exists(themes_dir):
        for f in os.listdir(themes_dir):
            if f.endswith(".css"):
                installed["theme"].add(f)
                
    if os.path.exists(plugins_dir):
        for f in os.listdir(plugins_dir):
            if f.endswith(".js"):
                installed["plugin"].add(f)
                
    return installed

def is_addon_installed(addon_type, filename):
    _, themes_dir, plugins_dir = get_bd_dirs()
    target_dir = themes_dir if addon_type == "theme" else plugins_dir
    target_path = os.path.join(target_dir, filename)
    return os.path.exists(target_path) and os.path.getsize(target_path) > 0

def download_addon(addon_dict):
    _, themes_dir, plugins_dir = get_bd_dirs()
    addon_type = addon_dict["type"]
    filename = addon_dict["filename"]
    url = addon_dict["url"]
    
    target_dir = themes_dir if addon_type == "theme" else plugins_dir
    target_path = os.path.join(target_dir, filename)
    
    # If local plugin
    if url == "local":
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_dir = os.path.dirname(script_dir)
        local_src = os.path.join(repo_dir, "plugins", filename)
        if os.path.exists(local_src):
            shutil.copy2(local_src, target_path)
            return True, f"Installed {filename} from local repository."
        return False, f"Local plugin file not found: {local_src}"
        
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Discord-Chan-Store/2.6.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
            if len(content) < 50:
                return False, "Downloaded file is empty or invalid."
            with open(target_path, "wb") as f:
                f.write(content)
        return True, f"Successfully downloaded and installed {filename} to BetterDiscord {addon_type}s!"
    except Exception as e:
        if os.path.exists(target_path):
            try:
                os.remove(target_path)
            except Exception:
                pass
        return False, f"Download error: {str(e)}"

def uninstall_addon(addon_type, filename):
    _, themes_dir, plugins_dir = get_bd_dirs()
    target_dir = themes_dir if addon_type == "theme" else plugins_dir
    target_path = os.path.join(target_dir, filename)
    
    if os.path.exists(target_path):
        try:
            os.remove(target_path)
            return True, f"Uninstalled {filename} from BetterDiscord."
        except Exception as e:
            return False, f"Failed to delete {filename}: {str(e)}"
    return False, f"File {filename} not found."

def install_custom_url(url):
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        return False, "Invalid URL format. Please start with http:// or https://"
        
    parsed = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed.path)
    
    if filename.endswith(".theme.css") or filename.endswith(".css"):
        addon_type = "theme"
    elif filename.endswith(".plugin.js") or filename.endswith(".js"):
        addon_type = "plugin"
    else:
        # Default by query or extension
        if ".theme.css" in url:
            addon_type = "theme"
            filename = "custom_theme.theme.css"
        elif ".plugin.js" in url:
            addon_type = "plugin"
            filename = "custom_plugin.plugin.js"
        else:
            return False, "URL must point to a .theme.css or .plugin.js file."
            
    custom_addon = {
        "id": "custom",
        "name": filename,
        "type": addon_type,
        "filename": filename,
        "url": url
    }
    return download_addon(custom_addon)
