"""
Test script to verify overlay + voice integration
Run this AFTER starting the overlay to test if voice triggers animations
"""
import sys
import time
from pathlib import Path

# Add voice directory to path
sys.path.append(str(Path(__file__).parent / "voice"))

try:
    from voice_output_edge import speak
    print("✅ Using Edge TTS")
except ImportError:
    try:
        from voice_output import speak
        print("⚠️ Using basic TTS (Edge TTS not available)")
    except ImportError:
        print("❌ No voice output available!")
        sys.exit(1)

print("=" * 60)
print("🎤 Testing Overlay + Voice Integration")
print("=" * 60)
print()
print("Make sure the overlay is running!")
print("You should see the avatar's mouth move when speaking.")
print()

# Test phrases
test_phrases = [
    "Hello! Testing overlay animation.",
    "This should make my mouth move!",
    "Hmph! It's not like I wanted to help you or anything!",
]

for i, phrase in enumerate(test_phrases, 1):
    print(f"\n[Test {i}/{len(test_phrases)}]")
    print(f"Speaking: '{phrase}'")
    
    speak(phrase)
    
    print("✓ Finished speaking")
    
    if i < len(test_phrases):
        time.sleep(1)  # Brief pause between phrases

print("\n" + "=" * 60)
print("🎉 Test complete!")
print("=" * 60)
print()
print("Did you see the avatar's mouth moving?")
print("✅ YES - Integration working perfectly!")
print("❌ NO  - Check if overlay is running and check console for errors")
