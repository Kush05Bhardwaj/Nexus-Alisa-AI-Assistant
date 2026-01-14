# Install Waifu Voice Dependencies
# Run this to get the cute voice working!

Write-Host "=" -NoNewline -ForegroundColor Magenta
Write-Host "=" * 59 -ForegroundColor Magenta
Write-Host "  🎀 Installing Alisa Waifu Voice System 🎀" -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Magenta
Write-Host "=" * 59 -ForegroundColor Magenta

# Activate virtual environment if it exists
if (Test-Path "../venv/Scripts/Activate.ps1") {
    Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
    & ../venv/Scripts/Activate.ps1
} elseif (Test-Path "venv/Scripts/Activate.ps1") {
    & venv/Scripts/Activate.ps1
}

Write-Host "`n📦 Installing voice dependencies..." -ForegroundColor Cyan

# Install the cute voice packages
pip install edge-tts
pip install simpleaudio
pip install soundfile

Write-Host "`n✅ Installation complete!" -ForegroundColor Green
Write-Host "`n🎮 Next steps:" -ForegroundColor Yellow
Write-Host "  1. Test your voice: python test_voice.py" -ForegroundColor White
Write-Host "  2. Customize settings in voice_config.py" -ForegroundColor White
Write-Host "  3. Start chatting: ..\start_text_chat.ps1" -ForegroundColor White
Write-Host "`n🎀 Enjoy your kawaii waifu voice! 🎀`n" -ForegroundColor Magenta
