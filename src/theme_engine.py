#!/usr/bin/env python3
"""
Discord-Chan Custom: Advanced Universal Theme Engine
Generates ultra-lightweight, customizable Discord theme CSS for BetterDiscord.
Supports:
- Master Toggle (ON / OFF)
- 3 Theme Modes: Anime Wallpaper, See-Through Window Transparency, or Vanilla Discord
- Full Chat Column Translucency & Native Styled Chat Input Box
- Customizable UI Corner Radius (0px to 24px)
- Fixed Embed Cards (clean translucent glass, no muddy shadows)
- Anti-Collision Window Clearance (Top Spacing)
- Zero-Lag Engine & Chat Avatar Grid Guard
Licensed under GNU General Public License v3.0 (GPLv3).
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
DEFAULT_WALLPAPER = os.path.join(REPO_DIR, "assets", "wallpapers", "kaede_to_suzu.webp")

DEFAULT_SETTINGS = {
    "theme_enabled": True,
    "theme_mode": "anime_wallpaper",  # "anime_wallpaper", "window_transparent", "vanilla_discord"
    "wallpaper_id": "kaede_to_suzu",
    "wallpaper_path": DEFAULT_WALLPAPER,
    "wallpaper_opacity": 0.55,        # Darkness overlay for anime wallpaper (0.10 - 0.95)
    "window_darkness": 0.40,          # Background tint for transparent window mode
    "sidebar_opacity": 0.65,          # Sidebar glass translucency
    "guilds_opacity": 0.82,           # Left server rail translucency
    "chat_opacity": 0.0,              # 0.0 = completely transparent so wallpaper or window shines through
    "chat_input_opacity": 0.72,       # Translucent chat input box
    "embed_opacity": 0.75,            # Translucent embed cards
    "corner_radius": 12,              # UI Corner Radius in px (0 - 24)
    "accent_color": "#ff85a2",        # Primary accent
    "soft_pink": "#fbcfe8",           # Secondary pastel
    "speaking_color": "#ff85a2",      # Voice speaking glow
    "tile_opacity": 0.35,             # Voice participant tiles
    "tile_radius": 12,                # Voice tile corner radius
    "profile_opacity": 0.88,          # User profile popout modal
    "top_spacing": 12,                # Window clearance margin
    "font_family": "gg sans, 'Noto Sans', sans-serif",
    "zero_lag": True,                 # Strip CPU blur & shadows
    "chat_avatar_fixed": True,        # Message avatar alignment guard
    "active_preset": "Sakura Soft",
    "show_hidden_channels": False,    # Discord UI: Style locked & hidden channels
    "compact_mode": False,            # Discord UI: Ultra compact message spacing
    "hide_member_list": False,        # Discord UI: Auto-collapse member list
    "hide_server_list": False,        # Discord UI: Auto-collapse guilds sidebar
    "smooth_animations": True,        # Discord UI: Smooth hover transitions
    "mention_glow": True,             # Discord UI: Soft neon glow on mentions & badges
    "blur_avatars": False,            # Discord UI: Blur avatars until hover
    "typing_indicator_fancy": True    # Discord UI: Styled typing bubble
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                res = DEFAULT_SETTINGS.copy()
                res.update(data)
                # Sanitize active_preset: strip any emoji characters
                if "active_preset" in res and isinstance(res["active_preset"], str):
                    for char in ["🌸", "🍓", "🍑", "🍭", "🌺", "💜", "🖤", "✨", "🎀"]:
                        res["active_preset"] = res["active_preset"].replace(char, "")
                    res["active_preset"] = res["active_preset"].strip()
                # Verify wallpaper path exists, else fallback
                if "wallpaper_path" in res and not os.path.exists(res["wallpaper_path"]):
                    kaede_path = os.path.join(REPO_DIR, "assets", "wallpapers", "kaede_to_suzu.webp")
                    whisper_path = os.path.join(REPO_DIR, "assets", "wallpapers", "1_whisper_me_a_love_song.jpg")
                    if os.path.exists(kaede_path):
                        res["wallpaper_path"] = kaede_path
                        res["wallpaper_id"] = "kaede_to_suzu"
                    elif os.path.exists(whisper_path):
                        res["wallpaper_path"] = whisper_path
                        res["wallpaper_id"] = "whisper"
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
        elif ext == "gif":
            mime = "image/gif"
        else:
            mime = "image/jpeg"
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return f"data:{mime};base64,{b64}"
    except Exception as e:
        print(f"Error encoding image: {e}")
        return ""

def clamp_opacity(val, default=0.5):
    try:
        f = float(val)
        if f > 1.0:
            f = f / 100.0
        return max(0.0, min(1.0, f))
    except (ValueError, TypeError):
        return default

def generate_theme_css(settings):
    # Master switch: if theme is disabled, return clean vanilla styles
    if not settings.get("theme_enabled", True) or settings.get("theme_mode") == "vanilla_discord":
        return """/**
 * @name WhisperMeALoveSong
 * @author Discord-Chan Custom Team
 * @version 2.6.0
 * @description Vanilla Discord Mode (Theme Disabled). Clean native Discord client.
 * @source https://github.com/myzert/discord-chan
 */

/* Theme is currently toggled OFF in Discord-Chan Studio */
"""

    mode = settings.get("theme_mode", "anime_wallpaper")
    wp_path = settings.get("wallpaper_path", "")
    data_uri = get_image_data_uri(wp_path) if mode == "anime_wallpaper" else ""
    if not data_uri and wp_path.startswith("http") and mode == "anime_wallpaper":
        data_uri = wp_path

    accent = settings.get("accent_color", "#ff85a2")
    soft_pink = settings.get("soft_pink", "#fbcfe8")
    speaking = settings.get("speaking_color", "#ff85a2")
    wp_opacity = clamp_opacity(settings.get("wallpaper_opacity", 0.55), 0.55)
    win_darkness = clamp_opacity(settings.get("window_darkness", 0.40), 0.40)
    sidebar_op = clamp_opacity(settings.get("sidebar_opacity", 0.65), 0.65)
    guilds_op = clamp_opacity(settings.get("guilds_opacity", 0.82), 0.82)
    chat_input_op = clamp_opacity(settings.get("chat_input_opacity", 0.72), 0.72)
    embed_op = clamp_opacity(settings.get("embed_opacity", 0.75), 0.75)
    corner_radius = int(settings.get("corner_radius", 12))
    tile_opacity = clamp_opacity(settings.get("tile_opacity", 0.35), 0.35)
    tile_radius = int(settings.get("tile_radius", 12))
    profile_opacity = clamp_opacity(settings.get("profile_opacity", 0.88), 0.88)
    top_spacing = int(settings.get("top_spacing", 12))

    # Background layer logic depending on mode
    if mode == "window_transparent":
        bg_wallpaper_css = """
html, body, #app-mount {
    background-color: transparent !important;
    background: transparent !important;
}
#app-mount::before {
    display: none !important;
}
#app-mount::after {
    content: "" !important;
    position: fixed !important;
    inset: 0 !important;
    background: rgba(12, 10, 16, """ + str(win_darkness) + """) !important;
    pointer-events: none !important;
    z-index: -1 !important;
}"""
    else:
        bg_wallpaper_css = """
html, body {
    background-color: #120e16 !important;
}
body {
    background-image: var(--anime-wallpaper) !important;
    background-size: cover !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
}
#app-mount {
    background: transparent !important;
    background-color: transparent !important;
}
#app-mount::before {
    content: "" !important;
    position: fixed !important;
    inset: 0 !important;
    background: var(--bg-overlay) !important;
    pointer-events: none !important;
    z-index: -1 !important;
}
#app-mount::after {
    display: none !important;
}"""

    css = f"""/**
 * @name WhisperMeALoveSong
 * @author Discord-Chan Custom Team
 * @version 2.6.0
 * @description All-Custom Anime & Glass Transparency Theme for Discord. Zero-lag, 100% translucent chat column, customizable corner radius, and safe client-side CSS.
 * @source https://github.com/myzert/discord-chan
 */

:root,
.theme-dark,
.theme-light {{
    --theme-name: "Discord-Chan All-Custom Glass Edition";
    --anime-wallpaper: url('{data_uri}');
    
    /* Aesthetic Color Palette */
    --accent-pink: {accent};
    --accent-pink-soft: {soft_pink};
    --accent-pink-hover: #ff9cb3;
    --accent-pink-active: #fa6d8f;
    --accent-pink-dim: rgba(255, 133, 162, 0.16);
    --accent-pink-glow: rgba(255, 133, 162, 0.35);

    /* UI Corner Radius */
    --ui-corner-radius: {corner_radius}px;

    /* Discord Design System Tokens (Full Chat & Scroller Translucency) */
    --background-primary: transparent !important;
    --background-secondary: rgba(24, 18, 30, {sidebar_op}) !important;
    --background-secondary-alt: rgba(18, 14, 22, 0.78) !important;
    --background-tertiary: rgba(14, 10, 18, {guilds_op}) !important;
    --background-accent: {accent} !important;
    --background-floating: rgba(26, 20, 32, 0.95) !important;
    --channeltextarea-background: rgba(18, 14, 22, {chat_input_op}) !important;
    --chat-background: transparent !important;
    --chat-background-default: transparent !important;
    --bg-base-primary: transparent !important;
    --bg-base-secondary: rgba(24, 18, 30, {sidebar_op}) !important;
    --bg-base-tertiary: rgba(14, 10, 18, {guilds_op}) !important;
    --bg-surface-raised: rgba(22, 17, 28, {embed_op}) !important;
    --bg-surface-overlay: rgba(26, 20, 32, 0.95) !important;

    /* Voice & Speaking Indicators */
    --speaking-glow: {speaking};
    --voice-tile-bg: rgba(24, 18, 30, {tile_opacity});
    --voice-tile-radius: {tile_radius}px;

    /* User Profile Card Styling */
    --profile-card-bg: rgba(22, 17, 28, {profile_opacity});

    /* Translucent Background Overlays */
    --bg-overlay: rgba(14, 11, 18, {wp_opacity});
    --bg-panels: rgba(24, 18, 29, 0.75);
    --bg-darker: rgba(14, 10, 18, {guilds_op});
    --bg-sidebar: rgba(20, 15, 24, {sidebar_op});
    --bg-floating: rgba(28, 21, 34, 0.95);

    /* Clean Borders */
    --border-subtle: rgba(255, 133, 162, 0.22);
    --border-focused: rgba(255, 133, 162, 0.55);

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
    box-sizing: border-box !important;
    padding-top: var(--top-spacing) !important;
    background: transparent !important;
}}

.typeWindows__421ed,
.titleBar__421ed,
[class*="titleBar_"] {{
    height: 24px !important;
    margin-bottom: 2px !important;
    background: transparent !important;
}}

/* ========================================================
   GLOBAL ZERO-LAG BACKGROUND (ANIME OR TRANSPARENT WINDOW)
   ======================================================== */
{bg_wallpaper_css}

/* ========================================================
   ZERO-LAG ENGINE: OPTIMIZED CHAT & SCROLLER HARDWARE ACCELERATION
   ======================================================== */
.messagesWrapper__36d07,
.scroller__36d07,
[class*="messagesWrapper_"],
[class*="scrollerContent_"],
[class*="chatContent_"],
[class*="chat_"] {{
    box-shadow: none !important;
    text-shadow: none !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
}}

/* ========================================================
   CHAT COLUMN & CONTAINER TRANSPARENCY (FIXED ZERO SOLID GREY)
   ======================================================== */
.appDevToolsWrapper__160d8,
[class*="appDevToolsWrapper_"],
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
.pageWrapper_a3a4ce,
[class*="app_"],
[class*="bg_"],
[class*="layer_"],
[class*="layers_"],
[class*="base_"],
[class*="chat_"],
[class*="chatContent_"],
[class*="messagesWrapper_"],
[class*="scroller_"],
[class*="scrollerInner_"],
[class*="scrollerContent_"],
[class*="scrollerBase_"],
[class*="pageWrapper_"],
[class*="subtitleContainer_"],
.chat__52833 > [class*="content_"],
main[class*="chatContent_"] {{
    background: transparent !important;
    background-color: transparent !important;
}}

/* Left Server List (Guilds Rail) */
.guilds__357e6,
[class*="guilds_"] {{
    background: var(--bg-darker) !important;
    border-right: 1px solid var(--border-subtle) !important;
}}
.guilds__357e6 [class*="folder_"],
[class*="guilds_"] [class*="folder_"] {{
    background: transparent !important;
}}

/* Channels Sidebar */
.sidebar_c48ade,
.container__2637a,
[class*="sidebar_"] {{
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-subtle) !important;
}}

/* Channel & Chat Headers */
.container__9293f,
.title__9293f,
[class*="header_"][class*="title_"] {{
    background: var(--bg-panels) !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    height: 48px !important;
    padding: 0 16px !important;
}}

/* Bottom User Bar */
.panels__357e6,
.container_b7e1cb,
[class*="panels_"] {{
    background: var(--bg-darker) !important;
    border-top: 1px solid var(--border-subtle) !important;
}}

/* Members List */
.membersWrap__5ca65,
.members__5ca65,
.container__5ca65,
[class*="membersWrap_"],
[class*="members_"] {{
    background: var(--bg-sidebar) !important;
    border-left: 1px solid var(--border-subtle) !important;
}}

/* ========================================================
   CHAT INPUT BAR (KOLOM MAU CHAT - NO DISRUPTIVE SHADOWS)
   ======================================================== */
[class*="channelBottom_"],
[class*="channelBottom_"]::before,
[class*="channelBottom_"]::after,
form[class*="form_"],
form[class*="form_"]::before,
form[class*="form_"]::after,
[class*="form_"],
[class*="form_"]::before,
[class*="form_"]::after {{
    background: transparent !important;
    background-color: transparent !important;
    background-image: none !important;
    box-shadow: none !important;
    border-top: none !important;
    border: none !important;
}}

form[class*="form_"]::before,
form[class*="form_"]::after,
[class*="channelBottom_"]::before,
[class*="channelBottom_"]::after {{
    display: none !important;
    content: none !important;
}}

.channelTextArea__74017,
.scrollableContainer__74017,
[class*="channelTextArea_"],
[class*="scrollableContainer_"] {{
    background: var(--channeltextarea-background) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--ui-corner-radius) !important;
    margin-bottom: 16px !important;
    box-shadow: none !important;
    filter: none !important;
    transition: border-color 0.2s ease, background 0.2s ease !important;
}}

.channelTextArea__74017:focus-within,
[class*="channelTextArea_"]:focus-within {{
    border-color: var(--accent-pink) !important;
    background: rgba(24, 18, 30, 0.88) !important;
    box-shadow: none !important;
}}

/* Chat Text Input Action Buttons */
[class*="buttons_"] [class*="button_"] {{
    color: var(--accent-pink-soft) !important;
    opacity: 0.85 !important;
    transition: opacity 0.2s ease, color 0.15s ease !important;
}}
[class*="buttons_"] [class*="button_"]:hover {{
    opacity: 1 !important;
    color: var(--accent-pink) !important;
}}

/* Placeholder and typed text */
[class*="placeholder_"],
[class*="textArea_"] {{
    color: #dbdee1 !important;
}}

/* ========================================================
   CHAT MESSAGES & AVATAR ALIGNMENT PROTECTION
   ======================================================== */
[class*="message__"] {{
    background: transparent !important;
    transition: background 0.15s ease !important;
    border-radius: var(--ui-corner-radius) !important;
    margin: 1px 8px !important;
}}

[class*="message__"]:hover {{
    background: var(--accent-pink-dim) !important;
}}

/* Avatar subtle pink ring & fixed alignment guard */
[class*="avatar__"],
[class*="avatarDecoration__"] {{
    border-radius: 50% !important;
    flex-shrink: 0 !important;
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

/* ========================================================
   EMOJI TRANSPARENCY FIX: NO DIRTY BLACK BOXES AROUND EMOJIS
   ======================================================== */
img[class*="emoji_"],
.emoji,
[class*="jumboable_"],
[class*="emojiContainer_"],
[class*="emojiWrapper_"],
[class*="messageEmoji_"] {{
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    filter: none !important;
}}

/* ========================================================
   EMBEDS FIX: NO DIRTY BLACK BOXES & CLEAN TRANSLUCENT CARDS
   ======================================================== */
[class*="embedWrapper_"],
[class*="embed_"],
[class*="embedFull_"],
.embed__734c5 {{
    background: rgba(24, 18, 30, {embed_op}) !important;
    background-color: rgba(24, 18, 30, {embed_op}) !important;
    border: 1px solid var(--border-subtle) !important;
    border-left: 4px solid var(--accent-pink) !important;
    border-radius: var(--ui-corner-radius) !important;
    box-shadow: none !important;
    filter: none !important;
    text-shadow: none !important;
}}

/* Force all inner elements inside embeds to be 100% transparent */
[class*="embedWrapper_"] *,
[class*="embedFull_"] *,
[class*="grid_"],
[class*="embedMargin_"],
[class*="embedSuppressButton_"] {{
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    border-color: transparent !important;
}}

[class*="embedAuthor_"],
[class*="embedTitle_"],
[class*="embedFieldName_"] {{
    color: var(--accent-pink-soft) !important;
    font-weight: 600 !important;
}}

[class*="embedDescription_"],
[class*="embedFieldValue_"] {{
    color: #f2f3f5 !important;
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
    border-radius: var(--ui-corner-radius) !important;
    transition: border-color 0.2s ease !important;
}}

/* Speaking indicator ring */
[class*="speaking_"],
[class*="avatarSpeaking_"],
[class*="borderSpeaking_"] {{
    outline: 3px solid var(--speaking-glow) !important;
    outline-offset: 2px !important;
}}

/* Bottom Floating Call Action Bar */
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
[class*="userPopoutOuter_"],
[class*="biteSizeProfile_"],
[class*="fullSizeProfile_"] {{
    background: var(--profile-card-bg) !important;
    border: 1px solid var(--border-focused) !important;
    border-radius: var(--ui-corner-radius) !important;
}}

[class*="userProfileInner_"] {{
    background: transparent !important;
}}

/* Roles badges */
[class*="role_"] {{
    background: var(--accent-pink-dim) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
}}

/* ========================================================
   MENUS & SCROLLBARS
   ======================================================== */
.menu_c1e9c4,
[class*="menu_"] {{
    background: var(--bg-floating) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--ui-corner-radius) !important;
}}

.item_c1e9c4:hover,
[class*="item_"]:hover {{
    background: var(--accent-pink) !important;
    color: #fff !important;
}}

::-webkit-scrollbar-thumb {{
    background: var(--accent-pink-dim) !important;
    border-radius: 8px !important;
}}
::-webkit-scrollbar-thumb:hover {{
    background: var(--accent-pink) !important;
}}

/* ========================================================
   RESPONSIVE DISCORD WINDOW ADAPTATION (FOLLOW WINDOW SIZE)
   ======================================================== */
@media (max-width: 1100px) {{
    .sidebar_c48ade,
    [class*="sidebar_"] {{
        width: 210px !important;
    }}
}}
@media (max-width: 900px) {{
    .membersWrap__5ca65,
    [class*="membersWrap_"] {{
        min-width: 54px !important;
        width: 54px !important;
        transition: width 0.22s ease !important;
    }}
    .membersWrap__5ca65:hover,
    [class*="membersWrap_"]:hover {{
        width: 240px !important;
    }}
}}
"""
    # ========================================================
    # DISCORD UI ENHANCEMENTS (CONDITIONAL TOGGLES)
    # ========================================================
    enhancements = []
    
    # 1. Hidden & Locked Channels Indicator
    if settings.get("show_hidden_channels", False):
        enhancements.append("""
/* Discord UI Enhancement: Hidden & Locked Channels Indicator */
[class*="modeLocked_"],
[class*="typeLocked_"],
[class*="channel_"][aria-disabled="true"],
li[class*="containerDefault_"]:has([class*="modeLocked_"]) {
    opacity: 0.6 !important;
    filter: grayscale(40%) !important;
}
[class*="modeLocked_"] [class*="icon_"] path,
[class*="typeLocked_"] [class*="icon_"] path {
    fill: #ff85a2 !important;
}
li[class*="containerDefault_"]:has([class*="modeLocked_"]):hover {
    opacity: 0.9 !important;
    filter: grayscale(0%) !important;
}
""")

    # 2. Ultra Compact Mode
    if settings.get("compact_mode", False):
        enhancements.append("""
/* Discord UI Enhancement: Ultra Compact Mode */
[class*="message__"] {
    margin-top: 0px !important;
    margin-bottom: 0px !important;
    padding-top: 2px !important;
    padding-bottom: 2px !important;
    min-height: auto !important;
}
[class*="contents__"] {
    padding-top: 0px !important;
}
[class*="avatar__"] {
    width: 32px !important;
    height: 32px !important;
    top: 2px !important;
}
[class*="containerDefault_"] {
    padding-top: 1px !important;
    padding-bottom: 1px !important;
}
""")

    # 3. Auto-Collapse Member List
    if settings.get("hide_member_list", False):
        enhancements.append("""
/* Discord UI Enhancement: Auto-Collapse Member List */
.membersWrap__5ca65,
[class*="membersWrap_"] {
    min-width: 48px !important;
    width: 48px !important;
    transition: width 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    overflow: hidden !important;
}
.membersWrap__5ca65:hover,
[class*="membersWrap_"]:hover {
    width: 240px !important;
}
""")

    # 4. Auto-Collapse Server List
    if settings.get("hide_server_list", False):
        enhancements.append("""
/* Discord UI Enhancement: Auto-Collapse Server List */
.guilds__357e6,
[class*="guilds_"] {
    width: 14px !important;
    transition: width 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    overflow: hidden !important;
}
.guilds__357e6:hover,
[class*="guilds_"]:hover {
    width: 72px !important;
}
""")

    # 5. Smooth Animations
    if settings.get("smooth_animations", True):
        enhancements.append("""
/* Discord UI Enhancement: Smooth Animations */
[class*="link__"],
[class*="channel_"],
[class*="message__"],
[class*="button_"],
[class*="item_"] {
    transition: background 0.18s cubic-bezier(0.4, 0, 0.2, 1),
                color 0.18s cubic-bezier(0.4, 0, 0.2, 1),
                transform 0.18s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
[class*="channel_"]:hover [class*="link__"] {
    transform: translateX(3px) !important;
}
""")

    # 6. Mention & Unread Soft Neon Glow
    if settings.get("mention_glow", True):
        enhancements.append(f"""
/* Discord UI Enhancement: Mention & Unread Soft Neon Glow */
[class*="mentioned__"] {{
    background: rgba(255, 133, 162, 0.12) !important;
    border-left: 3px solid {accent} !important;
    position: relative !important;
}}
[class*="mentioned__"]::before {{
    content: "" !important;
    position: absolute !important;
    inset: 0 !important;
    background: radial-gradient(circle at left, rgba(255, 133, 162, 0.15) 0%, transparent 70%) !important;
    pointer-events: none !important;
}}
[class*="unreadPill_"],
[class*="badge_"] {{
    background-color: {accent} !important;
    color: #ffffff !important;
}}
""")

    # 7. Privacy Blur Avatars
    if settings.get("blur_avatars", False):
        enhancements.append("""
/* Discord UI Enhancement: Privacy Blur Avatars Until Hover */
[class*="avatar__"]:not(:hover) {
    filter: blur(5px) !important;
    transition: filter 0.2s ease !important;
}
[class*="avatar__"]:hover {
    filter: blur(0px) !important;
}
""")

    # 8. Styled Typing Indicator
    if settings.get("typing_indicator_fancy", True):
        enhancements.append(f"""
/* Discord UI Enhancement: Styled Typing Indicator */
[class*="typing__"] {{
    background: rgba(24, 18, 30, 0.65) !important;
    border-radius: 12px !important;
    padding: 2px 10px !important;
    width: fit-content !important;
    margin-bottom: 2px !important;
}}
[class*="typing__"] [class*="dots_"] span {{
    background-color: {accent} !important;
}}
""")

    if enhancements:
        css += "\n" + "\n".join(enhancements)

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
        # Enable or disable depending on theme_enabled
        is_enabled = settings.get("theme_enabled", True)
        t_data["WhisperMeALoveSong"] = is_enabled
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
