import asyncio
import edge_tts
import os
import sys
from pathlib import Path

# Try to import overlay controller, but make it truly optional
OVERLAY_AVAILABLE = False
try:
    sys.path.append(str(Path(__file__).parent.parent / "overlay"))
    from avatar_controller import on_speech_start, on_speech_end
    OVERLAY_AVAILABLE = True
except ImportError:
    def on_speech_start():
        pass
    def on_speech_end():
        pass

# Import voice configuration
try:
    from voice_config import get_voice, SPEECH_RATE, PITCH_SHIFT
    VOICE = get_voice()
    print(f"🎀 Using voice: {VOICE}")
except ImportError:
    VOICE = "en-US-AnaNeural"  # Fallback to cute voice
    SPEECH_RATE = "+10%"
    PITCH_SHIFT = "+5Hz"

OUTPUT_FILE = "alisa_voice.mp3"

async def tts_generate(text):
    """Generate speech with cute voice using Edge TTS"""
    communicate = edge_tts.Communicate(
        text, 
        VOICE,
        rate=SPEECH_RATE,
        pitch=PITCH_SHIFT
    )
    await communicate.save(OUTPUT_FILE)

async def speak_async(text):
    """Async version of speak - use this from async contexts"""
    try:
        import pygame
        
        # Only call overlay functions if overlay is actually running
        if OVERLAY_AVAILABLE:
            try:
                on_speech_start()
            except:
                pass  # Overlay not running, ignore

        # Stop and unload any previous audio to release the file
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        
        # Generate TTS audio
        await tts_generate(text)

        # Initialize pygame mixer if not already
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Play audio using pygame
        pygame.mixer.music.load(OUTPUT_FILE)
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        # Unload the music to release the file
        pygame.mixer.music.unload()

        # Only call overlay functions if overlay is actually running
        if OVERLAY_AVAILABLE:
            try:
                on_speech_end()
            except:
                pass  # Overlay not running, ignore
                
    except Exception as e:
        print(f"❌ Voice output error: {e}")
        import traceback
        traceback.print_exc()
        print(f"[TEXT] {text}")

def speak(text):
    """Speak text using cute Edge TTS voice - sync wrapper"""
    try:
        # Simple approach: just run in new event loop in thread
        import threading
        
        def run_in_thread():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                new_loop.run_until_complete(speak_async(text))
            finally:
                new_loop.close()
        
        thread = threading.Thread(target=run_in_thread, daemon=True)
        thread.start()
        thread.join()  # Wait for speech to complete
        
    except Exception as e:
        print(f"❌ Voice output error: {e}")
        print(f"[TEXT] {text}")

if __name__ == "__main__":
    # Test the voice
    speak("Hmph! It's not like I wanted to help you or anything, baka!")
