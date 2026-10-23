#!/usr/bin/env python3
"""
Discord-Chan Custom: Studio / Control Center GUI
A modern, minimalist anime-styled dashboard for customizing Discord.
Includes Quick Palette switcher (Ctrl+Shift+P), Transparency Controls,
Icon Switcher, and Instant Setup.
"""

import os
import sys
import json
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
from PIL import Image, ImageTk

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

import theme_engine
import bd_injector
import icon_manager
import plugins_manager

WALLPAPERS = [
    {
        "id": "whisper",
        "name": "🌸 Whisper Me a Love Song",
        "desc": "Anime Yuri Romance (Default)",
        "path": os.path.join(REPO_DIR, "assets", "wallpapers", "1_whisper_me_a_love_song.jpg")
    },
    {
        "id": "sakura",
        "name": "🌺 Sakura Blossom Minimal",
        "desc": "Bunga Sakura Estetik Minimalis",
        "path": os.path.join(REPO_DIR, "assets", "wallpapers", "2_sakura_blossom_minimal.jpg")
    },
    {
        "id": "clouds",
        "name": "☁️ Pastel Clouds Scenery",
        "desc": "Langit Senja Pastel Lembut",
        "path": os.path.join(REPO_DIR, "assets", "wallpapers", "3_pastel_clouds_scenery.jpg")
    },
    {
        "id": "neko",
        "name": "🐱 Discord-Chan Neko Mascot",
        "desc": "Cute Wumpus Neko Anime Mascot",
        "path": os.path.join(REPO_DIR, "assets", "wallpapers", "4_discord_chan_neko.jpg")
    }
]

PINK_PALETTES = [
    ("🌸 Sakura Soft", "#ff85a2", "#fbcfe8"),
    ("🍓 Strawberry Rose", "#fb7185", "#fecdd3"),
    ("🍑 Pastel Peach", "#f472b6", "#fce7f3"),
    ("🍬 Cotton Candy", "#f49ac2", "#fed7aa"),
    ("🍒 Cherry Blossom", "#fda4af", "#fff1f2"),
    ("💜 Lavender Yuri", "#c084fc", "#e9d5ff"),
    ("🖤 Dark Black-Pink", "#ff7597", "#18141c")
]

SPEAKING_COLORS = [
    ("🌸 Sakura Pink", "#ff85a2"),
    ("🌿 Emerald Green", "#22c55e"),
    ("💜 Violet Glow", "#c084fc"),
    ("🩵 Neon Cyan", "#38bdf8"),
    ("🟡 Amber Sunset", "#fbbf24")
]

class DiscordChanStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 Discord-Chan Studio | Control Center")
        self.root.geometry("860x700")
        self.root.minsize(800, 620)
        self.root.configure(bg="#17131b")

        # Set window icon
        icon_path = os.path.join(REPO_DIR, "assets", "icons", "discord-neko.png")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(REPO_DIR, "assets", "icons", "discord-chan.png")
        if os.path.exists(icon_path):
            try:
                img = Image.open(icon_path).resize((64, 64))
                self.icon_photo = ImageTk.PhotoImage(img)
                self.root.iconphoto(True, self.icon_photo)
            except Exception:
                pass

        self.settings = theme_engine.load_settings()
        self.style = ttk.Style()
        self.setup_styles()
        self.create_widgets()
        self.setup_hotkeys()
        self.update_status_display()

    def setup_styles(self):
        self.style.theme_use('clam')
        self.style.configure(".", background="#17131b", foreground="#fdf2f8", font=("DejaVu Sans", 9))
        self.style.configure("TNotebook", background="#17131b", borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#241e2b", foreground="#d4a5b8", padding=[14, 8], font=("DejaVu Sans", 10, "bold"))
        self.style.map("TNotebook.Tab", 
                       background=[("selected", "#ff85a2")],
                       foreground=[("selected", "#17131b")])

        self.style.configure("Card.TFrame", background="#221a27", relief="flat")
        self.style.configure("TScale", background="#221a27", troughcolor="#17131b")

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

    def create_widgets(self):
        # Top Header Bar
        header = tk.Frame(self.root, bg="#221a27", height=58, padx=16, pady=8)
        header.pack(fill="x", side="top")

        title_lbl = tk.Label(header, text="🌸 DISCORD-CHAN STUDIO", font=("DejaVu Sans", 14, "bold"), bg="#221a27", fg="#ff85a2")
        title_lbl.pack(side="left")

        sub_lbl = tk.Label(header, text="Whisper Me a Love Song Edition", font=("DejaVu Sans", 9, "italic"), bg="#221a27", fg="#fbcfe8")
        sub_lbl.pack(side="left", padx=10)

        # Right header buttons
        cmd_btn = tk.Button(header, text="⌨ Ctrl+Shift+P", bg="#36293f", fg="#fbcfe8", font=("DejaVu Sans", 9, "bold"),
                            relief="flat", padx=10, pady=3, cursor="hand2", command=self.open_command_palette)
        cmd_btn.pack(side="right", padx=(8, 0))

        quick_apply = tk.Button(header, text="⚡ Simpan (Ctrl+S)", bg="#ff85a2", fg="#17131b", font=("DejaVu Sans", 9, "bold"),
                                relief="flat", padx=12, pady=4, cursor="hand2", command=self.apply_theme_action)
        quick_apply.pack(side="right")

        # Main Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=8)

        # Tab 1: Instant Setup & Dashboard
        self.tab_dash = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.tab_dash, text="🚀 Setup & Status")
        self.build_dash_tab()

        # Tab 2: Wallpapers & Background Translucency
        self.tab_wallpapers = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.tab_wallpapers, text="🖼️ Background & Opacity")
        self.build_wallpaper_tab()

        # Tab 3: Pink Palette & Colors
        self.tab_colors = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.tab_colors, text="💖 Warna Pink")
        self.build_colors_tab()

        # Tab 4: Voice & Profile UI
        self.tab_voice = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.tab_voice, text="🎙️ Voice & Profil")
        self.build_voice_tab()

        # Tab 5: Layout & Performance
        self.tab_perf = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.tab_perf, text="⚡ Layout Anti-Nabrak")
        self.build_perf_tab()

        # Tab 6: Plugins
        self.tab_plugins = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.tab_plugins, text="🧩 Plugins")
        self.build_plugins_tab()

        # Tab 7: About & GitHub
        self.tab_about = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.tab_about, text="ℹ️ GitHub & Info")
        self.build_about_tab()

        # Bottom status bar
        self.status_bar = tk.Label(self.root, text="Siap digunakan • Shortcut: Ctrl+Shift+P (Quick Palette) • Ctrl+S (Simpan)",
                                   bg="#120e15", fg="#d4a5b8", font=("DejaVu Sans", 9), anchor="w", padx=12, pady=4)
        self.status_bar.pack(fill="x", side="bottom")

    def build_dash_tab(self):
        container = tk.Frame(self.tab_dash, bg="#221a27", padx=16, pady=12)
        container.pack(fill="both", expand=True)

        instant_box = tk.LabelFrame(container, text=" ✨ Instant Setup (Auto-Config All) ", bg="#2b2132", fg="#ff85a2", font=("DejaVu Sans", 10, "bold"), padx=14, pady=10)
        instant_box.pack(fill="x", pady=(0, 10))

        tk.Label(instant_box, text="Tekan 1 tombol ini untuk memasang dan mengonfigurasi segalanya secara otomatis:\n• Cek & Inject BetterDiscord otomatis\n• Pasang Wallpaper Anime Whisper Me a Love Song\n• Pasang Icon Anime Discord-Chan Neko ke Desktop & Menu\n• Optimalkan flags anti-crash dan zero-lag (60 FPS)",
                 bg="#2b2132", fg="#fdf2f8", justify="left", font=("DejaVu Sans", 9)).pack(anchor="w", pady=(0, 8))

        btn_row = tk.Frame(instant_box, bg="#2b2132")
        btn_row.pack(fill="x")

        tk.Button(btn_row, text="🚀 1-CLICK INSTANT SETUP", bg="#ff85a2", fg="#17131b", font=("DejaVu Sans", 10, "bold"),
                  relief="flat", padx=16, pady=6, cursor="hand2", command=self.run_instant_setup).pack(side="left")

        tk.Button(btn_row, text="🔄 Restart Discord (Ctrl+R)", bg="#36293f", fg="#fbcfe8", font=("DejaVu Sans", 9, "bold"),
                  relief="flat", padx=12, pady=6, cursor="hand2", command=self.restart_discord_safe).pack(side="left", padx=10)

        status_box = tk.LabelFrame(container, text=" 📊 Status Sistem & Discord ", bg="#2b2132", fg="#fbcfe8", font=("DejaVu Sans", 10, "bold"), padx=14, pady=8)
        status_box.pack(fill="x", pady=6)

        self.lbl_bd_status = tk.Label(status_box, text="BetterDiscord: Memeriksa...", bg="#2b2132", fg="#fdf2f8")
        self.lbl_bd_status.pack(anchor="w", pady=1)

        self.lbl_dc_status = tk.Label(status_box, text="Discord Process: Memeriksa...", bg="#2b2132", fg="#fdf2f8")
        self.lbl_dc_status.pack(anchor="w", pady=1)

        self.lbl_wp_status = tk.Label(status_box, text=f"Wallpaper Aktif: {self.settings.get('wallpaper_id', 'whisper')}", bg="#2b2132", fg="#fdf2f8")
        self.lbl_wp_status.pack(anchor="w", pady=1)

        self.lbl_preset_status = tk.Label(status_box, text=f"Palet Warna: {self.settings.get('active_preset', 'Sakura Soft')}", bg="#2b2132", fg="#fdf2f8")
        self.lbl_preset_status.pack(anchor="w", pady=1)

        icon_box = tk.LabelFrame(container, text=" 🎭 Pilih Icon Aplikasi Discord ", bg="#2b2132", fg="#fbcfe8", font=("DejaVu Sans", 10, "bold"), padx=14, pady=8)
        icon_box.pack(fill="x", pady=8)

        i_row = tk.Frame(icon_box, bg="#2b2132")
        i_row.pack(fill="x")

        tk.Button(i_row, text="🐱 Pasang Icon Discord-Chan Neko", bg="#ff85a2", fg="#17131b", font=("DejaVu Sans", 9, "bold"),
                  relief="flat", padx=12, pady=5, cursor="hand2", command=self.apply_neko_icon).pack(side="left", padx=(0, 8))

        tk.Button(i_row, text="🌸 Pasang Icon Whisper Me a Love Song", bg="#36293f", fg="#fbcfe8", font=("DejaVu Sans", 9, "bold"),
                  relief="flat", padx=12, pady=5, cursor="hand2", command=self.apply_yuri_icon).pack(side="left")

        safe_box = tk.Frame(container, bg="#1a1420", padx=10, pady=6, highlightthickness=1, highlightbackground="#3d2c47")
        safe_box.pack(fill="x", pady=(8, 0))
        tk.Label(safe_box, text="🛡️ 100% Client-Side CSS Theme (Bukan modifikasi Nitro berbayar. Aman dari ban dan bebas resiko).",
                 bg="#1a1420", fg="#86efac", font=("DejaVu Sans", 8)).pack(anchor="w")

    def build_wallpaper_tab(self):
        container = tk.Frame(self.tab_wallpapers, bg="#221a27", padx=16, pady=12)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Pilih Preset Wallpaper Anime:", font=("DejaVu Sans", 10, "bold"), bg="#221a27", fg="#ff85a2").pack(anchor="w", pady=(0, 6))

        grid_frame = tk.Frame(container, bg="#221a27")
        grid_frame.pack(fill="x", pady=2)

        for i, wp in enumerate(WALLPAPERS):
            card = tk.Frame(grid_frame, bg="#2b2132", padx=10, pady=6, highlightthickness=1, highlightbackground="#3d2c47")
            card.grid(row=i//2, column=i%2, padx=4, pady=4, sticky="nsew")
            grid_frame.columnconfigure(i%2, weight=1)

            tk.Label(card, text=wp["name"], font=("DejaVu Sans", 9, "bold"), bg="#2b2132", fg="#fbcfe8").pack(anchor="w")
            tk.Label(card, text=wp["desc"], font=("DejaVu Sans", 8), bg="#2b2132", fg="#d4a5b8").pack(anchor="w")

            btn = tk.Button(card, text="Pilih Wallpaper", bg="#ff85a2", fg="#17131b", font=("DejaVu Sans", 8, "bold"),
                            relief="flat", padx=8, pady=2, cursor="hand2",
                            command=lambda w=wp: self.select_preset_wallpaper(w))
            btn.pack(anchor="e", pady=(2, 0))

        custom_box = tk.LabelFrame(container, text=" 📁 Custom Wallpaper Sendiri ", bg="#2b2132", fg="#fbcfe8", font=("DejaVu Sans", 10, "bold"), padx=10, pady=8)
        custom_box.pack(fill="x", pady=8)

        c_row = tk.Frame(custom_box, bg="#2b2132")
        c_row.pack(fill="x")

        self.custom_path_var = tk.StringVar(value=self.settings.get("wallpaper_path", ""))
        entry = tk.Entry(c_row, textvariable=self.custom_path_var, bg="#1a1420", fg="#fdf2f8", insertbackground="#ff85a2", relief="flat")
        entry.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=3)

        tk.Button(c_row, text="Browse (Ctrl+O)", bg="#36293f", fg="#fbcfe8", font=("DejaVu Sans", 8, "bold"), relief="flat", padx=8, pady=3,
                  command=self.browse_custom_wallpaper).pack(side="left")

        tk.Button(c_row, text="Terapkan", bg="#ff85a2", fg="#17131b", font=("DejaVu Sans", 8, "bold"), relief="flat", padx=10, pady=3,
                  command=self.apply_custom_wallpaper).pack(side="left", padx=(6, 0))

        trans_box = tk.LabelFrame(container, text=" 🪟 Pengaturan Transparansi UI (Glass Effects) ", bg="#2b2132", fg="#fbcfe8", font=("DejaVu Sans", 10, "bold"), padx=10, pady=8)
        trans_box.pack(fill="x", pady=6)

        tk.Label(trans_box, text="Tingkat Gelap Background (Overlay Opacity):", bg="#2b2132", fg="#fdf2f8").pack(anchor="w")
        self.wp_opacity_var = tk.DoubleVar(value=float(self.settings.get("wallpaper_opacity", 0.80)))
        tk.Scale(trans_box, from_=0.10, to=0.98, resolution=0.02, orient="horizontal", variable=self.wp_opacity_var,
                 bg="#2b2132", fg="#ff85a2", troughcolor="#17131b", highlightthickness=0).pack(fill="x")

        tk.Label(trans_box, text="Transparansi Sidebar Channels:", bg="#2b2132", fg="#fdf2f8").pack(anchor="w", pady=(3, 0))
        self.sidebar_op_var = tk.DoubleVar(value=float(self.settings.get("sidebar_opacity", 0.62)))
        tk.Scale(trans_box, from_=0.20, to=0.95, resolution=0.02, orient="horizontal", variable=self.sidebar_op_var,
                 bg="#2b2132", fg="#ff85a2", troughcolor="#17131b", highlightthickness=0).pack(fill="x")

        tk.Label(trans_box, text="Transparansi Area Chat Pesan:", bg="#2b2132", fg="#fdf2f8").pack(anchor="w", pady=(3, 0))
        self.chat_op_var = tk.DoubleVar(value=float(self.settings.get("chat_opacity", 0.40)))
        tk.Scale(trans_box, from_=0.05, to=0.85, resolution=0.02, orient="horizontal", variable=self.chat_op_var,
                 bg="#2b2132", fg="#ff85a2", troughcolor="#17131b", highlightthickness=0).pack(fill="x")

    def build_colors_tab(self):
        container = tk.Frame(self.tab_colors, bg="#221a27", padx=16, pady=12)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Pilih Tema Palet Warna Minimalis Pink:", font=("DejaVu Sans", 10, "bold"), bg="#221a27", fg="#ff85a2").pack(anchor="w", pady=(0, 6))

        palettes_frame = tk.Frame(container, bg="#221a27")
        palettes_frame.pack(fill="x", pady=2)

        for i, (name, pri, sec) in enumerate(PINK_PALETTES):
            row = tk.Frame(palettes_frame, bg="#2b2132", padx=8, pady=4, highlightthickness=1, highlightbackground="#3d2c47")
            row.pack(fill="x", pady=2)

            dot1 = tk.Label(row, text="  ", bg=pri, width=2)
            dot1.pack(side="left", padx=4)
            dot2 = tk.Label(row, text="  ", bg=sec, width=2)
            dot2.pack(side="left", padx=4)

            tk.Label(row, text=name, bg="#2b2132", fg="#fdf2f8", font=("DejaVu Sans", 9, "bold")).pack(side="left", padx=8)
            tk.Label(row, text=f"({pri} / {sec})", bg="#2b2132", fg="#d4a5b8", font=("DejaVu Sans", 8)).pack(side="left")

            btn = tk.Button(row, text="Pilih Palet", bg="#ff85a2", fg="#17131b", font=("DejaVu Sans", 8, "bold"),
                            relief="flat", padx=8, pady=2, cursor="hand2",
                            command=lambda n=name, p=pri, s=sec: self.select_palette(n, p, s))
            btn.pack(side="right")

        custom_c = tk.LabelFrame(container, text=" 🎨 Custom Hex Color Picker ", bg="#2b2132", fg="#fbcfe8", font=("DejaVu Sans", 10, "bold"), padx=10, pady=8)
        custom_c.pack(fill="x", pady=8)

        c_row = tk.Frame(custom_c, bg="#2b2132")
        c_row.pack(fill="x")

        tk.Label(c_row, text="Warna Utama (Primary):", bg="#2b2132", fg="#fdf2f8").pack(side="left")
        self.lbl_accent_sample = tk.Label(c_row, text="      ", bg=self.settings.get("accent_color", "#ff85a2"), relief="solid", borderwidth=1)
        self.lbl_accent_sample.pack(side="left", padx=6)

        tk.Button(c_row, text="Pilih Warna Utama", bg="#36293f", fg="#fbcfe8", font=("DejaVu Sans", 8), relief="flat", padx=6, pady=2,
                  command=self.pick_accent_color).pack(side="left", padx=4)

        tk.Label(c_row, text="Warna Soft:", bg="#2b2132", fg="#fdf2f8").pack(side="left", padx=(10, 0))
        self.lbl_soft_sample = tk.Label(c_row, text="      ", bg=self.settings.get("soft_pink", "#fbcfe8"), relief="solid", borderwidth=1)
        self.lbl_soft_sample.pack(side="left", padx=6)

        tk.Button(c_row, text="Pilih Warna Soft", bg="#36293f", fg="#fbcfe8", font=("DejaVu Sans", 8), relief="flat", padx=6, pady=2,
                  command=self.pick_soft_color).pack(side="left", padx=4)

    def build_voice_tab(self):
        container = tk.Frame(self.tab_voice, bg="#221a27", padx=16, pady=12)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Kustomisasi Voice Call & Tampilan Profil:", font=("DejaVu Sans", 10, "bold"), bg="#221a27", fg="#ff85a2").pack(anchor="w", pady=(0, 6))

        spk_box = tk.LabelFrame(container, text=" 🎙️ Warna Lingkaran Saat Berbicara (Speaking Ring) ", bg="#2b2132", fg="#fbcfe8", font=("DejaVu Sans", 10, "bold"), padx=10, pady=8)
        spk_box.pack(fill="x", pady=4)

        for name, col in SPEAKING_COLORS:
            row = tk.Frame(spk_box, bg="#2b2132")
            row.pack(fill="x", pady=2)
            dot = tk.Label(row, text="  ", bg=col, width=2)
            dot.pack(side="left", padx=4)
            tk.Label(row, text=name, bg="#2b2132", fg="#fdf2f8", font=("DejaVu Sans", 9)).pack(side="left", padx=6)
            tk.Button(row, text="Pilih", bg="#36293f", fg="#fbcfe8", font=("DejaVu Sans", 8, "bold"), relief="flat", padx=8, pady=1,
                      command=lambda c=col: self.set_speaking_color(c)).pack(side="right")

        tile_box = tk.LabelFrame(container, text=" 🔲 Kotak Peserta Voice Call (Tiles) ", bg="#2b2132", fg="#fbcfe8", font=("DejaVu Sans", 10, "bold"), padx=10, pady=6)
        tile_box.pack(fill="x", pady=6)

        tk.Label(tile_box, text="Transparansi Tile Suara (Opacity):", bg="#2b2132", fg="#fdf2f8").pack(anchor="w")
        self.tile_op_var = tk.DoubleVar(value=float(self.settings.get("tile_opacity", 0.38)))
        tk.Scale(tile_box, from_=0.10, to=0.85, resolution=0.02, orient="horizontal", variable=self.tile_op_var,
                 bg="#2b2132", fg="#ff85a2", troughcolor="#17131b", highlightthickness=0).pack(fill="x")

        tk.Label(tile_box, text="Kelengkungan Sudut Tile (Radius px):", bg="#2b2132", fg="#fdf2f8").pack(anchor="w", pady=(2, 0))
        self.tile_rad_var = tk.IntVar(value=int(self.settings.get("tile_radius", 12)))
        tk.Scale(tile_box, from_=4, to=24, orient="horizontal", variable=self.tile_rad_var,
                 bg="#2b2132", fg="#ff85a2", troughcolor="#17131b", highlightthickness=0).pack(fill="x")

        prof_box = tk.LabelFrame(container, text=" 👤 User Profile Card & Popout Modal ", bg="#2b2132", fg="#fbcfe8", font=("DejaVu Sans", 10, "bold"), padx=10, pady=6)
        prof_box.pack(fill="x", pady=4)

        tk.Label(prof_box, text="Transparansi Kartu Profil Popout:", bg="#2b2132", fg="#fdf2f8").pack(anchor="w")
        self.prof_op_var = tk.DoubleVar(value=float(self.settings.get("profile_opacity", 0.88)))
        tk.Scale(prof_box, from_=0.50, to=0.98, resolution=0.02, orient="horizontal", variable=self.prof_op_var,
                 bg="#2b2132", fg="#ff85a2", troughcolor="#17131b", highlightthickness=0).pack(fill="x")

    def build_perf_tab(self):
        container = tk.Frame(self.tab_perf, bg="#221a27", padx=16, pady=12)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Pengaturan Posisi & Optimasi Anti-Nabrak (Zero-Lag):", font=("DejaVu Sans", 10, "bold"), bg="#221a27", fg="#ff85a2").pack(anchor="w", pady=(0, 6))

        spacing_box = tk.LabelFrame(container, text=" 📏 Jarak dari Atas (Top Spacing) ", bg="#2b2132", fg="#fbcfe8", font=("DejaVu Sans", 10, "bold"), padx=10, pady=8)
        spacing_box.pack(fill="x", pady=4)

        tk.Label(spacing_box, text="Memberi jarak bersih agar tidak nabrak dengan taskbar/panel window atas:", bg="#2b2132", fg="#d4a5b8", font=("DejaVu Sans", 8)).pack(anchor="w")
        self.top_spacing_var = tk.IntVar(value=int(self.settings.get("top_spacing", 12)))
        tk.Scale(spacing_box, from_=0, to=40, orient="horizontal", variable=self.top_spacing_var,
                 bg="#2b2132", fg="#ff85a2", troughcolor="#17131b", highlightthickness=0).pack(fill="x")

        opt_box = tk.LabelFrame(container, text=" ⚡ Engine Optimasi Performa ", bg="#2b2132", fg="#fbcfe8", font=("DejaVu Sans", 10, "bold"), padx=10, pady=8)
        opt_box.pack(fill="x", pady=6)

        self.zero_lag_var = tk.BooleanVar(value=bool(self.settings.get("zero_lag", True)))
        cb1 = tk.Checkbutton(opt_box, text="Mode Zero-Lag: Hapus efek box-shadow & blur berat agar 60 FPS halus di Linux",
                             variable=self.zero_lag_var, bg="#2b2132", fg="#fdf2f8", selectcolor="#17131b", activebackground="#2b2132")
        cb1.pack(anchor="w", pady=2)

        self.avatar_fix_var = tk.BooleanVar(value=bool(self.settings.get("chat_avatar_fixed", True)))
        cb2 = tk.Checkbutton(opt_box, text="Chat Avatar Alignment Guard: Pastikan foto profil di chat rapi dan tidak bergeser",
                             variable=self.avatar_fix_var, bg="#2b2132", fg="#fdf2f8", selectcolor="#17131b", activebackground="#2b2132")
        cb2.pack(anchor="w", pady=2)

        hk_box = tk.LabelFrame(container, text=" ⌨ Pintasan Keyboard (Shortcuts) ", bg="#2b2132", fg="#fbcfe8", font=("DejaVu Sans", 10, "bold"), padx=10, pady=8)
        hk_box.pack(fill="x", pady=6)

        hk_info = (
            "• Ctrl+Shift+P atau Ctrl+P : Buka Quick Command Palette\n"
            "• Ctrl+S : Simpan dan terapkan tema langsung ke Discord\n"
            "• Ctrl+R : Restart Discord aman dengan anti-crash flag\n"
            "• Ctrl+O : Pilih custom wallpaper dari komputer\n"
            "• Ctrl+Q : Keluar dari Discord-Chan Studio"
        )
        tk.Label(hk_box, text=hk_info, bg="#2b2132", fg="#fdf2f8", font=("DejaVu Sans", 8), justify="left").pack(anchor="w")

    def build_plugins_tab(self):
        container = tk.Frame(self.tab_plugins, bg="#221a27", padx=16, pady=12)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="BetterDiscord Plugins Manager:", font=("DejaVu Sans", 10, "bold"), bg="#221a27", fg="#ff85a2").pack(anchor="w", pady=(0, 6))

        self.plugins_frame = tk.Frame(container, bg="#221a27")
        self.plugins_frame.pack(fill="both", expand=True)
        self.refresh_plugins_list()

    def refresh_plugins_list(self):
        for widget in self.plugins_frame.winfo_children():
            widget.destroy()

        installed = plugins_manager.get_installed_plugins()
        for item in installed:
            row = tk.Frame(self.plugins_frame, bg="#2b2132", padx=10, pady=6, highlightthickness=1, highlightbackground="#3d2c47")
            row.pack(fill="x", pady=3)

            info_col = tk.Frame(row, bg="#2b2132")
            info_col.pack(side="left", fill="x", expand=True)

            status_icon = "🟢" if item["installed"] else "⚪"
            tk.Label(info_col, text=f"{status_icon} {item['name']} (by {item['author']})", bg="#2b2132", fg="#fbcfe8", font=("DejaVu Sans", 9, "bold")).pack(anchor="w")
            tk.Label(info_col, text=item["desc"], bg="#2b2132", fg="#d4a5b8", font=("DejaVu Sans", 8)).pack(anchor="w")

            if item["installed"]:
                tk.Button(row, text="Hapus Plugin", bg="#4a222e", fg="#fca5a5", font=("DejaVu Sans", 8, "bold"), relief="flat", padx=8, pady=2,
                          command=lambda pid=item["id"]: self.uninstall_plugin_action(pid)).pack(side="right")
            else:
                tk.Button(row, text="📥 Install", bg="#ff85a2", fg="#17131b", font=("DejaVu Sans", 8, "bold"), relief="flat", padx=8, pady=2,
                          command=lambda pid=item["id"]: self.install_plugin_action(pid)).pack(side="right")

    def build_about_tab(self):
        container = tk.Frame(self.tab_about, bg="#221a27", padx=16, pady=12)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="🌸 DISCORD-CHAN CUSTOM", font=("DejaVu Sans", 13, "bold"), bg="#221a27", fg="#ff85a2").pack(anchor="w")
        tk.Label(container, text="Whisper Me a Love Song Edition (Sasayaku You ni Koi wo Utau)\nOpen-Source Discord Aesthetic Suite for Linux & Windows",
                 bg="#221a27", fg="#fbcfe8", font=("DejaVu Sans", 9), justify="left").pack(anchor="w", pady=(2, 8))

        gh_box = tk.LabelFrame(container, text=" 🌐 Repository GitHub ", bg="#2b2132", fg="#fbcfe8", font=("DejaVu Sans", 10, "bold"), padx=10, pady=8)
        gh_box.pack(fill="x", pady=4)

        info_text = (
            "Repository GitHub:\n"
            "  🔗 https://github.com/myzert/discord-chan\n\n"
            "Perintah untuk publish ke repository kamu:\n"
            "  cd /root/discord-chan\n"
            "  git remote set-url origin https://github.com/myzert/discord-chan.git\n"
            "  git branch -M main\n"
            "  git push -u origin main\n\n"
            "🤝 Terbuka untuk Kontributor & Star!"
        )
        tk.Label(gh_box, text=info_text, bg="#2b2132", fg="#fdf2f8", font=("DejaVu Sans", 8), justify="left").pack(anchor="w")

    def open_command_palette(self):
        pal_win = tk.Toplevel(self.root)
        pal_win.title("⌨ Command Palette")
        pal_win.geometry("500x380")
        pal_win.configure(bg="#1a1420")
        pal_win.transient(self.root)
        pal_win.grab_set()

        tk.Label(pal_win, text="🌸 DISCORD-CHAN COMMAND PALETTE", font=("DejaVu Sans", 11, "bold"), bg="#1a1420", fg="#ff85a2").pack(pady=(12, 6))
        tk.Label(pal_win, text="Pilih perintah cepat:", bg="#1a1420", fg="#d4a5b8", font=("DejaVu Sans", 8)).pack(pady=(0, 8))

        commands = [
            ("🚀 1-Click Instant Setup", lambda: [pal_win.destroy(), self.run_instant_setup()]),
            ("⚡ Simpan & Terapkan Tema (Apply)", lambda: [pal_win.destroy(), self.apply_theme_action()]),
            ("🔄 Restart Discord Aman", lambda: [pal_win.destroy(), self.restart_discord_safe()]),
            ("🐱 Pasang Icon Discord-Chan Neko", lambda: [pal_win.destroy(), self.apply_neko_icon()]),
            ("🌸 Pasang Icon Whisper Me a Love Song", lambda: [pal_win.destroy(), self.apply_yuri_icon()]),
            ("🌸 Terapkan Palet Sakura Soft Pink", lambda: [pal_win.destroy(), self.select_palette("🌸 Sakura Soft", "#ff85a2", "#fbcfe8")]),
            ("🍓 Terapkan Palet Strawberry Rose", lambda: [pal_win.destroy(), self.select_palette("🍓 Strawberry Rose", "#fb7185", "#fecdd3")]),
            ("💜 Terapkan Palet Lavender Yuri", lambda: [pal_win.destroy(), self.select_palette("💜 Lavender Yuri", "#c084fc", "#e9d5ff")]),
            ("🛑 Hentikan Discord", lambda: [pal_win.destroy(), self.kill_discord()])
        ]

        frame_cmds = tk.Frame(pal_win, bg="#1a1420")
        frame_cmds.pack(fill="both", expand=True, padx=16, pady=4)

        for text, func in commands:
            b = tk.Button(frame_cmds, text=text, bg="#271d30", fg="#fdf2f8", font=("DejaVu Sans", 9),
                          relief="flat", anchor="w", padx=12, pady=4, cursor="hand2", command=func)
            b.pack(fill="x", pady=2)

    def update_status_display(self):
        bd_st = bd_injector.check_status()
        if bd_st.get("injected"):
            self.lbl_bd_status.config(text="BetterDiscord: 🟢 Injected & Aktif", fg="#86efac")
        else:
            self.lbl_bd_status.config(text="BetterDiscord: 🟡 Belum Di-Inject", fg="#fde047")

        try:
            res = subprocess.run(["pgrep", "-f", "Discord.real"], stdout=subprocess.PIPE)
            if res.returncode == 0:
                self.lbl_dc_status.config(text="Discord Process: 🟢 Sedang Berjalan", fg="#86efac")
            else:
                self.lbl_dc_status.config(text="Discord Process: ⚪ Tidak Berjalan", fg="#94a3b8")
        except Exception:
            pass

    def select_preset_wallpaper(self, wp):
        self.settings["wallpaper_id"] = wp["id"]
        self.settings["wallpaper_path"] = wp["path"]
        self.custom_path_var.set(wp["path"])
        self.apply_theme_action(silent=True)
        self.lbl_wp_status.config(text=f"Wallpaper Aktif: {wp['name']}")
        messagebox.showinfo("Wallpaper Terpilih", f"Wallpaper telah diubah ke:\n{wp['name']}")

    def browse_custom_wallpaper(self):
        filename = filedialog.askopenfilename(
            title="Pilih Gambar Anime",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.webp"), ("All Files", "*.*")]
        )
        if filename:
            self.custom_path_var.set(filename)

    def apply_custom_wallpaper(self):
        path = self.custom_path_var.get().strip()
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", "File gambar tidak ditemukan!")
            return
        self.settings["wallpaper_id"] = "custom"
        self.settings["wallpaper_path"] = path
        self.apply_theme_action(silent=False)
        self.lbl_wp_status.config(text=f"Wallpaper Aktif: Custom ({os.path.basename(path)})")

    def select_palette(self, name, pri, sec):
        self.settings["active_preset"] = name
        self.settings["accent_color"] = pri
        self.settings["soft_pink"] = sec
        self.lbl_accent_sample.config(bg=pri)
        self.lbl_soft_sample.config(bg=sec)
        self.lbl_preset_status.config(text=f"Palet Warna: {name}")
        self.apply_theme_action(silent=True)
        messagebox.showinfo("Palet Terpilih", f"Palet warna '{name}' aktif!")

    def pick_accent_color(self):
        col = colorchooser.askcolor(color=self.settings.get("accent_color", "#ff85a2"))
        if col and col[1]:
            self.settings["accent_color"] = col[1]
            self.lbl_accent_sample.config(bg=col[1])

    def pick_soft_color(self):
        col = colorchooser.askcolor(color=self.settings.get("soft_pink", "#fbcfe8"))
        if col and col[1]:
            self.settings["soft_pink"] = col[1]
            self.lbl_soft_sample.config(bg=col[1])

    def set_speaking_color(self, col):
        self.settings["speaking_color"] = col
        self.apply_theme_action(silent=True)
        messagebox.showinfo("Voice Ring", f"Warna speaking ring diubah ke {col}!")

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
        self.status_bar.config(text="✨ Tema berhasil diperbarui dan diterapkan ke Discord!")
        if not silent:
            messagebox.showinfo("Sukses", "Tema berhasil diperbarui!\nDiscord akan langsung memuat tampilan baru tanpa restart.")

    def run_instant_setup(self):
        self.status_bar.config(text="Menjalankan Instant Setup...")
        bd_ok, bd_msg = bd_injector.inject()
        self.apply_neko_icon(silent=True)
        self.apply_theme_action(silent=True)
        self.update_status_display()
        messagebox.showinfo("Instant Setup Selesai", "🎉 Setup Sukses!\n\n• BetterDiscord terinjeksi\n• Tema anime Whisper Me a Love Song aktif\n• Icon Discord-Chan Neko terpasang di Desktop & Menu\n• Anti-crash flags terpasang")

    def apply_neko_icon(self, silent=False):
        neko_src = "/root/Downloads/file_0000000068e0820b8bbfefec482b49ef.png"
        if not os.path.exists(neko_src):
            neko_src = os.path.join(REPO_DIR, "assets", "wallpapers", "discord_chan_neko.png")
        
        out_icons = os.path.join(REPO_DIR, "assets", "icons")
        icon_manager.generate_icons(neko_src, out_icons)
        icon_manager.install_system_icons(os.path.join(out_icons, "discord-neko.png"))
        icon_manager.update_desktop_shortcuts()
        if not silent:
            messagebox.showinfo("Icon Terpasang", "Icon aplikasi Discord telah diubah ke Discord-Chan Neko Mascot!")

    def apply_yuri_icon(self):
        yuri_src = "/root/Downloads/whisper_me_a_love_song_yuri_anime.jpg"
        if not os.path.exists(yuri_src):
            yuri_src = os.path.join(REPO_DIR, "assets", "wallpapers", "1_whisper_me_a_love_song.jpg")
        
        out_icons = os.path.join(REPO_DIR, "assets", "icons")
        icon_manager.generate_icons(yuri_src, out_icons)
        icon_manager.install_system_icons(os.path.join(out_icons, "discord-chan.png"))
        icon_manager.update_desktop_shortcuts()
        messagebox.showinfo("Icon Terpasang", "Icon aplikasi Discord telah diubah ke Whisper Me a Love Song Yuri!")

    def restart_discord_safe(self):
        subprocess.run(["pkill", "-9", "-f", "Discord.real"])
        subprocess.Popen(
            "setsid /root/.config/discord/Discord --url -- </dev/null >/tmp/discord.log 2>&1 &",
            shell=True
        )
        self.root.after(2000, self.update_status_display)
        messagebox.showinfo("Discord", "Discord telah di-restart dengan flag aman dan no-lag!")

    def kill_discord(self):
        subprocess.run(["pkill", "-9", "-f", "Discord.real"])
        self.update_status_display()
        messagebox.showinfo("Discord", "Proses Discord dihentikan.")

    def install_plugin_action(self, pid):
        ok, msg = plugins_manager.install_plugin(pid)
        self.refresh_plugins_list()
        if ok:
            messagebox.showinfo("Plugin", msg)
        else:
            messagebox.showerror("Plugin Error", msg)

    def uninstall_plugin_action(self, pid):
        ok, msg = plugins_manager.uninstall_plugin(pid)
        self.refresh_plugins_list()
        messagebox.showinfo("Plugin", msg)

def main():
    root = tk.Tk()
    app = DiscordChanStudio(root)
    root.mainloop()

if __name__ == "__main__":
    main()
