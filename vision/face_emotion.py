import cv2
import numpy as np
import time
from vision_config import (
    USE_MEDIAPIPE, USE_DETECTION_CACHE,
    CASCADE_SCALE_FACTOR, CASCADE_MIN_NEIGHBORS, CASCADE_MIN_FACE_SIZE,
    MEDIAPIPE_MIN_CONFIDENCE, MIN_EYES_FOR_FOCUS
)

# Try to use Haar Cascade first (lightweight, built-in to OpenCV)
try:
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    CASCADE_AVAILABLE = True
    print("✅ OpenCV Haar Cascade loaded (lightweight mode)")
except Exception as e:
    CASCADE_AVAILABLE = False
    print(f"⚠️ Haar Cascade not available: {e}")

# MediaPipe as optional enhancement
MEDIAPIPE_AVAILABLE = False

if USE_MEDIAPIPE:
    try:
        import mediapipe as mp
        
        # Use lighter MediaPipe settings
        mp_face_detection = mp.solutions.face_detection.FaceDetection(
            model_selection=0,  # 0 = short-range (faster), 1 = full-range
            min_detection_confidence=MEDIAPIPE_MIN_CONFIDENCE
        )
        
        MEDIAPIPE_AVAILABLE = True
        print("✅ MediaPipe loaded (enhanced mode)")
        
    except Exception as e:
        MEDIAPIPE_AVAILABLE = False
        print(f"⚠️ MediaPipe not available: {e}")

# Cache for reducing redundant processing
last_detection_time = 0
detection_cache = {
    'face': None,
    'emotion': 'neutral',
    'attention': 'unknown',
    'timestamp': 0
}

def detect_face_and_emotion(frame, use_cache=USE_DETECTION_CACHE):
    """
    Optimized face detection with multiple fallback methods
    1. Haar Cascade (lightweight, always available)
    2. MediaPipe (optional, more accurate but heavier)
    
    Args:
        frame: Input image frame
        use_cache: Use cached results if detection was recent (< 0.5s ago)
    
    Returns: (face_present, emotion, attention_state)
    """
    global last_detection_time, detection_cache
    
    current_time = time.time()
    
    # Use cache if enabled and recent
    if use_cache and (current_time - detection_cache['timestamp']) < 0.5:
        return detection_cache['face'], detection_cache['emotion'], detection_cache['attention']
    
    # Method 1: Haar Cascade (Fast and Lightweight)
    if CASCADE_AVAILABLE:
        result = detect_with_cascade(frame)
        if result is not None:
            detection_cache = {
                'face': result[0],
                'emotion': result[1],
                'attention': result[2],
                'timestamp': current_time
            }
            return result
    
    # Method 2: MediaPipe (Optional Enhancement)
    if MEDIAPIPE_AVAILABLE and USE_MEDIAPIPE:
        result = detect_with_mediapipe(frame)
        if result is not None:
            detection_cache = {
                'face': result[0],
                'emotion': result[1],
                'attention': result[2],
                'timestamp': current_time
            }
            return result
    
    # No detection method available
    return None, "neutral", "unknown"

def detect_with_cascade(frame):
    """
    Lightweight detection using Haar Cascade
    Fast and works on CPU without heavy dependencies
    """
    try:
        # Convert to grayscale for faster processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=CASCADE_SCALE_FACTOR,
            minNeighbors=CASCADE_MIN_NEIGHBORS,
            minSize=CASCADE_MIN_FACE_SIZE
        )
        
        if len(faces) == 0:
            return None, "no_face", "away"
        
        # Get the largest face
        largest_face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = largest_face
        
        # Detect eyes to determine attention
        face_roi = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(
            face_roi,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(15, 15)
        )
        
        # If 2 eyes detected, user is likely looking at camera
        attention = "focused" if len(eyes) >= MIN_EYES_FOR_FOCUS else "away"
        
        # Emotion detection can be added here with a lightweight model
        # For now, just return neutral
        emotion = "neutral"
        
        return "face", emotion, attention
        
    except Exception as e:
        print(f"⚠️ Error in cascade detection: {e}")
        return None, "neutral", "unknown"

def detect_with_mediapipe(frame):
    """
    Enhanced detection using MediaPipe (optional)
    More accurate but uses more resources
    """
    try:
        # Convert BGR to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect face
        result = mp_face_detection.process(rgb)

        if not result.detections:
            return None, "no_face", "away"

        # Get detection confidence
        detection = result.detections[0]
        confidence = detection.score[0]
        
        # Simple attention heuristic based on face size
        # Larger face = closer to camera = more likely paying attention
        bbox = detection.location_data.relative_bounding_box
        face_size = bbox.width * bbox.height
        
        attention = "focused" if face_size > 0.15 else "away"
        emotion = "neutral"
        
        return "face", emotion, attention
        
    except Exception as e:
        print(f"⚠️ Error in MediaPipe detection: {e}")
        return None, "neutral", "unknown"

def get_detection_mode():
    """Return current detection mode for debugging"""
    if MEDIAPIPE_AVAILABLE and USE_MEDIAPIPE:
        return "MediaPipe (Enhanced)"
    elif CASCADE_AVAILABLE:
        return "Haar Cascade (Lightweight)"
    else:
        return "None"
