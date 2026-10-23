#!/usr/bin/env bash
# ==============================================================================
#  🌸 DISCORD-CHAN CUSTOM: UNINSTALLER
# ==============================================================================

set -e

C_RESET="\033[0m"
C_PINK="\033[1;38;5;211m"
C_GREEN="\033[1;32m"
C_YELLOW="\033[1;33m"

echo -e "${C_PINK}🌸 Mencopot Discord-Chan Custom...${C_RESET}"

USER_HOME="${HOME:-/root}"
BD_THEME="$USER_HOME/.config/BetterDiscord/themes/WhisperMeALoveSong.theme.css"

# 1. Remove theme
if [ -f "$BD_THEME" ]; then
    rm -f "$BD_THEME"
    echo -e "${C_GREEN}✓ File tema dihapus.${C_RESET}"
fi

# 2. Restore original icons
if [ -f "/usr/share/pixmaps/discord.png.orig" ]; then
    mv -f "/usr/share/pixmaps/discord.png.orig" "/usr/share/pixmaps/discord.png"
    echo -e "${C_GREEN}✓ Icon asli Discord dipulihkan.${C_RESET}"
fi

# 3. Remove custom desktop shortcuts
rm -f "$USER_HOME/Desktop/discord-chan-custom.desktop"
rm -f "$USER_HOME/Desktop/discord-theme-editor.desktop"
rm -f /usr/share/applications/discord-chan-custom.desktop
rm -f /usr/share/applications/discord-theme-editor.desktop
rm -f /usr/local/bin/discord-chan-custom
rm -f /usr/local/bin/discord-theme-editor

echo -e "${C_GREEN}✓ Shortcut desktop dan perintah dibersihkan.${C_RESET}"
echo -e "${C_PINK}Selesai. Discord kini kembali ke setelan semula.${C_RESET}"
