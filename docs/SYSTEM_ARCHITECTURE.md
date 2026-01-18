# 🏗️ Alisa System Architecture

Complete system architecture documentation for the Alisa AI Assistant project.

**Last Updated:** January 17, 2026  
**Version:** 3.0 

---

## 📋 Table of Contents

- [Overview](#overview)
- [System Design](#system-design)
- [Module Architecture](#module-architecture)
- [Communication Flow](#communication-flow)
- [Data Flow](#data-flow)
- [Technology Stack](#technology-stack)
- [Deployment Architecture](#deployment-architecture)
- [Security Architecture](#security-architecture)
- [Performance Architecture](#performance-architecture)

---

## 🎯 Overview

### System Purpose

Alisa is a local-first AI assistant with a personality-driven tsundere girlfriend character. The system provides:

- Real-time conversation with LLM integration
- Multi-modal interaction (text, voice, vision)
- Animated avatar with emotion expression
- Context-aware desktop understanding
- Adaptive learning from user patterns

### Design Principles

1. **Local-First** - All processing happens on user's machine
2. **Modular** - Independent modules communicate via WebSocket
3. **Real-Time** - Streaming responses with <100ms latency
4. **Privacy-First** - No cloud uploads, minimal data storage
5. **Extensible** - Easy to add new capabilities
6. **Fail-Safe** - Graceful degradation when modules unavailable

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         User Interface Layer                         │
├─────────────┬─────────────┬─────────────┬──────────────────────────┤
│   Overlay   │    Voice    │   Vision    │   Scripts (Startup)      │
│  (Avatar)   │ (I/O Chat)  │ (Presence)  │                          │
└──────┬──────┴──────┬──────┴──────┬──────┴──────────────────────────┘
       │             │             │
       │    WebSocket Connections  │
       │             │             │
┌──────▼─────────────▼─────────────▼──────────────────────────────────┐
│                     Backend Core (FastAPI)                           │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  WebSocket Handler (ws.py)                                     │ │
│  │  - Message routing                                              │ │
│  │  - State management                                             │ │
│  │  - Idle thought loop                                            │ │
│  └────────────────────────────────────────────────────────────────┘ │
│  ┌──────────┬──────────┬──────────┬──────────┬─────────────────┐  │
│  │  Memory  │   LLM    │ Desktop  │  Task    │ Idle Companion  │  │
│  │  System  │  Client  │ Actions  │  Memory  │    System       │  │
│  └──────────┴──────────┴──────────┴──────────┴─────────────────┘  │
└─────────────────────────────┬────────────────────────────────────────┘
                              │
                    HTTP Streaming API
                              │
┌─────────────────────────────▼────────────────────────────────────────┐
│                    LLM Server (Llama.cpp)                             │
│  - Model: Meta-Llama-3.1-8B-Instruct-Q4_K_M                          │
│  - Context: 4096 tokens                                               │
│  - GPU Offload: 33 layers                                            │
└───────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────┐
│                      Storage Layer                                     │
│  ┌──────────────┬──────────────┬──────────────────────────────────┐  │
│  │   SQLite     │   JSON Files │    Temporary Files               │  │
│  │ (Conversation│ (Task Memory)│  (Audio, Screenshots)            │  │
│  │   History)   │              │                                  │  │
│  └──────────────┴──────────────┴──────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
```

---

## 🏛️ System Design

### Architectural Pattern

**Microservices-Inspired Modular Monolith**

- **Backend** - Central hub (FastAPI)
- **Modules** - Independent processes (Overlay, Voice, Vision)
- **Communication** - WebSocket pub/sub pattern
- **Storage** - Shared database, isolated configs

### Design Patterns Used

1. **Observer Pattern** - WebSocket clients observe backend state
2. **Strategy Pattern** - Multiple TTS/STT implementations
3. **Singleton Pattern** - Global memory buffer, task memory
4. **Factory Pattern** - Emotion detection, mode selection
5. **Decorator Pattern** - Emotion tag extraction
6. **Adapter Pattern** - LLM client wraps API calls

### Module Independence

Each module can run independently:

```
Backend Only:        Text-based chat via HTTP API
Backend + Overlay:   Visual chat with emotions
Backend + Voice:     Voice conversation
Backend + Vision:    Context-aware responses
All Modules:         Full experience
```

---

## 🧩 Module Architecture

### Backend Module

**Technology:** FastAPI + SQLAlchemy + asyncio

**Components:**

```
backend/app/
├── main.py              # FastAPI app, routes, startup/shutdown
├── ws.py                # WebSocket handler, idle loop, broadcasting
├── llm_client.py        # LLM streaming (HTTP → Generator)
├── memory.py            # In-memory buffer (10 turns, 3000 tokens)
├── memory_long.py       # SQLite persistence
├── emotion.py           # Emotion tag extraction
├── modes.py             # Conversation mode management
├── prompt.py            # System prompt + personality
├── idle_companion.py    # Phase 9B: Spontaneous behavior
├── desktop_actions.py   # Phase 10B: Desktop automation
├── task_memory.py       # Phase 10C: Pattern learning
├── db.py                # SQLAlchemy engine + session
├── models.py            # ORM models (ConversationHistory)
└── schemas.py           # Pydantic schemas
```

**Responsibilities:**
- WebSocket connection management
- LLM response streaming
- Memory persistence
- State synchronization
- Idle thought generation
- Desktop action execution
- Task pattern learning

**State Management:**
```python
# Global state
connected_clients: List[WebSocket]
vision_state: Dict[str, Any]
last_user_activity: float
idle_thought_active: bool
```

### Overlay Module

**Technology:** Tkinter + PIL + WebSocket client

**Components:**

```
overlay/
├── main.py              # Entry point, WebSocket listener
├── avatar_window.py     # Tkinter UI, animation logic
├── avatar_controller.py # Thread-safe API
├── assets/              # PNG images (RGBA)
│   ├── base.png         # Emotions (6 files)
│   ├── eyes_closed.png  # Blink layer
│   └── mouth_open.png   # Talk layer
└── test_animations.py   # Animation testing
```

**Responsibilities:**
- Display transparent window
- Render layered images
- Animate mouth (talking)
- Animate eyes (blinking)
- Switch emotions
- Maintain always-on-top

**Thread Safety:**
```python
# WebSocket thread → Main thread communication
root.after(0, lambda: callback())  # Queue in Tkinter main loop
```

### Voice Module

**Technology:** Faster Whisper + Edge TTS + PyGame

**Components:**

```
voice/
├── text_chat.py             # Text input + voice output
├── voice_chat_optimized.py  # Full voice conversation
├── voice_input.py           # Faster Whisper STT
├── voice_output_edge.py     # Edge TTS (default)
├── voice_output_rvc.py      # Edge TTS + RVC (optional)
├── voice_config.py          # Voice customization
└── rvc/                     # RVC voice conversion
    ├── inferencer.py
    ├── weights/
    └── index/
```

**Responsibilities:**
- Microphone capture
- Speech-to-text transcription
- Text-to-speech synthesis
- Audio playback
- Overlay animation sync
- Emotion text cleaning

**Audio Pipeline:**
```
Input:  Mic → sounddevice → WAV → Whisper → Text
Output: Text → Edge TTS → MP3 → PyGame → Speakers
```

### Vision Module

**Technology:** OpenCV + MediaPipe + mss + Tesseract

**Components:**

```
vision/
├── vision_client.py         # Webcam presence (lightweight)
├── vision_client_screen.py  # Full vision + desktop understanding
├── webcam.py                # Camera capture
├── face_emotion.py          # Face/eye detection
├── screen_capture.py        # Screenshot via mss
├── screen_analyze.py        # OCR + window detection
├── desktop_understanding.py # Phase 10A context analysis
├── vision_config.py         # Performance presets
└── test_vision_performance.py
```

**Responsibilities:**
- Face detection (presence)
- Eye detection (attention)
- Screen capture
- OCR text extraction
- Window title detection
- Application categorization
- Error detection
- Contextual help offers

**Detection Pipeline:**
```
Webcam: Camera → Frame → Haar/MediaPipe → Face/Eyes → State
Screen: Desktop → Screenshot → OCR → Text + Window → Context
```

---

## 🔄 Communication Flow

### WebSocket Protocol

**URL:** `ws://127.0.0.1:8000/ws/chat`

**Message Types:**

| Direction | Message | Format | Purpose |
|-----------|---------|--------|---------|
| Client → Server | User message | `{"message": "text"}` | Send user input |
| Client → Server | Vision update | `[VISION_FACE]state` | Presence/attention |
| Client → Server | Desktop context | `[VISION_DESKTOP]data` | Screen analysis |
| Server → Client | LLM token | `token` | Streaming response |
| Server → Client | Emotion | `[EMOTION]name` | Emotion change |
| Server → Client | End marker | `[END]` | Response complete |
| Server → Client | Speech control | `[SPEECH_START/END]` | Animation sync |
| Server → Client | Mode change | `[MODE CHANGED]` | Mode switch confirm |

**Connection Management:**

```python
# Auto-reconnect pattern (all clients)
while True:
    try:
        async with websockets.connect(WS_URL) as ws:
            # Handle messages
    except ConnectionClosedError:
        await asyncio.sleep(2)  # Reconnect delay
```

**Broadcasting:**

```python
# Backend broadcasts to all connected clients
async def broadcast_message(message: str, exclude: WebSocket = None):
    for client in connected_clients:
        if client != exclude:
            await client.send(message)
```

### HTTP API

**Endpoints:**

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | Health check |
| GET | `/history/summary` | Memory stats |
| POST | `/history/clear` | Clear memory |
| WS | `/ws/chat` | WebSocket chat |

### LLM Communication

**Protocol:** HTTP streaming (OpenAI-compatible)

```python
# Request
POST http://127.0.0.1:8080/v1/chat/completions
{
    "model": "local",
    "messages": [...],
    "stream": true,
    "temperature": 0.7
}

# Response (SSE)
data: {"choices":[{"delta":{"content":"token"}}]}
data: {"choices":[{"delta":{"content":"token"}}]}
data: [DONE]
```

---

## 📊 Data Flow

### User Message Flow

```
1. User types/speaks message
   ↓
2. Voice module (optional): Audio → Text
   ↓
3. Client sends via WebSocket → Backend
   ↓
4. Backend adds to memory buffer
   ↓
5. Backend builds prompt (system + history + vision context)
   ↓
6. Backend streams to LLM server
   ↓
7. LLM generates tokens
   ↓
8. Backend streams tokens to all clients
   ↓
9. Backend extracts emotion
   ↓
10. Backend broadcasts [EMOTION] and [END]
    ↓
11. Overlay updates emotion
    ↓
12. Voice module speaks (optional)
    ↓
13. Backend saves to database
```

### Vision State Flow

```
1. Vision captures frame (every 1.5s)
   ↓
2. Face/eye detection
   ↓
3. Determine state (present/absent/focused/away)
   ↓
4. Send [VISION_FACE]state to backend
   ↓
5. Backend updates vision_state dict
   ↓
6. Backend uses in idle thought decisions
   ↓
7. Vision captures screen (every 10s)
   ↓
8. OCR + window detection
   ↓
9. Desktop understanding analysis
   ↓
10. Send [VISION_DESKTOP]context to backend
    ↓
11. Backend stores in vision_state
    ↓
12. Backend may offer help if error detected
```

### Memory Persistence Flow

```
1. Message added to memory.messages (in-memory)
   ↓
2. Simultaneously saved to SQLite
   ↓
3. Memory buffer trims to 3000 tokens
   ↓
4. Database keeps all history
   ↓
5. On backend restart: Load last 3000 tokens from DB
```

### Idle Thought Flow

```
1. Background task checks every 30s
   ↓
2. Calculate silence duration
   ↓
3. Get vision state
   ↓
4. Phase 9B: Companion system decides if should speak
   ↓
5. Phase 10C: Task memory checks interrupt timing
   ↓
6. If approved: Generate idle thought
   ↓
7. Broadcast to all clients
   ↓
8. Mark as spontaneous speech
```

---

## 🛠️ Technology Stack

### Backend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | FastAPI | 0.104.1 | HTTP + WebSocket server |
| ASGI Server | Uvicorn | 0.24.0 | Production server |
| Database | SQLite | 3.x | Conversation storage |
| ORM | SQLAlchemy | 2.x | Database models |
| Validation | Pydantic | 2.5.0 | Data schemas |
| HTTP Client | httpx | Latest | LLM streaming |
| Desktop Automation | pyautogui | Latest | Phase 10B actions |
| Process Management | psutil | Latest | System info |

### Overlay

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| GUI | Tkinter | Built-in | Window management |
| Image Processing | Pillow | 10.0.0+ | PNG loading/compositing |
| WebSocket Client | websockets | 12.0 | Backend connection |

### Voice

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| STT Engine | Faster Whisper | 0.10.0+ | Speech recognition |
| TTS Engine | Edge TTS | 6.1.0+ | Speech synthesis |
| Audio I/O | sounddevice | 0.4.0+ | Microphone/speaker |
| Audio Processing | scipy | 1.10.0+ | Signal processing |
| Playback | PyGame | 2.5.0+ | Audio playback |
| RVC (Optional) | PyTorch | Latest | Voice conversion |
| Audio Processing | librosa | 0.10.0+ | RVC audio processing |

### Vision

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Computer Vision | OpenCV | 4.8.0+ | Face/eye detection |
| Face Detection | MediaPipe | 0.10.9 | Enhanced detection (optional) |
| Screen Capture | mss | 9.0.0+ | Fast screenshots |
| OCR | Tesseract | 0.3.10+ | Text extraction |
| Window Management | pywin32 | 306+ | Window info (Windows) |
| Performance | psutil | 5.9.0+ | Resource monitoring |

### LLM Server

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Server | llama.cpp | Latest | Model inference |
| Model | Llama-3.1-8B | Q4_K_M | Text generation |
| API | OpenAI-compatible | v1 | HTTP streaming |

---

## 🚀 Deployment Architecture

### Local Deployment (Current)

```
User's Machine
├── LLM Server (Port 8080)
│   └── Process: llama-server.exe
│
├── Backend (Port 8000)
│   └── Process: uvicorn
│
├── Overlay (GUI Window)
│   └── Process: python main.py
│
├── Voice (Terminal)
│   └── Process: python text_chat.py
│
└── Vision (Background)
    └── Process: python vision_client_screen.py
```

### Startup Scripts

Located in `scripts/`:

```powershell
start_backend.ps1       # Starts backend server
start_overlay.ps1       # Starts avatar overlay
start_text_chat.ps1     # Starts text chat
start_voice.ps1         # Starts voice chat
start_vision.ps1        # Starts webcam vision
start_vision_screen.ps1 # Starts full vision
start_phase10a.ps1      # All features
start_phase10b.ps1      # + Desktop actions
start_phase10c.ps1      # + Task memory
```

### Port Assignments

| Service | Port | Protocol | Purpose |
|---------|------|----------|---------|
| Backend | 8000 | HTTP/WS | Main API |
| LLM Server | 8080 | HTTP | Model inference |

### Process Dependencies

```
LLM Server (Required)
    ↓
Backend (Required)
    ↓
┌───────┬─────────┬─────────┐
Overlay  Voice    Vision
(Optional)(Optional)(Optional)
```

---

## 🔒 Security Architecture

### Threat Model

**Assumptions:**
- Single-user local environment
- Trusted local network
- No external attackers
- User has physical access

**Out of Scope:**
- Multi-user authentication
- Network encryption
- Remote access security

### Security Measures

#### 1. Network Security

```python
# CORS - Localhost only
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:*"],
    allow_credentials=True
)

# No external network access
# All services bind to 127.0.0.1
```

#### 2. Desktop Actions Security (Phase 10B)

```python
# Command blacklist
DANGEROUS_COMMANDS = ["rm -rf", "del /f", "format", "shutdown"]

# Path restrictions
BLOCKED_PATHS = ["C:\\Windows", "C:\\Program Files"]

# Rate limiting
MAX_ACTIONS_PER_MINUTE = 10

# Permission system
explicit_commands → execute immediately
ambiguous_requests → ask for confirmation
```

#### 3. Data Privacy

- **No Cloud Uploads** - All processing local
- **No Screenshots Saved** - Memory-only processing
- **No Webcam Recording** - Single frame capture
- **Minimal Data Sent** - Only metadata via WebSocket
- **SQLite Encryption** - Optional (not implemented)

#### 4. Input Validation

```python
# Pydantic schemas validate all inputs
class MessageSchema(BaseModel):
    message: str = Field(max_length=10000)

# SQL injection prevention
# SQLAlchemy ORM prevents raw SQL
```

#### 5. Error Handling

```python
# Never expose internal paths in errors
try:
    # Operation
except Exception as e:
    logger.error(f"Operation failed: {e}")
    return {"error": "Internal error"}  # Generic message
```

---

## ⚡ Performance Architecture

### Performance Targets

| Metric | Target | Actual |
|--------|--------|--------|
| LLM First Token | <200ms | ~100ms |
| WebSocket Latency | <20ms | ~10ms |
| Database Query | <10ms | ~5ms |
| Memory Load | <100ms | ~50ms |
| Face Detection | <50ms | ~20ms |
| Screen Capture | <200ms | ~100ms |

### Optimization Strategies

#### 1. Memory Management

```python
# Token-based trimming (not message count)
def _trim_by_tokens(self):
    while total_tokens > self.max_tokens:
        self.messages.pop(0)  # Remove oldest

# Connection pooling
SessionLocal = sessionmaker(bind=engine, pool_size=5)
```

#### 2. Async Processing

```python
# Non-blocking WebSocket broadcasting
async def broadcast_message(message: str):
    tasks = [client.send(message) for client in connected_clients]
    await asyncio.gather(*tasks, return_exceptions=True)

# Background idle loop
idle_task = asyncio.create_task(idle_thought_loop())
```

#### 3. Caching

```python
# Vision detection cache (0.5s TTL)
if use_cache and (time.time() - cache['timestamp']) < 0.5:
    return cached_result

# LLM model stays loaded in memory
# No model loading overhead per request
```

#### 4. Streaming

```python
# Token streaming (not batched)
async for token in stream_llm_response(messages):
    await broadcast_message(token)
    # User sees response immediately
```

#### 5. Resource Limits

```python
# Vision config
DETECTION_INTERVAL = 1.5  # Don't detect every frame
FRAME_SKIP = 2  # Process every 2nd frame
PROCESS_WIDTH = 320  # Downscale for detection

# Memory limits
MAX_TURNS = 10
MAX_TOKENS = 3000
```

### Performance Monitoring

```python
# test_vision_performance.py
# Measures:
# - FPS
# - CPU usage
# - Memory usage
# - Detection accuracy
# - Latency
```

### Scalability Considerations

**Current:** Single user, localhost

**Future:**
- Multi-user: Add authentication, session isolation
- Remote: Add TLS, authentication tokens
- Load balancing: Multiple backend instances
- Database: PostgreSQL for concurrent access

---

## 📐 Design Decisions

### Why WebSocket over REST?

**Chosen:** WebSocket  
**Reason:** Bidirectional real-time communication for:
- Token streaming
- Idle thoughts (server-initiated)
- Vision updates (client-initiated)
- Overlay sync (broadcast)

### Why SQLite over PostgreSQL?

**Chosen:** SQLite  
**Reason:**
- Single-user application
- No setup required
- File-based, portable
- Fast for read-heavy workload
- Sufficient for conversation history

### Why Tkinter over Qt/Electron?

**Chosen:** Tkinter  
**Reason:**
- Built-in with Python
- Lightweight (low memory)
- Perfect for simple overlay
- Cross-platform
- No additional dependencies

### Why Local LLM over API?

**Chosen:** Local (llama.cpp)  
**Reason:**
- Privacy (no data leaves machine)
- No API costs
- Low latency (<100ms first token)
- Offline capability
- Full control over model

### Why Faster Whisper over OpenAI Whisper?

**Chosen:** Faster Whisper  
**Reason:**
- 4x faster inference
- Lower memory usage
- Same accuracy
- Better for real-time
- GPU acceleration support

---

## 🔮 Future Architecture

### Planned Enhancements

1. **Plugin System**
   - Load modules dynamically
   - Third-party extensions
   - Hot-reload capabilities

2. **Event Bus**
   - Replace WebSocket broadcasting
   - Better decoupling
   - Event replay capability

3. **State Management**
   - Redux-like state store
   - Time-travel debugging
   - State persistence

4. **Microservices**
   - Separate processes per module
   - Independent scaling
   - Docker containers

5. **Cloud Sync (Optional)**
   - End-to-end encrypted
   - Multi-device sync
   - Backup to cloud storage

---

## 📚 References

### External Dependencies

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [llama.cpp GitHub](https://github.com/ggerganov/llama.cpp)
- [Faster Whisper GitHub](https://github.com/guillaumekln/faster-whisper)
- [Edge TTS GitHub](https://github.com/rany2/edge-tts)
- [OpenCV Documentation](https://docs.opencv.org/)

### Related Documentation

- [Backend README](../backend/README.md)
- [Overlay README](../overlay/README.md)
- [Voice README](../voice/README.md)
- [Vision README](../vision/README.md)
- [Codebase Structure](CODEBASE_STRUCTURE.md)

---

**Document Version:** 1.0  
**Last Updated:** January 17, 2026  
**Status:** Complete ✅
