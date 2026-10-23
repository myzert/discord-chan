#!/usr/bin/env python3
"""
Discord-Chan Custom: Pixel Retro Anime Studio
A retro-styled 16-bit arcade / pixel anime control center for Discord.
Supports SVG vector logo rendering, Command Palette (Ctrl+Shift+P),
full translucency glass sliders, anti-collision layout, and instant 1-click setup.
Licensed under GNU General Public License v3.0 (GPLv3).
"""

import os
import sys
import json
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
from PIL import Image, ImageTk

# Support vector SVG rendering via cairosvg or rsvg-convert
HAS_CAIROSVG = False
try:
    import cairosvg
    HAS_CAIROSVG = True
except ImportError:
    pass

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
        "desc": "Anime Yuri Romance (Sasakoi - Default)",
        "path": os.path.join(REPO_DIR, "assets", "wallpapers", "1_whisper_me_a_love_song.jpg")
    },
    {
        "id": "sakura",
        "name": "🌺 Sakura Blossom Minimal",
        "desc": "Bunga Sakura Estetik 16-Bit Minimalis",
        "path": os.path.join(REPO_DIR, "assets", "wallpapers", "2_sakura_blossom_minimal.jpg")
    },
    {
        "id": "clouds",
        "name": "☁️ Pastel Clouds Scenery",
        "desc": "Langit Senja Pastel Lembut Retro",
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

def load_svg_image(svg_path, width, height):
    """Loads an SVG vector image and returns an ImageTk.PhotoImage."""
    if not os.path.exists(svg_path):
        return None
    try:
        if HAS_CAIROSVG:
            png_bytes = cairosvg.svg2png(url=svg_path, output_width=width, output_height=height)
            import io
            im = Image.open(io.BytesIO(png_bytes))
            return ImageTk.PhotoImage(im)
        else:
            # Fallback to rsvg-convert CLI
            tmp_png = f"/tmp/svg_conv_{width}_{height}.png"
            res = subprocess.run(["rsvg-convert", "-w", str(width), "-h", str(height), svg_path, "-o", tmp_png], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res.returncode == 0 and os.path.exists(tmp_png):
                im = Image.open(tmp_png)
                return ImageTk.PhotoImage(im)
    except Exception as e:
        print(f"Notice: SVG render error: {e}")
    return None

class PixelRetroStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("👾 [DISCORD-CHAN] • PIXEL RETRO STUDIO v2.6")
        self.root.geometry("880x720")
        self.root.minsize(820, 640)
        self.root.configure(bg="#140f1a")

        self.settings = theme_engine.load_settings()
        self.setup_pixel_styles()
        self.load_icons()
        self.create_widgets()
        self.setup_hotkeys()
        self.update_status_display()

    def setup_pixel_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Retro Pixel Dark Palette
        self.bg_main = "#140f1a"
        self.bg_card = "#1e1627"
        self.bg_inner = "#281d34"
        self.accent_pink = "#ff85a2"
        self.accent_soft = "#fbcfe8"
        self.border_retro = "#ff85a2"
        self.border_dark = "#4a2c59"

        self.style.configure(".", background=self.bg_main, foreground="#fdf2f8", font=("DejaVu Sans", 9))
        self.style.configure("TNotebook", background=self.bg_main, borderwidth=0)
        self.style.configure("TNotebook.Tab", 
                             background="#22182d", 
                             foreground="#d4a5b8", 
                             padding=[14, 8], 
                             font=("DejaVu Sans", 9, "bold"))
        self.style.map("TNotebook.Tab", 
                       background=[("selected", self.accent_pink)],
                       foreground=[("selected", "#140f1a")])

        self.style.configure("PixelCard.TFrame", background=self.bg_card, relief="flat")
        self.style.configure("TScale", background=self.bg_card, troughcolor="#120c18")

    def load_icons(self):
        svg_logo_path = os.path.join(REPO_DIR, "assets", "icons", "discord-chan-logo.svg")
        self.svg_logo_photo = load_svg_image(svg_logo_path, 48, 48)
        
        # Window icon
        png_icon = os.path.join(REPO_DIR, "assets", "icons", "discord-neko.png")
        if os.path.exists(png_icon):
            try:
                img = Image.open(png_icon).resize((64, 64))
                self.win_icon = ImageTk.PhotoImage(img)
                self.root.iconphoto(True, self.win_icon)
            except Exception:
                pass

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

    def play_chime(self):
        try:
            print("\a", end="", flush=True)
        except Exception:
            pass

    def create_widgets(self):
        # -------------------------------------------------------------
        # TOP RETRO PIXEL HEADER
        # -------------------------------------------------------------
        header_outer = tk.Frame(self.root, bg="#ff85a2", height=66)
        header_outer.pack(fill="x", side="top", padx=8, pady=(8, 4))

        header = tk.Frame(header_outer, bg="#1e1627", padx=12, pady=6)
        header.pack(fill="both", expand=True, padx=2, pady=2)

        # SVG Vector Logo
        if self.svg_logo_photo:
            logo_lbl = tk.Label(header, image=self.svg_logo_photo, bg="#1e1627")
            logo_lbl.pack(side="left", padx=(0, 10))

        # Title block
        title_box = tk.Frame(header, bg="#1e1627")
        title_box.pack(side="left")

        title_lbl = tk.Label(title_box, text="👾 DISCORD-CHAN • PIXEL RETRO STUDIO", 
                             font=("DejaVu Sans", 13, "bold"), bg="#1e1627", fg="#ff85a2")
        title_lbl.pack(anchor="w")

        sub_lbl = tk.Label(title_box, text="🌸 Whisper Me a Love Song Edition • 16-Bit Glass Engine • GPLv3", 
                           font=("DejaVu Sans", 8), bg="#1e1627", fg="#fbcfe8")
        sub_lbl.pack(anchor="w")

        # Right buttons & badges
        right_box = tk.Frame(header, bg="#1e1627")
        right_box.pack(side="right")

        cmd_btn = tk.Button(right_box, text="[ ⌨ Ctrl+Shift+P ]", bg="#362344", fg="#fbcfe8", 
                            font=("DejaVu Sans", 8, "bold"), relief="flat", padx=8, pady=4, 
                            cursor="hand2", command=self.open_command_palette)
        cmd_btn.pack(side="left", padx=4)

        quick_apply = tk.Button(right_box, text="[ 💾 SIMPAN (Ctrl+S) ]", bg="#ff85a2", fg="#140f1a", 
                                font=("DejaVu Sans", 9, "bold"), relief="flat", padx=12, pady=4, 
                                cursor="hand2", command=self.apply_theme_action)
        quick_apply.pack(side="left", padx=4)

        # -------------------------------------------------------------
        # MAIN NOTEBOOK TABS
        # -------------------------------------------------------------
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=4)

        # Tab 1: Setup & Status
        self.tab_dash = ttk.Frame(self.notebook, style="PixelCard.TFrame")
        self.notebook.add(self.tab_dash, text="🚀 Setup & Status")
        self.build_dash_tab()

        # Tab 2: Wallpapers & Glass Translucency
        self.tab_wallpapers = ttk.Frame(self.notebook, style="PixelCard.TFrame")
        self.notebook.add(self.tab_wallpapers, text="🖼️ Background & Glass")
        self.build_wallpaper_tab()

        # Tab 3: Pink Palette & Colors
        self.tab_colors = ttk.Frame(self.notebook, style="PixelCard.TFrame")
        self.notebook.add(self.tab_colors, text="💖 Palet Warna")
        self.build_colors_tab()

        # Tab 4: Voice & Profile UI
        self.tab_voice = ttk.Frame(self.notebook, style="PixelCard.TFrame")
        self.notebook.add(self.tab_voice, text="🎙️ Voice & Profil")
        self.build_voice_tab()

        # Tab 5: Anti-Collision Layout
        self.tab_perf = ttk.Frame(self.notebook, style="PixelCard.TFrame")
        self.notebook.add(self.tab_perf, text="⚡ Layout Anti-Nabrak")
        self.build_perf_tab()

        # Tab 6: Plugins
        self.tab_plugins = ttk.Frame(self.notebook, style="PixelCard.TFrame")
        self.notebook.add(self.tab_plugins, text="🧩 Plugins BD")
        self.build_plugins_tab()

        # Tab 7: About & Contributors
        self.tab_about = ttk.Frame(self.notebook, style="PixelCard.TFrame")
        self.notebook.add(self.tab_about, text="ℹ️ GitHub & Kontribusi")
        self.build_about_tab()

        # -------------------------------------------------------------
        # RETRO BOTTOM STATUS BAR (PIXEL HUD)
        # -------------------------------------------------------------
        hud_bar = tk.Frame(self.root, bg="#100b15", height=26, padx=10, pady=2)
        hud_bar.pack(fill="x", side="bottom")

        self.hud_text = tk.Label(hud_bar, text="👾 [STATUS: OK] • LVL.99 • ZERO-LAG ENGINE: 60 FPS • LISENSI: GPLv3", 
                                 bg="#100b15", fg="#ff85a2", font=("DejaVu Sans", 8, "bold"))
        self.hud_text.pack(side="left")

        safe_tag = tk.Label(hud_bar, text="🛡️ 100% CLIENT-SIDE CSS (BUKAN MOD NITRO)", 
                            bg="#100b15", fg="#86efac", font=("DejaVu Sans", 8))
        safe_tag.pack(side="right")

    # -------------------------------------------------------------
    # TAB 1: DASHBOARD & INSTANT SETUP
    # -------------------------------------------------------------
    def build_dash_tab(self):
        container = tk.Frame(self.tab_dash, bg="#1e1627", padx=16, pady=12)
        container.pack(fill="both", expand=True)

        # Big Instant Setup Pixel Box
        box_border = tk.Frame(container, bg="#ff85a2", padx=2, pady=2)
        box_border.pack(fill="x", pady=(0, 10))

        instant_box = tk.Frame(box_border, bg="#281d34", padx=14, pady=10)
        instant_box.pack(fill="both", expand=True)

        tk.Label(instant_box, text="✨ 1-CLICK INSTANT SETUP (AUTO-CONFIGURE ALL)", 
                 bg="#281d34", fg="#ff85a2", font=("DejaVu Sans", 10, "bold")).pack(anchor="w")

        info_setup = (
            "Tekan 1 tombol ini untuk memasang dan mengonfigurasi segalanya secara otomatis:\n"
            "• Auto-detect & Inject BetterDiscord tanpa install manual\n"
            "• Terapkan Wallpaper Anime Whisper Me a Love Song (Sasakoi)\n"
            "• Pasang Icon Anime Discord-Chan Neko ke Desktop & Application Menu\n"
            "• Optimalkan flags anti-crash dan performa 60 FPS zero-lag"
        )
        tk.Label(instant_box, text=info_setup, bg="#281d34", fg="#fdf2f8", justify="left", font=("DejaVu Sans", 8)).pack(anchor="w", pady=(4, 8))

        btn_row = tk.Frame(instant_box, bg="#281d34")
        btn_row.pack(fill="x")

        tk.Button(btn_row, text="▶ 1-CLICK INSTANT SETUP", bg="#ff85a2", fg="#140f1a", font=("DejaVu Sans", 10, "bold"),
                  relief="flat", padx=16, pady=6, cursor="hand2", command=self.run_instant_setup).pack(side="left")

        tk.Button(btn_row, text="🔄 RESTART DISCORD (Ctrl+R)", bg="#3e2a4f", fg="#fbcfe8", font=("DejaVu Sans", 9, "bold"),
                  relief="flat", padx=12, pady=6, cursor="hand2", command=self.restart_discord_safe).pack(side="left", padx=10)

        # System Status Box
        stat_border = tk.Frame(container, bg="#4a2c59", padx=1, pady=1)
        stat_border.pack(fill="x", pady=4)

        status_box = tk.Frame(stat_border, bg="#281d34", padx=12, pady=8)
        status_box.pack(fill="both", expand=True)

        tk.Label(status_box, text="📊 STATUS SISTEM & CLIENT", bg="#281d34", fg="#fbcfe8", font=("DejaVu Sans", 9, "bold")).pack(anchor="w", pady=(0, 4))

        self.lbl_bd_status = tk.Label(status_box, text="BetterDiscord: Memeriksa...", bg="#281d34", fg="#fdf2f8", font=("DejaVu Sans", 8))
        self.lbl_bd_status.pack(anchor="w", pady=1)

        self.lbl_dc_status = tk.Label(status_box, text="Discord Process: Memeriksa...", bg="#281d34", fg="#fdf2f8", font=("DejaVu Sans", 8))
        self.lbl_dc_status.pack(anchor="w", pady=1)

        self.lbl_wp_status = tk.Label(status_box, text=f"Wallpaper Aktif: {self.settings.get('wallpaper_id', 'whisper')}", bg="#281d34", fg="#fdf2f8", font=("DejaVu Sans", 8))
        self.lbl_wp_status.pack(anchor="w", pady=1)

        self.lbl_preset_status = tk.Label(status_box, text=f"Palet Warna: {self.settings.get('active_preset', 'Sakura Soft')}", bg="#281d34", fg="#fdf2f8", font=("DejaVu Sans", 8))
        self.lbl_preset_status.pack(anchor="w", pady=1)

        # Icon Selector Box (Neko vs Yuri)
        icon_border = tk.Frame(container, bg="#4a2c59", padx=1, pady=1)
        icon_border.pack(fill="x", pady=6)

        icon_box = tk.Frame(icon_border, bg="#281d34", padx=12, pady=8)
        icon_box.pack(fill="both", expand=True)

        tk.Label(icon_box, text="🎭 PILIH ICON APLIKASI DISCORD (1-KLIK GANTI)", bg="#281d34", fg="#fbcfe8", font=("DejaVu Sans", 9, "bold")).pack(anchor="w", pady=(0, 4))

        i_row = tk.Frame(icon_box, bg="#281d34")
        i_row.pack(fill="x")

        tk.Button(i_row, text="🐱 Pasang Icon Discord-Chan Neko", bg="#ff85a2", fg="#140f1a", font=("DejaVu Sans", 8, "bold"),
                  relief="flat", padx=12, pady=5, cursor="hand2", command=self.apply_neko_icon).pack(side="left", padx=(0, 8))

        tk.Button(i_row, text="🌸 Pasang Icon Whisper Me a Love Song", bg="#3e2a4f", fg="#fbcfe8", font=("DejaVu Sans", 8, "bold"),
                  relief="flat", padx=12, pady=5, cursor="hand2", command=self.apply_yuri_icon).pack(side="left")

        # ToS Disclaimer Badge
        safe_card = tk.Frame(container, bg="#100b15", padx=10, pady=6, highlightthickness=1, highlightbackground="#2d5a3f")
        safe_card.pack(fill="x", pady=(8, 0))
        tk.Label(safe_card, text="🛡️ PENTING: Tema ini 100% Client-Side CSS visual saja. BUKAN modifikasi fitur Nitro berbayar. Aman dari banned dan ramah aturan Discord.",
                 bg="#100b15", fg="#86efac", font=("DejaVu Sans", 8)).pack(anchor="w")

    # -------------------------------------------------------------
    # TAB 2: WALLPAPERS & GLASS TRANSLUCENCY
    # -------------------------------------------------------------
    def build_wallpaper_tab(self):
        container = tk.Frame(self.tab_wallpapers, bg="#1e1627", padx=16, pady=12)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="PILIH PRESET WALLPAPER ANIME:", font=("DejaVu Sans", 10, "bold"), bg="#1e1627", fg="#ff85a2").pack(anchor="w", pady=(0, 6))

        grid_frame = tk.Frame(container, bg="#1e1627")
        grid_frame.pack(fill="x", pady=2)

        for i, wp in enumerate(WALLPAPERS):
            card = tk.Frame(grid_frame, bg="#281d34", padx=10, pady=6, highlightthickness=1, highlightbackground="#4a2c59")
            card.grid(row=i//2, column=i%2, padx=4, pady=4, sticky="nsew")
            grid_frame.columnconfigure(i%2, weight=1)

            tk.Label(card, text=wp["name"], font=("DejaVu Sans", 9, "bold"), bg="#281d34", fg="#fbcfe8").pack(anchor="w")
            tk.Label(card, text=wp["desc"], font=("DejaVu Sans", 8), bg="#281d34", fg="#d4a5b8").pack(anchor="w")

            btn = tk.Button(card, text="Pilih Wallpaper", bg="#ff85a2", fg="#140f1a", font=("DejaVu Sans", 8, "bold"),
                            relief="flat", padx=8, pady=2, cursor="hand2",
                            command=lambda w=wp: self.select_preset_wallpaper(w))
            btn.pack(anchor="e", pady=(2, 0))

        # Custom Wallpaper Box
        custom_box = tk.LabelFrame(container, text=" 📁 Custom Wallpaper Sendiri ", bg="#281d34", fg="#fbcfe8", font=("DejaVu Sans", 9, "bold"), padx=10, pady=6)
        custom_box.pack(fill="x", pady=6)

        c_row = tk.Frame(custom_box, bg="#281d34")
        c_row.pack(fill="x")

        self.custom_path_var = tk.StringVar(value=self.settings.get("wallpaper_path", ""))
        entry = tk.Entry(c_row, textvariable=self.custom_path_var, bg="#120c18", fg="#fdf2f8", insertbackground="#ff85a2", relief="flat")
        entry.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=3)

        tk.Button(c_row, text="Browse (Ctrl+O)", bg="#3e2a4f", fg="#fbcfe8", font=("DejaVu Sans", 8, "bold"), relief="flat", padx=8, pady=3,
                  command=self.browse_custom_wallpaper).pack(side="left")

        tk.Button(c_row, text="Terapkan", bg="#ff85a2", fg="#140f1a", font=("DejaVu Sans", 8, "bold"), relief="flat", padx=10, pady=3,
                  command=self.apply_custom_wallpaper).pack(side="left", padx=(6, 0))

        # Translucency Sliders (Glass UI)
        trans_box = tk.LabelFrame(container, text=" 🪟 Pengaturan Transparansi Kaca (Glass UI) ", bg="#281d34", fg="#fbcfe8", font=("DejaVu Sans", 9, "bold"), padx=10, pady=6)
        trans_box.pack(fill="x", pady=4)

        # 1. Overlay opacity
        tk.Label(trans_box, text="Tingkat Gelap Background (Overlay Opacity):", bg="#281d34", fg="#fdf2f8", font=("DejaVu Sans", 8)).pack(anchor="w")
        self.wp_opacity_var = tk.DoubleVar(value=float(self.settings.get("wallpaper_opacity", 0.80)))
        tk.Scale(trans_box, from_=0.10, to=0.98, resolution=0.02, orient="horizontal", variable=self.wp_opacity_var,
                 bg="#281d34", fg="#ff85a2", troughcolor="#120c18", highlightthickness=0).pack(fill="x")

        # 2. Sidebar opacity
        tk.Label(trans_box, text="Transparansi Sidebar Channels:", bg="#281d34", fg="#fdf2f8", font=("DejaVu Sans", 8)).pack(anchor="w", pady=(2, 0))
        self.sidebar_op_var = tk.DoubleVar(value=float(self.settings.get("sidebar_opacity", 0.62)))
        tk.Scale(trans_box, from_=0.20, to=0.95, resolution=0.02, orient="horizontal", variable=self.sidebar_op_var,
                 bg="#281d34", fg="#ff85a2", troughcolor="#120c18", highlightthickness=0).pack(fill="x")

        # 3. Chat layer opacity
        tk.Label(trans_box, text="Transparansi Area Chat Pesan:", bg="#281d34", fg="#fdf2f8", font=("DejaVu Sans", 8)).pack(anchor="w", pady=(2, 0))
        self.chat_op_var = tk.DoubleVar(value=float(self.settings.get("chat_opacity", 0.40)))
        tk.Scale(trans_box, from_=0.05, to=0.85, resolution=0.02, orient="horizontal", variable=self.chat_op_var,
                 bg="#281d34", fg="#ff85a2", troughcolor="#120c18", highlightthickness=0).pack(fill="x")

    # -------------------------------------------------------------
    # TAB 3: COLORS & PINK PALETTES
    # -------------------------------------------------------------
    def build_colors_tab(self):
        container = tk.Frame(self.tab_colors, bg="#1e1627", padx=16, pady=12)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="PILIH TEMA PALET WARNA MINIMALIS PINK:", font=("DejaVu Sans", 10, "bold"), bg="#1e1627", fg="#ff85a2").pack(anchor="w", pady=(0, 6))

        palettes_frame = tk.Frame(container, bg="#1e1627")
        palettes_frame.pack(fill="x", pady=2)

        for i, (name, pri, sec) in enumerate(PINK_PALETTES):
            row = tk.Frame(palettes_frame, bg="#281d34", padx=8, pady=4, highlightthickness=1, highlightbackground="#4a2c59")
            row.pack(fill="x", pady=2)

            dot1 = tk.Label(row, text="  ", bg=pri, width=2)
            dot1.pack(side="left", padx=4)
            dot2 = tk.Label(row, text="  ", bg=sec, width=2)
            dot2.pack(side="left", padx=4)

            tk.Label(row, text=name, bg="#281d34", fg="#fdf2f8", font=("DejaVu Sans", 9, "bold")).pack(side="left", padx=8)
            tk.Label(row, text=f"({pri} / {sec})", bg="#281d34", fg="#d4a5b8", font=("DejaVu Sans", 8)).pack(side="left")

            btn = tk.Button(row, text="Pilih Palet", bg="#ff85a2", fg="#140f1a", font=("DejaVu Sans", 8, "bold"),
                            relief="flat", padx=8, pady=2, cursor="hand2",
                            command=lambda n=name, p=pri, s=sec: self.select_palette(n, p, s))
            btn.pack(side="right")

        # Custom Color Picker
        custom_c = tk.LabelFrame(container, text=" 🎨 Custom Hex Color Picker ", bg="#281d34", fg="#fbcfe8", font=("DejaVu Sans", 9, "bold"), padx=10, pady=6)
        custom_c.pack(fill="x", pady=6)

        c_row = tk.Frame(custom_c, bg="#281d34")
        c_row.pack(fill="x")

        tk.Label(c_row, text="Warna Utama (Primary):", bg="#281d34", fg="#fdf2f8", font=("DejaVu Sans", 8)).pack(side="left")
        self.lbl_accent_sample = tk.Label(c_row, text="      ", bg=self.settings.get("accent_color", "#ff85a2"), relief="solid", borderwidth=1)
        self.lbl_accent_sample.pack(side="left", padx=6)

        tk.Button(c_row, text="Pilih", bg="#3e2a4f", fg="#fbcfe8", font=("DejaVu Sans", 8), relief="flat", padx=6, pady=2,
                  command=self.pick_accent_color).pack(side="left", padx=4)

        tk.Label(c_row, text="Warna Soft:", bg="#281d34", fg="#fdf2f8", font=("DejaVu Sans", 8)).pack(side="left", padx=(10, 0))
        self.lbl_soft_sample = tk.Label(c_row, text="      ", bg=self.settings.get("soft_pink", "#fbcfe8"), relief="solid", borderwidth=1)
        self.lbl_soft_sample.pack(side="left", padx=6)

        tk.Button(c_row, text="Pilih", bg="#3e2a4f", fg="#fbcfe8", font=("DejaVu Sans", 8), relief="flat", padx=6, pady=2,
                  command=self.pick_soft_color).pack(side="left", padx=4)

    # -------------------------------------------------------------
    # TAB 4: VOICE CALL & PROFILE UI
    # -------------------------------------------------------------
    def build_voice_tab(self):
        container = tk.Frame(self.tab_voice, bg="#1e1627", padx=16, pady=12)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="KUSTOMISASI VOICE CALL & TAMPILAN PROFIL:", font=("DejaVu Sans", 10, "bold"), bg="#1e1627", fg="#ff85a2").pack(anchor="w", pady=(0, 6))

        spk_box = tk.LabelFrame(container, text=" 🎙️ Warna Lingkaran Saat Berbicara (Speaking Ring) ", bg="#281d34", fg="#fbcfe8", font=("DejaVu Sans", 9, "bold"), padx=10, pady=6)
        spk_box.pack(fill="x", pady=4)

        for name, col in SPEAKING_COLORS:
            row = tk.Frame(spk_box, bg="#281d34")
            row.pack(fill="x", pady=2)
            dot = tk.Label(row, text="  ", bg=col, width=2)
            dot.pack(side="left", padx=4)
            tk.Label(row, text=name, bg="#281d34", fg="#fdf2f8", font=("DejaVu Sans", 8)).pack(side="left", padx=6)
            tk.Button(row, text="Pilih", bg="#3e2a4f", fg="#fbcfe8", font=("DejaVu Sans", 8, "bold"), relief="flat", padx=8, pady=1,
                      command=lambda c=col: self.set_speaking_color(c)).pack(side="right")

        tile_box = tk.LabelFrame(container, text=" 🔲 Kotak Peserta Voice Call (Tiles) ", bg="#281d34", fg="#fbcfe8", font=("DejaVu Sans", 9, "bold"), padx=10, pady=6)
        tile_box.pack(fill="x", pady=4)

        tk.Label(tile_box, text="Transparansi Tile Suara (Opacity):", bg="#281d34", fg="#fdf2f8", font=("DejaVu Sans", 8)).pack(anchor="w")
        self.tile_op_var = tk.DoubleVar(value=float(self.settings.get("tile_opacity", 0.38)))
        tk.Scale(tile_box, from_=0.10, to=0.85, resolution=0.02, orient="horizontal", variable=self.tile_op_var,
                 bg="#281d34", fg="#ff85a2", troughcolor="#120c18", highlightthickness=0).pack(fill="x")

        tk.Label(tile_box, text="Kelengkungan Sudut Tile (Radius px):", bg="#281d34", fg="#fdf2f8", font=("DejaVu Sans", 8)).pack(anchor="w", pady=(2, 0))
        self.tile_rad_var = tk.IntVar(value=int(self.settings.get("tile_radius", 12)))
        tk.Scale(tile_box, from_=4, to=24, orient="horizontal", variable=self.tile_rad_var,
                 bg="#281d34", fg="#ff85a2", troughcolor="#120c18", highlightthickness=0).pack(fill="x")

        prof_box = tk.LabelFrame(container, text=" 👤 User Profile Card & Popout Modal ", bg="#281d34", fg="#fbcfe8", font=("DejaVu Sans", 9, "bold"), padx=10, pady=6)
        prof_box.pack(fill="x", pady=4)

        tk.Label(prof_box, text="Transparansi Kartu Profil Popout:", bg="#281d34", fg="#fdf2f8", font=("DejaVu Sans", 8)).pack(anchor="w")
        self.prof_op_var = tk.DoubleVar(value=float(self.settings.get("profile_opacity", 0.88)))
        tk.Scale(prof_box, from_=0.50, to=0.98, resolution=0.02, orient="horizontal", variable=self.prof_op_var,
                 bg="#281d34", fg="#ff85a2", troughcolor="#120c18", highlightthickness=0).pack(fill="x")

    # -------------------------------------------------------------
    # TAB 5: LAYOUT & ANTI-NABRAK PERFORMANCE
    # -------------------------------------------------------------
    def build_perf_tab(self):
        container = tk.Frame(self.tab_perf, bg="#1e1627", padx=16, pady=12)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="PENGATURAN POSISI & OPTIMASI ANTI-NABRAK:", font=("DejaVu Sans", 10, "bold"), bg="#1e1627", fg="#ff85a2").pack(anchor="w", pady=(0, 6))

        spacing_box = tk.LabelFrame(container, text=" 📏 Jarak dari Atas (Top Spacing Clearance) ", bg="#281d34", fg="#fbcfe8", font=("DejaVu Sans", 9, "bold"), padx=10, pady=6)
        spacing_box.pack(fill="x", pady=4)

        tk.Label(spacing_box, text="Memberi jarak bersih agar tidak nabrak dengan taskbar/panel window atas:", bg="#281d34", fg="#d4a5b8", font=("DejaVu Sans", 8)).pack(anchor="w")
        self.top_spacing_var = tk.IntVar(value=int(self.settings.get("top_spacing", 14)))
        tk.Scale(spacing_box, from_=0, to=40, orient="horizontal", variable=self.top_spacing_var,
                 bg="#281d34", fg="#ff85a2", troughcolor="#120c18", highlightthickness=0).pack(fill="x")

        opt_box = tk.LabelFrame(container, text=" ⚡ Engine Optimasi Performa ", bg="#281d34", fg="#fbcfe8", font=("DejaVu Sans", 9, "bold"), padx=10, pady=6)
        opt_box.pack(fill="x", pady=6)

        self.zero_lag_var = tk.BooleanVar(value=bool(self.settings.get("zero_lag", True)))
        cb1 = tk.Checkbutton(opt_box, text="Mode Zero-Lag: Hapus efek box-shadow & blur berat agar 60 FPS halus di Linux",
                             variable=self.zero_lag_var, bg="#281d34", fg="#fdf2f8", selectcolor="#120c18", activebackground="#281d34", font=("DejaVu Sans", 8))
        cb1.pack(anchor="w", pady=2)

        self.avatar_fix_var = tk.BooleanVar(value=bool(self.settings.get("chat_avatar_fixed", True)))
        cb2 = tk.Checkbutton(opt_box, text="Chat Avatar Alignment Guard: Pastikan foto profil di chat rapi dan tidak bergeser",
                             variable=self.avatar_fix_var, bg="#281d34", fg="#fdf2f8", selectcolor="#120c18", activebackground="#281d34", font=("DejaVu Sans", 8))
        cb2.pack(anchor="w", pady=2)

        hk_box = tk.LabelFrame(container, text=" ⌨ Pintasan Keyboard Cepat (Shortcuts) ", bg="#281d34", fg="#fbcfe8", font=("DejaVu Sans", 9, "bold"), padx=10, pady=6)
        hk_box.pack(fill="x", pady=4)

        hk_info = (
            "• Ctrl+Shift+P / Ctrl+P : Buka Quick Command Palette\n"
            "• Ctrl+S : Simpan dan terapkan tema langsung ke Discord\n"
            "• Ctrl+R : Restart Discord aman dengan anti-crash flag\n"
            "• Ctrl+O : Pilih custom wallpaper dari komputer\n"
            "• Ctrl+Q : Keluar dari Discord-Chan Studio"
        )
        tk.Label(hk_box, text=hk_info, bg="#281d34", fg="#fdf2f8", font=("DejaVu Sans", 8), justify="left").pack(anchor="w")

    # -------------------------------------------------------------
    # TAB 6: PLUGINS
    # -------------------------------------------------------------
    def build_plugins_tab(self):
        container = tk.Frame(self.tab_plugins, bg="#1e1627", padx=16, pady=12)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="BETTERDISCORD PLUGINS MANAGER:", font=("DejaVu Sans", 10, "bold"), bg="#1e1627", fg="#ff85a2").pack(anchor="w", pady=(0, 6))

        self.plugins_frame = tk.Frame(container, bg="#1e1627")
        self.plugins_frame.pack(fill="both", expand=True)
        self.refresh_plugins_list()

    def refresh_plugins_list(self):
        for widget in self.plugins_frame.winfo_children():
            widget.destroy()

        installed = plugins_manager.get_installed_plugins()
        for item in installed:
            row = tk.Frame(self.plugins_frame, bg="#281d34", padx=10, pady=6, highlightthickness=1, highlightbackground="#4a2c59")
            row.pack(fill="x", pady=3)

            info_col = tk.Frame(row, bg="#281d34")
            info_col.pack(side="left", fill="x", expand=True)

            status_icon = "🟢" if item["installed"] else "⚪"
            tk.Label(info_col, text=f"{status_icon} {item['name']} (by {item['author']})", bg="#281d34", fg="#fbcfe8", font=("DejaVu Sans", 8, "bold")).pack(anchor="w")
            tk.Label(info_col, text=item["desc"], bg="#281d34", fg="#d4a5b8", font=("DejaVu Sans", 8)).pack(anchor="w")

            if item["installed"]:
                tk.Button(row, text="Hapus Plugin", bg="#4a222e", fg="#fca5a5", font=("DejaVu Sans", 8, "bold"), relief="flat", padx=8, pady=2,
                          command=lambda pid=item["id"]: self.uninstall_plugin_action(pid)).pack(side="right")
            else:
                tk.Button(row, text="📥 Install", bg="#ff85a2", fg="#140f1a", font=("DejaVu Sans", 8, "bold"), relief="flat", padx=8, pady=2,
                          command=lambda pid=item["id"]: self.install_plugin_action(pid)).pack(side="right")

    # -------------------------------------------------------------
    # TAB 7: ABOUT & CONTRIBUTORS
    # -------------------------------------------------------------
    def build_about_tab(self):
        container = tk.Frame(self.tab_about, bg="#1e1627", padx=16, pady=12)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="👾 DISCORD-CHAN • PIXEL RETRO STUDIO", font=("DejaVu Sans", 12, "bold"), bg="#1e1627", fg="#ff85a2").pack(anchor="w")
        tk.Label(container, text="Whisper Me a Love Song Edition (Sasayaku You ni Koi wo Utau)\nOpen-Source Discord Aesthetic Suite for Linux & Windows • Licensed under GPLv3",
                 bg="#1e1627", fg="#fbcfe8", font=("DejaVu Sans", 8), justify="left").pack(anchor="w", pady=(2, 6))

        gh_box = tk.LabelFrame(container, text=" 🌐 Repository GitHub & Kontribusi ", bg="#281d34", fg="#fbcfe8", font=("DejaVu Sans", 9, "bold"), padx=10, pady=6)
        gh_box.pack(fill="x", pady=4)

        info_text = (
            "Repository Resmi:\n"
            "  🔗 https://github.com/myzert/discord-chan\n\n"
            "Perintah untuk publish ke repository kamu:\n"
            "  cd /root/discord-chan\n"
            "  git remote set-url origin https://github.com/myzert/discord-chan.git\n"
            "  git branch -M main\n"
            "  git push -u origin main\n\n"
            "🤝 Terbuka untuk Kontributor & Star! Bantu kembangkan tema anime ini!"
        )
        tk.Label(gh_box, text=info_text, bg="#281d34", fg="#fdf2f8", font=("DejaVu Sans", 8), justify="left").pack(anchor="w")

    # -------------------------------------------------------------
    # COMMAND PALETTE (CTRL+SHIFT+P)
    # -------------------------------------------------------------
    def open_command_palette(self):
        pal_win = tk.Toplevel(self.root)
        pal_win.title("⌨ Command Palette")
        pal_win.geometry("520x400")
        pal_win.configure(bg="#120c18")
        pal_win.transient(self.root)
        pal_win.grab_set()

        header_pal = tk.Frame(pal_win, bg="#ff85a2", padx=1, pady=1)
        header_pal.pack(fill="x", padx=8, pady=(8, 4))
        inner_pal = tk.Frame(header_pal, bg="#1e1627", padx=8, pady=4)
        inner_pal.pack(fill="both")

        tk.Label(inner_pal, text="👾 DISCORD-CHAN COMMAND PALETTE (Ctrl+Shift+P)", 
                 font=("DejaVu Sans", 10, "bold"), bg="#1e1627", fg="#ff85a2").pack(anchor="w")
        tk.Label(inner_pal, text="Pilih perintah cepat di bawah ini:", bg="#1e1627", fg="#d4a5b8", font=("DejaVu Sans", 8)).pack(anchor="w")

        commands = [
            ("🚀 [EXEC] 1-Click Instant Setup", lambda: [pal_win.destroy(), self.run_instant_setup()]),
            ("⚡ [EXEC] Simpan & Terapkan Tema (Apply)", lambda: [pal_win.destroy(), self.apply_theme_action()]),
            ("🔄 [EXEC] Restart Discord Aman", lambda: [pal_win.destroy(), self.restart_discord_safe()]),
            ("🐱 [ICON] Pasang Icon Discord-Chan Neko", lambda: [pal_win.destroy(), self.apply_neko_icon()]),
            ("🌸 [ICON] Pasang Icon Whisper Me a Love Song", lambda: [pal_win.destroy(), self.apply_yuri_icon()]),
            ("🌸 [THEME] Terapkan Palet Sakura Soft Pink", lambda: [pal_win.destroy(), self.select_palette("🌸 Sakura Soft", "#ff85a2", "#fbcfe8")]),
            ("🍓 [THEME] Terapkan Palet Strawberry Rose", lambda: [pal_win.destroy(), self.select_palette("🍓 Strawberry Rose", "#fb7185", "#fecdd3")]),
            ("💜 [THEME] Terapkan Palet Lavender Yuri", lambda: [pal_win.destroy(), self.select_palette("💜 Lavender Yuri", "#c084fc", "#e9d5ff")]),
            ("🛑 [EXEC] Hentikan Proses Discord", lambda: [pal_win.destroy(), self.kill_discord()])
        ]

        frame_cmds = tk.Frame(pal_win, bg="#120c18")
        frame_cmds.pack(fill="both", expand=True, padx=8, pady=4)

        for text, func in commands:
            b = tk.Button(frame_cmds, text=text, bg="#22182d", fg="#fdf2f8", font=("DejaVu Sans", 8),
                          relief="flat", anchor="w", padx=10, pady=3, cursor="hand2", command=func)
            b.pack(fill="x", pady=2)

    # -------------------------------------------------------------
    # ACTIONS & CALLBACKS
    # -------------------------------------------------------------
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
        self.play_chime()
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
        self.play_chime()
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
        self.play_chime()
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
        self.hud_text.config(text="👾 [TEMA AKTIF] • TEMA BERHASIL DITERAPKAN KE DISCORD! (60 FPS)")
        self.play_chime()
        if not silent:
            messagebox.showinfo("Sukses", "Tema berhasil diperbarui!\nDiscord akan langsung memuat tampilan baru tanpa restart.")

    def run_instant_setup(self):
        bd_ok, bd_msg = bd_injector.inject()
        self.apply_neko_icon(silent=True)
        self.apply_theme_action(silent=True)
        self.update_status_display()
        self.play_chime()
        messagebox.showinfo("Instant Setup Selesai", "🎉 Setup Sukses!\n\n• BetterDiscord terinjeksi\n• Tema anime Whisper Me a Love Song aktif\n• Icon Discord-Chan Neko terpasang di Desktop & Menu\n• Anti-crash flags terpasang")

    def apply_neko_icon(self, silent=False):
        neko_src = "/root/Downloads/file_0000000068e0820b8bbfefec482b49ef.png"
        if not os.path.exists(neko_src):
            neko_src = os.path.join(REPO_DIR, "assets", "wallpapers", "discord_chan_neko.png")
        
        out_icons = os.path.join(REPO_DIR, "assets", "icons")
        icon_manager.generate_icons(neko_src, out_icons)
        icon_manager.install_system_icons(os.path.join(out_icons, "discord-neko.png"))
        icon_manager.update_desktop_shortcuts()
        self.play_chime()
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
        self.play_chime()
        messagebox.showinfo("Icon Terpasang", "Icon aplikasi Discord telah diubah ke Whisper Me a Love Song Yuri!")

    def restart_discord_safe(self):
        subprocess.run(["pkill", "-9", "-f", "Discord.real"])
        subprocess.Popen(
            "setsid /root/.config/discord/Discord --url -- </dev/null >/tmp/discord.log 2>&1 &",
            shell=True
        )
        self.root.after(2000, self.update_status_display)
        self.play_chime()
        messagebox.showinfo("Discord", "Discord telah di-restart dengan flag aman dan no-lag!")

    def kill_discord(self):
        subprocess.run(["pkill", "-9", "-f", "Discord.real"])
        self.update_status_display()
        self.play_chime()
        messagebox.showinfo("Discord", "Proses Discord dihentikan.")

    def install_plugin_action(self, pid):
        ok, msg = plugins_manager.install_plugin(pid)
        self.refresh_plugins_list()
        self.play_chime()
        if ok:
            messagebox.showinfo("Plugin", msg)
        else:
            messagebox.showerror("Plugin Error", msg)

    def uninstall_plugin_action(self, pid):
        ok, msg = plugins_manager.uninstall_plugin(pid)
        self.refresh_plugins_list()
        self.play_chime()
        messagebox.showinfo("Plugin", msg)

def main():
    root = tk.Tk()
    app = PixelRetroStudio(root)
    root.mainloop()

if __name__ == "__main__":
    main()
