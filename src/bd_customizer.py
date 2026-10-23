#!/usr/bin/env python3
"""
BetterDiscord Customizer Engine: Theme & Plugin Uploader, Parser, and Modifier
Provides full control over BetterDiscord themes and plugins:
- Upload any .theme.css or .css theme
- Parse theme metadata (@name, @author, @version, @description, etc.)
- Modify theme variables (accent color, background image, opacity, radius)
- Built-in CSS editor and patcher
- Upload and manage .plugin.js and .zip plugins
- Toggle active state in themes.json and plugins.json
Licensed under GNU General Public License v3.0 (GPLv3).
"""

import os
import re
import json
import shutil
import zipfile

HOME_DIR = os.path.expanduser("~")
BD_DIR = os.path.join(HOME_DIR, ".config", "BetterDiscord")
THEMES_DIR = os.path.join(BD_DIR, "themes")
PLUGINS_DIR = os.path.join(BD_DIR, "plugins")
DATA_DIR = os.path.join(BD_DIR, "data", "stable")
THEMES_JSON = os.path.join(DATA_DIR, "themes.json")
PLUGINS_JSON = os.path.join(DATA_DIR, "plugins.json")


def ensure_bd_dirs():
    os.makedirs(THEMES_DIR, exist_ok=True)
    os.makedirs(PLUGINS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)


def parse_metadata(content):
    meta = {
        "name": "Untitled Theme",
        "author": "Unknown",
        "version": "1.0.0",
        "description": "Custom BetterDiscord theme or plugin.",
        "source": "",
        "website": "",
        "invite": ""
    }
    patterns = {
        "name": r"@name\s+([^\r\n*]+)",
        "author": r"@author\s+([^\r\n*]+)",
        "version": r"@version\s+([^\r\n*]+)",
        "description": r"@description\s+([^\r\n*]+)",
        "source": r"@source\s+([^\r\n*]+)",
        "website": r"@website\s+([^\r\n*]+)",
        "invite": r"@invite\s+([^\r\n*]+)"
    }
    for key, pat in patterns.items():
        m = re.search(pat, content)
        if m:
            meta[key] = m.group(1).strip()
    return meta


# ========================================================
# THEME MANAGEMENT & MODIFIER
# ========================================================

def load_themes_config():
    ensure_bd_dirs()
    if os.path.exists(THEMES_JSON):
        try:
            with open(THEMES_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_themes_config(cfg):
    ensure_bd_dirs()
    with open(THEMES_JSON, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)


def list_installed_themes():
    ensure_bd_dirs()
    cfg = load_themes_config()
    themes = []
    if not os.path.exists(THEMES_DIR):
        return themes

    for fname in sorted(os.listdir(THEMES_DIR)):
        if not fname.endswith(".css"):
            continue
        fpath = os.path.join(THEMES_DIR, fname)
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(4000)
            meta = parse_metadata(content)
            stem = fname.replace(".theme.css", "").replace(".css", "")
            
            # Check enabled status by exact name or stem
            is_enabled = cfg.get(meta["name"], False) or cfg.get(fname, False) or cfg.get(stem, False)
            
            themes.append({
                "filename": fname,
                "filepath": fpath,
                "name": meta["name"],
                "author": meta["author"],
                "version": meta["version"],
                "description": meta["description"],
                "source": meta["source"],
                "is_enabled": bool(is_enabled),
                "size_kb": round(os.path.getsize(fpath) / 1024, 1)
            })
        except Exception as e:
            print(f"Error reading theme {fname}: {e}")
    return themes


def toggle_theme(theme_name, filename, enabled=True):
    cfg = load_themes_config()
    stem = filename.replace(".theme.css", "").replace(".css", "")
    cfg[theme_name] = enabled
    cfg[stem] = enabled
    save_themes_config(cfg)
    return True


def upload_theme(source_path):
    ensure_bd_dirs()
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source file not found: {source_path}")

    base = os.path.basename(source_path)
    if not (base.endswith(".theme.css") or base.endswith(".css")):
        base += ".theme.css"
    elif base.endswith(".css") and not base.endswith(".theme.css"):
        base = base[:-4] + ".theme.css"

    target_path = os.path.join(THEMES_DIR, base)
    shutil.copy2(source_path, target_path)

    # Read and parse metadata
    with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read(4000)
    meta = parse_metadata(content)

    # Auto-enable uploaded theme
    toggle_theme(meta["name"], base, True)
    return {
        "filename": base,
        "filepath": target_path,
        "meta": meta
    }


def read_theme_full_css(filename):
    fpath = os.path.join(THEMES_DIR, filename)
    if not os.path.exists(fpath):
        raise FileNotFoundError(f"Theme file not found: {filename}")
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def save_theme_full_css(filename, new_css):
    ensure_bd_dirs()
    fpath = os.path.join(THEMES_DIR, filename)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_css)
    return True


def delete_theme(filename):
    fpath = os.path.join(THEMES_DIR, filename)
    if os.path.exists(fpath):
        os.remove(fpath)
    cfg = load_themes_config()
    stem = filename.replace(".theme.css", "").replace(".css", "")
    cfg.pop(filename, None)
    cfg.pop(stem, None)
    save_themes_config(cfg)
    return True


def clone_theme(filename, new_name):
    fpath = os.path.join(THEMES_DIR, filename)
    if not os.path.exists(fpath):
        raise FileNotFoundError(f"Theme file not found: {filename}")

    clean_stem = re.sub(r'[^a-zA-Z0-9_-]', '', new_name.replace(" ", "_"))
    new_filename = f"{clean_stem}.theme.css"
    new_path = os.path.join(THEMES_DIR, new_filename)

    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        css = f.read()

    # Update metadata header
    css = re.sub(r'@name\s+[^\r\n*]+', f'@name {new_name}', css, count=1)
    with open(new_path, "w", encoding="utf-8") as f:
        f.write(css)

    return new_filename


def extract_theme_variables(css):
    """
    Extracts configurable CSS variables from the theme CSS.
    Returns list of dicts: [{'var': '--main-color', 'val': '#ff85a2', 'type': 'color'|'url'|'other'}]
    """
    vars_found = []
    # Match root CSS variables
    root_match = re.search(r':root\s*\{([^}]+)\}', css, re.DOTALL)
    if not root_match:
        root_match = re.search(r'\{([^}]+)\}', css, re.DOTALL)
    
    if root_match:
        block = root_match.group(1)
        for line in block.split(";"):
            line = line.strip()
            if not line or not line.startswith("--"):
                continue
            parts = line.split(":", 1)
            if len(parts) == 2:
                v_name = parts[0].strip()
                v_val = parts[1].strip().replace("!important", "").strip()
                v_type = "other"
                if re.match(r'^#[0-9a-fA-F]{3,8}$', v_val) or "rgb" in v_val or "hsl" in v_val:
                    v_type = "color"
                elif "url(" in v_val:
                    v_type = "url"
                vars_found.append({"var": v_name, "val": v_val, "type": v_type})
    return vars_found


def apply_variable_modifications(css, replacements):
    """
    replacements: dict of {'--var-name': 'new-value'}
    """
    updated_css = css
    for var_name, new_val in replacements.items():
        escaped_name = re.escape(var_name)
        # Replace variable definition
        pattern = rf'({escaped_name}\s*:\s*)([^;!]+)((\s*!important)?\s*;)'
        if re.search(pattern, updated_css):
            updated_css = re.sub(pattern, rf'\g<1>{new_val}\g<3>', updated_css)
        else:
            # If not found in :root, inject at top of :root
            if ":root {" in updated_css:
                updated_css = updated_css.replace(":root {", f":root {{\n    {var_name}: {new_val} !important;", 1)
            elif ":root{" in updated_css:
                updated_css = updated_css.replace(":root{", f":root{{\n    {var_name}: {new_val} !important;", 1)
            else:
                updated_css = f":root {{\n    {var_name}: {new_val} !important;\n}}\n" + updated_css
    return updated_css


# ========================================================
# PLUGIN MANAGEMENT & UPLOADER
# ========================================================

def load_plugins_config():
    ensure_bd_dirs()
    if os.path.exists(PLUGINS_JSON):
        try:
            with open(PLUGINS_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_plugins_config(cfg):
    ensure_bd_dirs()
    with open(PLUGINS_JSON, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)


def list_installed_plugins():
    ensure_bd_dirs()
    cfg = load_plugins_config()
    plugins = []
    if not os.path.exists(PLUGINS_DIR):
        return plugins

    for fname in sorted(os.listdir(PLUGINS_DIR)):
        if not (fname.endswith(".plugin.js") or fname.endswith(".js")):
            continue
        fpath = os.path.join(PLUGINS_DIR, fname)
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(4000)
            meta = parse_metadata(content)
            stem = fname.replace(".plugin.js", "").replace(".js", "")
            
            is_enabled = cfg.get(meta["name"], False) or cfg.get(fname, False) or cfg.get(stem, False)
            
            plugins.append({
                "filename": fname,
                "filepath": fpath,
                "name": meta["name"],
                "author": meta["author"],
                "version": meta["version"],
                "description": meta["description"],
                "source": meta["source"],
                "is_enabled": bool(is_enabled),
                "size_kb": round(os.path.getsize(fpath) / 1024, 1)
            })
        except Exception as e:
            print(f"Error reading plugin {fname}: {e}")
    return plugins


def toggle_plugin(plugin_name, filename, enabled=True):
    cfg = load_plugins_config()
    stem = filename.replace(".plugin.js", "").replace(".js", "")
    cfg[plugin_name] = enabled
    cfg[stem] = enabled
    save_plugins_config(cfg)
    return True


def upload_plugin(source_path):
    ensure_bd_dirs()
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source file not found: {source_path}")

    # If it's a zip file, extract and search for .plugin.js
    if source_path.endswith(".zip"):
        installed = []
        with zipfile.ZipFile(source_path, "r") as z:
            for item in z.namelist():
                if item.endswith(".plugin.js") or item.endswith(".js"):
                    base = os.path.basename(item)
                    if not base:
                        continue
                    if not base.endswith(".plugin.js") and base.endswith(".js"):
                        base = base[:-3] + ".plugin.js"
                    target = os.path.join(PLUGINS_DIR, base)
                    with z.open(item) as zf, open(target, "wb") as out:
                        out.write(zf.read())
                    with open(target, "r", encoding="utf-8", errors="ignore") as f:
                        meta = parse_metadata(f.read(4000))
                    toggle_plugin(meta["name"], base, True)
                    installed.append(base)
        if not installed:
            raise ValueError("No .plugin.js or .js file found inside ZIP archive.")
        return installed[0]

    base = os.path.basename(source_path)
    if not (base.endswith(".plugin.js") or base.endswith(".js")):
        base += ".plugin.js"
    elif base.endswith(".js") and not base.endswith(".plugin.js"):
        base = base[:-3] + ".plugin.js"

    target_path = os.path.join(PLUGINS_DIR, base)
    shutil.copy2(source_path, target_path)

    with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
        meta = parse_metadata(f.read(4000))

    toggle_plugin(meta["name"], base, True)
    return base


def read_plugin_content(filename):
    fpath = os.path.join(PLUGINS_DIR, filename)
    if not os.path.exists(fpath):
        raise FileNotFoundError(f"Plugin file not found: {filename}")
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def save_plugin_content(filename, new_js):
    ensure_bd_dirs()
    fpath = os.path.join(PLUGINS_DIR, filename)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_js)
    return True


def delete_plugin(filename):
    fpath = os.path.join(PLUGINS_DIR, filename)
    if os.path.exists(fpath):
        os.remove(fpath)
    cfg = load_plugins_config()
    stem = filename.replace(".plugin.js", "").replace(".js", "")
    cfg.pop(filename, None)
    cfg.pop(stem, None)
    save_plugins_config(cfg)
    return True
