import cv2
import numpy as np
from vision_config import CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_FPS, PROCESS_WIDTH, PROCESS_HEIGHT

# Initialize camera with optimized settings
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)

def get_frame(downscale=True):
    """
    Get frame from webcam with optional downscaling for faster processing
    Args:
        downscale: If True, returns a smaller frame for detection
    """
    ret, frame = cap.read()
    if not ret:
        return None
    
    # Downscale for faster processing if requested
    if downscale:
        frame = cv2.resize(frame, (PROCESS_WIDTH, PROCESS_HEIGHT), interpolation=cv2.INTER_LINEAR)
    
    return frame

def release_camera():
    """Release camera resources"""
    global cap
    if cap is not None:
        cap.release()
