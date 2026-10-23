#!/usr/bin/env bash
# ==============================================================================
#  🌸 DISCORD-CHAN: UNIVERSAL AUTO-INSTALLER & INSTANT SETUP
#  Whisper Me a Love Song (Sasayaku You ni Koi wo Utau) Edition
#  Minimalist Pink Anime Theme & Studio Control Center for Linux
#  Repository: https://github.com/myzert/discord-chan.git
# ==============================================================================

set -e

# ANSI Color Codes
C_RESET="\033[0m"
C_PINK="\033[1;38;5;211m"
C_SOFT_PINK="\033[38;5;218m"
C_GREEN="\033[1;32m"
C_YELLOW="\033[1;33m"
C_BLUE="\033[1;34m"
C_CYAN="\033[1;36m"
C_BOLD="\033[1m"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
USER_HOME="${HOME:-/root}"
DISCORD_CONFIG_DIR="$USER_HOME/.config/discord"
BD_DIR="$USER_HOME/.config/BetterDiscord"

print_banner() {
    echo -e "${C_PINK}"
    echo "  ╔══════════════════════════════════════════════════════════════════════╗"
    echo "  ║                                                                      ║"
    echo "  ║     🌸  DISCORD-CHAN: WHISPER ME A LOVE SONG EDITION  🌸             ║"
    echo "  ║        Minimalist Pink Anime Theme & Studio Control Center           ║"
    echo "  ║            Repository: https://github.com/myzert/discord-chan        ║"
    echo "  ║                                                                      ║"
    echo "  ╚══════════════════════════════════════════════════════════════════════╝"
    echo -e "${C_RESET}"
    echo -e "  ${C_GREEN}🛡️ 100% Client-Side CSS Theme (Bukan mod Nitro, aman dari ban & ToS-friendly)${C_RESET}"
    echo ""
}

print_step() {
    echo -e "${C_PINK}❯ ${C_BOLD}$1${C_RESET}"
}

print_success() {
    echo -e "  ${C_GREEN}✓ $1${C_RESET}"
}

print_warning() {
    echo -e "  ${C_YELLOW}⚠ $1${C_RESET}"
}

print_info() {
    echo -e "  ${C_SOFT_PINK}• $1${C_RESET}"
}

print_banner

# Step 1: Check dependencies
print_step "1. Memeriksa Kebutuhan Sistem (Dependencies)..."

MISSING_PKGS=""
for cmd in python3 curl git; do
    if ! command -v "$cmd" &>/dev/null; then
        MISSING_PKGS="$MISSING_PKGS $cmd"
    fi
done

if command -v python3 &>/dev/null; then
    if ! python3 -c "import PIL" &>/dev/null; then
        MISSING_PKGS="$MISSING_PKGS python3-pil"
    fi
    if ! python3 -c "import tkinter" &>/dev/null; then
        MISSING_PKGS="$MISSING_PKGS python3-tk"
    fi
fi

if [ -n "$MISSING_PKGS" ]; then
    print_warning "Paket yang belum terpasang:$MISSING_PKGS"
    if command -v apt-get &>/dev/null; then
        print_info "Memasang dependensi melalui apt..."
        apt-get update -qq && apt-get install -y -qq python3 python3-pil python3-tk curl git || true
    fi
fi
print_success "Dependensi sistem lengkap."

# Step 2: Check Discord installation
print_step "2. Memeriksa Instalasi Discord..."

CORE_FOUND=false
for p in \
    "$DISCORD_CONFIG_DIR"/app-*/modules/discord_desktop_core-*/discord_desktop_core/index.js \
    "$USER_HOME"/.var/app/com.discordapp.Discord/config/discord/app-*/modules/discord_desktop_core-*/discord_desktop_core/index.js \
    /opt/discord/resources/app/discord_desktop_core/index.js; do
    if [ -f "$p" ]; then
        CORE_FOUND=true
        print_success "Discord Core ditemukan di: $p"
        break
    fi
done

if [ "$CORE_FOUND" = false ]; then
    print_warning "Discord belum terpasang atau belum pernah dijalankan."
    print_info "Silakan pasang Discord terlebih dahulu atau jalankan Discord sekali."
fi

# Step 3: Inject BetterDiscord
print_step "3. Menginjeksi BetterDiscord..."
python3 "$SCRIPT_DIR/src/bd_injector.py"
print_success "BetterDiscord berhasil diintegrasikan."

# Step 4: Process & Apply Anime Application Icons
print_step "4. Membuat & Memasang Icon Anime Discord-Chan Neko..."

NEKO_ICON_SRC="/root/Downloads/file_0000000068e0820b8bbfefec482b49ef.png"
if [ ! -f "$NEKO_ICON_SRC" ]; then
    NEKO_ICON_SRC="$SCRIPT_DIR/assets/icons/discord-neko.png"
fi

python3 -c "
import sys, os
sys.path.insert(0, '$SCRIPT_DIR/src')
import icon_manager
src = '$NEKO_ICON_SRC'
out = '$SCRIPT_DIR/assets/icons'
icon_manager.generate_icons(src, out)
icon_manager.install_system_icons(os.path.join(out, 'discord-neko.png'))
icon_manager.update_desktop_shortcuts()
"
print_success "Icon aplikasi Discord dan Studio berhasil diganti dengan Discord-Chan Neko Mascot."

# Step 5: Install & Activate Theme
print_step "5. Membangun & Mengaktifkan Tema Minimalist Pink (No-Lag & Anti-Nabrak)..."
python3 "$SCRIPT_DIR/src/theme_engine.py"
print_success "Tema WhisperMeALoveSong.theme.css berhasil diterapkan."

# Step 6: Install Studio Launcher
print_step "6. Menyiapkan Discord-Chan Studio CLI & Desktop Launcher..."
chmod +x "$SCRIPT_DIR/discord-chan-studio.py" "$SCRIPT_DIR/src/"*.py
ln -sf "$SCRIPT_DIR/discord-chan-studio.py" /usr/local/bin/discord-chan-custom
print_success "Perintah 'discord-chan-custom' aktif secara global."

# Step 7: Apply GPU Anti-Crash Fix for Linux Virtual Displays
print_step "7. Mengoptimalkan Flags Anti-Crash untuk Linux..."
for app_dir in "$DISCORD_CONFIG_DIR"/app-*; do
    if [ -d "$app_dir" ] && [ -f "$app_dir/Discord" ]; then
        if [ ! -f "$app_dir/Discord.real" ]; then
            mv "$app_dir/Discord" "$app_dir/Discord.real"
            cat << 'EOF' > "$app_dir/Discord"
#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$DIR/Discord.real" --no-sandbox --disable-gpu "$@"
EOF
            chmod +x "$app_dir/Discord"
            print_success "Anti-crash wrapper dibuat untuk $app_dir"
        fi
    fi
done

echo ""
echo -e "${C_PINK}══════════════════════════════════════════════════════════════════════${C_RESET}"
echo -e "${C_GREEN}  🎉 INSTANT SETUP SELESAI DENGAN SUKSES! 🎉${C_RESET}"
echo -e "${C_PINK}══════════════════════════════════════════════════════════════════════${C_RESET}"
echo -e "${C_BOLD}Fitur yang telah aktif:${C_RESET}"
echo -e "  🌸 Tema Anime: Whisper Me a Love Song (Sasakoi Yuri Romance)"
echo -e "  ⚡ Zero-Lag Mode: 60 FPS halus tanpa shadow berat atau blur lag"
echo -e "  🎀 Palet Warna: Sakura Soft Pink & Transparansi Kaca (Glass UI)"
echo -e "  🐱 Icon Aplikasi: Discord-Chan Neko Mascot di Desktop & Menu"
echo -e "  🎙️ Voice UI: Translucent tiles & Sakura Pink speaking indicator"
echo -e "  📏 Anti-Nabrak: Jarak bersih (top-spacing) dari panel window atas"
echo -e "  ⌨ Shortcuts: Ctrl+Shift+P (Command Palette), Ctrl+S (Simpan Cepat)"
echo -e "  🎛️ Control Center: Buka dengan ${C_CYAN}discord-chan-custom${C_RESET} atau klik icon di desktop!"
echo ""
