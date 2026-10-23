#!/usr/bin/env python3
"""
Discord-Chan Custom: Theme Engine
Generates ultra-lightweight, minimalist pink anime theme CSS for BetterDiscord.
Optimized for 0 lag, zero heavy box-shadows, fixed chat avatars, top-spacing clearance,
and smooth customizable translucency.
"""

import os
import json
import base64

HOME_DIR = os.path.expanduser("~")
BD_DIR = os.path.join(HOME_DIR, ".config", "BetterDiscord")
SETTINGS_FILE = os.path.join(BD_DIR, "anime_theme_settings.json")
THEMES_DIR = os.path.join(BD_DIR, "themes")
THEME_FILE = os.path.join(THEMES_DIR, "WhisperMeALoveSong.theme.css")
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_WALLPAPER = os.path.join(REPO_DIR, "assets", "wallpapers", "1_whisper_me_a_love_song.jpg")

DEFAULT_SETTINGS = {
    "wallpaper_id": "whisper",
    "wallpaper_path": DEFAULT_WALLPAPER,
    "wallpaper_opacity": 0.80,
    "sidebar_opacity": 0.62,
    "chat_opacity": 0.40,
    "wallpaper_blur": 0,
    "accent_color": "#ff85a2",
    "soft_pink": "#fbcfe8",
    "speaking_color": "#ff85a2",
    "tile_opacity": 0.38,
    "tile_radius": 12,
    "profile_opacity": 0.88,
    "top_spacing": 12,
    "font_family": "gg sans, 'Noto Sans', sans-serif",
    "zero_lag": True,
    "chat_avatar_fixed": True,
    "active_preset": "Sakura Soft"
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                res = DEFAULT_SETTINGS.copy()
                res.update(data)
                return res
        except Exception:
            pass
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)

def get_image_data_uri(file_path):
    if not file_path or not os.path.exists(file_path):
        return ""
    try:
        ext = os.path.splitext(file_path)[1].lower().replace(".", "")
        if ext in ("jpg", "jpeg"):
            mime = "image/jpeg"
        elif ext == "png":
            mime = "image/png"
        elif ext == "webp":
            mime = "image/webp"
        else:
            mime = "image/jpeg"
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return f"data:{mime};base64,{b64}"
    except Exception as e:
        print(f"Error encoding image: {e}")
        return ""

def generate_theme_css(settings):
    wp_path = settings.get("wallpaper_path", "")
    data_uri = get_image_data_uri(wp_path)
    if not data_uri and wp_path.startswith("http"):
        data_uri = wp_path

    accent = settings.get("accent_color", "#ff85a2")
    soft_pink = settings.get("soft_pink", "#fbcfe8")
    speaking = settings.get("speaking_color", "#ff85a2")
    wp_opacity = float(settings.get("wallpaper_opacity", 0.80))
    sidebar_op = float(settings.get("sidebar_opacity", 0.62))
    chat_op = float(settings.get("chat_opacity", 0.40))
    tile_opacity = float(settings.get("tile_opacity", 0.38))
    tile_radius = int(settings.get("tile_radius", 12))
    profile_opacity = float(settings.get("profile_opacity", 0.88))
    top_spacing = int(settings.get("top_spacing", 12))
    blur = int(settings.get("wallpaper_blur", 0))

    css = f"""/**
 * @name WhisperMeALoveSong
 * @author Discord-Chan Custom Team
 * @version 2.6.0
 * @description Minimalist Pink Anime Theme featuring Whisper Me a Love Song (Sasakoi). Zero lag, fixed chat avatars, top-spacing clearance, customizable translucency, and sleek voice call UI.
 * @source https://github.com/myzert/discord-chan
 */

:root {{
    --theme-name: "Whisper Me a Love Song (Minimalist Pink Edition)";
    --anime-wallpaper: url('{data_uri}');
    
    /* Aesthetic Pink Color Palette */
    --accent-pink: {accent};
    --accent-pink-soft: {soft_pink};
    --accent-pink-hover: #ff9cb3;
    --accent-pink-active: #fa6d8f;
    --accent-pink-dim: rgba(255, 133, 162, 0.14);
    --accent-pink-glow: rgba(255, 133, 162, 0.35);

    /* Voice & Speaking Indicators */
    --speaking-glow: {speaking};
    --voice-tile-bg: rgba(24, 18, 30, {tile_opacity});
    --voice-tile-radius: {tile_radius}px;

    /* User Profile Card Styling */
    --profile-card-bg: rgba(22, 17, 28, {profile_opacity});

    /* Translucent Background Overlays (Clean Flat Alpha - Zero Shadow Lag) */
    --bg-overlay: rgba(18, 14, 22, {wp_opacity});
    --bg-panels: rgba(24, 18, 29, 0.70);
    --bg-darker: rgba(14, 10, 18, 0.82);
    --bg-sidebar: rgba(20, 15, 24, {sidebar_op});
    --bg-chat-layer: rgba(18, 14, 22, {chat_op});
    --bg-floating: rgba(28, 21, 34, 0.94);

    /* Borders */
    --border-subtle: rgba(255, 133, 162, 0.18);
    --border-focused: rgba(255, 133, 162, 0.45);

    /* Text Colors */
    --text-pure: #ffffff;
    --text-primary: #fdf2f8;
    --text-secondary: #fbcfe8;
    --text-muted: #d4a5b8;

    /* Window Clearance */
    --top-spacing: {top_spacing}px;
}}

/* ========================================================
   TOP SPACING & CLEAN WINDOW CLEARANCE (ANTI-NABRAK)
   ======================================================== */
#app-mount {{
    padding-top: var(--top-spacing) !important;
    background: transparent !important;
}}

/* Clean separation for top bar and headers */
.typeWindows__421ed,
.titleBar__421ed {{
    height: 24px !important;
    margin-bottom: 2px !important;
    background: transparent !important;
}}

/* ========================================================
   GLOBAL ZERO-LAG ANIME WALLPAPER
   ======================================================== */
body {{
    background-color: #120e16 !important;
}}

#app-mount::before {{
    content: "" !important;
    position: fixed !important;
    inset: 0 !important;
    background-image: var(--anime-wallpaper) !important;
    background-size: cover !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    pointer-events: none !important;
    z-index: -2 !important;
    {'filter: blur(' + str(blur) + 'px) !important;' if blur > 0 else ''}
}}

#app-mount::after {{
    content: "" !important;
    position: fixed !important;
    inset: 0 !important;
    background: var(--bg-overlay) !important;
    pointer-events: none !important;
    z-index: -1 !important;
}}

/* ========================================================
   ZERO-LAG ENGINE: REMOVE HEAVY BOX-SHADOWS & CPU BLURS
   ======================================================== */
*, *::before, *::after {{
    box-shadow: none !important;
    text-shadow: none !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
}}

/* ========================================================
   CONTAINER TRANSPARENCY & LAYOUT HARMONY
   ======================================================== */
.app__160d8,
.bg__960e4,
.layer__960e4,
.layers__960e4,
.container__133bf,
.base__357e6,
.content__133bf,
.chat__52833,
.chatContent__52833,
.messagesWrapper__36d07,
.scroller__36d07,
.scrollerContent__36d07,
.pageWrapper_a3a4ce {{
    background: transparent !important;
}}

/* Left Server List */
.guilds__357e6 {{
    background: var(--bg-darker) !important;
    border-right: 1px solid var(--border-subtle) !important;
}}
.guilds__357e6 [class*="folder_"] {{
    background: transparent !important;
}}

/* Channels Sidebar */
.sidebar_c48ade,
.container__2637a {{
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-subtle) !important;
}}

/* Channel & Chat Headers */
.container__9293f,
.title__9293f {{
    background: var(--bg-panels) !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    height: 48px !important;
    padding: 0 16px !important;
}}

/* Chat Message Background Layer */
.chat__52833 {{
    background: var(--bg-chat-layer) !important;
}}

/* Bottom User Bar */
.panels__357e6,
.container_b7e1cb {{
    background: var(--bg-darker) !important;
    border-top: 1px solid var(--border-subtle) !important;
}}

/* Members List */
.membersWrap__5ca65,
.members__5ca65,
.container__5ca65 {{
    background: var(--bg-sidebar) !important;
    border-left: 1px solid var(--border-subtle) !important;
}}

/* ========================================================
   CHAT MESSAGE AREA & AVATAR ALIGNMENT PROTECTION
   ======================================================== */
[class*="message__"] {{
    background: transparent !important;
    transition: background 0.15s ease !important;
    border-radius: 6px !important;
    margin: 1px 8px !important;
}}

[class*="message__"]:hover {{
    background: var(--accent-pink-dim) !important;
}}

/* Avatar subtle pink accent ring */
[class*="avatar__"] {{
    border-radius: 50% !important;
    outline: 2px solid rgba(255, 133, 162, 0.45) !important;
    outline-offset: 1px !important;
    transition: outline-color 0.2s ease !important;
}}
[class*="message__"]:hover [class*="avatar__"] {{
    outline-color: var(--accent-pink) !important;
}}

/* Usernames */
[class*="username__"] {{
    font-weight: 600 !important;
    color: var(--accent-pink-soft) !important;
}}

/* Chat Text Input Bar */
.channelTextArea__74017,
.scrollableContainer__74017 {{
    background: var(--bg-darker) !important;
    border: 1px solid var(--border-focused) !important;
    border-radius: 12px !important;
    margin-bottom: 16px !important;
}}
.channelTextArea__74017:focus-within {{
    border-color: var(--accent-pink) !important;
}}

/* ========================================================
   VOICE CALL & AUDIO UI
   ======================================================== */
[class*="callContainer_"] {{
    background: transparent !important;
}}

/* Participant video & voice tiles */
[class*="tile_"] {{
    background: var(--voice-tile-bg) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--voice-tile-radius) !important;
    transition: border-color 0.2s ease !important;
}}

/* Speaking indicator ring */
[class*="speaking_"] {{
    outline: 3px solid var(--speaking-glow) !important;
    outline-offset: 2px !important;
}}

/* Bottom Floating Call Action Bar (Pill Shape) */
[class*="actionButtons_"],
[class*="bottomControls_"] {{
    background: rgba(22, 17, 28, 0.90) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 28px !important;
    padding: 6px 14px !important;
    margin-bottom: 12px !important;
}}

/* Voice Connected Panel */
[class*="connection_"] {{
    color: var(--accent-pink) !important;
}}

/* ========================================================
   USER PROFILE POPOUT & MODAL
   ======================================================== */
[class*="userProfileOuter_"],
[class*="userProfileModalOuter_"],
[class*="userPopoutOuter_"] {{
    background: var(--profile-card-bg) !important;
    border: 1px solid var(--border-focused) !important;
    border-radius: 18px !important;
}}

[class*="userProfileInner_"] {{
    background: transparent !important;
}}

/* Profile Avatar */
[class*="avatarPositionNormal_"] [class*="avatar_"] {{
    outline: 3px solid var(--accent-pink) !important;
    outline-offset: 2px !important;
}}

/* Roles badges */
[class*="role_"] {{
    background: var(--accent-pink-dim) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
}}

/* ========================================================
   MODALS, SEARCH & CONTEXT MENUS
   ======================================================== */
.menu_c1e9c4,
[class*="menu_"] {{
    background: var(--bg-floating) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
}}

.item_c1e9c4:hover,
[class*="item_"]:hover {{
    background: var(--accent-pink) !important;
    color: #fff !important;
}}

/* Scrollbar */
::-webkit-scrollbar-thumb {{
    background: var(--accent-pink-dim) !important;
    border-radius: 8px !important;
}}
::-webkit-scrollbar-thumb:hover {{
    background: var(--accent-pink) !important;
}}
"""
    return css

def apply_theme(settings=None):
    if settings is None:
        settings = load_settings()
    css_content = generate_theme_css(settings)
    os.makedirs(THEMES_DIR, exist_ok=True)
    with open(THEME_FILE, "w", encoding="utf-8") as f:
        f.write(css_content)
    
    # Also update repo copy
    repo_theme = os.path.join(REPO_DIR, "themes", "WhisperMeALoveSong.theme.css")
    try:
        os.makedirs(os.path.dirname(repo_theme), exist_ok=True)
        with open(repo_theme, "w", encoding="utf-8") as f:
            f.write(css_content)
    except Exception:
        pass

    # BetterDiscord auto-enable
    themes_json_path = os.path.join(BD_DIR, "data", "stable", "themes.json")
    try:
        os.makedirs(os.path.dirname(themes_json_path), exist_ok=True)
        t_data = {}
        if os.path.exists(themes_json_path):
            with open(themes_json_path, "r") as f:
                t_data = json.load(f)
        t_data["WhisperMeALoveSong"] = True
        with open(themes_json_path, "w") as f:
            json.dump(t_data, f, indent=2)
    except Exception as e:
        print(f"Notice: themes.json update: {e}")

    save_settings(settings)
    return True

if __name__ == "__main__":
    settings = load_settings()
    apply_theme(settings)
    print("Theme generated and applied successfully!")
