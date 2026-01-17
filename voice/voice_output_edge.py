import asyncio
import edge_tts
import os
import sys
import tempfile
import time
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

async def tts_generate(text, output_file):
    """Generate speech with cute voice using Edge TTS"""
    communicate = edge_tts.Communicate(
        text, 
        VOICE,
        rate=SPEECH_RATE,
        pitch=PITCH_SHIFT
    )
    await communicate.save(output_file)

async def speak_async(text):
    """Async version of speak - use this from async contexts"""
    output_file = None
    try:
        import pygame
        
        # Note: Avatar control is now done via WebSocket, not direct function calls
        # This allows overlay to run in separate process
        
        # Create a unique temporary file for this TTS generation
        fd, output_file = tempfile.mkstemp(suffix='.mp3', prefix='alisa_voice_')
        os.close(fd)  # Close the file descriptor immediately

        # Stop and unload any previous audio to release the file
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        
        # Generate TTS audio to the temporary file
        await tts_generate(text, output_file)

        # Initialize pygame mixer if not already
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Play audio using pygame
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        
        print(f"🎵 Audio playback started (duration tracking enabled)")
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        print(f"🎵 Audio playback finished")
        
        # Unload the music to release the file
        pygame.mixer.music.unload()
        
        # Clean up the temporary file
        if output_file and os.path.exists(output_file):
            try:
                # Small delay to ensure file is fully released
                time.sleep(0.1)
                os.unlink(output_file)
            except Exception as cleanup_error:
                print(f"⚠️ Warning: Could not delete temp file {output_file}: {cleanup_error}")
                
    except Exception as e:
        print(f"⚠️ TTS error: {e}")
        import traceback
        traceback.print_exc()
        print(f"[TEXT] {text}")
        
        # Try to clean up on error
        if output_file and os.path.exists(output_file):
            try:
                os.unlink(output_file)
            except:
                pass

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
