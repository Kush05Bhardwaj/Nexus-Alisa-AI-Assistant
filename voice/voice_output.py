import pyttsx3
import sys
from pathlib import Path

# Try to import overlay controller
sys.path.append(str(Path(__file__).parent.parent / "overlay"))
try:
    from avatar_controller import on_speech_start, on_speech_end
except ImportError:
    def on_speech_start():
        pass
    def on_speech_end():
        pass

# Initialize TTS engine
try:
    engine = pyttsx3.init()
    
    # Get available voices
    voices = engine.getProperty('voices')
    
    # Try to find a female voice (usually has "female" in name or higher pitch)
    female_voice = None
    for voice in voices:
        # Look for female voices (Microsoft Zira, Hazel, etc.)
        if 'zira' in voice.name.lower() or 'female' in voice.name.lower():
            female_voice = voice.id
            break
    
    if female_voice:
        engine.setProperty('voice', female_voice)
        print(f"🎀 Using voice: {female_voice}")
    
    # Make it sound cuter/faster
    engine.setProperty("rate", 180)  # Slightly faster
    engine.setProperty("volume", 1.0)  # Full volume
    
except Exception as e:
    print(f"⚠️  TTS initialization warning: {e}")
    engine = None

def speak(text: str):
    """Speak text using pyttsx3 (fallback TTS)"""
    if engine is None:
        print(f"[SPEAK] {text}")
        return
    
    try:
        on_speech_start()
        engine.say(text)
        engine.runAndWait()
        on_speech_end()
    except Exception as e:
        print(f"❌ Speech error: {e}")
        print(f"[SPEAK] {text}")
