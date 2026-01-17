# 📁 Alisa Codebase Structure

Complete file-by-file documentation of the entire Alisa AI Assistant codebase.

**Last Updated:** January 17, 2026  
**Version:** 3.0 (Phase 10C Complete)

---

## 📋 Table of Contents

- [Project Root](#project-root)
- [Backend Module](#backend-module)
- [Overlay Module](#overlay-module)
- [Voice Module](#voice-module)
- [Vision Module](#vision-module)
- [Scripts Module](#scripts-module)
- [Documentation](#documentation)

---

## 🏠 Project Root

```
Alisa-AI Assistant/
├── README.md                               # Main project documentation
├── LICENSE                                 # Project license
├── DOCUMENTATION_UPDATE_2026-01-17.md     # Latest update notes
├── FINAL_DOCUMENTATION_SUMMARY.md         # Documentation summary
├── VERIFICATION_COMPLETE.md               # Verification status
├── backend/                               # Backend server module
├── overlay/                               # Avatar overlay module
├── voice/                                 # Voice I/O module
├── vision/                                # Vision detection module
├── scripts/                               # Startup scripts
└── docs/                                  # Documentation
```

### Root Files

#### `README.md`
**Purpose:** Main project overview and quick start guide  
**Contents:**
- Project description
- Features overview
- Quick start guide
- Architecture overview
- Module descriptions
- Setup instructions
- Contributing guide

#### `LICENSE`
**Purpose:** Project licensing information  
**Type:** [License Type]

#### `DOCUMENTATION_UPDATE_2026-01-17.md`
**Purpose:** Latest documentation update log  
**Contents:**
- Changes made
- Files updated
- New features documented

#### `FINAL_DOCUMENTATION_SUMMARY.md`
**Purpose:** Comprehensive documentation summary  
**Contents:**
- All modules documented
- Feature completion status
- Known issues

#### `VERIFICATION_COMPLETE.md`
**Purpose:** Verification checklist  
**Contents:**
- Tested features
- Verification status
- Known limitations

---

## 🔧 Backend Module

**Location:** `backend/`  
**Purpose:** Central server handling LLM, memory, and coordination  
**Technology:** FastAPI, SQLAlchemy, asyncio

### Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── ws.py
│   ├── llm_client.py
│   ├── memory.py
│   ├── memory_long.py
│   ├── emotion.py
│   ├── modes.py
│   ├── prompt.py
│   ├── idle_companion.py
│   ├── desktop_actions.py
│   ├── task_memory.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   └── __pycache__/
├── alisa_memory.db
├── requirements.txt
└── README.md
```

### Files

#### `app/__init__.py`
**Purpose:** Package initialization  
**Contents:** Empty (marks directory as Python package)

#### `app/main.py`
**Purpose:** FastAPI application entry point  
**Key Components:**
```python
app = FastAPI()  # Main app instance
startup_event()  # Database initialization
shutdown_event()  # Cleanup
health_check()   # GET /
history_summary()  # GET /history/summary
clear_history()  # POST /history/clear
```
**Dependencies:** FastAPI, CORS middleware  
**Lines:** ~60

#### `app/ws.py`
**Purpose:** WebSocket handler and idle thought engine  
**Key Components:**
```python
connected_clients: List[WebSocket]  # Active connections
vision_state: Dict  # Vision system state
broadcast_message()  # Send to all clients
trigger_idle_response()  # Phase 9B idle thoughts
idle_thought_loop()  # Background task (30s interval)
chat_endpoint()  # WebSocket /ws/chat
```
**Dependencies:** websockets, llm_client, memory, idle_companion, desktop_actions, task_memory  
**Lines:** ~834

#### `app/llm_client.py`
**Purpose:** LLM streaming integration  
**Key Components:**
```python
LLM_URL = "http://127.0.0.1:8080/v1/chat/completions"

async def stream_llm_response(messages):
    # HTTP streaming with httpx
    # Yields tokens one by one
    # Returns generator
```
**Dependencies:** httpx  
**Lines:** ~30

#### `app/memory.py`
**Purpose:** Short-term in-memory conversation buffer  
**Key Components:**
```python
class MemoryBuffer:
    max_turns: int = 10
    max_tokens: int = 3000
    session_id: str
    messages: List[Dict]
    
    _load_from_db()  # Load on init
    add(role, content)  # Add + persist
    _trim_by_tokens()  # Auto-trim
    get()  # Return messages
    clear()  # Reset buffer
```
**Dependencies:** db, models, datetime  
**Lines:** ~104

#### `app/memory_long.py`
**Purpose:** SQLite persistent storage  
**Key Components:**
```python
def save_memory(emotion, content):
    # Save to database
    
def fetch_recent_memories(limit=10):
    # Query recent entries
    # Return as formatted string
    
def clear_history():
    # Delete all entries
```
**Dependencies:** db, models  
**Lines:** ~50

#### `app/emotion.py`
**Purpose:** Extract emotion tags from LLM output  
**Key Components:**
```python
def extract_emotion(text: str) -> Tuple[str, str]:
    # Pattern 1: <emotion=name>text
    # Pattern 2: emotion word at start
    # Pattern 3: Broken (just emotion word)
    # Fallback: neutral
    # Returns: (emotion, clean_text)
```
**Valid Emotions:** teasing, calm, serious, happy, sad, neutral  
**Lines:** ~44

#### `app/modes.py`
**Purpose:** Conversation mode management  
**Key Components:**
```python
MODES = {
    "teasing": "You tease gently and act playful.",
    "serious": "You are calm, mature, and direct.",
    "calm": "You speak softly and reassuringly."
}

current_mode = "teasing"

def set_mode(mode): ...
def get_mode_prompt(): ...
```
**Lines:** ~12

#### `app/prompt.py`
**Purpose:** System prompt and personality definition  
**Key Components:**
```python
SYSTEM_PROMPT = """
Your name is Alisa.
[Comprehensive personality definition]
- Tsundere girlfriend character
- Emotional behavior rules
- Speech style guidelines
- Idle behavior rules
- Output constraints
- Emotion tagging instructions
"""

def build_prompt(mode_prompt, memories, vision_context=""):
    # Combine system + mode + memories + vision
    # Return complete prompt
```
**Lines:** ~199

#### `app/idle_companion.py`
**Purpose:** Phase 9B - Spontaneous behavior system  
**Key Components:**
```python
class IdleCompanionSystem:
    last_spontaneous_speech: float
    silence_start: float
    companion_mode_active: bool
    
    MIN_SILENCE_FOR_SPEECH = {
        "short": 120,    # 2 min
        "medium": 300,   # 5 min
        "long": 600,     # 10 min
        "very_long": 1800  # 30 min
    }
    
    BASE_PROBABILITY = {
        "short": 0.08,
        "medium": 0.15,
        "long": 0.25,
        "very_long": 0.40
    }
    
    should_speak_spontaneously()  # Decision logic
    build_companion_prompt()  # Context-aware prompt
    get_silence_category()  # Categorize silence
```
**Lines:** ~365

#### `app/desktop_actions.py`
**Purpose:** Phase 10B - Desktop automation system  
**Key Components:**
```python
class DesktopActionsSystem:
    app_paths: Dict  # Common app paths
    pending_action: Optional[Dict]
    actions_this_session: List
    
    # Action methods
    open_app(app_name)
    close_app(app_name)
    browser_tab(action, url)
    type_text(text)
    press_key(key)
    click(x, y)
    scroll(direction, amount)
    read_file(path)
    write_note(content, path)
    
    # Safety
    is_action_safe(action_type, params)
    # Command blacklist
    # Path restrictions
    # Rate limiting
```
**Dependencies:** pyautogui, psutil, subprocess  
**Lines:** ~509

#### `app/task_memory.py`
**Purpose:** Phase 10C - Habit learning system  
**Key Components:**
```python
class TaskMemorySystem:
    storage_path: Path
    work_schedule: Dict  # hour → timestamps
    app_usage: Dict  # task → app → count
    silence_preferences: Dict  # hour → durations
    repeated_tasks: Dict  # task → count
    task_sequences: List
    
    # Observation
    observe_activity(activity_type, context)
    observe_silence(duration_minutes)
    
    # Analysis
    analyze_work_schedule()
    detect_silence_patterns()
    identify_task_sequences()
    
    # Decision
    should_interrupt_now()  # Based on patterns
    get_typical_work_hours()
    
    # Persistence
    save_memory()
    load_memory()
```
**Dependencies:** json, time, datetime, collections  
**Lines:** ~438

#### `app/db.py`
**Purpose:** Database configuration  
**Key Components:**
```python
DATABASE_URL = "sqlite:///alisa_memory.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```
**Lines:** ~7

#### `app/models.py`
**Purpose:** SQLAlchemy ORM models  
**Key Components:**
```python
class Memory(Base):
    __tablename__ = "memory"
    id: Integer (PK)
    emotion: String
    content: Text

class ConversationHistory(Base):
    __tablename__ = "conversation_history"
    id: Integer (PK, indexed)
    role: String (user/assistant)
    content: Text
    timestamp: DateTime
    session_id: String
```
**Lines:** ~19

#### `app/schemas.py`
**Purpose:** Pydantic validation schemas  
**Key Components:**
```python
class MessageRequest(BaseModel):
    message: str

class HistorySummary(BaseModel):
    messages: int
    turns: int
    estimated_tokens: int
    session_id: str
```
**Lines:** ~15

#### `alisa_memory.db`
**Purpose:** SQLite database file (auto-created)  
**Schema:** See models.py  
**Size:** Grows with conversation history

#### `requirements.txt`
**Purpose:** Python dependencies  
**Contents:**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
websockets==12.0
aiohttp==3.9.1
pydantic==2.5.0
python-multipart==0.0.6
httpx
python-dotenv
pyautogui
psutil
```

#### `README.md`
**Purpose:** Backend module documentation  
**Sections:**
- Overview
- Quick start
- Structure
- API endpoints
- WebSocket protocol
- Memory system
- Phase 9B/10A/10B/10C documentation
- Configuration
- Troubleshooting
**Lines:** 681

---

## 🎭 Overlay Module

**Location:** `overlay/`  
**Purpose:** Animated avatar window with emotions  
**Technology:** Tkinter, PIL, WebSocket

### Structure

```
overlay/
├── main.py
├── avatar_window.py
├── avatar_controller.py
├── check_images.py
├── test_animations.py
├── assets/
│   ├── base.png
│   ├── happy.png
│   ├── teasing.png
│   ├── serious.png
│   ├── calm.png
│   ├── sad.png
│   ├── eyes_closed.png
│   └── mouth_open.png
├── requirements.txt
└── README.md
```

### Files

#### `main.py`
**Purpose:** Entry point and WebSocket client  
**Key Components:**
```python
class AvatarApp:
    ws_task: Optional[Task]
    loop: Optional[EventLoop]
    
    safe_start_talking()  # Thread-safe
    safe_stop_talking()
    safe_on_emotion(emotion)
    
    listen_to_backend()  # Async WebSocket listener
    start_websocket_thread()  # Background thread
    run()  # Main entry point
```
**Message Handling:**
- `[SPEECH_START]` → Start mouth animation
- `[SPEECH_END]` → Stop mouth animation
- `[EMOTION]name` → Change facial expression
- `[END]` → Ignored
- Tokens → Ignored
**Lines:** ~133

#### `avatar_window.py`
**Purpose:** Tkinter UI and animation logic  
**Key Components:**
```python
# Global state
faces: Dict[str, ImageTk]  # Loaded emotion images
current_face: str = "neutral"
is_talking: bool = False
is_blinking: bool = False
talking_timeout_id: Optional[str]

# Window config
WINDOW_SIZE = 400
root: Tk
canvas: Canvas
base_layer: int  # Canvas image ID
overlay_layer: int

# Functions
initialize()  # Create window, load images
animate_blink()  # 3s interval, 150ms duration
animate_mouth()  # 500ms cycle when talking
set_emotion(emotion)  # Switch base image
start_talking()  # Set flag, start animation
stop_talking()  # Clear flag, return to neutral
run()  # Main loop
```
**Animations:**
- Blinking: Every 3 seconds, pauses during talking
- Talking: 200ms open, 300ms closed, loops
- Safety: 30-second auto-timeout
**Lines:** ~204

#### `avatar_controller.py`
**Purpose:** Thread-safe API for external control  
**Key Components:**
```python
_last_emotion: str = "neutral"

def on_speech_start():
    start_talking()

def on_speech_end():
    stop_talking()

def on_emotion(emotion: str):
    # Track and set emotion
    set_emotion(emotion)
```
**Usage:** Import from voice modules for direct control  
**Lines:** ~27

#### `check_images.py`
**Purpose:** Verify asset integrity  
**Key Components:**
```python
def check_image(name):
    # Load image
    # Check mode (RGBA)
    # Check transparency
    # Check visible content
    # Print report
```
**Usage:** `python check_images.py`  
**Lines:** ~28

#### `test_animations.py`
**Purpose:** Manual animation testing  
**Key Components:**
```python
def test_emotions():
    # Cycle through all 6 emotions (2s each)

def test_talking():
    # Test mouth animation (5s)

def run_tests():
    # Schedule and run all tests
```
**Usage:** `python test_animations.py`  
**Lines:** ~52

#### `assets/` Directory
**Purpose:** Avatar image assets  
**Format:** PNG with RGBA (transparency)  
**Size:** 400x400 pixels (recommended)

**Files:**
- `base.png` - Neutral expression (default)
- `happy.png` - Happy/cheerful expression
- `teasing.png` - Playful/mischievous expression
- `serious.png` - Focused/mature expression
- `calm.png` - Peaceful/relaxed expression
- `sad.png` - Sad/empathetic expression
- `eyes_closed.png` - Blinking overlay (aligned to eyes)
- `mouth_open.png` - Talking overlay (aligned to mouth)

#### `requirements.txt`
**Contents:**
```
pillow>=10.0.0
websockets>=12.0
```

#### `README.md`
**Purpose:** Overlay module documentation  
**Sections:**
- Overview
- Quick start
- Emotion system
- Animation system
- WebSocket protocol
- Thread-safe architecture
- Customization
- Troubleshooting
**Lines:** 663

---

## 🎙️ Voice Module

**Location:** `voice/`  
**Purpose:** Speech recognition and synthesis  
**Technology:** Faster Whisper, Edge TTS, PyGame

### Structure

```
voice/
├── text_chat.py
├── voice_chat_optimized.py
├── voice_input.py
├── voice_output_edge.py
├── voice_output_rvc.py
├── voice_config.py
├── install_voice.ps1
├── rvc/
│   ├── inferencer.py
│   ├── weights/
│   └── index/
├── requirements.txt
└── README.md
```

### Files

#### `text_chat.py`
**Purpose:** Text input + voice output interface  
**Key Components:**
```python
WS_URL = "ws://127.0.0.1:8000/ws/chat"
VOICE = get_voice()  # From config
SPEECH_RATE = "+10%"
PITCH_SHIFT = "+5Hz"

async def speak_with_timing(text, ws):
    # Generate TTS to temp file
    # Load into PyGame
    # Start playback
    # Send [SPEECH_START]
    # Wait for completion
    # Send [SPEECH_END]
    # Cleanup temp file

def clean_text_for_speech(text: str):
    # Remove <emotion=> tags
    # Remove standalone emotion words
    # Clean whitespace
    # Return clean text

async def text_chat():
    # Connect WebSocket
    # Read user input
    # Send to backend
    # Collect response tokens
    # Extract emotion
    # Clean text
    # Speak with timing
    # Loop
```
**Features:**
- Precise timing sync with overlay
- Emotion text cleaning
- Temporary file cleanup
- Error handling
**Lines:** ~255

#### `voice_chat_optimized.py`
**Purpose:** Full voice conversation interface  
**Key Components:**
```python
EMOTION_EMOJI = {
    'happy': '😊',
    'calm': '😌',
    'teasing': '😏',
    # ...
}

async def speak_with_timing(text, ws):
    # Same as text_chat.py
    # Generate → Play → Signal

async def listen_for_messages(ws):
    # Background task
    # Collect full message
    # Display with emoji
    # Speak response

async def voice_input_loop(ws):
    # Wait for Enter press
    # Record audio
    # Transcribe
    # Send to backend

async def voice_chat():
    # Connect WebSocket
    # Start message listener (background)
    # Run voice input loop
    # Handle exit
```
**Features:**
- Press-to-talk (Enter key)
- Clean console output (no token spam)
- Emotion emoji display
- Continuous conversation
**Lines:** ~270

#### `voice_input.py`
**Purpose:** Speech-to-text using Faster Whisper  
**Key Components:**
```python
SAMPLE_RATE = 16000
DURATION = 5  # seconds
model = WhisperModel("small", device="cpu", compute_type="int8")

def record_audio():
    # Capture from mic using sounddevice
    # Save to input.wav

def speech_to_text():
    # Transcribe with Faster Whisper
    # Return text
```
**Configuration:**
- Model size: small (base/medium/large available)
- Device: cpu (cuda for GPU)
- Compute type: int8 (float16 for GPU)
**Lines:** ~29

#### `voice_output_edge.py`
**Purpose:** Text-to-speech using Edge TTS (default)  
**Key Components:**
```python
VOICE = get_voice()  # From voice_config
SPEECH_RATE = "+10%"
PITCH_SHIFT = "+5Hz"

async def tts_generate(text, output_file):
    # Generate speech with Edge TTS
    # Save to file

async def speak_async(text):
    # Create temp file
    # Generate TTS
    # Play with PyGame
    # Cleanup temp file

def speak(text):
    # Sync wrapper
    # Run in new thread
```
**Features:**
- Temporary file management
- Overlay integration (optional)
- Error handling
- Thread-safe
**Lines:** ~123

#### `voice_output_rvc.py`
**Purpose:** TTS + RVC voice conversion (advanced)  
**Key Components:**
```python
from rvc.inferencer import convert

BASE_WAV = "base.wav"
RVC_WAV = "alisa.wav"

async def tts_base(text):
    # Generate with Edge TTS
    # Save to base.wav

async def speak_async(text):
    # Generate base TTS
    # Convert with RVC
    # Play with PyGame

def speak(text):
    # Sync wrapper
```
**Requirements:**
- RVC model (.pth)
- Feature index (.index)
- PyTorch
**Lines:** ~105

#### `voice_config.py`
**Purpose:** Voice customization settings  
**Key Components:**
```python
VOICE_OPTIONS = {
    "ana": "en-US-AnaNeural",  # Recommended
    "jenny": "en-US-JennyNeural",
    "nanami": "ja-JP-NanamiNeural",
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",
    # ...
}

SELECTED_VOICE = "ana"
SPEECH_RATE = "+15%"
PITCH_SHIFT = "+10Hz"

EMOTION_PROSODY = {
    "happy": {"rate": "+15%", "pitch": "+8Hz"},
    "sad": {"rate": "-10%", "pitch": "-5Hz"},
    # ...
}

def get_voice():
    return VOICE_OPTIONS[SELECTED_VOICE]

def get_prosody(emotion="neutral"):
    return EMOTION_PROSODY[emotion]
```
**Lines:** ~47

#### `install_voice.ps1`
**Purpose:** Automated dependency installer  
**Contents:**
```powershell
# Activate venv if exists
# Install edge-tts
# Install simpleaudio
# Install soundfile
# Show next steps
```
**Lines:** ~33

#### `rvc/inferencer.py`
**Purpose:** RVC conversion wrapper  
**Key Components:**
```python
RVC_PATH = "rvc"
MODEL_PATH = "rvc/weights/alisa.pth"
INDEX_PATH = "rvc/index/alisa.index"

def convert(input_wav, output_wav):
    # Run RVC inference
    # subprocess.run() to call RVC script
```
**Lines:** ~14

#### `rvc/weights/` Directory
**Purpose:** Store RVC model weights (.pth files)  
**Contents:** User-provided or trained models

#### `rvc/index/` Directory
**Purpose:** Store RVC feature indices (.index files)  
**Contents:** User-provided or trained indices

#### `requirements.txt`
**Contents:**
```
edge-tts>=6.1.0
soundfile>=0.12.0
simpleaudio>=1.0.4
librosa>=0.10.0
numpy>=1.24.0
sounddevice>=0.4.0
scipy>=1.10.0
faster-whisper>=0.10.0
pyttsx3>=2.90
pygame>=2.5.0
```

#### `README.md`
**Purpose:** Voice module documentation  
**Sections:**
- Overview
- Quick start
- Speech-to-text (Faster Whisper)
- Text-to-speech (Edge TTS)
- RVC voice conversion
- Chat interfaces
- Overlay integration
- Emotion processing
- Configuration
- Troubleshooting
**Lines:** 956

---

## 👁️ Vision Module

**Location:** `vision/`  
**Purpose:** Presence detection and screen analysis  
**Technology:** OpenCV, MediaPipe, mss, Tesseract

### Structure

```
vision/
├── vision_client.py
├── vision_client_screen.py
├── webcam.py
├── face_emotion.py
├── screen_capture.py
├── screen_analyze.py
├── desktop_understanding.py
├── vision_config.py
├── test_vision_performance.py
├── requirements.txt
└── README.md
```

### Files

#### `vision_client.py`
**Purpose:** Webcam presence detection (lightweight)  
**Key Components:**
```python
WS_URL = "ws://127.0.0.1:8000/ws/chat"

async def vision_loop():
    # Connect to backend
    # Loop:
    #   - Get downscaled frame
    #   - Skip frames (performance)
    #   - Detect face/emotion/attention
    #   - Track state changes
    #   - Send updates: [VISION_FACE]state
    #   - Sleep DETECTION_INTERVAL
    # Auto-reconnect on disconnect
```
**Messages Sent:**
- `[VISION_FACE]present` - Face detected
- `[VISION_FACE]absent` - No face
- `[VISION_FACE]focused` - Looking at screen
- `[VISION_FACE]distracted` - Looking away
**Lines:** ~128

#### `vision_client_screen.py`
**Purpose:** Full vision + desktop understanding  
**Key Components:**
```python
SCREEN_CAPTURE_INTERVAL = 10  # seconds
MIN_SCREEN_CAPTURE_INTERVAL = 10

async def vision_with_screen_loop():
    # Initialize webcam
    # Connect to backend
    # Loop:
    #   - Capture webcam frame
    #   - Detect face/attention
    #   - Send presence updates
    #   
    #   - Periodic screen capture (10s)
    #   - Analyze screen (OCR + window)
    #   - Desktop understanding analysis
    #   - Send: [VISION_DESKTOP]context
    # Auto-reconnect
```
**Message Format:**
```
[VISION_DESKTOP]task|app|file_type|has_error|offer|window|text
```
**Lines:** ~158

#### `webcam.py`
**Purpose:** Webcam capture and frame processing  
**Key Components:**
```python
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)

def get_frame(downscale=True):
    # Capture frame
    # Optionally downscale to PROCESS_WIDTH x PROCESS_HEIGHT
    # Return numpy array

def release_camera():
    # Cleanup
```
**Configuration:** See vision_config.py  
**Lines:** ~27

#### `face_emotion.py`
**Purpose:** Face and eye detection  
**Key Components:**
```python
# Haar Cascade (lightweight, default)
face_cascade = cv2.CascadeClassifier(...)
eye_cascade = cv2.CascadeClassifier(...)

# MediaPipe (optional, better accuracy)
mp_face_detection = mp.solutions.face_detection.FaceDetection(...)

# Detection cache (0.5s TTL)
detection_cache = {'face': None, 'emotion': 'neutral', ...}

def detect_face_and_emotion(frame, use_cache=True):
    # Check cache if enabled
    # Try Haar Cascade first (fast)
    # Fallback to MediaPipe if enabled
    # Return: (face_present, emotion, attention_state)

def detect_with_cascade(frame):
    # Convert to grayscale
    # Detect faces
    # Detect eyes in face ROI
    # Return: ("face", "neutral", "focused"/"away")

def detect_with_mediapipe(frame):
    # Convert to RGB
    # Detect with MediaPipe
    # Analyze landmarks
    # Return: (face, emotion, attention)
```
**Lines:** ~183

#### `screen_capture.py`
**Purpose:** Screenshot capture using mss  
**Key Components:**
```python
import mss

sct = mss.mss()

def capture_screen():
    monitor = sct.monitors[1]  # Primary monitor
    img = sct.grab(monitor)
    return np.array(img)
```
**Performance:** ~50-100ms  
**Lines:** ~8

#### `screen_analyze.py`
**Purpose:** OCR and window detection  
**Key Components:**
```python
import pytesseract
import win32gui

def get_active_window():
    # Get foreground window title
    return win32gui.GetWindowText(...)

def analyze_screen(frame):
    # Convert to grayscale
    # Run OCR with Tesseract
    # Get active window
    # Return: {"window": title, "text": text[:300]}
```
**Lines:** ~15

#### `desktop_understanding.py`
**Purpose:** Phase 10A - Context analysis system  
**Key Components:**
```python
class DesktopUnderstandingSystem:
    app_categories: Dict  # 8 categories
    error_patterns: List  # 12+ patterns
    file_extensions: Dict  # 20+ extensions
    
    last_screen_context: Dict
    last_offer_time: float
    
    analyze_screen_context(window_title, screen_text):
        # Detect app type (8 categories)
        # Detect file type (5 categories)
        # Detect errors (12+ patterns)
        # Infer task (12 types)
        # Build context summary
        # Decide if should offer help
        # Return complete analysis
    
    _detect_app_type()
    _detect_file_type()
    _detect_errors()
    _infer_task()
    _should_offer_help()
    _build_context_summary()
```
**Categories:**
- Apps: code, browser, terminal, document, pdf, media, communication
- Files: code, web, data, doc, config
- Tasks: coding_python, coding_js, browsing, debugging, etc.
**Lines:** ~351

#### `vision_config.py`
**Purpose:** Performance presets and settings  
**Key Components:**
```python
# Detection method
USE_MEDIAPIPE = False  # True for enhanced

# Performance
DETECTION_INTERVAL = 1.5  # seconds
FRAME_SKIP = 2
USE_DETECTION_CACHE = True

# Camera
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 15
PROCESS_WIDTH = 320
PROCESS_HEIGHT = 240

# Thresholds
CASCADE_SCALE_FACTOR = 1.2
CASCADE_MIN_NEIGHBORS = 4
CASCADE_MIN_FACE_SIZE = (40, 40)
MEDIAPIPE_MIN_CONFIDENCE = 0.7
MIN_EYES_FOR_FOCUS = 2

# Presets
def apply_preset(preset_name):
    # "ultra_light" - Minimal CPU
    # "balanced" - Default
    # "enhanced" - Better accuracy

CURRENT_PRESET = "balanced"
```
**Lines:** ~88

#### `test_vision_performance.py`
**Purpose:** Performance benchmarking tool  
**Key Components:**
```python
def get_process_stats():
    # CPU and memory usage

def test_vision_performance(duration=30):
    # Warm up camera
    # Run for specified duration
    # Collect metrics:
    #   - Frame count
    #   - Detection count
    #   - Face detected count
    #   - CPU usage
    #   - Memory usage
    #   - Detection time
    # Print summary report
```
**Usage:** `python test_vision_performance.py`  
**Lines:** ~177

#### `requirements.txt`
**Contents:**
```
opencv-python>=4.8.0
mediapipe==0.10.9
numpy>=1.24.0
websockets>=11.0
mss>=9.0.0
pytesseract>=0.3.10
pywin32>=306
Pillow>=10.0.0
psutil>=5.9.0
```

#### `README.md`
**Purpose:** Vision module documentation  
**Sections:**
- Overview
- Quick start
- Presence detection
- Screen analysis
- Desktop understanding (Phase 10A)
- Configuration (presets)
- Troubleshooting
- Performance metrics
**Lines:** 894

---

## 🚀 Scripts Module

**Location:** `scripts/`  
**Purpose:** Startup scripts for different configurations  
**Technology:** PowerShell

### Structure

```
scripts/
├── start_backend.ps1
├── start_overlay.ps1
├── start_text_chat.ps1
├── start_voice_chat.ps1
├── start_voice.ps1
├── start_vision.ps1
├── start_vision_screen.ps1
├── start_phase10a.ps1
├── start_phase10b.ps1
├── start_phase10c.ps1
├── test_idle_system.py
├── test_phase10b.py
├── test_phase10c.py
├── view_history.py
└── README.md
```

### Files

#### `start_backend.ps1`
**Purpose:** Start backend server  
**Actions:**
```powershell
# Navigate to backend/
# Activate venv
# Start: uvicorn backend.app.main:app --reload
```
**Lines:** ~15

#### `start_overlay.ps1`
**Purpose:** Start avatar overlay  
**Actions:**
```powershell
# Navigate to overlay/
# Start: python main.py
```
**Lines:** ~10

#### `start_text_chat.ps1`
**Purpose:** Start text chat interface  
**Actions:**
```powershell
# Navigate to voice/
# Start: python text_chat.py
```
**Lines:** ~10

#### `start_voice_chat.ps1`
**Purpose:** Start voice chat interface  
**Actions:**
```powershell
# Navigate to voice/
# Start: python voice_chat_optimized.py
```
**Lines:** ~10

#### `start_voice.ps1`
**Purpose:** Alias for start_voice_chat.ps1  
**Lines:** ~10

#### `start_vision.ps1`
**Purpose:** Start webcam presence detection  
**Actions:**
```powershell
# Navigate to vision/
# Start: python vision_client.py
```
**Lines:** ~10

#### `start_vision_screen.ps1`
**Purpose:** Start full vision with screen analysis  
**Actions:**
```powershell
# Navigate to vision/
# Start: python vision_client_screen.py
```
**Lines:** ~10

#### `start_phase10a.ps1`
**Purpose:** Start all modules for Phase 10A  
**Actions:**
```powershell
# Start backend
# Start overlay
# Start vision (screen)
# Start text chat
```
**Lines:** ~20

#### `start_phase10b.ps1`
**Purpose:** Start with desktop actions enabled  
**Actions:**
```powershell
# Same as Phase 10A
# Desktop actions already in backend
```
**Lines:** ~20

#### `start_phase10c.ps1`
**Purpose:** Start with task memory enabled  
**Actions:**
```powershell
# Same as Phase 10B
# Task memory already in backend
```
**Lines:** ~20

#### `test_idle_system.py`
**Purpose:** Test idle thought system  
**Key Components:**
```python
# Test idle companion timing
# Test probability calculations
# Test context generation
```
**Usage:** `python test_idle_system.py`  
**Lines:** ~50

#### `test_phase10b.py`
**Purpose:** Test desktop actions  
**Key Components:**
```python
# Test action parsing
# Test safety checks
# Test execution
```
**Usage:** `python test_phase10b.py`  
**Lines:** ~50

#### `test_phase10c.py`
**Purpose:** Test task memory  
**Key Components:**
```python
# Test pattern detection
# Test learning
# Test interrupt decisions
```
**Usage:** `python test_phase10c.py`  
**Lines:** ~50

#### `view_history.py`
**Purpose:** View conversation history  
**Key Components:**
```python
from backend.app.db import SessionLocal
from backend.app.models import ConversationHistory

# Query all messages
# Display with formatting
```
**Usage:** `python view_history.py`  
**Lines:** ~30

#### `README.md`
**Purpose:** Scripts documentation  
**Contents:**
- Overview of all scripts
- Usage instructions
- Prerequisites
**Lines:** ~100

---

## 📚 Documentation

**Location:** `docs/`  
**Purpose:** Comprehensive project documentation  
**Technology:** Markdown

### Structure

```
docs/
├── SYSTEM_ARCHITECTURE.md
├── CODEBASE_STRUCTURE.md
├── DEVELOPMENT.md
├── QUICK_REFERENCE.md
├── README.md
├── IDLE_THOUGHT_ENHANCED.md
├── IDLE_THOUGHT_GUIDE.md
├── PHASE_10A_GETTING_STARTED.md
├── PHASE_10A_IMPLEMENTATION.md
├── PHASE_10A_QUICK_REF.md
├── PHASE_10A_VISUAL_GUIDE.md
├── PHASE_10B_GETTING_STARTED.md
├── PHASE_10B_IMPLEMENTATION.md
├── PHASE_10B_QUICK_REF.md
├── PHASE_10B_VISUAL_GUIDE.md
├── PHASE_10C_GETTING_STARTED.md
├── PHASE_10C_IMPLEMENTATION.md
├── PHASE_10C_QUICK_REF.md
└── PHASE_10C_VISUAL_GUIDE.md
```

### Files

#### `SYSTEM_ARCHITECTURE.md`
**Purpose:** Complete system architecture documentation  
**Sections:**
- Overview and design principles
- System design patterns
- Module architecture
- Communication flow
- Data flow diagrams
- Technology stack
- Deployment architecture
- Security architecture
- Performance architecture
**Lines:** ~800

#### `CODEBASE_STRUCTURE.md` (this document)
**Purpose:** File-by-file codebase documentation  
**Sections:**
- Project root
- Backend module (all files)
- Overlay module (all files)
- Voice module (all files)
- Vision module (all files)
- Scripts module (all files)
- Documentation (all files)

#### `DEVELOPMENT.md`
**Purpose:** Development guide and best practices  
**Sections:**
- Setup instructions
- Development workflow
- Code style guide
- Testing guidelines
- Contribution guide
- Git workflow

#### `QUICK_REFERENCE.md`
**Purpose:** Quick command reference  
**Sections:**
- Common commands
- Startup sequences
- Configuration shortcuts
- Troubleshooting quick fixes

#### `README.md`
**Purpose:** Documentation overview  
**Contents:**
- Index of all documentation
- Getting started guide
- Documentation navigation

#### Phase Documentation Files

Each phase (10A, 10B, 10C) has 4 documents:

1. **GETTING_STARTED.md** - Quick start guide
2. **IMPLEMENTATION.md** - Technical implementation details
3. **QUICK_REF.md** - Command and API reference
4. **VISUAL_GUIDE.md** - Diagrams and visual explanations

**Phase 10A:** Desktop Understanding  
**Phase 10B:** Desktop Actions  
**Phase 10C:** Task Memory & Habits  

#### `IDLE_THOUGHT_ENHANCED.md`
**Purpose:** Enhanced idle thought system documentation  
**Sections:**
- Phase 9B companion mode
- Timing and probability
- Context awareness
- Integration guide

#### `IDLE_THOUGHT_GUIDE.md`
**Purpose:** Idle thought user guide  
**Sections:**
- How it works
- Configuration
- Customization
- Examples

---

## 📊 File Statistics

### Total Files by Module

| Module | Python Files | Config Files | Docs | Total |
|--------|-------------|--------------|------|-------|
| Backend | 12 | 1 (requirements.txt) | 1 README | 14 |
| Overlay | 5 | 1 | 1 README | 7 |
| Voice | 6 | 2 | 1 README | 9 |
| Vision | 8 | 1 | 1 README | 10 |
| Scripts | 7 | 0 | 1 README | 8 |
| Docs | 0 | 0 | 19 | 19 |
| **Total** | **38** | **5** | **24** | **67** |

### Lines of Code (Approximate)

| Module | Python LOC | Docs LOC | Total LOC |
|--------|-----------|----------|-----------|
| Backend | ~2,500 | 681 | ~3,181 |
| Overlay | ~400 | 663 | ~1,063 |
| Voice | ~800 | 956 | ~1,756 |
| Vision | ~800 | 894 | ~1,694 |
| Scripts | ~200 | ~100 | ~300 |
| Docs | 0 | ~5,000 | ~5,000 |
| **Total** | **~4,700** | **~8,294** | **~12,994** |

---

## 🔍 Quick File Lookup

### By Functionality

**WebSocket Communication:**
- `backend/app/ws.py` - Server handler
- `overlay/main.py` - Client
- `voice/text_chat.py` - Client
- `vision/vision_client.py` - Client

**LLM Integration:**
- `backend/app/llm_client.py` - HTTP streaming
- `backend/app/prompt.py` - System prompt

**Memory System:**
- `backend/app/memory.py` - In-memory buffer
- `backend/app/memory_long.py` - SQLite persistence
- `backend/app/db.py` - Database config
- `backend/app/models.py` - ORM models

**Emotion System:**
- `backend/app/emotion.py` - Extraction
- `overlay/avatar_window.py` - Display
- `voice/text_chat.py` - Cleaning

**Voice I/O:**
- `voice/voice_input.py` - STT
- `voice/voice_output_edge.py` - TTS
- `voice/voice_config.py` - Settings

**Vision Detection:**
- `vision/face_emotion.py` - Face/eye detection
- `vision/screen_capture.py` - Screenshots
- `vision/desktop_understanding.py` - Context analysis

**Phase Features:**
- `backend/app/idle_companion.py` - Phase 9B
- `vision/desktop_understanding.py` - Phase 10A
- `backend/app/desktop_actions.py` - Phase 10B
- `backend/app/task_memory.py` - Phase 10C

---

## 📝 Notes

### File Naming Conventions

- **snake_case** - All Python files
- **PascalCase** - Class names only
- **UPPERCASE** - Constants, markdown docs
- **kebab-case** - Not used

### Import Patterns

**Absolute imports (backend):**
```python
from .memory import MemoryBuffer
from .llm_client import stream_llm_response
```

**Relative imports (cross-module):**
```python
sys.path.append("../overlay")
from avatar_controller import on_speech_start
```

### Configuration Files

- `*_config.py` - Python configuration modules
- `requirements.txt` - Pip dependencies
- `*.ps1` - PowerShell scripts
- `*.md` - Markdown documentation

---

**Document Version:** 1.0  
**Last Updated:** January 17, 2026  
**Status:** Complete ✅  
**Total Files Documented:** 67
