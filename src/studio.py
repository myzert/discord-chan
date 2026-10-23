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
import bd_store
import icon_manager
import plugins_manager
import theme_packager
import extensions_system

# Discord Official Dark Palette
C_GUILDS    = "#1e1f22"
C_SIDEBAR   = "#2b2d31"
C_CONTENT   = "#313338"
C_CARD      = "#232428"
C_CARD_ALT  = "#1e1f22"
C_HEADER    = "#313338"
C_BORDER    = "#1f2023"
C_BLURPLE   = "#5865f2"
C_BLURPLE_H = "#4752c4"
C_PINK      = "#ff85a2"
C_GREEN     = "#23a55a"
C_GREEN_H   = "#1f8b4c"
C_RED       = "#da373c"
C_TEXT      = "#dbdee1"
C_TEXT_H    = "#f2f3f5"
C_MUTED     = "#949ba4"

WALLPAPERS = [
    {
        "id": "kaede_to_suzu",
        "name": "Kaede to Suzu The Animation",
        "desc": "Maid Twins Anime (1920x1080 Full HD)",
        "path": os.path.join(REPO_DIR, "assets", "wallpapers", "kaede_to_suzu.webp")
    },
    {
        "id": "whisper",
        "name": "Whisper Me a Love Song",
        "desc": "Sasayaku You ni Koi wo Utau (Yori & Himari)",
        "path": os.path.join(REPO_DIR, "assets", "wallpapers", "1_whisper_me_a_love_song.jpg")
    },
    {
        "id": "sakura",
        "name": "Sakura Blossom Minimal",
        "desc": "Japanese Cherry Blossom Aesthetic",
        "path": os.path.join(REPO_DIR, "assets", "wallpapers", "2_sakura_blossom_minimal.jpg")
    },
    {
        "id": "clouds",
        "name": "Pastel Sunset Clouds",
        "desc": "Soft Evening Pastel Scenery",
        "path": os.path.join(REPO_DIR, "assets", "wallpapers", "3_pastel_clouds_scenery.jpg")
    },
    {
        "id": "neko",
        "name": "Discord-Chan Neko Mascot",
        "desc": "Minimalist Dark Neko Wallpaper",
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

        self.create_guild_action("SETUP", C_BLURPLE, "#ffffff", self.run_instant_setup)
        self.create_guild_action("APPLY", C_CARD, C_TEXT_H, self.apply_theme_action)
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

        self.add_category_header("CUSTOMIZATION")
        self.add_channel_btn("wallpapers", "wallpapers-manager")
        self.add_channel_btn("colors", "color-palette")
        self.add_channel_btn("voice", "voice-and-video")
        self.add_channel_btn("layout", "layout-and-clearance")

        self.add_category_header("BETTERDISCORD ADDONS")
        self.add_channel_btn("bd_store", "download-ui-and-plugins")

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
        elif tab_id == "wallpapers":
            self.top_channel_title.config(text="wallpapers-manager")
            self.top_topic.config(text="| Featured anime presets and manual all-custom image loader")
            self.render_wallpapers_tab()
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
        elif tab_id == "bd_store":
            self.top_channel_title.config(text="betterdiscord-addons-store")
            self.top_topic.config(text="| Download BetterDiscord UI themes & plugins directly with 1-click")
            self.render_bd_store_tab()
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
    # TAB 3: WALLPAPERS MANAGER (ALL-CUSTOM & PRESETS)
    # -------------------------------------------------------------
    def render_wallpapers_tab(self):
        c = self.content_scroll
        active_id = self.settings.get("wallpaper_id", "kaede_to_suzu")
        current_path = self.settings.get("wallpaper_path", "")

        hero_card = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        hero_card.pack(fill="x", pady=(0, 14))

        tk.Label(hero_card, text="CURRENT ACTIVE WALLPAPER", font=("DejaVu Sans", 8, "bold"), bg=C_CARD, fg=C_PINK).pack(anchor="w")

        row_h = tk.Frame(hero_card, bg=C_CARD)
        row_h.pack(fill="x", pady=(6, 0))

        thumb = self.get_thumbnail(current_path, width=160, height=90)
        lbl_h_thumb = tk.Label(row_h, image=thumb, bg=C_CARD)
        lbl_h_thumb.image = thumb
        lbl_h_thumb.pack(side="left", padx=(0, 14))

        info_h = tk.Frame(row_h, bg=C_CARD)
        info_h.pack(side="left", fill="both", expand=True)

        active_name = "Custom Wallpaper"
        for wp in WALLPAPERS:
            if wp["id"] == active_id:
                active_name = wp["name"]
                break

        tk.Label(info_h, text=active_name, font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(info_h, text=f"Path: {current_path}", font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED, wraplength=480, justify="left").pack(anchor="w", pady=(2, 4))

        tag_row = tk.Frame(info_h, bg=C_CARD)
        tag_row.pack(anchor="w", pady=(2, 0))
        tk.Label(tag_row, text="[ ACTIVE IN DISCORD ]", font=("DejaVu Sans", 8, "bold"), bg=C_GREEN, fg="#ffffff", padx=8, pady=2).pack(side="left")

        # Featured Presets
        card_presets = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_presets.pack(fill="x", pady=(0, 14))

        tk.Label(card_presets, text="Featured Anime Presets", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_presets, text="Click to apply high-definition anime backgrounds immediately:", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 10))

        for wp in WALLPAPERS:
            is_active = (wp["id"] == active_id)
            row = tk.Frame(card_presets, bg=C_CARD_ALT, padx=10, pady=8)
            row.pack(fill="x", pady=4)

            wp_thumb = self.get_thumbnail(wp["path"], width=110, height=62)
            lbl_t = tk.Label(row, image=wp_thumb, bg=C_CARD_ALT)
            lbl_t.image = wp_thumb
            lbl_t.pack(side="left", padx=(0, 12))

            col_d = tk.Frame(row, bg=C_CARD_ALT)
            col_d.pack(side="left", fill="both", expand=True)
            tk.Label(col_d, text=wp["name"], font=("DejaVu Sans", 9, "bold"), bg=C_CARD_ALT, fg=C_TEXT_H).pack(anchor="w")
            tk.Label(col_d, text=wp["desc"], font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_MUTED).pack(anchor="w", pady=(2, 0))

            if is_active:
                tk.Label(row, text="[ CURRENT ]", font=("DejaVu Sans", 8, "bold"), bg=C_GREEN, fg="#ffffff", padx=10, pady=4).pack(side="right")
            else:
                btn = tk.Button(row, text="Select Wallpaper", font=("DejaVu Sans", 8, "bold"), bg=C_BLURPLE, fg="#fff",
                                relief="flat", padx=12, pady=4, cursor="hand2", command=lambda w=wp: self.select_preset_wallpaper(w))
                btn.pack(side="right")

        # All-Custom Manual File Selection
        card_custom = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_custom.pack(fill="x", pady=(0, 14))

        tk.Label(card_custom, text="Custom Wallpaper (Manual File Selection)", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_custom, text="Choose ANY image file from your computer without restriction (jpg, png, webp, gif):", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 8))

        row_c = tk.Frame(card_custom, bg=C_CARD)
        row_c.pack(fill="x", pady=4)

        entry = tk.Entry(row_c, textvariable=self.custom_path_var, bg=C_CARD_ALT, fg=C_TEXT_H, insertbackground=C_TEXT_H, relief="flat", font=("DejaVu Sans", 9))
        entry.pack(side="left", fill="x", expand=True, ipady=5, padx=(0, 8))

        tk.Button(row_c, text="Browse File...", font=("DejaVu Sans", 8, "bold"), bg="#3b3e45", fg=C_TEXT_H, relief="flat", padx=10, pady=5, cursor="hand2",
                  command=self.browse_custom_wallpaper).pack(side="left")

        tk.Button(row_c, text="Apply Custom Image", font=("DejaVu Sans", 8, "bold"), bg=C_BLURPLE, fg="#fff", relief="flat", padx=12, pady=5, cursor="hand2",
                  command=self.apply_custom_wallpaper).pack(side="left", padx=(8, 0))

        # Quick directory jumps
        row_quick = tk.Frame(card_custom, bg=C_CARD)
        row_quick.pack(fill="x", pady=(8, 0))
        tk.Label(row_quick, text="Quick folders:", font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED).pack(side="left", padx=(0, 6))

        home = os.path.expanduser("~")
        for q_name, q_dir in [("Downloads", os.path.join(home, "Downloads")), ("Pictures", os.path.join(home, "Pictures")), ("Wallpapers", os.path.join(REPO_DIR, "assets", "wallpapers"))]:
            tk.Button(row_quick, text=f"[{q_name}]", font=("DejaVu Sans", 8), bg=C_CARD, fg=C_TEXT, relief="flat", cursor="hand2",
                      command=lambda d=q_dir: self.browse_in_directory(d)).pack(side="left", padx=3)

        # Wallpaper Darkness Overlay
        card_trans = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_trans.pack(fill="x")

        tk.Label(card_trans, text="Wallpaper Darkening Overlay", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_trans, text="Adjust dark overlay to ensure high contrast text against light anime artwork:", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 8))

        self.create_slider(card_trans, "Wallpaper Darkening Level:", self.wp_opacity_var, 0.10, 0.95, 0.02)

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
    # TAB: BETTERDISCORD ADDON STORE (THEMES & PLUGINS)
    # -------------------------------------------------------------
    def render_bd_store_tab(self):
        c = self.content_scroll

        # 1. Store Header & Powered by BetterDiscord Card
        card_head = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_head.pack(fill="x", pady=(0, 14))

        head_row = tk.Frame(card_head, bg=C_CARD)
        head_row.pack(fill="x")

        title_col = tk.Frame(head_row, bg=C_CARD)
        title_col.pack(side="left", fill="both", expand=True)

        tk.Label(title_col, text="BetterDiscord Addon Store & UI Downloader", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        desc = "Download popular community UI themes and plugins directly into BetterDiscord with 1-click. No manual file moving required."
        tk.Label(title_col, text=desc, font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED, wraplength=640, justify="left").pack(anchor="w", pady=(2, 4))

        # Big Distinction Badge
        badge_frame = tk.Frame(head_row, bg="#5865f2", padx=14, pady=8)
        badge_frame.pack(side="right", padx=(10, 0))
        tk.Label(badge_frame, text="POWERED BY", font=("DejaVu Sans", 7, "bold"), bg="#5865f2", fg="#e0e3ff").pack(anchor="center")
        tk.Label(badge_frame, text="BetterDiscord Engine", font=("DejaVu Sans", 9, "bold"), bg="#5865f2", fg="#ffffff").pack(anchor="center")

        tk.Frame(card_head, bg=C_BORDER, height=1).pack(fill="x", pady=10)

        # BetterDiscord Directory Status & Open Buttons
        bd_base, bd_themes, bd_plugins = bd_store.get_bd_dirs()
        bd_status = bd_injector.check_status()
        status_txt = "Active & Injected" if bd_status.get("injected") else "Installed (Not Injected)"

        info_row = tk.Frame(card_head, bg=C_CARD)
        info_row.pack(fill="x")

        stat_badge_col = tk.Frame(info_row, bg=C_CARD)
        stat_badge_col.pack(side="left")
        tk.Label(stat_badge_col, text=f"Engine Status: {status_txt}", font=("DejaVu Sans", 8, "bold"), bg=C_CARD, fg=C_GREEN if bd_status.get("injected") else C_MUTED).pack(side="left")
        tk.Label(stat_badge_col, text=f"  |  Location: {bd_base}", font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED).pack(side="left")

        actions_sub = tk.Frame(info_row, bg=C_CARD)
        actions_sub.pack(side="right")

        tk.Button(actions_sub, text="Open Themes Folder", font=("DejaVu Sans", 8), bg="#3b3e45", fg=C_TEXT_H,
                  relief="flat", padx=8, pady=3, cursor="hand2",
                  command=lambda: self.open_folder_system(bd_themes)).pack(side="left", padx=(0, 6))

        tk.Button(actions_sub, text="Open Plugins Folder", font=("DejaVu Sans", 8), bg="#3b3e45", fg=C_TEXT_H,
                  relief="flat", padx=8, pady=3, cursor="hand2",
                  command=lambda: self.open_folder_system(bd_plugins)).pack(side="left")

        # 2. Custom URL Downloader
        card_url = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_url.pack(fill="x", pady=(0, 14))

        tk.Label(card_url, text="Direct Link Downloader (Custom GitHub / BetterDiscord Addon URL)", font=("DejaVu Sans", 9, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_url, text="Paste any .theme.css or .plugin.js raw URL to automatically download and install it into BetterDiscord:", font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(1, 6))

        row_input = tk.Frame(card_url, bg=C_CARD)
        row_input.pack(fill="x")

        self.bd_url_entry = tk.Entry(row_input, bg="#1e1f22", fg="#ffffff", insertbackground="#ffffff", relief="flat", font=("DejaVu Sans", 9))
        self.bd_url_entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))

        btn_url_dl = tk.Button(row_input, text="Download & Install URL", font=("DejaVu Sans", 8, "bold"), bg=C_BLURPLE, fg="#ffffff",
                               relief="flat", padx=14, pady=5, cursor="hand2",
                               command=self.action_install_from_url)
        btn_url_dl.pack(side="right")

        # 3. Addon Filter & Catalog
        card_addons = tk.Frame(c, bg=C_CARD, padx=16, pady=16)
        card_addons.pack(fill="x")

        filter_row = tk.Frame(card_addons, bg=C_CARD)
        filter_row.pack(fill="x", pady=(0, 10))

        tk.Label(filter_row, text="Curated Community Catalog", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(side="left")

        curr_filter = getattr(self, "bd_filter", "all")

        btn_all = tk.Button(filter_row, text="All Addons (12)", font=("DejaVu Sans", 8, "bold" if curr_filter == "all" else "normal"),
                            bg=C_BLURPLE if curr_filter == "all" else "#3b3e45", fg="#ffffff",
                            relief="flat", padx=10, pady=3, cursor="hand2", command=lambda: self.set_bd_filter("all"))
        btn_all.pack(side="right", padx=(4, 0))

        btn_plug = tk.Button(filter_row, text="Plugins (6)", font=("DejaVu Sans", 8, "bold" if curr_filter == "plugin" else "normal"),
                             bg=C_BLURPLE if curr_filter == "plugin" else "#3b3e45", fg="#ffffff",
                             relief="flat", padx=10, pady=3, cursor="hand2", command=lambda: self.set_bd_filter("plugin"))
        btn_plug.pack(side="right", padx=(4, 0))

        btn_thm = tk.Button(filter_row, text="Themes / UI (6)", font=("DejaVu Sans", 8, "bold" if curr_filter == "theme" else "normal"),
                            bg=C_BLURPLE if curr_filter == "theme" else "#3b3e45", fg="#ffffff",
                            relief="flat", padx=10, pady=3, cursor="hand2", command=lambda: self.set_bd_filter("theme"))
        btn_thm.pack(side="right")

        items = [x for x in bd_store.CURATED_ADDONS if curr_filter == "all" or x["type"] == curr_filter]

        for item in items:
            is_inst = bd_store.is_addon_installed(item["type"], item["filename"])
            row_item = tk.Frame(card_addons, bg=C_CARD_ALT, padx=12, pady=10)
            row_item.pack(fill="x", pady=4)

            left_c = tk.Frame(row_item, bg=C_CARD_ALT)
            left_c.pack(side="left", fill="both", expand=True)

            t_row = tk.Frame(left_c, bg=C_CARD_ALT)
            t_row.pack(fill="x")

            type_bg = "#805ad5" if item["type"] == "theme" else "#2b6cb0"
            type_txt = "THEME (UI)" if item["type"] == "theme" else "PLUGIN"
            tk.Label(t_row, text=f" {type_txt} ", font=("DejaVu Sans", 7, "bold"), bg=type_bg, fg="#ffffff").pack(side="left", padx=(0, 6))

            tk.Label(t_row, text=f"{item['name']} v{item['version']}", font=("DejaVu Sans", 9, "bold"), bg=C_CARD_ALT, fg=C_TEXT_H).pack(side="left")
            tk.Label(t_row, text=f"  •  by {item['author']} ({item['tag']})", font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_MUTED).pack(side="left")

            tk.Label(left_c, text=item["description"], font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_MUTED, wraplength=620, justify="left").pack(anchor="w", pady=(3, 0))

            right_c = tk.Frame(row_item, bg=C_CARD_ALT)
            right_c.pack(side="right", padx=(10, 0))

            if is_inst:
                tk.Label(right_c, text="[Installed]", font=("DejaVu Sans", 8, "bold"), bg=C_CARD_ALT, fg=C_GREEN).pack(side="left", padx=(0, 8))
                btn_del = tk.Button(right_c, text="Uninstall", font=("DejaVu Sans", 8), bg=C_RED, fg="#ffffff",
                                    relief="flat", padx=10, pady=3, cursor="hand2",
                                    command=lambda it=item: self.action_uninstall_bd_addon(it))
                btn_del.pack(side="left")
            else:
                btn_dl = tk.Button(right_c, text="Download & Install", font=("DejaVu Sans", 8, "bold"), bg=C_BLURPLE, fg="#ffffff",
                                   relief="flat", padx=12, pady=4, cursor="hand2",
                                   command=lambda it=item: self.action_download_bd_addon(it))
                btn_dl.pack(side="left")

    def set_bd_filter(self, filter_name):
        self.bd_filter = filter_name
        self.show_tab("bd_store")

    def open_folder_system(self, path):
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.run(["open", path])
        else:
            subprocess.run(["xdg-open", path])

    def action_download_bd_addon(self, addon_item):
        def _task():
            ok, msg = bd_store.download_addon(addon_item)
            self.root.after(0, lambda: self._on_addon_downloaded(ok, msg))

        threading.Thread(target=_task, daemon=True).start()

    def _on_addon_downloaded(self, ok, msg):
        self.show_tab("bd_store")
        if ok:
            messagebox.showinfo("Success", f"{msg}\n\nTip: Press Ctrl+R in Discord to reload and activate!")
        else:
            messagebox.showerror("Download Failed", msg)

    def action_uninstall_bd_addon(self, addon_item):
        ok, msg = bd_store.uninstall_addon(addon_item["type"], addon_item["filename"])
        self.show_tab("bd_store")
        if ok:
            messagebox.showinfo("Uninstalled", f"{msg}\n\nTip: Press Ctrl+R in Discord to reload.")
        else:
            messagebox.showerror("Error", msg)

    def action_install_from_url(self):
        url = getattr(self, "bd_url_entry", None)
        if not url:
            return
        url_text = url.get().strip()
        if not url_text:
            messagebox.showwarning("Notice", "Please enter a valid URL to download.")
            return

        def _task():
            ok, msg = bd_store.install_custom_url(url_text)
            self.root.after(0, lambda: self._on_addon_downloaded(ok, msg))

        threading.Thread(target=_task, daemon=True).start()

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
            ("Browse BetterDiscord Addon Store (Themes & Plugins)", lambda: [pal_win.destroy(), self.show_tab("bd_store")]),
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
        self.apply_theme_action(silent=True)
        self.show_tab("wallpapers")
        messagebox.showinfo("Wallpaper Applied", f"Active wallpaper changed to:\n{wp['name']}")

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
        self.show_tab("wallpapers")

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
        self.show_tab("mode")
        messagebox.showinfo("Setup Complete", "Instant Setup finished!\nTheme and icons are configured.")

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
