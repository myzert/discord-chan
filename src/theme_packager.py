#!/usr/bin/env python3
"""
Discord-Chan Custom: Theme Packager (Export & Import System)
Exports and imports full custom themes as .zip bundles containing:
- meta.json (Theme info & metadata)
- config.json (Full theme parameters, sliders, opacities, colors)
- theme.css (Generated CSS stylesheet)
- wallpaper.* (Embedded high-res wallpaper image file)
Licensed under GNU General Public License v3.0 (GPLv3).
"""

import os
import json
import shutil
import zipfile
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
IMPORTED_WALLPAPERS_DIR = os.path.join(REPO_DIR, "assets", "wallpapers", "imported")

def export_theme_zip(output_zip_path, settings, theme_name="Custom Anime Theme", author="myzert", description="Custom Discord-Chan theme"):
    os.makedirs(os.path.dirname(os.path.abspath(output_zip_path)), exist_ok=True)
    temp_dir = f"/tmp/export_theme_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # 1. Meta file
        meta = {
            "name": theme_name,
            "author": author,
            "version": "2.6.0",
            "created_at": datetime.now().isoformat(),
            "description": description,
            "format": "discord-chan-theme-zip"
        }
        with open(os.path.join(temp_dir, "meta.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        # 2. Config file
        # Make a copy of settings without machine-specific absolute path
        conf_copy = settings.copy()
        wp_path = settings.get("wallpaper_path", "")
        wp_filename = os.path.basename(wp_path) if wp_path else ""
        conf_copy["wallpaper_embedded"] = wp_filename

        with open(os.path.join(temp_dir, "config.json"), "w", encoding="utf-8") as f:
            json.dump(conf_copy, f, indent=2)

        # 3. Theme CSS
        import theme_engine
        css_content = theme_engine.generate_theme_css(settings)
        with open(os.path.join(temp_dir, "theme.css"), "w", encoding="utf-8") as f:
            f.write(css_content)

        # 4. Embedded Wallpaper
        if wp_path and os.path.exists(wp_path):
            shutil.copy2(wp_path, os.path.join(temp_dir, wp_filename))

        # 5. Pack into .zip
        with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    full_p = os.path.join(root, file)
                    arc_p = os.path.relpath(full_p, temp_dir)
                    zf.write(full_p, arc_p)

        shutil.rmtree(temp_dir, ignore_errors=True)
        return True, f"Theme exported successfully to:\n{output_zip_path}"
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return False, f"Failed to export theme: {e}"

def import_theme_zip(zip_path):
    if not os.path.exists(zip_path) or not zipfile.is_zipfile(zip_path):
        return False, None, "Invalid zip archive file!"

    temp_dir = f"/tmp/import_theme_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(IMPORTED_WALLPAPERS_DIR, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(temp_dir)

        config_path = os.path.join(temp_dir, "config.json")
        if not os.path.exists(config_path):
            return False, None, "The zip file does not contain config.json!"

        with open(config_path, "r", encoding="utf-8") as f:
            imported_settings = json.load(f)

        # Check for embedded wallpaper
        embedded_wp = imported_settings.get("wallpaper_embedded")
        if embedded_wp:
            wp_source = os.path.join(temp_dir, embedded_wp)
            if os.path.exists(wp_source):
                dest_wp = os.path.join(IMPORTED_WALLPAPERS_DIR, embedded_wp)
                shutil.copy2(wp_source, dest_wp)
                imported_settings["wallpaper_path"] = dest_wp
                imported_settings["wallpaper_id"] = f"imported_{os.path.splitext(embedded_wp)[0]}"

        # Apply imported settings
        import theme_engine
        theme_engine.apply_theme(imported_settings)

        shutil.rmtree(temp_dir, ignore_errors=True)
        return True, imported_settings, "Theme imported and activated successfully in Discord!"
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return False, None, f"Failed to import theme: {e}"
