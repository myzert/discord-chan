!define PRODUCT_NAME "Discord-Chan Studio"
!define PRODUCT_VERSION "2.6.0"
!define PRODUCT_PUBLISHER "myzert"
!define PRODUCT_WEB_SITE "https://github.com/myzert/discord-chan"
!define PRODUCT_DIR_REGKEY "Software\DiscordChan"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\DiscordChan"

; Use zlib compression to eliminate ML false positives (Trojan:Win32/Wacatac.C!ml)
SetCompressor /SOLID zlib

; Explicit user execution level (no suspicious elevated privilege requests)
RequestExecutionLevel user

; PE Header Version Information (Prevents Antivirus Heuristic & ML scoring)
VIProductVersion "2.6.0.0"
VIAddVersionKey "ProductName" "${PRODUCT_NAME}"
VIAddVersionKey "CompanyName" "${PRODUCT_PUBLISHER}"
VIAddVersionKey "LegalCopyright" "Copyright (C) 2026 myzert. Licensed under GNU General Public License v3.0."
VIAddVersionKey "FileDescription" "Discord-Chan Studio Official Installer"
VIAddVersionKey "FileVersion" "2.6.0.0"
VIAddVersionKey "ProductVersion" "2.6.0.0"
VIAddVersionKey "LegalTrademarks" "GPLv3"
VIAddVersionKey "OriginalFilename" "discord-chan_2.6.0_setup.exe"

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "release/discord-chan_2.6.0_setup.exe"
InstallDir "$LOCALAPPDATA\DiscordChan"
InstallDirRegKey HKCU "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

!include "MUI2.nsh"

!define MUI_ICON "assets/icons/discord-neko.ico"
!define MUI_UNICON "assets/icons/discord-neko.ico"
!define MUI_ABORTWARNING

; Welcome Page
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Uninstaller Pages
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    File /r "assets"
    File /r "desktop"
    File /r "plugins"
    File /r "src"
    File /r "themes"
    File "install.bat"
    File "install.ps1"
    File "setup.py"
    File "discord-chan-studio.py"
    File "LICENSE"
    File "README.md"
    File "README.id.md"

    ; Copy Themes directly to BetterDiscord folder if exists
    CreateDirectory "$APPDATA\BetterDiscord\themes"
    CopyFiles "$INSTDIR\themes\*.theme.css" "$APPDATA\BetterDiscord\themes\"

    ; Copy Plugins (Translator, ReadAllNotifications, Hotkey, BDFDB) directly to BetterDiscord
    CreateDirectory "$APPDATA\BetterDiscord\plugins"
    CopyFiles "$INSTDIR\plugins\*.js" "$APPDATA\BetterDiscord\plugins\"

    ; Create Shortcuts
    CreateShortCut "$DESKTOP\Discord-Chan Studio.lnk" "python.exe" '"$INSTDIR\discord-chan-studio.py"' "$INSTDIR\assets\icons\discord-neko.ico"
    CreateDirectory "$SMPROGRAMS\Discord-Chan"
    CreateShortCut "$SMPROGRAMS\Discord-Chan\Discord-Chan Studio.lnk" "python.exe" '"$INSTDIR\discord-chan-studio.py"' "$INSTDIR\assets\icons\discord-neko.ico"
    CreateShortCut "$SMPROGRAMS\Discord-Chan\Uninstall.lnk" "$INSTDIR\uninst.exe"

    ; Register Uninstaller in Windows Registry (Official App Recognition)
    WriteRegStr HKCU "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "DisplayName" "${PRODUCT_NAME}"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "UninstallString" '"$INSTDIR\uninst.exe"'
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\assets\icons\discord-neko.ico"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
    WriteUninstaller "$INSTDIR\uninst.exe"
SectionEnd

Section "Uninstall"
    RMDir /r "$INSTDIR"
    Delete "$DESKTOP\Discord-Chan Studio.lnk"
    RMDir /r "$SMPROGRAMS\Discord-Chan"
    Delete "$APPDATA\BetterDiscord\themes\WhisperMeALoveSong.theme.css"
    Delete "$APPDATA\BetterDiscord\plugins\DiscordChanStudioHotkey.plugin.js"
    Delete "$APPDATA\BetterDiscord\plugins\Translator.plugin.js"
    Delete "$APPDATA\BetterDiscord\plugins\ReadAllNotificationsButton.plugin.js"
    Delete "$APPDATA\BetterDiscord\plugins\0BDFDB.plugin.js"

    DeleteRegKey HKCU "${PRODUCT_UNINST_KEY}"
    DeleteRegKey HKCU "${PRODUCT_DIR_REGKEY}"
SectionEnd
