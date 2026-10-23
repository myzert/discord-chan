#!/usr/bin/env python3
"""
Discord-Chan Custom: Icon Manager
Generates clean, authentic squircle and standard icons directly from the original
Neko mascot without harsh borders or artificial high-contrast outlines.
Installs icons into system paths and desktop launchers without clutter.
"""

import os
import shutil
from PIL import Image, ImageDraw

def generate_icons(source_image_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    if not os.path.exists(source_image_path):
        raise FileNotFoundError(f"Source image not found: {source_image_path}")

    im = Image.open(source_image_path).convert("RGBA")
    w, h = im.size

    # Focus crop around character center
    if w != h:
        box_size = min(w, h)
        if w > h:
            left = max(0, int((w - box_size) * 0.5))
            crop = im.crop((left, 0, left + box_size, h))
        else:
            top = max(0, int((h - box_size) * 0.3))
            crop = im.crop((0, top, w, top + box_size))
    else:
        crop = im

    size_512 = (512, 512)
    base_512 = crop.resize(size_512, Image.Resampling.LANCZOS)

    # 1. Clean Modern Squircle icon (Smooth natural corner radius, NO harsh borders)
    mask = Image.new('L', size_512, 0)
    draw_mask = ImageDraw.Draw(mask)
    radius = 115
    draw_mask.rounded_rectangle([(0, 0), size_512], radius=radius, fill=255)

    icon_squircle = Image.new('RGBA', size_512, (0, 0, 0, 0))
    icon_squircle.paste(base_512, (0, 0), mask=mask)

    main_icon_path = os.path.join(output_dir, 'discord-neko.png')
    icon_squircle.save(main_icon_path)
    icon_squircle.save(os.path.join(output_dir, 'discord-neko-512.png'))
    icon_squircle.save(os.path.join(output_dir, 'discord-chan.png'))
    icon_squircle.save(os.path.join(output_dir, 'discord-chan-512.png'))

    # Standard sizes
    for s in [256, 128, 64, 48, 32, 16]:
        resized = icon_squircle.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(os.path.join(output_dir, f'discord-neko-{s}.png'))
        resized.save(os.path.join(output_dir, f'discord-chan-{s}.png'))

    # ICO format for Windows setup and desktop shortcuts
    icon_squircle.save(
        os.path.join(output_dir, 'discord-neko.ico'),
        format='ICO',
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    )
    icon_squircle.save(
        os.path.join(output_dir, 'discord-chan.ico'),
        format='ICO',
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    )

    return main_icon_path

def install_system_icons(icon_path):
    if not os.path.exists(icon_path):
        return False, "Icon file does not exist"
    
    try:
        os.makedirs('/usr/share/pixmaps', exist_ok=True)
        shutil.copy2(icon_path, '/usr/share/pixmaps/discord.png')
        shutil.copy2(icon_path, '/usr/share/pixmaps/discord-chan.png')

        icon_dir = os.path.dirname(icon_path)
        sizes = [('512x512', 512), ('256x256', 256), ('128x128', 128), ('64x64', 64), ('48x48', 48), ('32x32', 32), ('16x16', 16)]
        for dirname, s in sizes:
            target_dir = f'/usr/share/icons/hicolor/{dirname}/apps'
            os.makedirs(target_dir, exist_ok=True)
            res_file = os.path.join(icon_dir, f'discord-neko-{s}.png')
            if not os.path.exists(res_file):
                res_file = os.path.join(icon_dir, f'discord-chan-{s}.png')
            if os.path.exists(res_file):
                shutil.copy2(res_file, os.path.join(target_dir, 'discord.png'))
                shutil.copy2(res_file, os.path.join(target_dir, 'discord-chan.png'))

        user_icons = os.path.expanduser('~/.local/share/icons')
        os.makedirs(user_icons, exist_ok=True)
        shutil.copy2(icon_path, os.path.join(user_icons, 'discord.png'))
        shutil.copy2(icon_path, os.path.join(user_icons, 'discord-chan.png'))

        return True, "Successfully installed icons across system directories"
    except Exception as e:
        return False, f"Icon installation error: {e}"

def update_desktop_shortcuts():
    home = os.path.expanduser('~')
    desktop_dirs = [
        '/usr/share/applications',
        os.path.join(home, 'Desktop'),
        os.path.join(home, '.local', 'share', 'applications')
    ]

    discord_content = """[Desktop Entry]
Name=Discord
StartupWMClass=discord
Comment=Discord Anime Edition - Whisper Me a Love Song
GenericName=Internet Messenger
Exec=/usr/bin/discord --no-sandbox %U
Icon=/usr/share/pixmaps/discord.png
Type=Application
Categories=Network;InstantMessaging;
MimeType=x-scheme-handler/discord;
Path=/usr/bin
"""

    panel_content = """[Desktop Entry]
Name=Discord-Chan Studio
Comment=Control Center & Anime Theme Customizer for Discord
Exec=/usr/local/bin/discord-chan-custom
Icon=/usr/share/pixmaps/discord-chan.png
Terminal=false
Type=Application
Categories=Settings;DesktopSettings;GTK;Network;
"""

    for d in desktop_dirs:
        try:
            os.makedirs(d, exist_ok=True)
            
            # Clean up old redundant desktop shortcuts to avoid clutter
            old_theme_editor = os.path.join(d, 'discord-theme-editor.desktop')
            if os.path.exists(old_theme_editor):
                try:
                    os.remove(old_theme_editor)
                except Exception:
                    pass

            dc_path = os.path.join(d, 'discord.desktop')
            with open(dc_path, 'w', encoding='utf-8') as f:
                f.write(discord_content)
            os.chmod(dc_path, 0o755)

            studio_path = os.path.join(d, 'discord-chan-custom.desktop')
            with open(studio_path, 'w', encoding='utf-8') as f:
                f.write(panel_content)
            os.chmod(studio_path, 0o755)
        except Exception:
            pass

    return True

if __name__ == "__main__":
    src = "/root/Downloads/file_0000000068e0820b8bbfefec482b49ef.png"
    if not os.path.exists(src):
        src = "/root/discord-chan/assets/icons/discord-neko.png"
    out = "/root/discord-chan/assets/icons"
    generate_icons(src, out)
    install_system_icons(os.path.join(out, "discord-neko.png"))
    update_desktop_shortcuts()
    print("Icons processed and installed successfully without harsh borders or desktop clutter!")
