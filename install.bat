@echo off
chcp 65001 >nul
title Discord-Chan Custom: Windows Installer
color 0D

echo ======================================================================
echo    🌸 DISCORD-CHAN CUSTOM: WHISPER ME A LOVE SONG (WINDOWS SETUP) 🌸
echo          Minimalist Pink Anime Theme & Studio Control Center
echo ======================================================================
echo.

set "APPDATA_DIR=%APPDATA%"
set "DISCORD_DIR=%APPDATA%\discord"
set "BD_DIR=%APPDATA%\BetterDiscord"
set "THEMES_DIR=%BD_DIR%\themes"
set "SCRIPT_DIR=%~dp0"

echo [1/4] Memeriksa Instalasi Discord...
if not exist "%DISCORD_DIR%" (
    echo [PERINGATAN] Folder Discord tidak ditemukan di %DISCORD_DIR%.
    echo Pastikan Discord sudah terpasang dan pernah dibuka.
) else (
    echo [OK] Discord terdeteksi.
)

echo [2/4] Menyiapkan Folder BetterDiscord...
if not exist "%THEMES_DIR%" mkdir "%THEMES_DIR%"
if not exist "%BD_DIR%\data\stable" mkdir "%BD_DIR%\data\stable"

echo [3/4] Memasang Tema WhisperMeALoveSong.theme.css...
if exist "%SCRIPT_DIR%themes\WhisperMeALoveSong.theme.css" (
    copy /Y "%SCRIPT_DIR%themes\WhisperMeALoveSong.theme.css" "%THEMES_DIR%\" >nul
    echo [OK] File tema berhasil disalin ke %THEMES_DIR%.
) else (
    echo [INFO] Mengunduh tema dari repository...
    powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/myzert/discord-chan/main/themes/WhisperMeALoveSong.theme.css' -OutFile '%THEMES_DIR%\WhisperMeALoveSong.theme.css'"
)

echo [4/4] Mengaktifkan Tema di BetterDiscord...
powershell -Command "$p = '%BD_DIR%\data\stable\themes.json'; $obj = @{}; if (Test-Path $p) { try { $obj = Get-Content $p | ConvertFrom-Json } catch {} }; $obj | Add-Member -Name 'WhisperMeALoveSong' -Value $true -MemberType NoteProperty -Force; $obj | ConvertTo-Json | Set-Content $p"

echo.
echo ======================================================================
echo   🎉 SETUP SELESAI DENGAN SUKSES!
echo   Buka Discord kamu dan nikmati tema Whisper Me a Love Song!
echo ======================================================================
echo.
pause
