#!/usr/bin/env python3
"""
Discord-Chan Custom: Plugin & Extension System (ZIP Chrome-Style Packages)
Allows community creators to package, distribute, and install modular extensions
in .zip format containing manifest.json, style.css, and optional plugin scripts.
Licensed under GNU General Public License v3.0 (GPLv3).
"""

import os
import json
import shutil
import zipfile

HOME_DIR = os.path.expanduser("~")
BD_DIR = os.path.join(HOME_DIR, ".config", "BetterDiscord")
EXTENSIONS_DIR = os.path.join(BD_DIR, "discord_chan_extensions")
PLUGINS_DIR = os.path.join(BD_DIR, "plugins")
ACTIVE_EXT_FILE = os.path.join(BD_DIR, "discord_chan_active_extensions.json")

def ensure_dirs():
    os.makedirs(EXTENSIONS_DIR, exist_ok=True)
    os.makedirs(PLUGINS_DIR, exist_ok=True)

def load_active_states():
    ensure_dirs()
    if os.path.exists(ACTIVE_EXT_FILE):
        try:
            with open(ACTIVE_EXT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_active_states(states):
    ensure_dirs()
    try:
        with open(ACTIVE_EXT_FILE, "w", encoding="utf-8") as f:
            json.dump(states, f, indent=2)
    except Exception:
        pass

def list_installed_extensions():
    ensure_dirs()
    states = load_active_states()
    extensions = []

    for item in os.listdir(EXTENSIONS_DIR):
        ext_folder = os.path.join(EXTENSIONS_DIR, item)
        if os.path.isdir(ext_folder):
            manifest_file = os.path.join(ext_folder, "manifest.json")
            if os.path.exists(manifest_file):
                try:
                    with open(manifest_file, "r", encoding="utf-8") as f:
                        manifest = json.load(f)
                    ext_id = manifest.get("id", item)
                    extensions.append({
                        "id": ext_id,
                        "name": manifest.get("name", item),
                        "author": manifest.get("author", "Community"),
                        "version": manifest.get("version", "1.0.0"),
                        "description": manifest.get("description", "No description provided."),
                        "enabled": states.get(ext_id, True),
                        "folder": ext_folder,
                        "has_css": os.path.exists(os.path.join(ext_folder, manifest.get("styles", "style.css"))),
                        "has_js": os.path.exists(os.path.join(ext_folder, manifest.get("script", "plugin.js")))
                    })
                except Exception:
                    pass
    return extensions

def install_extension_zip(zip_path):
    ensure_dirs()
    if not os.path.exists(zip_path) or not zipfile.is_zipfile(zip_path):
        return False, "Selected file is not a valid zip archive!"

    temp_dir = f"/tmp/install_ext_{os.path.basename(zip_path)}"
    shutil.rmtree(temp_dir, ignore_errors=True)
    os.makedirs(temp_dir, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(temp_dir)

        # Check for manifest.json
        manifest_path = os.path.join(temp_dir, "manifest.json")
        if not os.path.exists(manifest_path):
            shutil.rmtree(temp_dir, ignore_errors=True)
            return False, "Extension zip is missing required 'manifest.json' file!"

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        ext_id = manifest.get("id")
        if not ext_id:
            shutil.rmtree(temp_dir, ignore_errors=True)
            return False, "'manifest.json' must specify a unique 'id'!"

        target_dir = os.path.join(EXTENSIONS_DIR, ext_id)
        shutil.rmtree(target_dir, ignore_errors=True)
        shutil.copytree(temp_dir, target_dir)

        # If extension includes a plugin.js, install it to BetterDiscord plugins
        js_file = manifest.get("script", "plugin.js")
        src_js = os.path.join(target_dir, js_file)
        if os.path.exists(src_js):
            dest_plugin = os.path.join(PLUGINS_DIR, f"{ext_id}.plugin.js")
            shutil.copy2(src_js, dest_plugin)

        # Enable by default
        states = load_active_states()
        states[ext_id] = True
        save_active_states(states)

        compile_all_extension_css()
        shutil.rmtree(temp_dir, ignore_errors=True)
        return True, f"Extension '{manifest.get('name', ext_id)}' installed successfully!"
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return False, f"Installation error: {e}"

def toggle_extension(ext_id, enabled):
    states = load_active_states()
    states[ext_id] = enabled
    save_active_states(states)

    # If plugin exists, enable/disable in BD
    ext_dir = os.path.join(EXTENSIONS_DIR, ext_id)
    manifest_p = os.path.join(ext_dir, "manifest.json")
    if os.path.exists(manifest_p):
        try:
            with open(manifest_p, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            js_name = f"{ext_id}.plugin.js"
            target_plugin = os.path.join(PLUGINS_DIR, js_name)
            if not enabled and os.path.exists(target_plugin):
                try:
                    os.remove(target_plugin)
                except Exception:
                    pass
            elif enabled and os.path.exists(os.path.join(ext_dir, manifest.get("script", "plugin.js"))):
                shutil.copy2(os.path.join(ext_dir, manifest.get("script", "plugin.js")), target_plugin)
        except Exception:
            pass

    compile_all_extension_css()
    return True

def uninstall_extension(ext_id):
    ext_dir = os.path.join(EXTENSIONS_DIR, ext_id)
    if os.path.exists(ext_dir):
        shutil.rmtree(ext_dir, ignore_errors=True)

    target_plugin = os.path.join(PLUGINS_DIR, f"{ext_id}.plugin.js")
    if os.path.exists(target_plugin):
        try:
            os.remove(target_plugin)
        except Exception:
            pass

    states = load_active_states()
    if ext_id in states:
        del states[ext_id]
        save_active_states(states)

    compile_all_extension_css()
    return True, f"Extension '{ext_id}' removed."

def compile_all_extension_css():
    ensure_dirs()
    states = load_active_states()
    compiled_css = "/* Discord-Chan Compiled Extension Styles */\n\n"

    for item in os.listdir(EXTENSIONS_DIR):
        ext_folder = os.path.join(EXTENSIONS_DIR, item)
        if os.path.isdir(ext_folder):
            manifest_file = os.path.join(ext_folder, "manifest.json")
            if os.path.exists(manifest_file):
                try:
                    with open(manifest_file, "r", encoding="utf-8") as f:
                        manifest = json.load(f)
                    ext_id = manifest.get("id", item)
                    if states.get(ext_id, True):
                        css_file = os.path.join(ext_folder, manifest.get("styles", "style.css"))
                        if os.path.exists(css_file):
                            with open(css_file, "r", encoding="utf-8") as cf:
                                compiled_css += f"/* --- Extension: {ext_id} --- */\n" + cf.read() + "\n\n"
                except Exception:
                    pass

    # Save to BetterDiscord custom.css or inject into themes
    bd_custom_css = os.path.join(BD_DIR, "data", "stable", "custom.css")
    try:
        os.makedirs(os.path.dirname(bd_custom_css), exist_ok=True)
        with open(bd_custom_css, "w", encoding="utf-8") as f:
            f.write(compiled_css)
    except Exception:
        pass

def create_extension_template(output_zip_path, name="My Extension", author="myzert", description="Custom CSS extension for Discord-Chan"):
    temp_dir = f"/tmp/template_{name.replace(' ', '_').lower()}"
    shutil.rmtree(temp_dir, ignore_errors=True)
    os.makedirs(temp_dir, exist_ok=True)

    ext_id = name.replace(" ", "-").lower()
    manifest = {
        "id": ext_id,
        "name": name,
        "version": "1.0.0",
        "author": author,
        "description": description,
        "styles": "style.css",
        "script": "plugin.js"
    }

    style_css = """/* Discord-Chan Extension Custom CSS */
/* Customize channel headers, badges, or chat glow: */
[class*="channelTextArea_"] {
    border-radius: 16px !important;
}

[class*="username_"]:hover {
    text-shadow: 0 0 8px rgba(255, 133, 162, 0.6) !important;
}
"""

    plugin_js = f"""/**
 * @name {name}
 * @author {author}
 * @version 1.0.0
 * @description {description}
 */
module.exports = class {name.replace(" ", "")} {{
    start() {{
        console.log("{name} started!");
    }}
    stop() {{
        console.log("{name} stopped!");
    }}
}};
"""

    with open(os.path.join(temp_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    with open(os.path.join(temp_dir, "style.css"), "w", encoding="utf-8") as f:
        f.write(style_css)

    with open(os.path.join(temp_dir, "plugin.js"), "w", encoding="utf-8") as f:
        f.write(plugin_js)

    with open(os.path.join(temp_dir, "README.txt"), "w", encoding="utf-8") as f:
        f.write(f"Discord-Chan Extension Package: {name}\nAuthor: {author}\nEdit style.css to add custom CSS, then zip and install through Discord-Chan Studio!\n")

    try:
        with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    full_p = os.path.join(root, file)
                    arc_p = os.path.relpath(full_p, temp_dir)
                    zf.write(full_p, arc_p)
        shutil.rmtree(temp_dir, ignore_errors=True)
        return True, f"Extension template created successfully at:\n{output_zip_path}"
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return False, f"Failed to create template: {e}"
