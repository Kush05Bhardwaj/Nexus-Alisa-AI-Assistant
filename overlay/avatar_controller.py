"""
Avatar Controller - Thread-safe API for controlling avatar
This module provides functions that can be called from other threads (like voice output)
to safely control the avatar animations in the main Tkinter thread.
"""

# Global reference to avatar window (set by main.py)
_avatar_window = None

def set_avatar_window(window):
    """Set the avatar window instance (called by main.py during startup)"""
    global _avatar_window
    _avatar_window = window

def on_speech_start():
    """Called when TTS starts speaking - triggers talking animation"""
    if _avatar_window:
        # Use Tkinter's thread-safe method to schedule in main thread
        _avatar_window.root.after(0, _avatar_window.start_talking)
        print("🎤 Avatar started talking")

def on_speech_end():
    """Called when TTS finishes speaking - stops talking animation"""
    if _avatar_window:
        # Use Tkinter's thread-safe method to schedule in main thread
        _avatar_window.root.after(0, _avatar_window.stop_talking)
        print("🤐 Avatar stopped talking")

def on_emotion(emotion: str):
    """Called when emotion is detected - changes avatar expression (future feature)"""
    print(f"[Avatar Emotion] {emotion}")
