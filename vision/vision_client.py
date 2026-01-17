import asyncio
import websockets
from webcam import get_frame
from face_emotion import detect_face_and_emotion, get_detection_mode
from vision_config import DETECTION_INTERVAL, FRAME_SKIP, CURRENT_PRESET
import time

WS_URL = "ws://127.0.0.1:8000/ws/chat"

async def vision_loop():
    """
    Optimized vision system with minimal resource usage
    - Uses lightweight Haar Cascade by default
    - Processes downscaled frames
    - Caches detection results
    - Only sends updates on state changes
    """
    print("=" * 60)
    print("👁️ Alisa Vision System - Starting (Optimized Mode)")
    print("=" * 60)
    print(f"Detection Method: {get_detection_mode()}")
    print(f"Current Preset: {CURRENT_PRESET}")
    print("Optimizations:")
    print(f"  ✓ Downscaled frames for processing")
    print(f"  ✓ Detection caching enabled")
    print(f"  ✓ Frame skipping ({FRAME_SKIP}x)")
    print(f"  ✓ Detection interval: {DETECTION_INTERVAL}s")
    print()
    print("Monitoring:")
    print("  - User presence (face detection)")
    print("  - Attention state (focused/away)")
    print("=" * 60)
    print()
    
    frame_counter = 0
    
    while True:  # Infinite reconnection loop
        try:
            async with websockets.connect(WS_URL) as ws:
                print(f"✅ Connected to backend at {WS_URL}")
                
                last_presence = None
                last_attention = None
                last_emotion = None
                away_time = 0
                focused_time = 0
                
                while True:
                    # Get downscaled frame for faster processing
                    frame = get_frame(downscale=True)
                    if frame is None:
                        await asyncio.sleep(0.5)
                        continue

                    # Skip frames to reduce CPU usage
                    frame_counter += 1
                    if frame_counter % FRAME_SKIP != 0:
                        await asyncio.sleep(0.1)
                        continue

                    # Detect with caching enabled
                    face, emotion, attention = detect_face_and_emotion(frame, use_cache=True)

                    # Track state changes
                    current_time = time.time()
                    
                    # User appeared/disappeared
                    if face != last_presence:
                        if face == "face":
                            print("✅ User detected")
                            await ws.send(f"[VISION_FACE]present")
                        else:
                            print("❌ User left")
                            await ws.send(f"[VISION_FACE]absent")
                            away_time = current_time
                        
                        last_presence = face
                    
                    # Attention state changed
                    if attention != last_attention and face == "face":
                        if attention == "focused":
                            print("👀 User looking at screen")
                            await ws.send(f"[VISION_FACE]focused")
                            focused_time = current_time
                        else:
                            print("😴 User looking away")
                            await ws.send(f"[VISION_FACE]distracted")
                            away_time = current_time
                        
                        last_attention = attention
                    
                    # Emotion changed (if implemented)
                    if emotion != last_emotion and face == "face" and emotion != "neutral":
                        print(f"😊 Emotion detected: {emotion}")
                        await ws.send(f"[VISION_FACE]{emotion}")
                        last_emotion = emotion
                    
                    # Sleep between detections
                    await asyncio.sleep(DETECTION_INTERVAL)
                    
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"\n⚠️ Connection lost: {e}")
            print("🔄 Reconnecting in 2 seconds...")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("🔄 Reconnecting in 2 seconds...")
            await asyncio.sleep(2)

if __name__ == "__main__":
    try:
        asyncio.run(vision_loop())
    except KeyboardInterrupt:
        print("\n\n👋 Vision system stopped")
        # Cleanup
        from webcam import release_camera
        release_camera()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
