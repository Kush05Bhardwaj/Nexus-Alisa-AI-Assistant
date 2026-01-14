"""
Voice Configuration for Alisa
Change these settings to customize your waifu's voice!
"""

# Voice Selection for Edge TTS (used before RVC conversion)
# These are cute/young sounding voices perfect for anime characters

VOICE_OPTIONS = {
    # English Voices (sorted by cuteness factor 😊)
    "ana": "en-US-AnaNeural",           # 🌟 RECOMMENDED - Young, bright, energetic
    "jenny": "en-US-JennyNeural",       # Neural, clear, professional
    "aria": "en-US-AriaNeural",         # Friendly, conversational
    "michelle": "en-US-MichelleNeural", # Young adult, clear
    
    # Japanese Voices (for maximum kawaii 🎌)
    "nanami": "ja-JP-NanamiNeural",     # 💖 Most anime-like, high pitch
    "aoi": "ja-JP-AoiNeural",           # Cute, youthful
    
    # Chinese Voices (also cute options 🎎)
    "xiaoxiao": "zh-CN-XiaoxiaoNeural", # Sweet, young-sounding
    "xiaoyi": "zh-CN-XiaoyiNeural",     # Cute, friendly
}

# 🎀 CHOOSE YOUR WAIFU VOICE HERE 🎀
# Options: "ana", "nanami", "xiaoxiao", "jenny", etc.
SELECTED_VOICE = "ana"  # Change this to try different voices!

# Get the actual voice ID
def get_voice():
    return VOICE_OPTIONS.get(SELECTED_VOICE, VOICE_OPTIONS["ana"])

# TTS Settings
SPEECH_RATE = "+15%"  # Make speech slightly faster/cuter (use +XX% or -XX%)
PITCH_SHIFT = "+10Hz"  # Make voice slightly higher pitched (use +XXHz or -XXHz)

# Advanced: Custom SSML for emotion expression
# You can add prosody changes based on emotion
EMOTION_PROSODY = {
    "happy": {"rate": "+15%", "pitch": "+8Hz"},
    "sad": {"rate": "-10%", "pitch": "-5Hz"},
    "angry": {"rate": "+20%", "pitch": "+10Hz"},
    "neutral": {"rate": "+10%", "pitch": "+5Hz"},
}

def get_prosody(emotion="neutral"):
    """Get prosody settings for an emotion"""
    return EMOTION_PROSODY.get(emotion, EMOTION_PROSODY["neutral"])
