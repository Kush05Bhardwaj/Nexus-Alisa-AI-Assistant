"""
Vision System Performance Test
Tests the optimized vision system and measures performance
"""

import cv2
import time
import psutil
import os
from webcam import get_frame
from face_emotion import detect_face_and_emotion, get_detection_mode
from vision_config import DETECTION_INTERVAL, FRAME_SKIP, CURRENT_PRESET

def get_process_stats():
    """Get current process CPU and memory usage"""
    process = psutil.Process(os.getpid())
    cpu_percent = process.cpu_percent(interval=0.1)
    memory_mb = process.memory_info().rss / 1024 / 1024
    return cpu_percent, memory_mb

def test_vision_performance(duration=30):
    """
    Test vision system performance for specified duration
    
    Args:
        duration: Test duration in seconds (default 30)
    """
    print("=" * 70)
    print("👁️ Vision System Performance Test")
    print("=" * 70)
    print()
    print(f"Configuration:")
    print(f"  Preset: {CURRENT_PRESET}")
    print(f"  Detection Method: {get_detection_mode()}")
    print(f"  Detection Interval: {DETECTION_INTERVAL}s")
    print(f"  Frame Skip: {FRAME_SKIP}x")
    print()
    print(f"Testing for {duration} seconds...")
    print("=" * 70)
    print()
    
    # Warm up
    print("Warming up camera...")
    for i in range(5):
        frame = get_frame(downscale=True)
        if frame is not None:
            detect_face_and_emotion(frame, use_cache=True)
    print("✅ Warm up complete")
    print()
    
    # Collect stats
    frame_count = 0
    detection_count = 0
    face_detected_count = 0
    total_cpu = 0
    total_memory = 0
    measurements = 0
    
    start_time = time.time()
    last_print = start_time
    
    print("🔍 Testing... (Press Ctrl+C to stop early)")
    print()
    
    try:
        while (time.time() - start_time) < duration:
            # Get frame
            frame = get_frame(downscale=True)
            if frame is None:
                continue
            
            frame_count += 1
            
            # Only detect on non-skipped frames
            if frame_count % FRAME_SKIP == 0:
                detection_count += 1
                face, emotion, attention = detect_face_and_emotion(frame, use_cache=True)
                
                if face == "face":
                    face_detected_count += 1
            
            # Measure every second
            if (time.time() - last_print) >= 1.0:
                cpu, mem = get_process_stats()
                total_cpu += cpu
                total_memory += mem
                measurements += 1
                last_print = time.time()
                
                elapsed = int(time.time() - start_time)
                remaining = duration - elapsed
                print(f"  [{elapsed:02d}s] CPU: {cpu:5.1f}% | RAM: {mem:6.1f} MB | "
                      f"Frames: {frame_count:4d} | Detections: {detection_count:3d} | "
                      f"Time left: {remaining:2d}s", end='\r')
            
            time.sleep(0.05)  # Small delay
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Test stopped by user")
    
    # Calculate results
    elapsed = time.time() - start_time
    avg_cpu = total_cpu / measurements if measurements > 0 else 0
    avg_memory = total_memory / measurements if measurements > 0 else 0
    fps = frame_count / elapsed
    detections_per_sec = detection_count / elapsed
    face_detection_rate = (face_detected_count / detection_count * 100) if detection_count > 0 else 0
    
    # Print results
    print("\n")
    print("=" * 70)
    print("📊 Test Results")
    print("=" * 70)
    print()
    print(f"Duration: {elapsed:.1f} seconds")
    print()
    print("Performance:")
    print(f"  Average CPU:    {avg_cpu:6.2f}%")
    print(f"  Average Memory: {avg_memory:6.1f} MB")
    print(f"  Frame Rate:     {fps:6.2f} FPS")
    print(f"  Detection Rate: {detections_per_sec:6.2f} /second")
    print()
    print("Statistics:")
    print(f"  Total Frames:      {frame_count:6d}")
    print(f"  Total Detections:  {detection_count:6d}")
    print(f"  Faces Detected:    {face_detected_count:6d} ({face_detection_rate:.1f}%)")
    print(f"  Frames Skipped:    {frame_count - detection_count:6d}")
    print()
    
    # Performance rating
    print("Performance Rating:")
    if avg_cpu < 10:
        print("  🟢 Excellent - Very low resource usage")
    elif avg_cpu < 20:
        print("  🟡 Good - Acceptable resource usage")
    elif avg_cpu < 30:
        print("  🟠 Fair - Moderate resource usage")
    else:
        print("  🔴 High - Consider optimizing settings")
    
    print()
    
    # Recommendations
    print("Recommendations:")
    if avg_cpu > 20:
        print("  💡 High CPU usage detected:")
        print("     - Try 'ultra_light' preset in vision_config.py")
        print("     - Increase DETECTION_INTERVAL to 2.5 or 3.0")
        print("     - Increase FRAME_SKIP to 3 or 4")
    elif avg_cpu < 5:
        print("  💡 Very low CPU usage - you can enhance accuracy:")
        print("     - Try 'enhanced' preset for better detection")
        print("     - Enable USE_MEDIAPIPE for more accurate tracking")
    else:
        print("  ✅ Performance is well balanced!")
    
    if face_detection_rate < 30 and face_detected_count > 0:
        print("  💡 Low face detection rate:")
        print("     - Ensure good lighting")
        print("     - Face camera directly")
        print("     - Try 'enhanced' preset")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    print()
    print("Vision System Performance Test")
    print("This will test your vision system for 30 seconds")
    print()
    
    choice = input("Run test? (y/n): ").lower()
    if choice == 'y':
        test_vision_performance(duration=30)
    else:
        print("Test cancelled")
