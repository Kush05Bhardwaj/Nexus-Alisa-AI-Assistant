# 🎀 Alisa Waifu Voice Setup Guide

## 🎯 Quick Start - Get Your Cute Tsundere Voice!

### Option 1: RVC Voice (BEST - Actual Waifu Voice!) 🌟

This uses your trained RVC model for authentic anime waifu vibes.

**Requirements:**
```powershell
cd voice
pip install edge-tts simpleaudio soundfile
```

**Test it:**
```powershell
python test_voice.py
```

**Customize:**
1. Edit `voice_config.py`
2. Change `SELECTED_VOICE` to try different base voices:
   - `"ana"` - Young, energetic (RECOMMENDED)
   - `"nanami"` - Japanese, very kawaii!
   - `"xiaoxiao"` - Chinese, sweet and cute
3. Adjust `SPEECH_RATE` and `PITCH_SHIFT` for perfect cuteness

### Option 2: Basic TTS (Fallback)

If RVC isn't working, it will use Windows TTS automatically.

## 🎮 Voice Options Explained

### English Voices (Easy to understand)
- **ana** 🌟 - Young, bright, perfect for tsundere
- **jenny** - Clear, professional (less cute)
- **aria** - Friendly, conversational
- **michelle** - Young adult

### Japanese Voices (Maximum Kawaii! 🎌)
- **nanami** 💖 - Most anime-like, high pitch
- **aoi** - Cute, youthful, gentle

### Chinese Voices (Also Very Cute! 🎎)
- **xiaoxiao** - Sweet, young-sounding
- **xiaoyi** - Cute, friendly

## 🔧 Troubleshooting

### Voice sounds robotic/weird?
- Make sure RVC model is in `rvc/weights/alisa.pth`
- Make sure RVC index is in `rvc/index/alisa.index`
- Try different base voices in `voice_config.py`

### No sound at all?
- Check if `edge-tts` and `simpleaudio` are installed
- Test with: `python test_voice.py`
- Check Windows sound settings

### Want MORE cuteness?
Edit `voice_config.py`:
```python
SPEECH_RATE = "+20%"  # Faster = cuter
PITCH_SHIFT = "+10Hz"  # Higher pitch = more kawaii
```

## 🎀 Pro Tips

1. **Test before committing**: Run `test_voice.py` to hear samples
2. **Mix and match**: Try different base voices with your RVC model
3. **Emotion support**: The system can adjust voice based on Alisa's emotion!
4. **Japanese mode**: Set `SELECTED_VOICE = "nanami"` for full weeb experience

## 💝 Perfect Tsundere Setup

For maximum tsundere waifu energy:
```python
# In voice_config.py
SELECTED_VOICE = "ana"  # Young, energetic
SPEECH_RATE = "+15%"    # Quick, dismissive
PITCH_SHIFT = "+8Hz"    # Slightly high, cute but not too much
```

Happy waifu voice customization! 🎀✨
