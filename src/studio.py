#!/usr/bin/env python3
"""
Discord-Chan Studio: Official Discord Client Styled Dashboard
Designed to mirror Discord's native dark interface layout (Guilds rail, Channels sidebar, and Chat cards).
NO emojis in panel UI as requested. Vector SVG logo, 1-Click Instant Setup,
All-Custom wallpaper manager with live thumbnails, and full translucency controls.
Licensed under GNU General Public License v3.0 (GPLv3).
"""

import os
import sys
import json
import subprocess
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageTk

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

import theme_engine
import bd_injector
import icon_manager
import plugins_manager

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
        self.root.geometry("1020x750")
        self.root.minsize(920, 640)
        self.root.configure(bg=C_GUILDS)

        self.settings = theme_engine.load_settings()
        self.active_tab = "wallpapers"
        self.thumb_cache = {}

        # Initialize all persistent setting variables once
        self.init_variables()
        self.load_app_icons()
        self.build_discord_shell()
        self.setup_hotkeys()
        self.show_tab("wallpapers")

    def init_variables(self):
        self.custom_path_var = tk.StringVar(value=self.settings.get("wallpaper_path", ""))
        self.wp_opacity_var = tk.DoubleVar(value=float(self.settings.get("wallpaper_opacity", 0.80)))
        self.sidebar_op_var = tk.DoubleVar(value=float(self.settings.get("sidebar_opacity", 0.62)))
        self.chat_op_var = tk.DoubleVar(value=float(self.settings.get("chat_opacity", 0.40)))
        self.tile_op_var = tk.DoubleVar(value=float(self.settings.get("tile_opacity", 0.38)))
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
                # Resize keeping aspect ratio, crop center
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

        # Placeholder fallback
        blank = Image.new("RGBA", (width, height), (35, 36, 40, 255))
        photo = ImageTk.PhotoImage(blank)
        self.thumb_cache[cache_key] = photo
        return photo

    def setup_hotkeys(self):
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

        # Discord white indicator pill + Guild Avatar container
        guild_item = tk.Frame(self.guilds_bar, bg=C_GUILDS, height=54)
        guild_item.pack(fill="x", pady=(10, 4))
        guild_item.pack_propagate(False)

        # Active white pill on the left
        pill = tk.Frame(guild_item, bg="#ffffff", width=4, height=36)
        pill.pack(side="left", padx=(0, 4), pady=9)

        if self.guild_icon_photo:
            logo_btn = tk.Label(guild_item, image=self.guild_icon_photo, bg=C_GUILDS, cursor="hand2")
            logo_btn.pack(side="left", padx=(4, 0))
            logo_btn.bind("<Button-1>", lambda e: self.show_tab("wallpapers"))
        else:
            logo_lbl = tk.Label(guild_item, text="DC", font=("DejaVu Sans", 11, "bold"), bg=C_BLURPLE, fg="#fff", width=3, height=2)
            logo_lbl.pack(side="left", padx=(4, 0))

        # Discord pill separator
        sep = tk.Frame(self.guilds_bar, bg="#35363c", height=2, width=32)
        sep.pack(pady=4)

        # Action Guild Buttons styled like Discord Server Bubbles
        self.create_guild_action("SETUP", C_BLURPLE, "#ffffff", self.run_instant_setup)
        self.create_guild_action("APPLY", C_CARD, C_TEXT_H, self.apply_theme_action)
        self.create_guild_action("RELOAD", C_CARD, C_TEXT_H, self.restart_discord_safe)

        # Bottom Add Server styled placeholder
        bot_add = tk.Label(self.guilds_bar, text="+", font=("DejaVu Sans", 14), bg=C_CARD, fg=C_GREEN,
                           width=3, height=1, cursor="hand2")
        bot_add.pack(side="bottom", pady=12)
        bot_add.bind("<Button-1>", lambda e: self.open_command_palette())

        # 2. Channels Sidebar (Width: 235px)
        self.sidebar = tk.Frame(self.root, bg=C_SIDEBAR, width=235)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Server Header Title with Discord Dropdown Arrow
        sb_header = tk.Frame(self.sidebar, bg=C_SIDEBAR, height=48, padx=14)
        sb_header.pack(fill="x")
        sb_header.pack_propagate(False)

        tk.Label(sb_header, text="Discord-Chan Studio", font=("DejaVu Sans", 10, "bold"), bg=C_SIDEBAR, fg=C_TEXT_H).pack(side="left", pady=14)
        arrow_lbl = tk.Label(sb_header, text="v", font=("DejaVu Sans", 8, "bold"), bg=C_SIDEBAR, fg=C_MUTED, cursor="hand2")
        arrow_lbl.pack(side="right", pady=14)
        arrow_lbl.bind("<Button-1>", lambda e: self.open_command_palette())

        # Sidebar Separator
        tk.Frame(self.sidebar, bg=C_BORDER, height=1).pack(fill="x")

        # Channels Container
        self.channels_frame = tk.Frame(self.sidebar, bg=C_SIDEBAR, padx=8, pady=8)
        self.channels_frame.pack(fill="both", expand=True)

        self.channel_buttons = {}
        self.add_category_header("CUSTOMIZATION")
        self.add_channel_btn("wallpapers", "wallpapers-and-bg")
        self.add_channel_btn("colors", "color-palette")
        self.add_channel_btn("voice", "voice-and-video")
        self.add_channel_btn("layout", "layout-and-clearance")

        self.add_category_header("SYSTEM & CORE")
        self.add_channel_btn("instant", "instant-setup-status")
        self.add_channel_btn("plugins", "betterdiscord-plugins")

        self.add_category_header("COMMUNITY")
        self.add_channel_btn("about", "about-and-contributors")

        # Bottom User Bar (Discord User Dock)
        self.build_user_bar()

        # 3. Main Content Container
        self.main_container = tk.Frame(self.root, bg=C_CONTENT)
        self.main_container.pack(side="left", fill="both", expand=True)

        # Top Channel Header
        self.top_bar = tk.Frame(self.main_container, bg=C_HEADER, height=48, padx=16)
        self.top_bar.pack(fill="x", side="top")
        self.top_bar.pack_propagate(False)

        self.top_hash = tk.Label(self.top_bar, text="#", font=("DejaVu Sans", 13), bg=C_HEADER, fg=C_MUTED)
        self.top_hash.pack(side="left")

        self.top_channel_title = tk.Label(self.top_bar, text="wallpapers-and-bg", font=("DejaVu Sans", 11, "bold"), bg=C_HEADER, fg=C_TEXT_H)
        self.top_channel_title.pack(side="left", padx=(4, 10))

        self.top_topic = tk.Label(self.top_bar, text="| Featured anime wallpapers and custom backgrounds", font=("DejaVu Sans", 9), bg=C_HEADER, fg=C_MUTED)
        self.top_topic.pack(side="left")

        # Header action buttons
        btn_cmd = tk.Button(self.top_bar, text="Command Palette (Ctrl+Shift+P)", font=("DejaVu Sans", 8),
                            bg="#3b3e45", fg=C_TEXT_H, relief="flat", padx=10, pady=4, cursor="hand2",
                            command=self.open_command_palette)
        btn_cmd.pack(side="right", padx=(8, 0))

        btn_save = tk.Button(self.top_bar, text="Save & Apply (Ctrl+S)", font=("DejaVu Sans", 8, "bold"),
                             bg=C_BLURPLE, fg="#ffffff", relief="flat", padx=12, pady=4, cursor="hand2",
                             command=self.apply_theme_action)
        btn_save.pack(side="right")

        tk.Frame(self.main_container, bg=C_BORDER, height=1).pack(fill="x")

        # 4. Scrollable Content Canvas Container
        self.content_canvas = tk.Canvas(self.main_container, bg=C_CONTENT, highlightthickness=0)
        self.content_scrollbar = tk.Scrollbar(self.main_container, orient="vertical", command=self.content_canvas.yview)
        self.content_scroll = tk.Frame(self.content_canvas, bg=C_CONTENT, padx=20, pady=16)

        self.content_scroll.bind("<Configure>", lambda e: self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all")))
        self.canvas_window = self.content_canvas.create_window((0, 0), window=self.content_scroll, anchor="nw")
        self.content_canvas.configure(yscrollcommand=self.content_scrollbar.set)

        self.content_canvas.bind("<Configure>", self.on_canvas_configure)
        self.content_canvas.pack(side="left", fill="both", expand=True)
        self.content_scrollbar.pack(side="right", fill="y")

        # Mouse wheel bindings
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
        user_bar = tk.Frame(self.sidebar, bg="#232428", height=54, padx=8)
        user_bar.pack(fill="x", side="bottom")
        user_bar.pack_propagate(False)

        # Avatar container with green online dot
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

        # Micro status buttons
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

        # Clear content frame
        for w in self.content_scroll.winfo_children():
            w.destroy()

        if tab_id == "wallpapers":
            self.top_channel_title.config(text="wallpapers-and-bg")
            self.top_topic.config(text="| Featured anime presets, manual file browser, and glass overlays")
            self.render_wallpapers_tab()
        elif tab_id == "colors":
            self.top_channel_title.config(text="color-palette")
            self.top_topic.config(text="| Configure primary accents and soft pink palettes")
            self.render_colors_tab()
        elif tab_id == "voice":
            self.top_channel_title.config(text="voice-and-video")
            self.top_topic.config(text="| Speaking rings, glass tiles, and profile modal popouts")
            self.render_voice_tab()
        elif tab_id == "layout":
            self.top_channel_title.config(text="layout-and-clearance")
            self.top_topic.config(text="| Prevent header collisions, fix chat avatars, zero-lag mode")
            self.render_layout_tab()
        elif tab_id == "instant":
            self.top_channel_title.config(text="instant-setup-status")
            self.top_topic.config(text="| 1-Click setup, BetterDiscord injection, process manager")
            self.render_instant_tab()
        elif tab_id == "plugins":
            self.top_channel_title.config(text="betterdiscord-plugins")
            self.top_topic.config(text="| Download and toggle essential BetterDiscord plugins")
            self.render_plugins_tab()
        elif tab_id == "about":
            self.top_channel_title.config(text="about-and-contributors")
            self.top_topic.config(text="| Credits, GPLv3 license, and contributor profiles")
            self.render_about_tab()

        self.content_canvas.yview_moveto(0)

    # -------------------------------------------------------------
    # TAB 1: WALLPAPERS (ALL-CUSTOM & PRESETS WITH THUMBNAILS)
    # -------------------------------------------------------------
    def render_wallpapers_tab(self):
        c = self.content_scroll
        active_id = self.settings.get("wallpaper_id", "kaede_to_suzu")
        current_path = self.settings.get("wallpaper_path", "")

        # 1. Active Wallpaper Hero Card
        hero_card = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        hero_card.pack(fill="x", pady=(0, 14))

        tk.Label(hero_card, text="CURRENT ACTIVE WALLPAPER", font=("DejaVu Sans", 8, "bold"), bg=C_CARD, fg=C_PINK).pack(anchor="w")

        row_h = tk.Frame(hero_card, bg=C_CARD)
        row_h.pack(fill="x", pady=(6, 0))

        # Hero Thumbnail
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
        tk.Label(tag_row, text="Zero-Lag Mode Enabled", font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED, padx=8).pack(side="left")

        # 2. Featured Anime Presets with Visual Cards
        card_presets = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_presets.pack(fill="x", pady=(0, 14))

        tk.Label(card_presets, text="Featured Anime Presets", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_presets, text="Click to apply high-definition anime backgrounds instantly to your Discord client:", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 10))

        for wp in WALLPAPERS:
            is_active = (wp["id"] == active_id)
            row = tk.Frame(card_presets, bg=C_CARD_ALT, padx=10, pady=8)
            row.pack(fill="x", pady=4)

            # Thumbnail
            wp_thumb = self.get_thumbnail(wp["path"], width=110, height=62)
            lbl_t = tk.Label(row, image=wp_thumb, bg=C_CARD_ALT)
            lbl_t.image = wp_thumb
            lbl_t.pack(side="left", padx=(0, 12))

            # Details
            col_d = tk.Frame(row, bg=C_CARD_ALT)
            col_d.pack(side="left", fill="both", expand=True)
            tk.Label(col_d, text=wp["name"], font=("DejaVu Sans", 9, "bold"), bg=C_CARD_ALT, fg=C_TEXT_H).pack(anchor="w")
            tk.Label(col_d, text=wp["desc"], font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_MUTED).pack(anchor="w", pady=(2, 0))

            # Action button
            if is_active:
                tk.Label(row, text="[ CURRENT ]", font=("DejaVu Sans", 8, "bold"), bg=C_GREEN, fg="#ffffff", padx=10, pady=4).pack(side="right")
            else:
                btn = tk.Button(row, text="Select Wallpaper", font=("DejaVu Sans", 8, "bold"), bg=C_BLURPLE, fg="#fff",
                                relief="flat", padx=12, pady=4, cursor="hand2", command=lambda w=wp: self.select_preset_wallpaper(w))
                btn.pack(side="right")

        # 3. All-Custom Wallpaper (Manual File Selection)
        card_custom = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_custom.pack(fill="x", pady=(0, 14))

        tk.Label(card_custom, text="Custom Wallpaper (All-Custom File Selection)", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_custom, text="Select ANY custom image file from your computer (jpg, png, webp, gif):", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 8))

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

        # 4. Translucency Controls Card
        card_trans = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_trans.pack(fill="x")

        tk.Label(card_trans, text="Background Glass Translucency", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_trans, text="Adjust opacity sliders to balance anime artwork visibility with chat readability:", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 8))

        self.create_slider(card_trans, "Background Overlay Darkness:", self.wp_opacity_var, 0.10, 0.98, 0.02)
        self.create_slider(card_trans, "Channels Sidebar Translucency:", self.sidebar_op_var, 0.20, 0.95, 0.02)
        self.create_slider(card_trans, "Chat Messages Layer Translucency:", self.chat_op_var, 0.05, 0.85, 0.02)

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
    # TAB 2: COLOR PALETTES
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

            # Swatches
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
        card_custom_c.pack(fill="x")

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

    # -------------------------------------------------------------
    # TAB 3: VOICE & PROFILE UI
    # -------------------------------------------------------------
    def render_voice_tab(self):
        c = self.content_scroll

        # Speaking Ring Colors
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

        # Tile Sliders
        card_tiles = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_tiles.pack(fill="x")

        tk.Label(card_tiles, text="Voice Video Tiles & Profile Modals", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_tiles, text="Configure participant tile glass opacity and user profile card styling:", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 8))

        self.create_slider(card_tiles, "Voice Tile Translucency (Opacity):", self.tile_op_var, 0.10, 0.85, 0.02)

        # Tile corner radius
        row_rad = tk.Frame(card_tiles, bg=C_CARD)
        row_rad.pack(fill="x", pady=(4, 2))
        tk.Label(row_rad, text="Tile Corner Radius (px):", font=("DejaVu Sans", 8, "bold"), bg=C_CARD, fg=C_TEXT).pack(side="left")
        lbl_rad_v = tk.Label(row_rad, text=f"{self.tile_rad_var.get()}px", font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED)
        lbl_rad_v.pack(side="right")
        tk.Scale(card_tiles, from_=4, to=24, orient="horizontal", variable=self.tile_rad_var,
                 bg=C_CARD, fg=C_TEXT_H, troughcolor=C_CARD_ALT, highlightthickness=0, showvalue=0,
                 command=lambda val: lbl_rad_v.config(text=f"{int(val)}px")).pack(fill="x", pady=(0, 6))

        self.create_slider(card_tiles, "User Profile Popout Modal Opacity:", self.prof_op_var, 0.50, 0.98, 0.02)

    # -------------------------------------------------------------
    # TAB 4: LAYOUT & CLEARANCE (ANTI-NABRAK)
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

        # Performance Toggles
        card_opt = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_opt.pack(fill="x")

        tk.Label(card_opt, text="Performance & Engine Guards", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")

        cb1 = tk.Checkbutton(card_opt, text="Zero-Lag Engine: Strips box-shadows and heavy blur filters for solid 60 FPS",
                             variable=self.zero_lag_var, bg=C_CARD, fg=C_TEXT, selectcolor=C_CARD_ALT, activebackground=C_CARD)
        cb1.pack(anchor="w", pady=(8, 4))

        cb2 = tk.Checkbutton(card_opt, text="Chat Avatar Guard: Preserves native Discord message grid alignment without distortion",
                             variable=self.avatar_fix_var, bg=C_CARD, fg=C_TEXT, selectcolor=C_CARD_ALT, activebackground=C_CARD)
        cb2.pack(anchor="w", pady=4)

        # Keyboard shortcuts reference
        card_hk = tk.Frame(c, bg=C_CARD, padx=16, pady=12)
        card_hk.pack(fill="x", pady=(14, 0))
        tk.Label(card_hk, text="Keyboard Shortcuts Reference", font=("DejaVu Sans", 9, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        info = "Ctrl+Shift+P : Open Command Palette inside Discord or desktop\nCtrl+S : Save & apply theme immediately without restart\nCtrl+R : Restart Discord with safety anti-crash flags"
        tk.Label(card_hk, text=info, font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED, justify="left").pack(anchor="w", pady=(4, 0))

    # -------------------------------------------------------------
    # TAB 5: INSTANT SETUP & STATUS
    # -------------------------------------------------------------
    def render_instant_tab(self):
        c = self.content_scroll

        card_box = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_box.pack(fill="x", pady=(0, 14))

        tk.Label(card_box, text="1-Click Instant Setup", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_box, text="Automatically verifies BetterDiscord injection, sets Kaede to Suzu or anime wallpaper, and configures icons:",
                 font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED, justify="left").pack(anchor="w", pady=(2, 10))

        row_b = tk.Frame(card_box, bg=C_CARD)
        row_b.pack(fill="x")

        tk.Button(row_b, text="Run 1-Click Instant Setup", font=("DejaVu Sans", 9, "bold"), bg=C_BLURPLE, fg="#fff",
                  relief="flat", padx=16, pady=6, cursor="hand2", command=self.run_instant_setup).pack(side="left")

        tk.Button(row_b, text="Restart Discord (Ctrl+R)", font=("DejaVu Sans", 9), bg="#3b3e45", fg=C_TEXT_H,
                  relief="flat", padx=12, pady=6, cursor="hand2", command=self.restart_discord_safe).pack(side="left", padx=10)

        # Status Diagnostics Card
        card_st = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_st.pack(fill="x")

        tk.Label(card_st, text="Client & System Status", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w", pady=(0, 6))

        bd_st = bd_injector.check_status()
        bd_text = "BetterDiscord: Injected & Active" if bd_st.get("injected") else "BetterDiscord: Not Injected"
        bd_color = C_GREEN if bd_st.get("injected") else "#fde047"
        tk.Label(card_st, text=bd_text, font=("DejaVu Sans", 9), bg=C_CARD, fg=bd_color).pack(anchor="w", pady=1)

        res = subprocess.run(["pgrep", "-f", "Discord.real"], stdout=subprocess.PIPE)
        dc_text = "Discord Process: Running" if res.returncode == 0 else "Discord Process: Stopped"
        dc_color = C_GREEN if res.returncode == 0 else C_MUTED
        tk.Label(card_st, text=dc_text, font=("DejaVu Sans", 9), bg=C_CARD, fg=dc_color).pack(anchor="w", pady=1)

        tk.Label(card_st, text=f"Active Wallpaper ID: {self.settings.get('wallpaper_id', 'kaede_to_suzu')}", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_TEXT).pack(anchor="w", pady=1)
        tk.Label(card_st, text=f"Active Palette: {self.settings.get('active_preset', 'Sakura Soft')}", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_TEXT).pack(anchor="w", pady=1)

        # Safe ToS Note
        card_safe = tk.Frame(c, bg="#1a1c1e", padx=12, pady=8, highlightthickness=1, highlightbackground="#2d5a3f")
        card_safe.pack(fill="x", pady=(14, 0))
        tk.Label(card_safe, text="Safety Notice: 100% Client-Side CSS Theme. NOT a Nitro modification. Completely safe and free from account bans.",
                 font=("DejaVu Sans", 8), bg="#1a1c1e", fg=C_GREEN).pack(anchor="w")

    # -------------------------------------------------------------
    # TAB 6: PLUGINS
    # -------------------------------------------------------------
    def render_plugins_tab(self):
        c = self.content_scroll

        card_pl = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_pl.pack(fill="x")

        tk.Label(card_pl, text="BetterDiscord Plugins", font=("DejaVu Sans", 11, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_pl, text="Manage plugins installed in your BetterDiscord configuration:", font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 10))

        plugins = plugins_manager.get_installed_plugins()
        for item in plugins:
            row = tk.Frame(card_pl, bg=C_CARD_ALT, padx=12, pady=6)
            row.pack(fill="x", pady=3)

            col = tk.Frame(row, bg=C_CARD_ALT)
            col.pack(side="left", fill="x", expand=True)
            status_text = "[Active]" if item["installed"] else "[Not Installed]"
            status_col = C_GREEN if item["installed"] else C_MUTED
            tk.Label(col, text=f"{item['name']} {status_text}", font=("DejaVu Sans", 9, "bold"), bg=C_CARD_ALT, fg=status_col).pack(anchor="w")
            tk.Label(col, text=f"{item['desc']} (by {item['author']})", font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_MUTED).pack(anchor="w")

            if item["installed"]:
                tk.Button(row, text="Remove", font=("DejaVu Sans", 8), bg=C_RED, fg="#fff", relief="flat", padx=8, pady=2,
                          command=lambda pid=item["id"]: [plugins_manager.uninstall_plugin(pid), self.show_tab("plugins")]).pack(side="right")
            else:
                tk.Button(row, text="Install", font=("DejaVu Sans", 8, "bold"), bg=C_BLURPLE, fg="#fff", relief="flat", padx=10, pady=2,
                          command=lambda pid=item["id"]: [plugins_manager.install_plugin(pid), self.show_tab("plugins")]).pack(side="right")

    # -------------------------------------------------------------
    # TAB 7: ABOUT & CONTRIBUTORS
    # -------------------------------------------------------------
    def render_about_tab(self):
        c = self.content_scroll

        card_about = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_about.pack(fill="x", pady=(0, 14))

        tk.Label(card_about, text="Discord-Chan Custom Theme & Studio", font=("DejaVu Sans", 12, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(card_about, text="Universal Anime Theme Customizer for Discord • Licensed under GNU GPLv3",
                 font=("DejaVu Sans", 9), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 8))

        # Contributor Profile Card (Discord User Profile Style)
        card_author = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_author.pack(fill="x", pady=(0, 14))

        tk.Label(card_author, text="Project Lead & Primary Contributor", font=("DejaVu Sans", 10, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w", pady=(0, 8))

        row_a = tk.Frame(card_author, bg=C_CARD_ALT, padx=14, pady=12)
        row_a.pack(fill="x")

        # Avatar
        if self.prof_icon_photo:
            tk.Label(row_a, image=self.prof_icon_photo, bg=C_CARD_ALT).pack(side="left", padx=(0, 12))

        col_a = tk.Frame(row_a, bg=C_CARD_ALT)
        col_a.pack(side="left", fill="both", expand=True)

        tk.Label(col_a, text="myzert (zerttcihuy@gmail.com)", font=("DejaVu Sans", 10, "bold"), bg=C_CARD_ALT, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(col_a, text="GitHub: https://github.com/myzert/discord-chan", font=("DejaVu Sans", 9), bg=C_CARD_ALT, fg=C_BLURPLE).pack(anchor="w", pady=2)
        tk.Label(col_a, text="Role: Creator, Anime UI Designer, and Open-Source Project Maintainer", font=("DejaVu Sans", 8), bg=C_CARD_ALT, fg=C_MUTED).pack(anchor="w")

        # Community Contribution Card
        card_contrib = tk.Frame(c, bg=C_CARD, padx=16, pady=14)
        card_contrib.pack(fill="x")

        tk.Label(card_contrib, text="Community & Open Source Contributions", font=("DejaVu Sans", 10, "bold"), bg=C_CARD, fg=C_TEXT_H).pack(anchor="w")
        contrib_info = (
            "We welcome all anime enthusiasts and developers!\n"
            "• Submit your own anime wallpapers via Pull Requests\n"
            "• Report bugs and request features on our GitHub Issues\n"
            "• Star the repository to show support and help the project grow"
        )
        tk.Label(card_contrib, text=contrib_info, font=("DejaVu Sans", 8), bg=C_CARD, fg=C_MUTED, justify="left").pack(anchor="w", pady=(4, 0))

    # -------------------------------------------------------------
    # ACTIONS & CALLBACKS
    # -------------------------------------------------------------
    def open_command_palette(self):
        pal_win = tk.Toplevel(self.root)
        pal_win.title("Command Palette")
        pal_win.geometry("540x420")
        pal_win.configure(bg=C_CARD)
        pal_win.transient(self.root)
        pal_win.grab_set()

        head = tk.Frame(pal_win, bg=C_SIDEBAR, padx=14, pady=10)
        head.pack(fill="x")
        tk.Label(head, text="DISCORD-CHAN COMMAND PALETTE", font=("DejaVu Sans", 10, "bold"), bg=C_SIDEBAR, fg=C_TEXT_H).pack(anchor="w")
        tk.Label(head, text="Select an action to execute immediately:", font=("DejaVu Sans", 8), bg=C_SIDEBAR, fg=C_MUTED).pack(anchor="w")

        commands = [
            ("1-Click Instant Setup", lambda: [pal_win.destroy(), self.run_instant_setup()]),
            ("Save & Apply Theme (Ctrl+S)", lambda: [pal_win.destroy(), self.apply_theme_action()]),
            ("Restart Discord Safely (Ctrl+R)", lambda: [pal_win.destroy(), self.restart_discord_safe()]),
            ("Switch to Kaede to Suzu Anime Theme", lambda: [pal_win.destroy(), self.select_preset_wallpaper(WALLPAPERS[0])]),
            ("Switch to Whisper Me a Love Song", lambda: [pal_win.destroy(), self.select_preset_wallpaper(WALLPAPERS[1])]),
            ("Apply Sakura Soft Pink Palette", lambda: [pal_win.destroy(), self.select_palette("Sakura Soft", "#ff85a2", "#fbcfe8")]),
            ("Apply Lavender Yuri Palette", lambda: [pal_win.destroy(), self.select_palette("Lavender Yuri", "#c084fc", "#e9d5ff")]),
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
        self.settings["wallpaper_opacity"] = self.wp_opacity_var.get()
        self.settings["sidebar_opacity"] = self.sidebar_op_var.get()
        self.settings["chat_opacity"] = self.chat_op_var.get()
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
        self.show_tab("instant")
        messagebox.showinfo("Setup Complete", "Instant Setup finished!\nTheme and icons are now configured.")

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
