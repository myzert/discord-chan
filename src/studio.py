#!/usr/bin/env python3
"""
Discord-Chan Studio: Official Discord Client Styled Dashboard
Universal Anime Theme Customizer & Extension Manager for Discord.
Features:
- Master Theme Toggle (ON / OFF)
- 3 Modes: Anime Wallpaper, See-Through Window Transparency, Vanilla Discord
- 100% Translucent Chat Column & Native Styled Chat Input Box
- Customizable UI Corner Radius (0px to 24px)
- Fixed Embed Cards (no muddy shadows, crisp colored border)
- All-Custom Wallpaper Manager with Live Thumbnails & Manual File Browser
- Export & Import Custom Themes (.zip format)
- Modular Plugin / Extension System (.zip Chrome-style packages)
- Safe Client-Side CSS, Anti-Collision Top Spacing, Zero-Lag Engine
Licensed under GNU General Public License v3.0 (GPLv3).
"""

import os
import sys
import json
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageTk

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

import theme_engine
import bd_injector
import bd_customizer
import icon_manager
import plugins_manager
import theme_packager
import extensions_system

# Discord-Chan Studio Modern Creative Palette (Distinct Studio Aesthetic)
C_GUILDS    = "#10121a"  # Deep studio obsidian workspace rail
C_SIDEBAR   = "#161822"  # Slate sidebar
C_CONTENT   = "#0f1118"  # Main canvas surface
C_CARD      = "#1a1d29"  # Elevated card surface
C_CARD_ALT  = "#141620"  # Dark inset / sub-card surface
C_HEADER    = "#151722"  # Top navigation bar
C_BORDER    = "#25293a"  # Crisp border separator
C_BLURPLE   = "#5865f2"  # Blurple brand
C_BLURPLE_H = "#4752c4"
C_PINK      = "#ff7597"  # Studio Sakura Pink accent
C_CYAN      = "#38bdf8"  # Neon Cyan highlight
C_PURPLE    = "#a78bfa"  # Cyber Violet / BetterDiscord accent
C_GREEN     = "#22c55e"  # Active emerald
C_GREEN_H   = "#16a34a"
C_RED       = "#f43f5e"  # Alert / Delete red
C_TEXT      = "#e2e8f0"  # Primary bright text
C_TEXT_H    = "#ffffff"  # Pure white header text
C_MUTED     = "#8e99a8"  # Muted secondary text

WALLPAPERS = [
    {
        "id": "kaede_to_suzu",
        "name": "Kaede to Suzu The Animation",
        "tag": "ANIME MAID TWINS UI MOD",
        "desc": "Maid Twins Anime (1920x1080 Full HD)",
        "details": "Brings the iconic Kaede and Suzu maid twin aesthetic to Discord. Overrides core Discord design tokens with crystal-clear chat translucency, soft sakura pink accent highlights, and crisp translucent embed cards without grey obstruction.",
        "recommended_radius": "12px",
        "recommended_opacity": "0.55",
        "accent_name": "Sakura Pink (#ff85a2)",
        "accent_hex": "#ff85a2",
        "path": os.path.join(REPO_DIR, "assets", "wallpapers", "kaede_to_suzu.webp")
    },
    {
        "id": "whisper",
        "name": "Whisper Me a Love Song",
        "tag": "YURI PASTEL ROMANCE UI MOD",
        "desc": "Sasayaku You ni Koi wo Utau (Yori & Himari)",
        "details": "A tender, heartwarming pastel theme inspired by the music and romance of Whisper Me a Love Song. Features warm strawberry-rose tones, translucent member lists, and smooth rounded channel buttons for a cozy chatting vibe.",
        "recommended_radius": "14px",
        "recommended_opacity": "0.50",
        "accent_name": "Strawberry Rose (#fb7185)",
        "accent_hex": "#fb7185",
        "path": os.path.join(REPO_DIR, "assets", "wallpapers", "1_whisper_me_a_love_song.jpg")
    },
    {
        "id": "sakura",
        "name": "Sakura Blossom Minimalist",
        "tag": "MINIMALIST SPRING UI MOD",
        "desc": "Japanese Cherry Blossom Aesthetic",
        "details": "Delicate cherry blossom petals falling gracefully across a soft twilight sky. Tailored for maximum text readability and distraction-free voice chat with subtle translucent backdrops and calming pastel peach accents.",
        "recommended_radius": "10px",
        "recommended_opacity": "0.45",
        "accent_name": "Pastel Peach (#f472b6)",
        "accent_hex": "#f472b6",
        "path": os.path.join(REPO_DIR, "assets", "wallpapers", "2_sakura_blossom_minimal.jpg")
    },
    {
        "id": "clouds",
        "name": "Pastel Sunset Clouds",
        "tag": "DUSK TWILIGHT SKY UI MOD",
        "desc": "Soft Evening Pastel Scenery",
        "details": "A breathtaking purple-gold sunset horizon that turns Discord into a tranquil twilight sanctuary. Combines deep violet glow accents with frosted translucent containers for long evening gaming and study sessions.",
        "recommended_radius": "12px",
        "recommended_opacity": "0.60",
        "accent_name": "Violet Glow (#c084fc)",
        "accent_hex": "#c084fc",
        "path": os.path.join(REPO_DIR, "assets", "wallpapers", "3_pastel_clouds_scenery.jpg")
    },
    {
        "id": "neko",
        "name": "Discord-Chan Neko Mascot",
        "tag": "DARK CYBER NEKO MASCOT MOD",
        "desc": "Minimalist Dark Neko Wallpaper",
        "details": "The signature Discord-Chan Neko Mascot artwork. Deep obsidian dark mode with glowing blurple and cyan neon trims. Perfect for coders, power users, and nighttime server moderation with sharp high-contrast text.",
        "recommended_radius": "16px",
        "recommended_opacity": "0.65",
        "accent_name": "Cyan Glow (#38bdf8)",
        "accent_hex": "#38bdf8",
        "path": os.path.join(REPO_DIR, "assets", "wallpapers", "4_discord_chan_neko.jpg")
    }
]

PINK_PALETTES = [
    ("Sakura Soft", "#ff85a2", "#fbcfe8"),
    ("Strawberry Rose", "#fb7185", "#fecdd3"),
    ("Pastel Peach", "#f472b6", "#fce7f3"),
    ("Cotton Candy", "#f49ac2", "#fed7aa"),
    ("Cherry Blossom", "#fda4af", "#fff1f2"),
    ("Lavender Yuri", "#c084fc", "#e9d5ff"),
    ("Dark Black-Pink", "#ff7597", "#18141c")
]

SPEAKING_COLORS = [
    ("Sakura Pink", "#ff85a2"),
    ("Classic Green", "#23a55a"),
    ("Violet Glow", "#c084fc"),
    ("Cyan Glow", "#38bdf8"),
    ("Amber Glow", "#fbbf24")
]

class DiscordStyledStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord-Chan Studio")
        self.root.geometry("1040x760")
        self.root.minsize(940, 650)
        self.root.configure(bg=C_GUILDS)

        self.settings = theme_engine.load_settings()
        self.active_tab = "mode"
        self.thumb_cache = {}
        self.is_fullscreen = False

        self.init_variables()
        self.load_app_icons()
        self.build_discord_shell()
        self.setup_hotkeys()
        self.show_tab("mode")

        if "--fullscreen" in sys.argv or "-f" in sys.argv:
            self.root.after(100, self.toggle_fullscreen)
        elif "--maximized" in sys.argv or "-m" in sys.argv:
            try:
                self.root.attributes("-zoomed", True)
            except Exception:
                pass

    def init_variables(self):
        self.theme_enabled_var = tk.BooleanVar(value=bool(self.settings.get("theme_enabled", True)))
        self.theme_mode_var = tk.StringVar(value=self.settings.get("theme_mode", "anime_wallpaper"))
        self.custom_path_var = tk.StringVar(value=self.settings.get("wallpaper_path", ""))
        self.wp_opacity_var = tk.DoubleVar(value=float(self.settings.get("wallpaper_opacity", 0.55)))
        self.win_darkness_var = tk.DoubleVar(value=float(self.settings.get("window_darkness", 0.40)))
        self.sidebar_op_var = tk.DoubleVar(value=float(self.settings.get("sidebar_opacity", 0.65)))
        self.guilds_op_var = tk.DoubleVar(value=float(self.settings.get("guilds_opacity", 0.82)))
        self.chat_input_op_var = tk.DoubleVar(value=float(self.settings.get("chat_input_opacity", 0.72)))
        self.embed_op_var = tk.DoubleVar(value=float(self.settings.get("embed_opacity", 0.75)))
        self.corner_radius_var = tk.IntVar(value=int(self.settings.get("corner_radius", 12)))
        self.tile_op_var = tk.DoubleVar(value=float(self.settings.get("tile_opacity", 0.35)))
        self.tile_rad_var = tk.IntVar(value=int(self.settings.get("tile_radius", 12)))
        self.prof_op_var = tk.DoubleVar(value=float(self.settings.get("profile_opacity", 0.88)))
        self.top_spacing_var = tk.IntVar(value=int(self.settings.get("top_spacing", 12)))
        self.zero_lag_var = tk.BooleanVar(value=bool(self.settings.get("zero_lag", True)))
        self.avatar_fix_var = tk.BooleanVar(value=bool(self.settings.get("chat_avatar_fixed", True)))
        # Discord UI Enhancements
        self.show_hidden_ch_var = tk.BooleanVar(value=bool(self.settings.get("show_hidden_channels", False)))
        self.compact_mode_var = tk.BooleanVar(value=bool(self.settings.get("compact_mode", False)))
        self.hide_member_list_var = tk.BooleanVar(value=bool(self.settings.get("hide_member_list", False)))
        self.hide_server_list_var = tk.BooleanVar(value=bool(self.settings.get("hide_server_list", False)))
        self.smooth_anim_var = tk.BooleanVar(value=bool(self.settings.get("smooth_animations", True)))
        self.mention_glow_var = tk.BooleanVar(value=bool(self.settings.get("mention_glow", True)))
        self.blur_avatars_var = tk.BooleanVar(value=bool(self.settings.get("blur_avatars", False)))
        self.typing_indicator_var = tk.BooleanVar(value=bool(self.settings.get("typing_indicator_fancy", True)))

    def load_app_icons(self):
        icon_path = os.path.join(REPO_DIR, "assets", "icons", "discord-neko.png")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(REPO_DIR, "assets", "icons", "discord-chan.png")

        if os.path.exists(icon_path):
            try:
                img = Image.open(icon_path).resize((44, 44), Image.Resampling.LANCZOS)
                self.guild_icon_photo = ImageTk.PhotoImage(img)
                u_img = Image.open(icon_path).resize((32, 32), Image.Resampling.LANCZOS)
                self.user_icon_photo = ImageTk.PhotoImage(u_img)
                prof_img = Image.open(icon_path).resize((64, 64), Image.Resampling.LANCZOS)
                self.prof_icon_photo = ImageTk.PhotoImage(prof_img)
                win_img = Image.open(icon_path).resize((64, 64), Image.Resampling.LANCZOS)
                self.win_icon = ImageTk.PhotoImage(win_img)
                self.root.iconphoto(True, self.win_icon)
            except Exception:
                self.guild_icon_photo = None
                self.user_icon_photo = None
                self.prof_icon_photo = None
        else:
            self.guild_icon_photo = None
            self.user_icon_photo = None
            self.prof_icon_photo = None

    def get_thumbnail(self, path, width=120, height=68):
        cache_key = f"{path}_{width}_{height}"
        if cache_key in self.thumb_cache:
            return self.thumb_cache[cache_key]

        if path and os.path.exists(path):
            try:
                im = Image.open(path)
                w, h = im.size
                target_ratio = width / height
                current_ratio = w / h
                if current_ratio > target_ratio:
                    new_w = int(h * target_ratio)
                    offset = (w - new_w) // 2
                    im = im.crop((offset, 0, offset + new_w, h))
                else:
                    new_h = int(w / target_ratio)
                    offset = (h - new_h) // 2
                    im = im.crop((0, offset, w, offset + new_h))

                im = im.resize((width, height), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(im)
                self.thumb_cache[cache_key] = photo
                return photo
            except Exception:
                pass

        blank = Image.new("RGBA", (width, height), (35, 36, 40, 255))
        photo = ImageTk.PhotoImage(blank)
        self.thumb_cache[cache_key] = photo
        return photo

    def setup_hotkeys(self):
        self.root.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.root.bind("<Escape>", lambda e: self.exit_fullscreen())
        self.root.bind("<Control-Shift-P>", lambda e: self.open_command_palette())
        self.root.bind("<Control-Shift-p>", lambda e: self.open_command_palette())
        self.root.bind("<Control-p>", lambda e: self.open_command_palette())
        self.root.bind("<Control-P>", lambda e: self.open_command_palette())
        self.root.bind("<Control-s>", lambda e: self.apply_theme_action())
        self.root.bind("<Control-S>", lambda e: self.apply_theme_action())
        self.root.bind("<Control-r>", lambda e: self.restart_discord_safe())
        self.root.bind("<Control-R>", lambda e: self.restart_discord_safe())
        self.root.bind("<Control-q>", lambda e: self.root.quit())
        self.root.bind("<Control-Q>", lambda e: self.root.quit())

    def build_discord_shell(self):
        # 1. Left Guilds Rail (Width: 70px)
        self.guilds_bar = tk.Frame(self.root, bg=C_GUILDS, width=70)
        self.guilds_bar.pack(side="left", fill="y")
        self.guilds_bar.pack_propagate(False)

        # Active Guild Pill + Logo
        guild_item = tk.Frame(self.guilds_bar, bg=C_GUILDS, height=54)
        guild_item.pack(fill="x", pady=(10, 4))
        guild_item.pack_propagate(False)

        pill = tk.Frame(guild_item, bg="#ffffff", width=4, height=36)
        pill.pack(side="left", padx=(0, 4), pady=9)

        if self.guild_icon_photo:
            logo_btn = tk.Label(guild_item, image=self.guild_icon_photo, bg=C_GUILDS, cursor="hand2")
            logo_btn.pack(side="left", padx=(4, 0))
            logo_btn.bind("<Button-1>", lambda e: self.show_tab("mode"))
        else:
            logo_lbl = tk.Label(guild_item, text="DC", font=("DejaVu Sans", 11, "bold"), bg=C_BLURPLE, fg="#fff", width=3, height=2)
            logo_lbl.pack(side="left", padx=(4, 0))

        sep = tk.Frame(self.guilds_bar, bg="#35363c", height=2, width=32)
        sep.pack(pady=4)

        self.create_guild_action("INSTALL", C_GREEN, "#ffffff", self.run_instant_setup)
        self.create_guild_action("THEMES", C_CARD, C_PINK, lambda: self.show_tab("theme_manager"))
        self.create_guild_action("BD UI", C_CARD, C_PURPLE, lambda: self.show_tab("bd_theme_studio"))
        self.create_guild_action("PLUGIN", C_CARD, C_CYAN, lambda: self.show_tab("bd_plugin_studio"))
        self.create_guild_action("ENHANCE", C_CARD, "#f59e0b", lambda: self.show_tab("discord_ui"))
        self.create_guild_action("APPLY", C_BLURPLE, "#ffffff", self.apply_theme_action)
        self.create_guild_action("RELOAD", C_CARD, C_TEXT_H, self.restart_discord_safe)

        bot_add = tk.Label(self.guilds_bar, text="+", font=("DejaVu Sans", 14), bg=C_CARD, fg=C_GREEN, width=3, height=1, cursor="hand2")
        bot_add.pack(side="bottom", pady=12)
        bot_add.bind("<Button-1>", lambda e: self.open_command_palette())

        # 2. Channels Sidebar (Width: 240px)
        self.sidebar = tk.Frame(self.root, bg=C_SIDEBAR, width=240)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        sb_header = tk.Frame(self.sidebar, bg=C_SIDEBAR, height=48, padx=14)
        sb_header.pack(fill="x")
        sb_header.pack_propagate(False)

        tk.Label(sb_header, text="Discord-Chan Studio", font=("DejaVu Sans", 10, "bold"), bg=C_SIDEBAR, fg=C_TEXT_H).pack(side="left", pady=14)
        arrow_lbl = tk.Label(sb_header, text="v", font=("DejaVu Sans", 8, "bold"), bg=C_SIDEBAR, fg=C_MUTED, cursor="hand2")
        arrow_lbl.pack(side="right", pady=14)
        arrow_lbl.bind("<Button-1>", lambda e: self.open_command_palette())

        tk.Frame(self.sidebar, bg=C_BORDER, height=1).pack(fill="x")

        self.channels_frame = tk.Frame(self.sidebar, bg=C_SIDEBAR, padx=8, pady=8)
        self.channels_frame.pack(fill="both", expand=True)

        self.channel_buttons = {}
        self.add_category_header("CORE & DISPLAY MODES")
        self.add_channel_btn("mode", "theme-mode-and-toggles")
        self.add_channel_btn("chat", "chat-and-transparency")

        self.add_category_header("ANIME THEMES & MODS")
        self.add_channel_btn("theme_manager", "theme-manager")
        self.add_channel_btn("colors", "color-palette")
        self.add_channel_btn("voice", "voice-and-video")
        self.add_channel_btn("layout", "layout-and-clearance")

        self.add_category_header("BETTERDISCORD STUDIO")
        self.add_channel_btn("bd_theme_studio", "upload-and-modify-themes")
        self.add_channel_btn("bd_plugin_studio", "upload-and-manage-plugins")
        self.add_channel_btn("discord_ui", "discord-ui-enhancements")

        self.add_category_header("EXTENSIONS & PACKAGES")
        self.add_channel_btn("packager", "export-import-themes")
        self.add_channel_btn("extensions", "plugin-extensions-zip")
        self.add_channel_btn("about", "contributors-and-wiki")

        self.build_user_bar()

        # 3. Main Content Container
        self.main_container = tk.Frame(self.root, bg=C_CONTENT)
        self.main_container.pack(side="left", fill="both", expand=True)

        # Top Bar
        self.top_bar = tk.Frame(self.main_container, bg=C_HEADER, height=48, padx=16)
        self.top_bar.pack(fill="x", side="top")
        self.top_bar.pack_propagate(False)

        self.top_hash = tk.Label(self.top_bar, text="#", font=("DejaVu Sans", 13), bg=C_HEADER, fg=C_MUTED)
        self.top_hash.pack(side="left")

        self.top_channel_title = tk.Label(self.top_bar, text="theme-mode-and-toggles", font=("DejaVu Sans", 11, "bold"), bg=C_HEADER, fg=C_TEXT_H)
        self.top_channel_title.pack(side="left", padx=(4, 10))

        self.top_topic = tk.Label(self.top_bar, text="| Master switch, theme modes, and all-custom options", font=("DejaVu Sans", 9), bg=C_HEADER, fg=C_MUTED)
        self.top_topic.pack(side="left")

        self.btn_fullscreen = tk.Button(self.top_bar, text="Full Screen (F11)", font=("DejaVu Sans", 8),
                                      bg="#3b3e45", fg=C_TEXT_H, relief="flat", padx=10, pady=4, cursor="hand2",
                                      command=self.toggle_fullscreen)
        self.btn_fullscreen.pack(side="right", padx=(8, 0))

        btn_cmd = tk.Button(self.top_bar, text="Command Palette (Ctrl+Shift+P)", font=("DejaVu Sans", 8),
                            bg="#3b3e45", fg=C_TEXT_H, relief="flat", padx=10, pady=4, cursor="hand2",
                            command=self.open_command_palette)
        btn_cmd.pack(side="right", padx=(8, 0))

        btn_save = tk.Button(self.top_bar, text="Save & Apply (Ctrl+S)", font=("DejaVu Sans", 8, "bold"),
                             bg=C_BLURPLE, fg="#ffffff", relief="flat", padx=12, pady=4, cursor="hand2",
                             command=self.apply_theme_action)
        btn_save.pack(side="right")

        tk.Frame(self.main_container, bg=C_BORDER, height=1).pack(fill="x")

        # 4. Scrollable Canvas
        self.content_canvas = tk.Canvas(self.main_container, bg=C_CONTENT, highlightthickness=0)
        self.content_scrollbar = tk.Scrollbar(self.main_container, orient="vertical", command=self.content_canvas.yview)
        self.content_scroll = tk.Frame(self.content_canvas, bg=C_CONTENT, padx=20, pady=16)

        self.content_scroll.bind("<Configure>", lambda e: self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all")))
        self.canvas_window = self.content_canvas.create_window((0, 0), window=self.content_scroll, anchor="nw")
        self.content_canvas.configure(yscrollcommand=self.content_scrollbar.set)

        self.content_canvas.bind("<Configure>", self.on_canvas_configure)
        self.content_canvas.pack(side="left", fill="both", expand=True)
        self.content_scrollbar.pack(side="right", fill="y")

        self.content_canvas.bind_all("<Button-4>", lambda e: self.content_canvas.yview_scroll(-1, "units"))
        self.content_canvas.bind_all("<Button-5>", lambda e: self.content_canvas.yview_scroll(1, "units"))
        self.content_canvas.bind_all("<MouseWheel>", lambda e: self.content_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    def on_canvas_configure(self, event):
        self.content_canvas.itemconfig(self.canvas_window, width=event.width)

    def create_guild_action(self, text, bg, fg, cmd):
        btn = tk.Button(self.guilds_bar, text=text, font=("DejaVu Sans", 7, "bold"), bg=bg, fg=fg,
                        relief="flat", width=6, height=2, cursor="hand2", command=cmd)
        btn.pack(pady=4)

    def build_user_bar(self):
        # Powered by BetterDiscord Footer Badge
        bd_badge = tk.Frame(self.sidebar, bg="#1e1f22", padx=10, pady=7)
        bd_badge.pack(fill="x", side="bottom")

        tk.Label(bd_badge, text="POWERED BY BETTERDISCORD", font=("DejaVu Sans", 7, "bold"), bg="#1e1f22", fg="#5865f2").pack(anchor="w")
        tk.Label(bd_badge, text="Client Modding Engine & API", font=("DejaVu Sans", 6), bg="#1e1f22", fg=C_MUTED).pack(anchor="w")

        tk.Frame(self.sidebar, bg=C_BORDER, height=1).pack(fill="x", side="bottom")

        user_bar = tk.Frame(self.sidebar, bg="#232428", height=54, padx=8)
        user_bar.pack(fill="x", side="bottom")
        user_bar.pack_propagate(False)

        av_frame = tk.Frame(user_bar, bg="#232428")
        av_frame.pack(side="left", pady=9)

        if self.user_icon_photo:
            tk.Label(av_frame, image=self.user_icon_photo, bg="#232428").pack(side="left")
        else:
            tk.Label(av_frame, text="M", font=("DejaVu Sans", 9, "bold"), bg=C_BLURPLE, fg="#fff", width=2, height=1).pack(side="left")

        u_info = tk.Frame(user_bar, bg="#232428")
        u_info.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        tk.Label(u_info, text="myzert", font=("DejaVu Sans", 9, "bold"), bg="#232428", fg=C_TEXT_H).pack(anchor="w")
        tk.Label(u_info, text="#neko • Online", font=("DejaVu Sans", 8), bg="#232428", fg=C_GREEN).pack(anchor="w")

        btn_opt = tk.Button(user_bar, text="[Settings]", font=("DejaVu Sans", 7), bg="#232428", fg=C_MUTED,
                            relief="flat", cursor="hand2", command=self.open_command_palette)
        btn_opt.pack(side="right", pady=14)

    def add_category_header(self, text):
        lbl = tk.Label(self.channels_frame, text=f"v  {text}", font=("DejaVu Sans", 7, "bold"), bg=C_SIDEBAR, fg=C_MUTED, anchor="w")
        lbl.pack(fill="x", pady=(10, 2), padx=6)

    def add_channel_btn(self, tab_id, display_name):
        btn = tk.Button(self.channels_frame, text=f"#  {display_name}", font=("DejaVu Sans", 9),
                        bg=C_SIDEBAR, fg=C_MUTED, activebackground="#35373c", activeforeground=C_TEXT_H,
                        relief="flat", anchor="w", padx=10, pady=5, cursor="hand2",
                        command=lambda tid=tab_id: self.show_tab(tid))
        btn.pack(fill="x", pady=1)
        self.channel_buttons[tab_id] = btn

    def show_tab(self, tab_id):
        self.active_tab = tab_id
        for tid, btn in self.channel_buttons.items():
            if tid == tab_id:
                btn.config(bg="#35373c", fg=C_TEXT_H, font=("DejaVu Sans", 9, "bold"))
            else:
                btn.config(bg=C_SIDEBAR, fg=C_MUTED, font=("DejaVu Sans", 9))

        for w in self.content_scroll.winfo_children():
            w.destroy()

        if tab_id == "mode":
            self.top_channel_title.config(text="theme-mode-and-toggles")
            self.top_topic.config(text="| Master ON/OFF toggle, transparent window mode, and vanilla Discord")
            self.render_mode_tab()
        elif tab_id == "chat":
            self.top_channel_title.config(text="chat-and-transparency")
            self.top_topic.config(text="| Chat column translucency, native chat input bar, corner radius & embeds")
            self.render_chat_tab()
        elif tab_id in ("theme_manager", "wallpapers"):
            self.top_channel_title.config(text="theme-manager")
            self.top_topic.config(text="| Visual anime UI mods, live wallpaper PVs, full descriptions & custom loader")
            self.render_theme_manager_tab()
        elif tab_id == "colors":
            self.top_channel_title.config(text="color-palette")
            self.top_topic.config(text="| Minimalist pastel palettes, hex pickers, and embed styling")
            self.render_colors_tab()
        elif tab_id == "voice":
            self.top_channel_title.config(text="voice-and-video")
            self.top_topic.config(text="| Glowing speaking indicators, participant tiles, and profile modals")
            self.render_voice_tab()
        elif tab_id == "layout":
            self.top_channel_title.config(text="layout-and-clearance")
            self.top_topic.config(text="| Window clearance (anti-collision), zero-lag mode, avatar grid guard")
            self.render_layout_tab()
        elif tab_id == "bd_theme_studio":
            self.top_channel_title.config(text="upload-and-modify-themes")
            self.top_topic.config(text="| Upload BetterDiscord themes (.css / .theme.css) and customize them with live editor")
            self.render_bd_theme_studio_tab()
        elif tab_id == "bd_plugin_studio":
            self.top_channel_title.config(text="upload-and-manage-plugins")
            self.top_topic.config(text="| Upload BetterDiscord plugins (.plugin.js / .zip), inspect code, and toggle activation")
            self.render_bd_plugin_studio_tab()
        elif tab_id == "discord_ui":
            self.top_channel_title.config(text="discord-ui-enhancements")
            self.top_topic.config(text="| Hidden channels styling, compact mode, avatar privacy blur, and smooth animations")
            self.render_discord_ui_tab()
        elif tab_id == "packager":
            self.top_channel_title.config(text="export-import-themes")
            self.top_topic.config(text="| Export and import full custom themes (.zip bundle)")
            self.render_packager_tab()
        elif tab_id == "extensions":
            self.top_channel_title.config(text="plugin-extensions-zip")
            self.top_topic.config(text="| Chrome-style extension packages (.zip), install, and create templates")
            self.render_extensions_tab()
        elif tab_id == "about":
            self.top_channel_title.config(text="contributors-and-wiki")
            self.top_topic.config(text="| Lead creator profile, GitHub Wiki, and contribution guide")
            self.render_about_tab()

        self.content_canvas.yview_moveto(0)

    # -------------------------------------------------------------
    # TAB 1: THEME MODES & MASTER TOGGLES
    # -------------------------------------------------------------
    def render_mode_tab(self):
        c = self.content_scroll

        # 1. Master Toggle Card
        card_toggle = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_toggle.pack(fill="x", pady=(0, 14))

        tk.Label(card_toggle, text="Master Theme Switch", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_toggle, text="Turn the entire custom theme ON or OFF without uninstalling:", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 10))

        row_t = tk.Frame(card_toggle, bg=C_CARD)
        row_t.pack(fill="x")

        is_on = self.theme_enabled_var.get()
        btn_master = tk.Button(row_t, text="[ THEME STATUS: ACTIVE (ON) ]" if is_on else "[ THEME STATUS: DISABLED (OFF) ]",
                               font=("DejaVu Sans", 9, "bold"), bg=C_GREEN if is_on else "#4e5058", fg="#ffffff",
                               relief="flat", padx=16, pady=8, cursor="hand2", command=self.toggle_master_theme)
        btn_master.pack(side="left")

        tk.Label(row_t, text="Tip: When OFF, Discord renders 100% standard vanilla Discord.", font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED).pack(side="left", padx=12)

        # 2. Display Modes Card
        card_modes = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_modes.pack(fill="x", pady=(0, 14))

        tk.Label(card_modes, text="Discord Display Modes (All-Custom Architecture)", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_modes, text="Choose how Discord renders its background layer:", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 12))

        current_mode = self.theme_mode_var.get()

        modes = [
            ("anime_wallpaper", "Anime Wallpaper Mode", "Displays high-res anime art (Kaede to Suzu, Whisper Me a Love Song, or custom image)."),
            ("window_transparent", "See-Through Window Transparency", "Transparent Discord window! Applications and desktop behind Discord can be seen."),
            ("vanilla_discord", "Vanilla Discord Client", "Clean native dark Discord theme with zero modifications.")
        ]

        for m_id, m_name, m_desc in modes:
            is_active = (current_mode == m_id)
            row_m = tk.Frame(card_modes, bg=C_CARD_ALT, padx=14, pady=10)
            row_m.pack(fill="x", pady=4)

            col = tk.Frame(row_m, bg=C_CARD_ALT)
            col.pack(side="left", fill="both", expand=True)
            tk.Label(col, text=m_name, font=("DejaVu Sans", 9, "bold"), bg=C_CARD_ALT, fg=C_TEXT_H).pack(anchor="w")
            tk.Label(col, text=m_desc, font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_MUTED).pack(anchor="w", pady=(2, 0))

            if is_active:
                tk.Label(row_m, text="[ ACTIVE ]", font=("DejaVu Sans", 8, "bold"), bg=C_GREEN, fg="#ffffff", padx=12, pady=4).pack(side="right")
            else:
                tk.Button(row_m, text="Select Mode", font=("DejaVu Sans", 8, "bold"), bg=C_BLURPLE, fg="#fff",
                          relief="flat", padx=12, pady=4, cursor="hand2", command=lambda md=m_id: self.select_display_mode(md)).pack(side="right")

        # 3. Transparent Window Tint Slider (if window transparency mode)
        card_tint = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_tint.pack(fill="x")

        tk.Label(card_tint, text="Window Transparency Behind-Tint", font=("DejaVu Sans", 10, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_tint, text="Darkness tint applied over applications visible behind Discord:", font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 6))

        self.create_slider(card_tint, "Behind-Window Darkness Tint:", self.win_darkness_var, 0.10, 0.85, 0.02)

    def toggle_master_theme(self):
        new_val = not self.theme_enabled_var.get()
        self.theme_enabled_var.set(new_val)
        self.settings["theme_enabled"] = new_val
        self.apply_theme_action(silent=True)
        self.show_tab("mode")
        status_text = "ENABLED (Active)" if new_val else "DISABLED (Vanilla Mode)"
        messagebox.showinfo("Theme Toggle", f"Master theme is now {status_text}!")

    def select_display_mode(self, mode_id):
        self.theme_mode_var.set(mode_id)
        self.settings["theme_mode"] = mode_id
        if mode_id == "vanilla_discord":
            self.settings["theme_enabled"] = False
        else:
            self.settings["theme_enabled"] = True
            self.theme_enabled_var.set(True)
        self.apply_theme_action(silent=True)
        self.show_tab("mode")

    # -------------------------------------------------------------
    # TAB 2: CHAT COLUMN & TRANSPARENCY CONTROLS
    # -------------------------------------------------------------
    def render_chat_tab(self):
        c = self.content_scroll

        # 1. Chat Transparency Guarantee Card
        card_chat = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_chat.pack(fill="x", pady=(0, 14))

        tk.Label(card_chat, text="Chat Column Translucency (Full Wallpaper Visibility)", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        desc = "The chat message column is 100% translucent so your anime background or transparent desktop shines through clearly without any solid grey obstruction."
        tk.Label(card_chat, text=desc, font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED, wraplength=640, justify="left").pack(anchor="w", pady=(2, 10))

        # 2. UI Corner Radius (Lingkar UI Kotak)
        card_radius = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_radius.pack(fill="x", pady=(0, 14))

        tk.Label(card_radius, text="UI Corner Radius Customization (Kelengkungan Kotak)", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_radius, text="Customize the border-radius for chat input, embed cards, modals, and buttons:", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 8))

        row_rad = tk.Frame(card_radius, bg=C_CARD)
        row_rad.pack(fill="x", pady=(4, 2))
        tk.Label(row_rad, text="Corner Radius (Sharp 0px to Round 24px):", font=("DejaVu Sans", 8, "bold"), bg=C_CARD, fg=C_TEXT).pack(side="left")
        lbl_rad_v = tk.Label(row_rad, text=f"{self.corner_radius_var.get()}px", font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED)
        lbl_rad_v.pack(side="right")
        tk.Scale(card_radius, from_=0, to=24, orient="horizontal", variable=self.corner_radius_var,
                 bg=C_CARD, fg=C_TEXT_H, troughcolor=C_CARD_ALT, highlightthickness=0, showvalue=0,
                 command=lambda val: lbl_rad_v.config(text=f"{int(val)}px")).pack(fill="x")

        # 3. Translucency Sliders (Chat Input, Embeds, Sidebar, Guilds)
        card_sliders = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_sliders.pack(fill="x")

        tk.Label(card_sliders, text="Component Glass Opacity Sliders", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_sliders, text="Independent opacity levels for every Discord UI layer:", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 8))

        self.create_slider(card_sliders, "Chat Input Text Box Opacity:", self.chat_input_op_var, 0.20, 0.95, 0.02)
        self.create_slider(card_sliders, "Embed Cards Opacity (Clean, No Shadow):", self.embed_op_var, 0.20, 0.95, 0.02)
        self.create_slider(card_sliders, "Channels Sidebar Translucency:", self.sidebar_op_var, 0.20, 0.95, 0.02)
        self.create_slider(card_sliders, "Server Rail (Guilds) Opacity:", self.guilds_op_var, 0.40, 0.98, 0.02)

    def create_slider(self, parent, title, var, from_, to, res):
        row = tk.Frame(parent, bg=C_CARD)
        row.pack(fill="x", pady=(4, 2))
        tk.Label(row, text=title, font=("DejaVu Sans", 8, "bold"), bg=C_CARD, fg=C_TEXT).pack(side="left")

        val_lbl = tk.Label(row, text=f"{int(var.get()*100)}%", font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED)
        val_lbl.pack(side="right")

        def update_val(val):
            val_lbl.config(text=f"{int(float(val)*100)}%")

        scale = tk.Scale(parent, from_=from_, to=to, resolution=res, orient="horizontal", variable=var,
                         bg=C_CARD, fg=C_TEXT_H, troughcolor=C_CARD_ALT, highlightthickness=0,
                         showvalue=0, command=update_val)
        scale.pack(fill="x", pady=(0, 6))

    # -------------------------------------------------------------
    # TAB 3: THEME MANAGER (WALLPAPERS, LIVE PVS & FULL UI MODS)
    # -------------------------------------------------------------
    def render_theme_manager_tab(self):
        c = self.content_scroll
        active_id = self.settings.get("wallpaper_id", "kaede_to_suzu")
        current_path = self.settings.get("wallpaper_path", "")
        current_mode = self.settings.get("theme_mode", "anime_wallpaper")
        is_enabled = self.settings.get("theme_enabled", True)

        # 1. Hero Card: Current Active Theme & Live Specs
        hero_card = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        hero_card.pack(fill="x", pady=(0, 14))

        tk.Label(hero_card, text="CURRENT ACTIVE THEME & UI MOD", font=("DejaVu Sans", 8, "bold"), bg=C_CARD, fg=C_PINK).pack(anchor="w")

        row_h = tk.Frame(hero_card, bg=C_CARD)
        row_h.pack(fill="x", pady=(8, 0))

        thumb = self.get_thumbnail(current_path, width=170, height=96)
        lbl_h_thumb = tk.Label(row_h, image=thumb, bg=C_CARD, relief="ridge", bd=1)
        lbl_h_thumb.image = thumb
        lbl_h_thumb.pack(side="left", padx=(0, 16))

        info_h = tk.Frame(row_h, bg=C_CARD)
        info_h.pack(side="left", fill="both", expand=True)

        active_name = "Custom Wallpaper Mod"
        active_tag = "CUSTOM USER IMAGE"
        active_desc = "User-selected custom anime background with translucent glass styling."
        for wp in WALLPAPERS:
            if wp["id"] == active_id:
                active_name = wp["name"]
                active_tag = wp.get("tag", "ANIME UI MOD")
                active_desc = wp.get("details", wp.get("desc", ""))
                break

        if not is_enabled:
            mode_badge = ("VANILLA DISCORD (THEME OFF)", "#3b3e45")
        elif current_mode == "window_transparent":
            mode_badge = ("SEE-THROUGH ACRYLIC WINDOW", "#0284c7")
        else:
            mode_badge = (active_tag, "#7c3aed")

        tag_row = tk.Frame(info_h, bg=C_CARD)
        tag_row.pack(anchor="w", pady=(0, 4))
        tk.Label(tag_row, text=f" {mode_badge[0]} ", font=("DejaVu Sans", 7, "bold"), bg=mode_badge[1], fg="#ffffff").pack(side="left", padx=(0, 6))
        tk.Label(tag_row, text="[ ACTIVE IN DISCORD ]", font=("DejaVu Sans", 7, "bold"), bg=C_GREEN, fg="#ffffff").pack(side="left")

        tk.Label(info_h, text=active_name, font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(info_h, text=active_desc, font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED, wraplength=520, justify="left").pack(anchor="w", pady=(2, 6))

        spec_row = tk.Frame(info_h, bg=C_CARD)
        spec_row.pack(anchor="w")
        tk.Label(spec_row, text=f"Corner Radius: {self.settings.get('corner_radius', 12)}px  |  Chat: 100% Glass  |  Overlay: {int(float(self.settings.get('wallpaper_opacity', 0.55))*100)}%",
                 font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED).pack(side="left")

        # 2. Curated Anime Themes & UI Mods with Live PVs
        card_presets = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_presets.pack(fill="x", pady=(0, 14))

        tk.Label(card_presets, text="Curated Anime Themes & UI Mods (Live Visual PV)", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_presets, text="Click 'Apply Theme Mod' to instantly inject high-definition anime visuals, glass CSS, and matching accents:",
                 font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 12))

        for wp in WALLPAPERS:
            is_active = (wp["id"] == active_id and current_mode == "anime_wallpaper" and is_enabled)
            row = tk.Frame(card_presets, bg=C_CARD_ALT, padx=12, pady=10)
            row.pack(fill="x", pady=5)

            # Left: Visual PV Thumbnail
            wp_thumb = self.get_thumbnail(wp["path"], width=140, height=80)
            lbl_t = tk.Label(row, image=wp_thumb, bg=C_CARD_ALT, relief="ridge", bd=1)
            lbl_t.image = wp_thumb
            lbl_t.pack(side="left", padx=(0, 14))

            # Middle: Full Details & Penjelasan Lengkap
            col_d = tk.Frame(row, bg=C_CARD_ALT)
            col_d.pack(side="left", fill="both", expand=True)

            t_box = tk.Frame(col_d, bg=C_CARD_ALT)
            t_box.pack(anchor="w")
            tk.Label(t_box, text=f" {wp.get('tag', 'ANIME MOD')} ", font=("DejaVu Sans", 7, "bold"), bg="#5865f2", fg="#ffffff").pack(side="left", padx=(0, 6))
            tk.Label(t_box, text=wp["name"], font=("DejaVu Sans", 10, "bold"), bg=C_CARD_ALT, fg=C_TEXT_H).pack(side="left")

            tk.Label(col_d, text=wp["desc"], font=("DejaVu Sans", 8, "bold"), bg=C_CARD_ALT, fg=C_PINK).pack(anchor="w", pady=(2, 2))
            tk.Label(col_d, text=wp.get("details", ""), font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_MUTED, wraplength=500, justify="left").pack(anchor="w", pady=(0, 4))

            spec_line = f"Accent: {wp.get('accent_name', 'Pink')}  •  Radius: {wp.get('recommended_radius', '12px')}  •  Opacity: {wp.get('recommended_opacity', '0.55')}"
            tk.Label(col_d, text=spec_line, font=("DejaVu Sans", 7), bg=C_CARD_ALT, fg=C_MUTED).pack(anchor="w")

            # Right: Action Button
            right_col = tk.Frame(row, bg=C_CARD_ALT)
            right_col.pack(side="right", padx=(10, 0))

            if is_active:
                tk.Label(right_col, text="[ CURRENTLY ACTIVE ]", font=("DejaVu Sans", 8, "bold"), bg=C_GREEN, fg="#ffffff", padx=12, pady=6).pack()
            else:
                btn = tk.Button(right_col, text="Apply Theme Mod", font=("DejaVu Sans", 8, "bold"), bg=C_BLURPLE, fg="#fff",
                                relief="flat", padx=14, pady=6, cursor="hand2", command=lambda w=wp: self.select_preset_wallpaper(w))
                btn.pack()

        # 3. Special Display Architecture Mods
        card_modes = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_modes.pack(fill="x", pady=(0, 14))

        tk.Label(card_modes, text="Special Display Architecture Mods", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_modes, text="Switch the fundamental rendering behavior of the Discord desktop client:", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 10))

        # Mode A: Window Transparent
        row_win = tk.Frame(card_modes, bg=C_CARD_ALT, padx=12, pady=10)
        row_win.pack(fill="x", pady=4)

        win_thumb = self.get_thumbnail(os.path.join(REPO_DIR, "assets", "previews", "preview_discord.png"), width=140, height=80)
        lbl_w = tk.Label(row_win, image=win_thumb, bg=C_CARD_ALT, relief="ridge", bd=1)
        lbl_w.image = win_thumb
        lbl_w.pack(side="left", padx=(0, 14))

        col_w = tk.Frame(row_win, bg=C_CARD_ALT)
        col_w.pack(side="left", fill="both", expand=True)
        t_w = tk.Frame(col_w, bg=C_CARD_ALT)
        t_w.pack(anchor="w")
        tk.Label(t_w, text=" SEE-THROUGH ACRYLIC MOD ", font=("DejaVu Sans", 7, "bold"), bg="#0284c7", fg="#ffffff").pack(side="left", padx=(0, 6))
        tk.Label(t_w, text="See-Through Window Transparency", font=("DejaVu Sans", 10, "bold"), bg=C_CARD_ALT, fg=C_TEXT_H).pack(side="left")
        tk.Label(col_w, text="Makes Discord completely transparent so applications and desktop behind Discord show through with adjustable darkness tint.",
                 font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_MUTED, wraplength=500, justify="left").pack(anchor="w", pady=(2, 0))

        is_win_active = (current_mode == "window_transparent" and is_enabled)
        r_w = tk.Frame(row_win, bg=C_CARD_ALT)
        r_w.pack(side="right", padx=(10, 0))
        if is_win_active:
            tk.Label(r_w, text="[ CURRENTLY ACTIVE ]", font=("DejaVu Sans", 8, "bold"), bg=C_GREEN, fg="#ffffff", padx=12, pady=6).pack()
        else:
            tk.Button(r_w, text="Switch to Window Mode", font=("DejaVu Sans", 8, "bold"), bg=C_BLURPLE, fg="#fff",
                      relief="flat", padx=12, pady=6, cursor="hand2", command=lambda: [self.select_display_mode("window_transparent"), self.show_tab("theme_manager")]).pack()

        # Mode B: Vanilla Discord
        row_van = tk.Frame(card_modes, bg=C_CARD_ALT, padx=12, pady=10)
        row_van.pack(fill="x", pady=4)

        col_v = tk.Frame(row_van, bg=C_CARD_ALT)
        col_v.pack(side="left", fill="both", expand=True)
        t_v = tk.Frame(col_v, bg=C_CARD_ALT)
        t_v.pack(anchor="w")
        tk.Label(t_v, text=" OFFICIAL DISCORD DEFAULT ", font=("DejaVu Sans", 7, "bold"), bg="#3b3e45", fg="#ffffff").pack(side="left", padx=(0, 6))
        tk.Label(t_v, text="Vanilla Discord Native Client", font=("DejaVu Sans", 10, "bold"), bg=C_CARD_ALT, fg=C_TEXT_H).pack(side="left")
        tk.Label(col_v, text="Temporarily disables all custom CSS injection and reverts Discord immediately to 100% native official styling.",
                 font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_MUTED, wraplength=500, justify="left").pack(anchor="w", pady=(2, 0))

        is_van_active = (current_mode == "vanilla_discord" or not is_enabled)
        r_v = tk.Frame(row_van, bg=C_CARD_ALT)
        r_v.pack(side="right", padx=(10, 0))
        if is_van_active:
            tk.Label(r_v, text="[ CURRENTLY ACTIVE ]", font=("DejaVu Sans", 8, "bold"), bg=C_GREEN, fg="#ffffff", padx=12, pady=6).pack()
        else:
            tk.Button(r_v, text="Switch to Vanilla Mode", font=("DejaVu Sans", 8, "bold"), bg="#3b3e45", fg="#fff",
                      relief="flat", padx=12, pady=6, cursor="hand2", command=lambda: [self.select_display_mode("vanilla_discord"), self.show_tab("theme_manager")]).pack()

        # 4. All-Custom Manual File Selection
        card_custom = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_custom.pack(fill="x", pady=(0, 14))

        tk.Label(card_custom, text="All-Custom Wallpaper & Image Mod", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_custom, text="Choose ANY image file from your computer without restriction (jpg, png, webp, gif):", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 8))

        row_c = tk.Frame(card_custom, bg=C_CARD)
        row_c.pack(fill="x", pady=4)

        entry = tk.Entry(row_c, textvariable=self.custom_path_var, bg=C_CARD_ALT, fg=C_TEXT_H, insertbackground=C_TEXT_H, relief="flat", font=("DejaVu Sans", 9))
        entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))

        tk.Button(row_c, text="Browse File...", font=("DejaVu Sans", 8, "bold"), bg="#3b3e45", fg=C_TEXT_H, relief="flat", padx=10, pady=5, cursor="hand2",
                  command=self.browse_custom_wallpaper).pack(side="left")

        tk.Button(row_c, text="Apply Custom Image", font=("DejaVu Sans", 8, "bold"), bg=C_BLURPLE, fg="#fff", relief="flat", padx=14, pady=5, cursor="hand2",
                  command=self.apply_custom_wallpaper).pack(side="left", padx=(8, 0))

        # Quick directory jumps
        row_quick = tk.Frame(card_custom, bg=C_CARD)
        row_quick.pack(fill="x", pady=(8, 0))
        tk.Label(row_quick, text="Quick folders:", font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED).pack(side="left", padx=(0, 6))

        home = os.path.expanduser("~")
        for q_name, q_dir in [("Downloads", os.path.join(home, "Downloads")), ("Pictures", os.path.join(home, "Pictures")), ("Wallpapers", os.path.join(REPO_DIR, "assets", "wallpapers"))]:
            tk.Button(row_quick, text=f"[{q_name}]", font=("DejaVu Sans", 8), bg=C_CARD, fg=C_TEXT, relief="flat", cursor="hand2",
                      command=lambda d=q_dir: self.browse_in_directory(d)).pack(side="left", padx=3)

        # 5. Wallpaper Darkness Overlay Slider
        card_trans = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_trans.pack(fill="x")

        tk.Label(card_trans, text="Wallpaper Darkening Overlay", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_trans, text="Adjust dark overlay to ensure high contrast text against light anime artwork:", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 8))

        self.create_slider(card_trans, "Wallpaper Darkening Level:", self.wp_opacity_var, 0.10, 0.95, 0.02)

    render_wallpapers_tab = render_theme_manager_tab

    # -------------------------------------------------------------
    # TAB 4: COLOR PALETTES & EMBEDS
    # -------------------------------------------------------------
    def render_colors_tab(self):
        c = self.content_scroll

        card_pal = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_pal.pack(fill="x", pady=(0, 14))

        tk.Label(card_pal, text="Minimalist Color Palettes", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_pal, text="Choose a curated pastel palette for channel indicators and accents:", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 10))

        active_preset = self.settings.get("active_preset", "Sakura Soft")

        for name, pri, sec in PINK_PALETTES:
            is_active = (name == active_preset)
            row = tk.Frame(card_pal, bg=C_CARD_ALT, padx=12, pady=7)
            row.pack(fill="x", pady=3)

            tk.Label(row, text="    ", bg=pri, relief="flat").pack(side="left", padx=4)
            tk.Label(row, text="    ", bg=sec, relief="flat").pack(side="left", padx=4)
            tk.Label(row, text=name, font=("DejaVu Sans", 9, "bold"), bg=C_CARD_ALT, fg=C_TEXT_H).pack(side="left", padx=10)
            tk.Label(row, text=f"({pri} / {sec})", font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_MUTED).pack(side="left")

            if is_active:
                tk.Label(row, text="[ ACTIVE ]", font=("DejaVu Sans", 8, "bold"), bg=C_GREEN, fg="#ffffff", padx=10, pady=2).pack(side="right")
            else:
                btn = tk.Button(row, text="Apply Palette", font=("DejaVu Sans", 8, "bold"), bg=C_BLURPLE, fg="#fff",
                                relief="flat", padx=10, pady=2, cursor="hand2", command=lambda n=name, p=pri, s=sec: self.select_palette(n, p, s))
                btn.pack(side="right")

        # Custom Hex Color Picker Card
        card_custom_c = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_custom_c.pack(fill="x", pady=(0, 14))

        tk.Label(card_custom_c, text="Custom Color Values (All-Custom Hex)", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_custom_c, text="Pick any exact hex color using the system color chooser:", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 8))

        row_pick = tk.Frame(card_custom_c, bg=C_CARD)
        row_pick.pack(fill="x", pady=6)

        tk.Label(row_pick, text="Primary Accent Color:", font=("DejaVu Sans", 8, "bold"), bg=C_CARD, fg=C_TEXT).pack(side="left")
        self.lbl_accent_sample = tk.Label(row_pick, text="      ", bg=self.settings.get("accent_color", "#ff85a2"), relief="solid", borderwidth=1)
        self.lbl_accent_sample.pack(side="left", padx=8)
        tk.Button(row_pick, text="Choose Color...", font=("DejaVu Sans", 8), bg="#3b3e45", fg=C_TEXT_H, relief="flat", padx=8, pady=2,
                  command=self.pick_accent_color).pack(side="left", padx=4)

        tk.Label(row_pick, text="Secondary Soft Color:", font=("DejaVu Sans", 8, "bold"), bg=C_CARD, fg=C_TEXT).pack(side="left", padx=(16, 0))
        self.lbl_soft_sample = tk.Label(row_pick, text="      ", bg=self.settings.get("soft_pink", "#fbcfe8"), relief="solid", borderwidth=1)
        self.lbl_soft_sample.pack(side="left", padx=8)
        tk.Button(row_pick, text="Choose Color...", font=("DejaVu Sans", 8), bg="#3b3e45", fg=C_TEXT_H, relief="flat", padx=8, pady=2,
                  command=self.pick_soft_color).pack(side="left", padx=4)

        # Embed Fix Explanation Card
        card_emb = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_emb.pack(fill="x")

        tk.Label(card_emb, text="Embed Cards Styling (No Muddy Shadows)", font=("DejaVu Sans", 10, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_emb, text="Embeds render as sleek translucent cards with a solid colored accent bar and zero laggy shadows.", font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 0))

    # -------------------------------------------------------------
    # TAB 5: VOICE & VIDEO UI
    # -------------------------------------------------------------
    def render_voice_tab(self):
        c = self.content_scroll

        card_spk = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_spk.pack(fill="x", pady=(0, 14))

        tk.Label(card_spk, text="Voice Speaking Indicator Ring", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_spk, text="Select the glowing avatar ring color when a user speaks in voice channels:", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 8))

        active_spk = self.settings.get("speaking_color", "#ff85a2")
        for name, col in SPEAKING_COLORS:
            is_active = (col.lower() == active_spk.lower())
            row = tk.Frame(card_spk, bg=C_CARD_ALT, padx=12, pady=5)
            row.pack(fill="x", pady=2)
            tk.Label(row, text="    ", bg=col, relief="flat").pack(side="left", padx=4)
            tk.Label(row, text=name, font=("DejaVu Sans", 8, "bold"), bg=C_CARD_ALT, fg=C_TEXT_H).pack(side="left", padx=8)

            if is_active:
                tk.Label(row, text="[ ACTIVE ]", font=("DejaVu Sans", 8, "bold"), bg=C_GREEN, fg="#ffffff", padx=8, pady=1).pack(side="right")
            else:
                tk.Button(row, text="Select", font=("DejaVu Sans", 8, "bold"), bg=C_BLURPLE, fg="#fff", relief="flat", padx=8, pady=1,
                          command=lambda cl=col: self.set_speaking_color(cl)).pack(side="right")

        card_tiles = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_tiles.pack(fill="x")

        tk.Label(card_tiles, text="Voice Video Tiles & Profile Modals", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_tiles, text="Configure participant tile glass opacity and user profile card styling:", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 8))

        self.create_slider(card_tiles, "Voice Tile Translucency (Opacity):", self.tile_op_var, 0.10, 0.85, 0.02)
        self.create_slider(card_tiles, "User Profile Popout Modal Opacity:", self.prof_op_var, 0.50, 0.98, 0.02)

    # -------------------------------------------------------------
    # TAB 6: LAYOUT & CLEARANCE (ANTI-NABRAK)
    # -------------------------------------------------------------
    def render_layout_tab(self):
        c = self.content_scroll

        card_layout = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_layout.pack(fill="x", pady=(0, 14))

        tk.Label(card_layout, text="Window Clearance & Top Spacing (Anti-Collision)", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_layout, text="Adds clean vertical clearance so Discord headers do not collide with desktop taskbars:", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 8))

        row_sp = tk.Frame(card_layout, bg=C_CARD)
        row_sp.pack(fill="x", pady=(4, 2))
        tk.Label(row_sp, text="Top Margin Spacing (px):", font=("DejaVu Sans", 8, "bold"), bg=C_CARD, fg=C_TEXT).pack(side="left")
        lbl_sp_v = tk.Label(row_sp, text=f"{self.top_spacing_var.get()}px", font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED)
        lbl_sp_v.pack(side="right")
        tk.Scale(card_layout, from_=0, to=40, orient="horizontal", variable=self.top_spacing_var,
                 bg=C_CARD, fg=C_TEXT_H, troughcolor=C_CARD_ALT, highlightthickness=0, showvalue=0,
                 command=lambda val: lbl_sp_v.config(text=f"{int(val)}px")).pack(fill="x")

        card_opt = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_opt.pack(fill="x")

        tk.Label(card_opt, text="Performance & Engine Guards", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")

        cb1 = tk.Checkbutton(card_opt, text="Zero-Lag Engine: Strips box-shadows and heavy blur filters for solid 60 FPS",
                             variable=self.zero_lag_var, bg=C_CARD, fg=C_TEXT, selectcolor=C_CARD_ALT, activebackground=C_CARD)
        cb1.pack(anchor="w", pady=(8, 4))

        cb2 = tk.Checkbutton(card_opt, text="Chat Avatar Guard: Preserves native Discord message grid alignment without distortion",
                             variable=self.avatar_fix_var, bg=C_CARD, fg=C_TEXT, selectcolor=C_CARD_ALT, activebackground=C_CARD)
        cb2.pack(anchor="w", pady=4)

    # -------------------------------------------------------------
    # TAB 7: EXPORT & IMPORT THEMES (.ZIP BUNDLES)
    # -------------------------------------------------------------
    def render_packager_tab(self):
        c = self.content_scroll

        # Export Card
        card_exp = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_exp.pack(fill="x", pady=(0, 14))

        tk.Label(card_exp, text="Export Current Theme as ZIP Bundle", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        desc_e = "Package your current colors, translucency, corner radius, and embedded wallpaper into a single portable .zip file to share with friends or backup."
        tk.Label(card_exp, text=desc_e, font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED, wraplength=640, justify="left").pack(anchor="w", pady=(2, 10))

        tk.Button(card_exp, text="Export Theme (.zip)", font=("DejaVu Sans", 9, "bold"), bg=C_BLURPLE, fg="#ffffff",
                  relief="flat", padx=16, pady=6, cursor="hand2", command=self.action_export_theme).pack(anchor="w")

        # Import Card
        card_imp = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_imp.pack(fill="x")

        tk.Label(card_imp, text="Import Theme from ZIP Bundle", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        desc_i = "Import any community theme zip file. It automatically extracts embedded wallpapers, configures all settings, and applies the theme to Discord immediately."
        tk.Label(card_imp, text=desc_i, font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED, wraplength=640, justify="left").pack(anchor="w", pady=(2, 10))

        tk.Button(card_imp, text="Import Theme (.zip)...", font=("DejaVu Sans", 9, "bold"), bg="#3b3e45", fg=C_TEXT_H,
                  relief="flat", padx=16, pady=6, cursor="hand2", command=self.action_import_theme).pack(anchor="w")

    def action_export_theme(self):
        f = filedialog.asksaveasfilename(
            title="Export Theme ZIP Package",
            defaultextension=".zip",
            filetypes=[("Zip Archive", "*.zip")]
        )
        if f:
            ok, msg = theme_packager.export_theme_zip(f, self.settings, theme_name="My Discord Custom Theme")
            if ok:
                messagebox.showinfo("Export Successful", msg)
            else:
                messagebox.showerror("Export Failed", msg)

    def action_import_theme(self):
        f = filedialog.askopenfilename(
            title="Select Theme ZIP Package to Import",
            filetypes=[("Zip Archive", "*.zip")]
        )
        if f:
            ok, new_s, msg = theme_packager.import_theme_zip(f)
            if ok:
                self.settings = new_s
                self.init_variables()
                self.show_tab("packager")
                messagebox.showinfo("Import Successful", msg)
            else:
                messagebox.showerror("Import Failed", msg)

    # -------------------------------------------------------------
    # TAB 8: PLUGIN / EXTENSION SYSTEM (.ZIP CHROME-STYLE)
    # -------------------------------------------------------------
    def render_extensions_tab(self):
        c = self.content_scroll

        # Actions Card
        card_act = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_act.pack(fill="x", pady=(0, 14))

        tk.Label(card_act, text="Modular Extension System (Chrome-Style ZIP Packages)", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        desc_x = "Install custom add-ons and community plugins packaged as .zip files containing manifest.json and style.css, or create your own extension template with 1 click."
        tk.Label(card_act, text=desc_x, font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED, wraplength=640, justify="left").pack(anchor="w", pady=(2, 10))

        row_b = tk.Frame(card_act, bg=C_CARD)
        row_b.pack(fill="x", pady=(4, 0))

        tk.Button(row_b, text="Install Extension (.zip)...", font=("DejaVu Sans", 9, "bold"), bg=C_BLURPLE, fg="#ffffff",
                  relief="flat", padx=14, pady=6, cursor="hand2", command=self.action_install_extension).pack(side="left")

        tk.Button(row_b, text="Create Extension Template (.zip)", font=("DejaVu Sans", 9), bg="#3b3e45", fg=C_TEXT_H,
                  relief="flat", padx=12, pady=6, cursor="hand2", command=self.action_create_extension_template).pack(side="left", padx=10)

        # Installed Extensions List
        card_list = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_list.pack(fill="x")

        tk.Label(card_list, text="Installed Extensions", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")

        exts = extensions_system.list_installed_extensions()
        if not exts:
            tk.Label(card_list, text="No custom extensions installed yet. Click 'Create Extension Template (.zip)' to start building one!",
                     font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(6, 0))
        else:
            for item in exts:
                row_e = tk.Frame(card_list, bg=C_CARD_ALT, padx=12, pady=8)
                row_e.pack(fill="x", pady=3)

                col = tk.Frame(row_e, bg=C_CARD_ALT)
                col.pack(side="left", fill="both", expand=True)

                st_text = "[Active]" if item["enabled"] else "[Disabled]"
                st_color = C_GREEN if item["enabled"] else C_MUTED
                tk.Label(col, text=f"{item['name']} v{item['version']} {st_text}", font=("DejaVu Sans", 9, "bold"), bg=C_CARD_ALT, fg=st_color).pack(anchor="w")
                tk.Label(col, text=f"{item['description']} (by {item['author']})", font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_MUTED).pack(anchor="w", pady=1)

                btn_toggle = tk.Button(row_e, text="Disable" if item["enabled"] else "Enable", font=("DejaVu Sans", 8, "bold"),
                                       bg="#3b3e45" if item["enabled"] else C_BLURPLE, fg="#ffffff", relief="flat", padx=8, pady=2,
                                       command=lambda eid=item["id"], en=not item["enabled"]: [extensions_system.toggle_extension(eid, en), self.show_tab("extensions")])
                btn_toggle.pack(side="right", padx=(6, 0))

                btn_del = tk.Button(row_e, text="Uninstall", font=("DejaVu Sans", 8), bg=C_RED, fg="#ffffff", relief="flat", padx=8, pady=2,
                                    command=lambda eid=item["id"]: [extensions_system.uninstall_extension(eid), self.show_tab("extensions")])
                btn_del.pack(side="right")

    def action_install_extension(self):
        f = filedialog.askopenfilename(
            title="Select Extension ZIP Archive to Install",
            filetypes=[("Zip Archive", "*.zip")]
        )
        if f:
            ok, msg = extensions_system.install_extension_zip(f)
            if ok:
                self.show_tab("extensions")
                messagebox.showinfo("Installed", msg)
            else:
                messagebox.showerror("Error", msg)

    def action_create_extension_template(self):
        f = filedialog.asksaveasfilename(
            title="Save Extension ZIP Template",
            defaultextension=".zip",
            initialfile="my-extension-template.zip",
            filetypes=[("Zip Archive", "*.zip")]
        )
        if f:
            ok, msg = extensions_system.create_extension_template(f, name="Custom Neon Theme", author="myzert")
            if ok:
                messagebox.showinfo("Template Created", msg)
            else:
                messagebox.showerror("Error", msg)

    # -------------------------------------------------------------
    # TAB: BETTERDISCORD THEME STUDIO (UPLOAD & LIVE MODIFIER)
    # -------------------------------------------------------------
    def render_bd_theme_studio_tab(self):
        c = self.content_scroll
        themes = bd_customizer.list_installed_themes()

        # 1. Header Banner & Upload Card
        card_head = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_head.pack(fill="x", pady=(0, 14))

        head_row = tk.Frame(card_head, bg=C_CARD)
        head_row.pack(fill="x")

        title_col = tk.Frame(head_row, bg=C_CARD)
        title_col.pack(side="left", fill="both", expand=True)

        tk.Label(title_col, text="BetterDiscord Theme Studio & Customizer", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        desc = "Upload any BetterDiscord theme (.theme.css / .css) from your computer or internet, and use the built-in live modifier to tweak colors, wallpapers, and CSS variables."
        tk.Label(title_col, text=desc, font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED, wraplength=640, justify="left").pack(anchor="w", pady=(2, 6))

        badge = tk.Frame(head_row, bg=C_PURPLE, padx=12, pady=6)
        badge.pack(side="right", padx=(10, 0))
        tk.Label(badge, text="THEME MODIFIER", font=("DejaVu Sans", 7, "bold"), bg=C_PURPLE, fg="#10121a").pack(anchor="center")
        tk.Label(badge, text="Live CSS Customizer", font=("DejaVu Sans", 8, "bold"), bg=C_PURPLE, fg="#10121a").pack(anchor="center")

        tk.Frame(card_head, bg=C_BORDER, height=1).pack(fill="x", pady=10)

        # Upload Action Buttons
        act_row = tk.Frame(card_head, bg=C_CARD)
        act_row.pack(fill="x")

        btn_up = tk.Button(act_row, text="+ UPLOAD BETTERDISCORD THEME (.theme.css)", font=("DejaVu Sans", 9, "bold"),
                           bg=C_PINK, fg="#10121a", relief="flat", padx=16, pady=6, cursor="hand2",
                           command=self.action_upload_bd_theme)
        btn_up.pack(side="left", padx=(0, 10))

        btn_fld = tk.Button(act_row, text="Open Themes Folder", font=("DejaVu Sans", 8),
                            bg="#2e3244", fg=C_TEXT_H, relief="flat", padx=12, pady=6, cursor="hand2",
                            command=lambda: self.open_folder_system(bd_customizer.THEMES_DIR))
        btn_fld.pack(side="left")

        # 2. Raw URL Downloader Card
        card_url = tk.Frame(c, bg=C_CARD, padx=16, pady=12)
        card_url.pack(fill="x", pady=(0, 14))

        tk.Label(card_url, text="Import Theme from Direct URL (GitHub / Pastebin)", font=("DejaVu Sans", 9, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        row_u = tk.Frame(card_url, bg=C_CARD)
        row_u.pack(fill="x", pady=(6, 0))

        self.theme_url_entry = tk.Entry(row_u, bg=C_CARD_ALT, fg="#ffffff", insertbackground="#ffffff", relief="flat", font=("DejaVu Sans", 9))
        self.theme_url_entry.pack(side="left", fill="x", expand=True, ipady=5, padx=(0, 8))

        btn_url_dl = tk.Button(row_u, text="Download & Import URL", font=("DejaVu Sans", 8, "bold"), bg=C_BLURPLE, fg="#ffffff",
                               relief="flat", padx=14, pady=5, cursor="hand2", command=self.action_import_theme_url)
        btn_url_dl.pack(side="right")

        # 3. Installed BetterDiscord Themes List
        card_list = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_list.pack(fill="x")

        tk.Label(card_list, text=f"Installed BetterDiscord Themes ({len(themes)})", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w", pady=(0, 10))

        if not themes:
            tk.Label(card_list, text="No BetterDiscord themes installed yet. Click '+ UPLOAD BETTERDISCORD THEME' above to add one!", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=10)
        else:
            for t in themes:
                self.create_theme_item_card(card_list, t)

    def create_theme_item_card(self, parent, t):
        card = tk.Frame(parent, bg=C_CARD_ALT, padx=14, pady=12)
        card.pack(fill="x", pady=5)

        top_r = tk.Frame(card, bg=C_CARD_ALT)
        top_r.pack(fill="x")

        status_color = C_GREEN if t["is_enabled"] else C_MUTED
        status_txt = "ACTIVE IN DISCORD" if t["is_enabled"] else "INACTIVE"
        tk.Label(top_r, text=f"[{status_txt}]", font=("DejaVu Sans", 7, "bold"), bg=C_CARD_ALT, fg=status_color).pack(side="left", padx=(0, 8))

        tk.Label(top_r, text=t["name"], font=("DejaVu Sans", 10, "bold"), bg=C_CARD_ALT, fg=C_TEXT_H).pack(side="left")
        tk.Label(top_r, text=f"v{t['version']} by {t['author']}  ({t['size_kb']} KB)", font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_MUTED).pack(side="left", padx=8)

        tk.Label(card, text=t["description"], font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_MUTED, wraplength=640, justify="left").pack(anchor="w", pady=(4, 8))

        act_r = tk.Frame(card, bg=C_CARD_ALT)
        act_r.pack(fill="x")

        # Toggle Button
        if t["is_enabled"]:
            btn_tog = tk.Button(act_r, text="Disable Theme", font=("DejaVu Sans", 8), bg="#3b3e4f", fg=C_TEXT,
                                relief="flat", padx=10, pady=3, cursor="hand2",
                                command=lambda fn=t["filename"], nm=t["name"]: self.action_toggle_theme(nm, fn, False))
        else:
            btn_tog = tk.Button(act_r, text="Enable / Use Theme", font=("DejaVu Sans", 8, "bold"), bg=C_GREEN, fg="#ffffff",
                                relief="flat", padx=10, pady=3, cursor="hand2",
                                command=lambda fn=t["filename"], nm=t["name"]: self.action_toggle_theme(nm, fn, True))
        btn_tog.pack(side="left", padx=(0, 6))

        # Modify / Edit Button
        btn_mod = tk.Button(act_r, text="[MODIFY THEME / EDIT CSS]", font=("DejaVu Sans", 8, "bold"), bg=C_PINK, fg="#10121a",
                            relief="flat", padx=12, pady=3, cursor="hand2",
                            command=lambda th=t: self.open_theme_modifier(th))
        btn_mod.pack(side="left", padx=(0, 6))

        # Duplicate Button
        btn_dup = tk.Button(act_r, text="Duplicate / Clone", font=("DejaVu Sans", 8), bg="#2b2e3e", fg=C_TEXT_H,
                            relief="flat", padx=8, pady=3, cursor="hand2",
                            command=lambda fn=t["filename"]: self.action_clone_theme(fn))
        btn_dup.pack(side="left", padx=(0, 6))

        # Delete Button (protect main WhisperMeALoveSong theme from accidental delete)
        if t["filename"] != "WhisperMeALoveSong.theme.css":
            btn_del = tk.Button(act_r, text="Delete", font=("DejaVu Sans", 8), bg=C_RED, fg="#ffffff",
                                relief="flat", padx=8, pady=3, cursor="hand2",
                                command=lambda fn=t["filename"], nm=t["name"]: self.action_delete_theme(fn, nm))
            btn_del.pack(side="right")

    def action_upload_bd_theme(self):
        f = filedialog.askopenfilename(
            title="Select BetterDiscord Theme to Upload",
            filetypes=[("BetterDiscord Theme / CSS", "*.theme.css *.css"), ("All Files", "*.*")]
        )
        if not f:
            return
        try:
            res = bd_customizer.upload_theme(f)
            self.show_tab("bd_theme_studio")
            messagebox.showinfo(
                "Theme Uploaded & Registered",
                f"Successfully uploaded and installed BetterDiscord theme:\n\n"
                f"Name: {res['meta']['name']}\n"
                f"Author: {res['meta']['author']}\n"
                f"File: {res['filename']}\n\n"
                f"It is now registered in BetterDiscord! You can click '[MODIFY THEME / EDIT CSS]' to customize its colors, wallpaper, or code."
            )
        except Exception as e:
            messagebox.showerror("Upload Error", f"Failed to upload theme:\n{e}")

    def action_import_theme_url(self):
        url = getattr(self, "theme_url_entry", None)
        if not url:
            return
        url_text = url.get().strip()
        if not url_text or not (url_text.startswith("http://") or url_text.startswith("https://")):
            messagebox.showwarning("Notice", "Please enter a valid HTTP or HTTPS URL to raw theme CSS.")
            return

        def _task():
            import urllib.request
            try:
                req = urllib.request.Request(url_text, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = resp.read()

                base = os.path.basename(url_text.split("?")[0])
                if not (base.endswith(".theme.css") or base.endswith(".css")):
                    base = "DownloadedTheme.theme.css"
                elif base.endswith(".css") and not base.endswith(".theme.css"):
                    base = base[:-4] + ".theme.css"

                target = os.path.join(bd_customizer.THEMES_DIR, base)
                with open(target, "wb") as f:
                    f.write(data)

                with open(target, "r", encoding="utf-8", errors="ignore") as f:
                    meta = bd_customizer.parse_metadata(f.read(4000))
                bd_customizer.toggle_theme(meta["name"], base, True)

                self.root.after(0, lambda: [
                    self.show_tab("bd_theme_studio"),
                    messagebox.showinfo("Success", f"Theme downloaded and installed:\n{meta['name']} by {meta['author']}")
                ])
            except Exception as e:
                self.root.after(0, lambda err=e: messagebox.showerror("Download Failed", f"Failed to download theme from URL:\n{err}"))

        threading.Thread(target=_task, daemon=True).start()

    def action_toggle_theme(self, name, filename, enable):
        bd_customizer.toggle_theme(name, filename, enable)
        self.show_tab("bd_theme_studio")
        state = "Enabled" if enable else "Disabled"
        messagebox.showinfo("Theme Status", f"Theme '{name}' is now {state} in BetterDiscord!\n\nPress Reload (Ctrl+R) to update Discord.")

    def action_clone_theme(self, filename):
        prompt_win = tk.Toplevel(self.root)
        prompt_win.title("Duplicate Theme")
        prompt_win.geometry("420x170")
        prompt_win.configure(bg=C_CARD)
        prompt_win.transient(self.root)
        prompt_win.grab_set()

        tk.Label(prompt_win, text="Enter a name for your cloned theme:", font=("DejaVu Sans", 9, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w", padx=16, pady=(16, 6))
        entry = tk.Entry(prompt_win, bg=C_CARD_ALT, fg="#ffffff", insertbackground="#ffffff", relief="flat", font=("DejaVu Sans", 10))
        entry.pack(fill="x", padx=16, ipady=4)
        entry.insert(0, "My Custom Modded Theme")
        entry.focus_set()

        def _do_clone():
            new_name = entry.get().strip()
            if not new_name:
                return
            prompt_win.destroy()
            try:
                new_fn = bd_customizer.clone_theme(filename, new_name)
                self.show_tab("bd_theme_studio")
                messagebox.showinfo("Theme Cloned", f"Successfully created cloned theme:\n{new_fn}\n\nYou can now modify it without altering the original!")
            except Exception as e:
                messagebox.showerror("Clone Error", str(e))

        btn_row = tk.Frame(prompt_win, bg=C_CARD)
        btn_row.pack(fill="x", padx=16, pady=(16, 0))
        tk.Button(btn_row, text="Create Clone", font=("DejaVu Sans", 8, "bold"), bg=C_PINK, fg="#10121a", relief="flat", padx=12, pady=4, cursor="hand2", command=_do_clone).pack(side="right")
        tk.Button(btn_row, text="Cancel", font=("DejaVu Sans", 8), bg="#3b3e4f", fg=C_TEXT, relief="flat", padx=10, pady=4, cursor="hand2", command=prompt_win.destroy).pack(side="right", padx=(0, 8))

    def action_delete_theme(self, filename, name):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete BetterDiscord theme '{name}' ({filename})?\n\nThis cannot be undone."):
            bd_customizer.delete_theme(filename)
            self.show_tab("bd_theme_studio")

    def open_theme_modifier(self, theme_info):
        filename = theme_info["filename"]
        try:
            full_css = bd_customizer.read_theme_full_css(filename)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read theme file:\n{e}")
            return

        mod_win = tk.Toplevel(self.root)
        mod_win.title(f"Discord-Chan Theme Studio - Modify Theme: {theme_info['name']}")
        mod_win.geometry("980x720")
        mod_win.configure(bg="#11131a")
        mod_win.transient(self.root)

        # Header Bar
        top = tk.Frame(mod_win, bg="#181b26", height=50, padx=16)
        top.pack(fill="x")
        top.pack_propagate(False)

        col_t = tk.Frame(top, bg="#181b26")
        col_t.pack(side="left", fill="both", expand=True, pady=6)
        tk.Label(col_t, text=f"THEME MODIFIER: {theme_info['name']}", font=("DejaVu Sans", 11, "bold"), bg="#181b26", fg=C_TEXT_H).pack(anchor="w")
        tk.Label(col_t, text=f"File: {filename}  |  Author: {theme_info['author']}  |  Version: {theme_info['version']}", font=("DejaVu Sans", 8), bg="#181b26", fg=C_MUTED).pack(anchor="w")

        btn_close = tk.Button(top, text="Close", font=("DejaVu Sans", 8), bg="#2b2f40", fg=C_TEXT_H, relief="flat", padx=12, pady=4, cursor="hand2", command=mod_win.destroy)
        btn_close.pack(side="right", pady=10)

        # Quick Tuner Card (Accent Color & Wallpaper replacer)
        tuner_card = tk.Frame(mod_win, bg="#161922", padx=16, pady=12)
        tuner_card.pack(fill="x", padx=14, pady=10)

        tk.Label(tuner_card, text="Quick Variable Modifiers (Color & Wallpaper Replacer)", font=("DejaVu Sans", 9, "bold"), bg="#161922", fg=C_PINK).pack(anchor="w")
        tk.Label(tuner_card, text="Quickly customize common theme variables without manually typing CSS:", font=("DejaVu Sans", 8), bg="#161922", fg=C_MUTED).pack(anchor="w", pady=(1, 8))

        row_vars = tk.Frame(tuner_card, bg="#161922")
        row_vars.pack(fill="x")

        # Color Tuner
        col_mod_color = tk.StringVar(value="#ff85a2")
        lbl_col_preview = tk.Label(row_vars, text="      ", bg=col_mod_color.get(), relief="solid", borderwidth=1)
        lbl_col_preview.pack(side="left", padx=(0, 6))

        def _pick_color():
            c = colorchooser.askcolor(col_mod_color.get(), title="Select New Theme Accent Color")[1]
            if c:
                col_mod_color.set(c)
                lbl_col_preview.config(bg=c)

        btn_c_pick = tk.Button(row_vars, text="Pick Accent Color", font=("DejaVu Sans", 8, "bold"), bg="#2d3244", fg=C_TEXT_H, relief="flat", padx=10, pady=3, cursor="hand2", command=_pick_color)
        btn_c_pick.pack(side="left", padx=(0, 14))

        # Wallpaper Tuner
        wp_mod_val = tk.StringVar(value="")
        tk.Label(row_vars, text="Custom Wallpaper:", font=("DejaVu Sans", 8, "bold"), bg="#161922", fg=C_TEXT).pack(side="left", padx=(0, 6))
        entry_wp = tk.Entry(row_vars, textvariable=wp_mod_val, bg="#10121a", fg="#ffffff", insertbackground="#ffffff", relief="flat", font=("DejaVu Sans", 8), width=24)
        entry_wp.pack(side="left", fill="x", expand=True, ipady=3, padx=(0, 6))

        def _browse_wp():
            f = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.webp *.gif"), ("All Files", "*.*")])
            if f:
                data_uri = theme_engine.get_image_data_uri(f)
                if data_uri:
                    wp_mod_val.set(data_uri)
                else:
                    wp_mod_val.set(f)

        btn_browse = tk.Button(row_vars, text="Browse Image...", font=("DejaVu Sans", 8), bg="#2d3244", fg=C_TEXT_H, relief="flat", padx=8, pady=3, cursor="hand2", command=_browse_wp)
        btn_browse.pack(side="left", padx=(0, 10))

        # CSS Code Editor Area
        editor_frame = tk.Frame(mod_win, bg="#11131a", padx=14)
        editor_frame.pack(fill="both", expand=True)

        toolbar = tk.Frame(editor_frame, bg="#161922", padx=8, pady=6)
        toolbar.pack(fill="x", pady=(0, 4))

        tk.Label(toolbar, text="Raw Theme CSS Editor", font=("DejaVu Sans", 8, "bold"), bg="#161922", fg=C_TEXT_H).pack(side="left", padx=(0, 10))

        # Search bar
        tk.Label(toolbar, text="Find:", font=("DejaVu Sans", 7), bg="#161922", fg=C_MUTED).pack(side="left")
        find_ent = tk.Entry(toolbar, width=14, bg="#10121a", fg="#ffffff", insertbackground="#ffffff", relief="flat", font=("DejaVu Sans", 8))
        find_ent.pack(side="left", padx=4)

        tk.Label(toolbar, text="Replace:", font=("DejaVu Sans", 7), bg="#161922", fg=C_MUTED).pack(side="left")
        rep_ent = tk.Entry(toolbar, width=14, bg="#10121a", fg="#ffffff", insertbackground="#ffffff", relief="flat", font=("DejaVu Sans", 8))
        rep_ent.pack(side="left", padx=4)

        text_scroll = tk.Scrollbar(editor_frame)
        text_editor = tk.Text(editor_frame, wrap="none", bg="#0e1017", fg="#d1d7e0",
                              insertbackground="#ffffff", selectbackground=C_BLURPLE,
                              font=("Courier", 10), padx=10, pady=8,
                              yscrollcommand=text_scroll.set)
        text_scroll.config(command=text_editor.yview)
        text_editor.pack(side="left", fill="both", expand=True)
        text_scroll.pack(side="right", fill="y")

        text_editor.insert("1.0", full_css)

        def _do_replace_all():
            target = find_ent.get()
            rep = rep_ent.get()
            if not target:
                return
            content = text_editor.get("1.0", "end-1c")
            count = content.count(target)
            if count == 0:
                messagebox.showinfo("Find & Replace", f"'{target}' not found in CSS.")
                return
            new_content = content.replace(target, rep)
            text_editor.delete("1.0", "end")
            text_editor.insert("1.0", new_content)
            messagebox.showinfo("Find & Replace", f"Replaced {count} occurrence(s) of '{target}'!")

        btn_rep = tk.Button(toolbar, text="Replace All", font=("DejaVu Sans", 7, "bold"), bg="#3b3f52", fg="#ffffff", relief="flat", padx=6, pady=2, cursor="hand2", command=_do_replace_all)
        btn_rep.pack(side="left", padx=4)

        # Snippet inserters
        def _insert_snippet(snip):
            text_editor.insert("end", "\n" + snip + "\n")
            text_editor.see("end")

        tk.Label(toolbar, text="| Snippets:", font=("DejaVu Sans", 7), bg="#161922", fg=C_MUTED).pack(side="left", padx=(10, 4))
        tk.Button(toolbar, text="+ Glass Chat", font=("DejaVu Sans", 7), bg="#2d3244", fg=C_PINK, relief="flat", padx=5, pady=2, cursor="hand2",
                  command=lambda: _insert_snippet(".messagesWrapper__36d07, .chatContent__52833 { background: transparent !important; }")).pack(side="left", padx=2)
        tk.Button(toolbar, text="+ Hidden Ch", font=("DejaVu Sans", 7), bg="#2d3244", fg=C_CYAN, relief="flat", padx=5, pady=2, cursor="hand2",
                  command=lambda: _insert_snippet("[class*='modeLocked_'] { opacity: 0.65 !important; }")).pack(side="left", padx=2)
        tk.Button(toolbar, text="+ Avatar Ring", font=("DejaVu Sans", 7), bg="#2d3244", fg=C_PURPLE, relief="flat", padx=5, pady=2, cursor="hand2",
                  command=lambda: _insert_snippet("[class*='avatar__'] { outline: 2px solid var(--accent-pink, #ff85a2) !important; outline-offset: 1px !important; }")).pack(side="left", padx=2)

        def _apply_tuner():
            cur_code = text_editor.get("1.0", "end-1c")
            replacements = {}
            if col_mod_color.get():
                replacements["--main-color"] = col_mod_color.get()
                replacements["--accent-pink"] = col_mod_color.get()
                replacements["--accent-color"] = col_mod_color.get()
            if wp_mod_val.get():
                replacements["--anime-wallpaper"] = f"url('{wp_mod_val.get()}')"
                replacements["--background-image"] = f"url('{wp_mod_val.get()}')"
            updated = bd_customizer.apply_variable_modifications(cur_code, replacements)
            text_editor.delete("1.0", "end")
            text_editor.insert("1.0", updated)
            messagebox.showinfo("Tuner Applied", "Quick variables updated in the CSS editor! Click 'Save Changes' to apply to Discord.")

        btn_apply_tuner = tk.Button(row_vars, text="APPLY QUICK TWEAKS", font=("DejaVu Sans", 8, "bold"), bg=C_GREEN, fg="#ffffff", relief="flat", padx=10, pady=3, cursor="hand2", command=_apply_tuner)
        btn_apply_tuner.pack(side="right")

        # Bottom Action Bar
        bot_bar = tk.Frame(mod_win, bg="#161922", padx=16, pady=10)
        bot_bar.pack(fill="x")

        def _save_changes(live=False):
            new_css = text_editor.get("1.0", "end-1c")
            try:
                bd_customizer.save_theme_full_css(filename, new_css)
                if live:
                    bd_customizer.toggle_theme(theme_info["name"], filename, True)
                    self.restart_discord_safe()
                    messagebox.showinfo("Saved & Applied", f"Theme '{theme_info['name']}' saved and hot-reloaded in Discord!")
                else:
                    messagebox.showinfo("Saved", f"Theme '{theme_info['name']}' changes saved successfully!")
                self.show_tab("bd_theme_studio")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

        btn_save_apply = tk.Button(bot_bar, text="LIVE APPLY TO DISCORD", font=("DejaVu Sans", 8, "bold"), bg=C_BLURPLE, fg="#ffffff", relief="flat", padx=14, pady=5, cursor="hand2", command=lambda: _save_changes(live=True))
        btn_save_apply.pack(side="left")

        btn_save = tk.Button(bot_bar, text="SAVE CHANGES", font=("DejaVu Sans", 8, "bold"), bg=C_PINK, fg="#10121a", relief="flat", padx=14, pady=5, cursor="hand2", command=lambda: _save_changes(live=False))
        btn_save.pack(side="left", padx=8)

        btn_dup_save = tk.Button(bot_bar, text="Save As New Theme...", font=("DejaVu Sans", 8), bg="#2d3244", fg=C_TEXT_H, relief="flat", padx=10, pady=5, cursor="hand2", command=lambda: self.action_clone_theme(filename))
        btn_dup_save.pack(side="left")

    # -------------------------------------------------------------
    # TAB: BETTERDISCORD PLUGIN MANAGER (UPLOAD & MANAGE)
    # -------------------------------------------------------------
    def render_bd_plugin_studio_tab(self):
        c = self.content_scroll
        plugins = bd_customizer.list_installed_plugins()

        # 1. Header Card
        card_head = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_head.pack(fill="x", pady=(0, 14))

        head_row = tk.Frame(card_head, bg=C_CARD)
        head_row.pack(fill="x")

        title_col = tk.Frame(head_row, bg=C_CARD)
        title_col.pack(side="left", fill="both", expand=True)

        tk.Label(title_col, text="BetterDiscord Plugin Manager & Uploader", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        desc = "Upload any BetterDiscord plugin (.plugin.js / .js / .zip), inspect source code, toggle active state, and manage your Discord client enhancements."
        tk.Label(title_col, text=desc, font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED, wraplength=640, justify="left").pack(anchor="w", pady=(2, 6))

        badge = tk.Frame(head_row, bg=C_CYAN, padx=12, pady=6)
        badge.pack(side="right", padx=(10, 0))
        tk.Label(badge, text="PLUGIN ENGINE", font=("DejaVu Sans", 7, "bold"), bg=C_CYAN, fg="#10121a").pack(anchor="center")
        tk.Label(badge, text="BetterDiscord JS API", font=("DejaVu Sans", 8, "bold"), bg=C_CYAN, fg="#10121a").pack(anchor="center")

        tk.Frame(card_head, bg=C_BORDER, height=1).pack(fill="x", pady=10)

        # Upload Action Buttons
        act_row = tk.Frame(card_head, bg=C_CARD)
        act_row.pack(fill="x")

        btn_up = tk.Button(act_row, text="+ UPLOAD BETTERDISCORD PLUGIN (.js / .zip)", font=("DejaVu Sans", 9, "bold"),
                           bg=C_CYAN, fg="#10121a", relief="flat", padx=16, pady=6, cursor="hand2",
                           command=self.action_upload_bd_plugin)
        btn_up.pack(side="left", padx=(0, 10))

        btn_fld = tk.Button(act_row, text="Open Plugins Folder", font=("DejaVu Sans", 8),
                            bg="#2e3244", fg=C_TEXT_H, relief="flat", padx=12, pady=6, cursor="hand2",
                            command=lambda: self.open_folder_system(bd_customizer.PLUGINS_DIR))
        btn_fld.pack(side="left", padx=(0, 10))

        btn_rel = tk.Button(act_row, text="Hot-Reload Discord Client", font=("DejaVu Sans", 8, "bold"),
                            bg=C_BLURPLE, fg="#ffffff", relief="flat", padx=12, pady=6, cursor="hand2",
                            command=self.restart_discord_safe)
        btn_rel.pack(side="left")

        # 2. Installed Plugins List
        card_list = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_list.pack(fill="x")

        tk.Label(card_list, text=f"Installed BetterDiscord Plugins ({len(plugins)})", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w", pady=(0, 10))

        if not plugins:
            tk.Label(card_list, text="No plugins installed. Click '+ UPLOAD BETTERDISCORD PLUGIN' above to add your first plugin!", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=10)
        else:
            for p in plugins:
                self.create_plugin_item_card(card_list, p)

    def create_plugin_item_card(self, parent, p):
        card = tk.Frame(parent, bg=C_CARD_ALT, padx=14, pady=12)
        card.pack(fill="x", pady=5)

        top_r = tk.Frame(card, bg=C_CARD_ALT)
        top_r.pack(fill="x")

        status_color = C_GREEN if p["is_enabled"] else C_MUTED
        status_txt = "RUNNING / ACTIVE" if p["is_enabled"] else "DISABLED"
        tk.Label(top_r, text=f"[{status_txt}]", font=("DejaVu Sans", 7, "bold"), bg=C_CARD_ALT, fg=status_color).pack(side="left", padx=(0, 8))

        tk.Label(top_r, text=p["name"], font=("DejaVu Sans", 10, "bold"), bg=C_CARD_ALT, fg=C_TEXT_H).pack(side="left")
        tk.Label(top_r, text=f"v{p['version']} by {p['author']}  ({p['size_kb']} KB)", font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_MUTED).pack(side="left", padx=8)

        tk.Label(card, text=p["description"], font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_MUTED, wraplength=640, justify="left").pack(anchor="w", pady=(4, 8))

        act_r = tk.Frame(card, bg=C_CARD_ALT)
        act_r.pack(fill="x")

        # Toggle Button
        if p["is_enabled"]:
            btn_tog = tk.Button(act_r, text="Deactivate Plugin", font=("DejaVu Sans", 8), bg="#3b3e4f", fg=C_TEXT,
                                relief="flat", padx=10, pady=3, cursor="hand2",
                                command=lambda fn=p["filename"], nm=p["name"]: self.action_toggle_plugin(nm, fn, False))
        else:
            btn_tog = tk.Button(act_r, text="Activate Plugin", font=("DejaVu Sans", 8, "bold"), bg=C_GREEN, fg="#ffffff",
                                relief="flat", padx=10, pady=3, cursor="hand2",
                                command=lambda fn=p["filename"], nm=p["name"]: self.action_toggle_plugin(nm, fn, True))
        btn_tog.pack(side="left", padx=(0, 6))

        # Inspect / Edit Code Button
        btn_mod = tk.Button(act_r, text="[VIEW / EDIT CODE]", font=("DejaVu Sans", 8, "bold"), bg=C_CYAN, fg="#10121a",
                            relief="flat", padx=12, pady=3, cursor="hand2",
                            command=lambda pl=p: self.open_plugin_code_inspector(pl))
        btn_mod.pack(side="left", padx=(0, 6))

        # Delete Button (protect studio hotkey plugin from deletion)
        if p["filename"] != "DiscordChanStudioHotkey.plugin.js":
            btn_del = tk.Button(act_r, text="Delete", font=("DejaVu Sans", 8), bg=C_RED, fg="#ffffff",
                                relief="flat", padx=8, pady=3, cursor="hand2",
                                command=lambda fn=p["filename"], nm=p["name"]: self.action_delete_plugin(fn, nm))
            btn_del.pack(side="right")

    def action_upload_bd_plugin(self):
        f = filedialog.askopenfilename(
            title="Select BetterDiscord Plugin to Upload",
            filetypes=[("BetterDiscord Plugin / JS / ZIP", "*.plugin.js *.js *.zip"), ("All Files", "*.*")]
        )
        if not f:
            return
        try:
            installed_name = bd_customizer.upload_plugin(f)
            self.show_tab("bd_plugin_studio")
            messagebox.showinfo(
                "Plugin Uploaded & Activated",
                f"Successfully installed and activated BetterDiscord plugin:\n\n{installed_name}\n\n"
                f"Tip: Click 'Hot-Reload Discord Client' or press Ctrl+R in Discord to start running it!"
            )
        except Exception as e:
            messagebox.showerror("Upload Error", f"Failed to upload plugin:\n{e}")

    def action_toggle_plugin(self, name, filename, enable):
        bd_customizer.toggle_plugin(name, filename, enable)
        self.show_tab("bd_plugin_studio")
        state = "Activated" if enable else "Deactivated"
        messagebox.showinfo("Plugin State", f"Plugin '{name}' is now {state}!\n\nHot-reload Discord (Ctrl+R) to apply changes.")

    def action_delete_plugin(self, filename, name):
        if messagebox.askyesno("Confirm Delete", f"Delete BetterDiscord plugin '{name}' ({filename})?"):
            bd_customizer.delete_plugin(filename)
            self.show_tab("bd_plugin_studio")

    def open_plugin_code_inspector(self, plugin_info):
        filename = plugin_info["filename"]
        try:
            content = bd_customizer.read_plugin_content(filename)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read plugin:\n{e}")
            return

        p_win = tk.Toplevel(self.root)
        p_win.title(f"Plugin Code Inspector: {plugin_info['name']}")
        p_win.geometry("900x640")
        p_win.configure(bg="#11131a")
        p_win.transient(self.root)

        top = tk.Frame(p_win, bg="#181b26", padx=14, pady=10)
        top.pack(fill="x")
        tk.Label(top, text=f"PLUGIN: {plugin_info['name']} v{plugin_info['version']}", font=("DejaVu Sans", 10, "bold"), bg="#181b26", fg=C_TEXT_H).pack(anchor="w")
        tk.Label(top, text=f"File: {filename}  |  by {plugin_info['author']}", font=("DejaVu Sans", 8), bg="#181b26", fg=C_MUTED).pack(anchor="w")

        f_text = tk.Frame(p_win, bg="#11131a", padx=12, pady=8)
        f_text.pack(fill="both", expand=True)

        sc = tk.Scrollbar(f_text)
        txt = tk.Text(f_text, wrap="none", bg="#0e1017", fg="#a6accd", insertbackground="#ffffff", selectbackground=C_BLURPLE, font=("Courier", 10), padx=8, pady=8, yscrollcommand=sc.set)
        sc.config(command=txt.yview)
        txt.pack(side="left", fill="both", expand=True)
        sc.pack(side="right", fill="y")
        txt.insert("1.0", content)

        bot = tk.Frame(p_win, bg="#181b26", padx=14, pady=10)
        bot.pack(fill="x")

        def _save_plugin():
            new_code = txt.get("1.0", "end-1c")
            try:
                bd_customizer.save_plugin_content(filename, new_code)
                messagebox.showinfo("Saved", f"Plugin '{plugin_info['name']}' saved successfully!")
                self.show_tab("bd_plugin_studio")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

        tk.Button(bot, text="SAVE CODE CHANGES", font=("DejaVu Sans", 8, "bold"), bg=C_CYAN, fg="#10121a", relief="flat", padx=14, pady=5, cursor="hand2", command=_save_plugin).pack(side="left")
        tk.Button(bot, text="Close", font=("DejaVu Sans", 8), bg="#2d3244", fg=C_TEXT_H, relief="flat", padx=12, pady=5, cursor="hand2", command=p_win.destroy).pack(side="right")

    # -------------------------------------------------------------
    # TAB: DISCORD UI ENHANCEMENTS & TOGGLES
    # -------------------------------------------------------------
    def render_discord_ui_tab(self):
        c = self.content_scroll

        # Header Card
        card_head = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_head.pack(fill="x", pady=(0, 14))

        tk.Label(card_head, text="Discord UI Enhancements & Toggles", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        desc = "Toggle specialized CSS modifications directly injected into the Discord client: hidden channels styling, compact layout, privacy avatar blur, and smooth animations."
        tk.Label(card_head, text=desc, font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED, wraplength=640, justify="left").pack(anchor="w", pady=(2, 10))

        btn_apply = tk.Button(card_head, text="SAVE & APPLY UI ENHANCEMENTS", font=("DejaVu Sans", 8, "bold"),
                              bg=C_BLURPLE, fg="#ffffff", relief="flat", padx=16, pady=6, cursor="hand2",
                              command=self.apply_theme_action)
        btn_apply.pack(anchor="w")

        # Enhancement Cards
        features = [
            (self.show_hidden_ch_var, "Show Hidden & Locked Channels Indicator",
             "Styles locked or restricted channels with soft rose lock icons and dimmed titles so you can navigate them clearly."),
            (self.compact_mode_var, "Ultra Compact Chat Mode",
             "Reduces vertical padding between messages, channel items, and embeds for high-density reading."),
            (self.hide_member_list_var, "Auto-Collapse Member List",
             "Collapses the right-hand server members list to a slim 48px bar; expands smoothly on mouse hover."),
            (self.hide_server_list_var, "Auto-Collapse Server Rail (Guilds)",
             "Collapses the left-hand server icon rail to a minimalist 14px strip; expands smoothly on hover."),
            (self.smooth_anim_var, "Smooth Hover Transitions & Animations",
             "Enables sleek 0.18s cubic-bezier sliding and fading animations on channel links, messages, and action buttons."),
            (self.mention_glow_var, "Mention & Unread Soft Neon Glow",
             "Highlights pings and unread channel badges with a soft luminous pink neon border and gradient glow."),
            (self.blur_avatars_var, "Privacy Blur User Avatars",
             "Applies a subtle privacy blur to all chat profile avatars; reveals avatar smoothly on mouse hover."),
            (self.typing_indicator_var, "Styled Typing Indicator Bubble",
             "Renders the 'several people are typing...' status inside a floating translucent pill with accent colored dots.")
        ]

        card_opts = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_opts.pack(fill="x")

        for var, title, detail in features:
            self.create_feature_toggle_row(card_opts, var, title, detail)

    def create_feature_toggle_row(self, parent, var, title, desc):
        row = tk.Frame(parent, bg=C_CARD_ALT, padx=14, pady=10)
        row.pack(fill="x", pady=4)

        col = tk.Frame(row, bg=C_CARD_ALT)
        col.pack(side="left", fill="both", expand=True)

        tk.Label(col, text=title, font=("DejaVu Sans", 9, "bold"), bg=C_CARD_ALT, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(col, text=desc, font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_MUTED, wraplength=580, justify="left").pack(anchor="w", pady=(2, 0))

        btn = tk.Button(row, text="[ ENABLED ]" if var.get() else "[ DISABLED ]",
                        font=("DejaVu Sans", 8, "bold"),
                        bg=C_GREEN if var.get() else "#3b3e4f",
                        fg="#ffffff", relief="flat", padx=12, pady=5, cursor="hand2")
        def _toggle():
            new_v = not var.get()
            var.set(new_v)
            btn.config(text="[ ENABLED ]" if new_v else "[ DISABLED ]",
                       bg=C_GREEN if new_v else "#3b3e4f")
        btn.config(command=_toggle)
        btn.pack(side="right")

    def open_folder_system(self, path):
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.run(["open", path])
        else:
            subprocess.run(["xdg-open", path])

    # -------------------------------------------------------------
    # TAB 9: CONTRIBUTORS & WIKI
    # -------------------------------------------------------------
    def render_about_tab(self):
        c = self.content_scroll

        card_author = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_author.pack(fill="x", pady=(0, 14))

        tk.Label(card_author, text="Project Lead & Maintainer", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w", pady=(0, 8))

        row_a = tk.Frame(card_author, bg=C_CARD_ALT, padx=14, pady=12)
        row_a.pack(fill="x")

        if self.prof_icon_photo:
            tk.Label(row_a, image=self.prof_icon_photo, bg=C_CARD_ALT).pack(side="left", padx=(0, 12))

        col_a = tk.Frame(row_a, bg=C_CARD_ALT)
        col_a.pack(side="left", fill="both", expand=True)

        tk.Label(col_a, text="myzert (zerttcihuy@gmail.com)", font=("DejaVu Sans", 10, "bold"), bg=C_CARD_ALT, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(col_a, text="GitHub: https://github.com/myzert/discord-chan", font=("DejaVu Sans", 9), bg=C_CARD_ALT, fg=C_BLURPLE).pack(anchor="w", pady=2)
        tk.Label(col_a, text="Role: Creator, UI/UX Designer, and Open-Source Project Maintainer", font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_MUTED).pack(anchor="w")

        # GitHub Wiki Card
        card_wiki = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_wiki.pack(fill="x")

        tk.Label(card_wiki, text="Official Documentation & Wiki", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        info = (
            "Explore full technical guides, tutorials, and customization guides in our GitHub Wiki:\n\n"
            "• Theme Customization Guide (Colors, Opacities, Corner Radius)\n"
            "• Transparent Window Mode Setup (See apps behind Discord)\n"
            "• Chrome-Style Extension Development Guide (.zip specification)\n"
            "• Theme Export/Import Workflow\n"
            "• Zero-Lag CSS Performance Optimization Guide"
        )
        tk.Label(card_wiki, text=info, font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED, justify="left").pack(anchor="w", pady=(4, 0))

    # -------------------------------------------------------------
    # ACTIONS & CALLBACKS
    # -------------------------------------------------------------
    def open_command_palette(self):
        pal_win = tk.Toplevel(self.root)
        pal_win.title("Command Palette")
        pal_win.geometry("540x440")
        pal_win.configure(bg=C_CARD)
        pal_win.transient(self.root)
        pal_win.grab_set()

        head = tk.Frame(pal_win, bg=C_SIDEBAR, padx=14, pady=10)
        head.pack(fill="x")
        tk.Label(head, text="DISCORD-CHAN COMMAND PALETTE", font=("DejaVu Sans", 10, "bold"), bg=C_SIDEBAR, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(head, text="Select an action to execute immediately:", font=("DejaVu Sans", 8), bg=C_SIDEBAR, fg=C_MUTED).pack(anchor="w")

        commands = [
            ("Toggle Master Theme (ON / OFF)", lambda: [pal_win.destroy(), self.toggle_master_theme()]),
            ("Open Theme Manager (Wallpapers & Live PVs)", lambda: [pal_win.destroy(), self.show_tab("theme_manager")]),
            ("Open BetterDiscord Theme Studio (Upload & Modify)", lambda: [pal_win.destroy(), self.show_tab("bd_theme_studio")]),
            ("Open BetterDiscord Plugin Manager (Upload & Manage)", lambda: [pal_win.destroy(), self.show_tab("bd_plugin_studio")]),
            ("Open Discord UI Enhancements (Toggles & Style)", lambda: [pal_win.destroy(), self.show_tab("discord_ui")]),
            ("Switch to Anime Wallpaper Mode", lambda: [pal_win.destroy(), self.select_display_mode("anime_wallpaper")]),
            ("Switch to Transparent Window Mode", lambda: [pal_win.destroy(), self.select_display_mode("window_transparent")]),
            ("Switch to Vanilla Discord Client", lambda: [pal_win.destroy(), self.select_display_mode("vanilla_discord")]),
            ("Save & Apply Theme (Ctrl+S)", lambda: [pal_win.destroy(), self.apply_theme_action()]),
            ("Export Theme as ZIP Bundle", lambda: [pal_win.destroy(), self.action_export_theme()]),
            ("Import Theme from ZIP Bundle", lambda: [pal_win.destroy(), self.action_import_theme()]),
            ("Restart Discord Safely (Ctrl+R)", lambda: [pal_win.destroy(), self.restart_discord_safe()]),
            ("Stop Discord Process", lambda: [pal_win.destroy(), subprocess.run(["pkill", "-9", "-f", "Discord.real"])])
        ]

        f = tk.Frame(pal_win, bg=C_CARD, padx=10, pady=8)
        f.pack(fill="both", expand=True)

        for text, func in commands:
            b = tk.Button(f, text=f"-  {text}", font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_TEXT_H,
                          relief="flat", anchor="w", padx=12, pady=4, cursor="hand2", command=func)
            b.pack(fill="x", pady=2)

    def select_preset_wallpaper(self, wp):
        self.settings["wallpaper_id"] = wp["id"]
        self.settings["wallpaper_path"] = wp["path"]
        self.custom_path_var.set(wp["path"])
        self.settings["theme_mode"] = "anime_wallpaper"
        self.settings["theme_enabled"] = True
        self.theme_mode_var.set("anime_wallpaper")
        self.theme_enabled_var.set(True)
        if "accent_hex" in wp:
            self.settings["accent_color"] = wp["accent_hex"]
        self.apply_theme_action(silent=True)
        self.show_tab("theme_manager")
        messagebox.showinfo("Theme Mod Applied", f"Theme successfully applied:\n{wp['name']}\n\nMode: Anime Glass Translucency\nAccent: {wp.get('accent_name', 'Default')}")

    def browse_custom_wallpaper(self):
        f = filedialog.askopenfilename(
            title="Select Custom Anime Wallpaper",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.webp *.gif"), ("All Files", "*.*")]
        )
        if f:
            self.custom_path_var.set(f)

    def browse_in_directory(self, d):
        if not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
        f = filedialog.askopenfilename(
            initialdir=d,
            title="Select Wallpaper",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.webp *.gif"), ("All Files", "*.*")]
        )
        if f:
            self.custom_path_var.set(f)
            self.apply_custom_wallpaper()

    def apply_custom_wallpaper(self):
        p = self.custom_path_var.get().strip()
        if not p or not os.path.exists(p):
            messagebox.showerror("Error", "Selected file does not exist!")
            return
        self.settings["wallpaper_id"] = "custom"
        self.settings["wallpaper_path"] = p
        self.apply_theme_action(silent=False)
        self.show_tab("theme_manager")

    def select_palette(self, name, pri, sec):
        self.settings["active_preset"] = name
        self.settings["accent_color"] = pri
        self.settings["soft_pink"] = sec
        self.apply_theme_action(silent=True)
        self.show_tab("colors")
        messagebox.showinfo("Palette Applied", f"Palette '{name}' activated!")

    def pick_accent_color(self):
        c = colorchooser.askcolor(color=self.settings.get("accent_color", "#ff85a2"))
        if c and c[1]:
            self.settings["accent_color"] = c[1]
            if hasattr(self, 'lbl_accent_sample'):
                self.lbl_accent_sample.config(bg=c[1])

    def pick_soft_color(self):
        c = colorchooser.askcolor(color=self.settings.get("soft_pink", "#fbcfe8"))
        if c and c[1]:
            self.settings["soft_pink"] = c[1]
            if hasattr(self, 'lbl_soft_sample'):
                self.lbl_soft_sample.config(bg=c[1])

    def set_speaking_color(self, col):
        self.settings["speaking_color"] = col
        self.apply_theme_action(silent=True)
        self.show_tab("voice")
        messagebox.showinfo("Voice Ring", f"Speaking ring color updated to {col}!")

    def apply_theme_action(self, silent=False):
        self.settings["theme_enabled"] = self.theme_enabled_var.get()
        self.settings["theme_mode"] = self.theme_mode_var.get()
        self.settings["wallpaper_opacity"] = self.wp_opacity_var.get()
        self.settings["window_darkness"] = self.win_darkness_var.get()
        self.settings["sidebar_opacity"] = self.sidebar_op_var.get()
        self.settings["guilds_opacity"] = self.guilds_op_var.get()
        self.settings["chat_input_opacity"] = self.chat_input_op_var.get()
        self.settings["embed_opacity"] = self.embed_op_var.get()
        self.settings["corner_radius"] = self.corner_radius_var.get()
        self.settings["tile_opacity"] = self.tile_op_var.get()
        self.settings["tile_radius"] = self.tile_rad_var.get()
        self.settings["profile_opacity"] = self.prof_op_var.get()
        self.settings["top_spacing"] = self.top_spacing_var.get()
        self.settings["zero_lag"] = self.zero_lag_var.get()
        self.settings["chat_avatar_fixed"] = self.avatar_fix_var.get()
        # Discord UI Enhancements
        self.settings["show_hidden_channels"] = self.show_hidden_ch_var.get()
        self.settings["compact_mode"] = self.compact_mode_var.get()
        self.settings["hide_member_list"] = self.hide_member_list_var.get()
        self.settings["hide_server_list"] = self.hide_server_list_var.get()
        self.settings["smooth_animations"] = self.smooth_anim_var.get()
        self.settings["mention_glow"] = self.mention_glow_var.get()
        self.settings["blur_avatars"] = self.blur_avatars_var.get()
        self.settings["typing_indicator_fancy"] = self.typing_indicator_var.get()

        theme_engine.apply_theme(self.settings)
        if not silent:
            messagebox.showinfo("Success", "Theme updated and applied to Discord successfully!")

    def run_instant_setup(self):
        bd_injector.inject()
        kaede = os.path.join(REPO_DIR, "assets", "wallpapers", "kaede_to_suzu.webp")
        if os.path.exists(kaede):
            self.settings["wallpaper_id"] = "kaede_to_suzu"
            self.settings["wallpaper_path"] = kaede
            self.custom_path_var.set(kaede)
        self.apply_theme_action(silent=True)
        self.show_tab("theme_manager")
        messagebox.showinfo("Install Complete", "Discord-Chan has been successfully installed and injected!\n\nWelcome to Theme Manager. Select your preferred anime theme mod or UI preset below.")

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not getattr(self, "is_fullscreen", False)
        try:
            self.root.attributes("-fullscreen", self.is_fullscreen)
        except Exception:
            try:
                self.root.attributes("-zoomed", self.is_fullscreen)
            except Exception:
                pass
        if hasattr(self, "btn_fullscreen"):
            self.btn_fullscreen.config(
                text="Windowed (F11)" if self.is_fullscreen else "Full Screen (F11)",
                bg=C_BLURPLE if self.is_fullscreen else "#3b3e45"
            )

    def exit_fullscreen(self, event=None):
        if getattr(self, "is_fullscreen", False):
            self.toggle_fullscreen()

    def restart_discord_safe(self):
        subprocess.run(["pkill", "-9", "-f", "Discord.real"])
        subprocess.Popen(
            "setsid /root/.config/discord/Discord --url -- </dev/null >/tmp/discord.log 2>&1 &",
            shell=True
        )
        messagebox.showinfo("Discord", "Discord restarted safely with anti-crash flags.")

def main():
    root = tk.Tk()
    app = DiscordStyledStudio(root)
    root.mainloop()

if __name__ == "__main__":
    main()
