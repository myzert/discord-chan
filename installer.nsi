!define PRODUCT_NAME "Discord-Chan"
!define PRODUCT_VERSION "2.6.0"
!define PRODUCT_PUBLISHER "Discord-Chan Team"
!define PRODUCT_WEB_SITE "https://github.com/myzert/discord-chan"

SetCompressor /SOLID lzma

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "release/discord-chan_2.6.0_setup.exe"
InstallDir "$LOCALAPPDATA\DiscordChan"
ShowInstDetails show

!include "MUI2.nsh"

!define MUI_ICON "assets/icons/discord-neko.ico"
!define MUI_UNICON "assets/icons/discord-neko.ico"

!define MUI_ABORTWARNING

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

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

    ; Copy Theme directly to BetterDiscord folder if exists
    CreateDirectory "$APPDATA\BetterDiscord\themes"
    CopyFiles "$INSTDIR\themes\WhisperMeALoveSong.theme.css" "$APPDATA\BetterDiscord\themes\"

    ; Copy Hotkey Plugin directly to BetterDiscord
    CreateDirectory "$APPDATA\BetterDiscord\plugins"
    CopyFiles "$INSTDIR\plugins\DiscordChanStudioHotkey.plugin.js" "$APPDATA\BetterDiscord\plugins\"

    ; Create Shortcuts
    CreateShortCut "$DESKTOP\Discord-Chan Studio.lnk" "python.exe" '"$INSTDIR\discord-chan-studio.py"' "$INSTDIR\assets\icons\discord-neko.ico"
    CreateDirectory "$SMPROGRAMS\Discord-Chan"
    CreateShortCut "$SMPROGRAMS\Discord-Chan\Discord-Chan Studio.lnk" "python.exe" '"$INSTDIR\discord-chan-studio.py"' "$INSTDIR\assets\icons\discord-neko.ico"
    CreateShortCut "$SMPROGRAMS\Discord-Chan\Uninstall.lnk" "$INSTDIR\uninst.exe"

    WriteUninstaller "$INSTDIR\uninst.exe"
SectionEnd

Section "Uninstall"
    RMDir /r "$INSTDIR"
    Delete "$DESKTOP\Discord-Chan Studio.lnk"
    RMDir /r "$SMPROGRAMS\Discord-Chan"
    Delete "$APPDATA\BetterDiscord\themes\WhisperMeALoveSong.theme.css"
    Delete "$APPDATA\BetterDiscord\plugins\DiscordChanStudioHotkey.plugin.js"
SectionEnd
