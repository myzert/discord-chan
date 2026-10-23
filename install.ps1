<#
.SYNOPSIS
    Discord-Chan Custom: One-Click Windows PowerShell Installer
    Whisper Me a Love Song (Sasayaku You ni Koi wo Utau) Edition
.DESCRIPTION
    Installs WhisperMeALoveSong minimalist pink theme, BetterDiscord configuration,
    and sets up Discord-Chan on Windows.
#>

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "══════════════════════════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host "  🌸 DISCORD-CHAN CUSTOM: WHISPER ME A LOVE SONG (POWERSHELL SETUP)  " -ForegroundColor White
Write-Host "     Minimalist Pink Anime Theme & Studio Control Center              " -ForegroundColor Cyan
Write-Host "══════════════════════════════════════════════════════════════════════`n" -ForegroundColor Magenta

$AppData = [Environment]::GetFolderPath('ApplicationData')
$DiscordDir = Join-Path $AppData "discord"
$BDDir = Join-Path $AppData "BetterDiscord"
$ThemesDir = Join-Path $BDDir "themes"
$ThemesJson = Join-Path (Join-Path $BDDir "data") "stable\themes.json"

# Step 1: Discord Check
Write-Host "[1/4] Memeriksa Instalasi Discord..." -ForegroundColor Yellow
if (-not (Test-Path $DiscordDir)) {
    Write-Warning "Folder Discord ($DiscordDir) belum ditemukan. Silakan buka Discord sekali terlebih dahulu."
} else {
    Write-Host "  ✓ Discord terdeteksi di $DiscordDir" -ForegroundColor Green
}

# Step 2: BetterDiscord Directories
Write-Host "[2/4] Menyiapkan Folder BetterDiscord..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $ThemesDir | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path $ThemesJson) | Out-Null
Write-Host "  ✓ Folder BetterDiscord siap." -ForegroundColor Green

# Step 3: Copy Theme
Write-Host "[3/4] Memasang Tema WhisperMeALoveSong.theme.css..." -ForegroundColor Yellow
$ThemeDest = Join-Path $ThemesDir "WhisperMeALoveSong.theme.css"
$LocalTheme = Join-Path $PSScriptRoot "themes\WhisperMeALoveSong.theme.css"

if (Test-Path $LocalTheme) {
    Copy-Item -Force $LocalTheme $ThemeDest
    Write-Host "  ✓ Tema disalin dari file lokal." -ForegroundColor Green
} else {
    Write-Host "  • Mengunduh tema dari GitHub..." -ForegroundColor Cyan
    $ThemeUrl = "https://raw.githubusercontent.com/myzert/discord-chan/main/themes/WhisperMeALoveSong.theme.css"
    Invoke-WebRequest -Uri $ThemeUrl -OutFile $ThemeDest
    Write-Host "  ✓ Tema berhasil diunduh." -ForegroundColor Green
}

# Step 4: Enable in BetterDiscord
Write-Host "[4/4] Mengaktifkan Tema di BetterDiscord..." -ForegroundColor Yellow
$Config = @{}
if (Test-Path $ThemesJson) {
    try {
        $Config = Get-Content $ThemesJson -Raw | ConvertFrom-Json -AsHashtable
    } catch {}
}
if (-not $Config) { $Config = @{} }
$Config["WhisperMeALoveSong"] = $true
$Config | ConvertTo-Json | Set-Content $ThemesJson -Encoding UTF8
Write-Host "  ✓ Tema diaktifkan di themes.json." -ForegroundColor Green

Write-Host "`n══════════════════════════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host "  🎉 INSTANT SETUP WINDOWS BERHASIL! Buka Discord kamu sekarang!     " -ForegroundColor Green
Write-Host "══════════════════════════════════════════════════════════════════════`n" -ForegroundColor Magenta
