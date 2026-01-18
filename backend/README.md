# 🔧 Backend - Alisa Assistant

FastAPI backend server with LLM integration, conversation memory, and advanced desktop integration features.

---

## 📋 Overview

The backend serves as the central brain of Alisa, handling:

- **LLM Integration** - Streaming responses from local LLM server (Llama.cpp)
- **Persistent Memory** - SQLite-based conversation history with token management
- **WebSocket Communication** - Real-time bidirectional messaging
- **Emotion Detection** - Extracts and broadcasts emotion states from responses
- **Conversation Modes** - Adaptive personality based on context (teasing, serious, calm)
- **Vision Integration** - Receives presence detection and screen analysis feedback
- **Idle Companion System (Phase 9B)** - Natural, spontaneous thoughts during user inactivity
- **Desktop Understanding (Phase 10A)** - Context awareness of user's work environment
- **Desktop Actions (Phase 10B)** - Permission-based desktop automation
- **Task Memory & Habits (Phase 10C)** - Adaptive learning from user work patterns

---

## 🚀 Quick Start

### Install Dependencies

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Start Server

```powershell
# From project root
.\scripts\start_backend.ps1

# Or manually
uvicorn backend.app.main:app --reload
```

**Server URLs:**
- HTTP API: `http://127.0.0.1:8000`
- WebSocket: `ws://127.0.0.1:8000/ws/chat`
- API Docs: `http://127.0.0.1:8000/docs`

---

## 📁 Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI entry point & routes
│   ├── ws.py                # WebSocket chat handler & idle loop
│   ├── llm_client.py        # LLM streaming integration
│   ├── emotion.py           # Emotion extraction from responses
│   ├── memory.py            # Short-term memory buffer (in-memory)
│   ├── memory_long.py       # Long-term SQLite storage
│   ├── prompt.py            # System prompt & personality definition
│   ├── modes.py             # Conversation mode management
│   ├── idle_companion.py    # Phase 9B: Spontaneous behavior system
│   ├── desktop_actions.py   # Phase 10B: Desktop automation
│   ├── task_memory.py       # Phase 10C: Habit learning system
│   ├── db.py                # Database configuration (SQLAlchemy)
│   ├── models.py            # SQLAlchemy ORM models
│   └── schemas.py           # Pydantic validation schemas
├── alisa_memory.db          # SQLite database (auto-created)
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## 🔌 API Endpoints

### Health Check

```http
GET /
```

**Response:**
```json
{"status": "Alisa online"}
```

### Get Conversation History Summary

```http
GET /history/summary
```

**Response:**
```json
{
  "messages": 24,
  "turns": 12,
  "estimated_tokens": 1850,
  "session_id": "default"
}
```

### Clear Conversation History

```http
POST /history/clear
```

**Response:**
```json
{"status": "History cleared"}
```

### WebSocket Chat

```http
WS /ws/chat
```

Real-time chat with token streaming, emotion detection, and bidirectional communication.

---

## 💬 WebSocket Protocol

### Client → Server Messages

```json
{"message": "Hello Alisa!"}
{"message": "/mode study"}
{"message": "open chrome"}  // Phase 10B: Desktop action
{"vision": {"presence": "present", "attention": "focused"}}  // Vision update
```

### Server → Client Messages

```
[token]                    # Response text chunks (streamed)
[EMOTION]happy             # Detected emotion
[END]                      # Response complete
[MODE CHANGED]             # Mode switch confirmed
[VISION]{"status": "..."}  # Vision system updates
[SPEECH_START]             # Avatar should start talking animation
[SPEECH_END]               # Avatar should stop talking animation
```

**Example Flow:**
```
Client: {"message": "Hey Alisa!"}
Server: [EMOTION]teasing
Server: Oh
Server: ,
Server:  look
Server:  who
Server:  remembered
Server:  I
Server:  exist
Server: .
Server: [END]
```

---

## 🎭 Conversation Modes

Switch modes with `/mode <name>`:

- **`teasing`** (default) - Standard tsundere girlfriend personality
- **`serious`** - Calm, mature, and direct responses
- **`calm`** - Soft, reassuring, gentle communication

**Example:** 
```json
{"message": "/mode serious"}
```

Modes affect Alisa's tone, response style, and emotional expression.

---

## 💾 Memory System

### Short-Term Memory (`memory.py`)

- **Storage:** In-memory buffer for current session
- **Capacity:** Last ~10 conversation turns (max 3000 tokens)
- **Trimming:** Automatic rolling window based on token count
- **Purpose:** Fast access for active conversation context
- **Persistence:** Loads from database on startup

**Features:**
- Rough token estimation (~4 chars = 1 token)
- Automatic trimming by age and token limit
- Session-based isolation (multi-user support ready)

### Long-Term Memory (`memory_long.py`)

- **Storage:** SQLite database (`alisa_memory.db`)
- **Persistence:** Across restarts and sessions
- **Retrieval:** Fetches recent memories for context building
- **Schema:** See `models.py` - `ConversationHistory` table

**Features:**
- Timestamped conversation entries
- Role-based storage (user/assistant)
- Session ID support for future multi-user scenarios
- Full conversation searchability

**Database Location:** `backend/alisa_memory.db`

---

## 🧠 Advanced Features

### Idle Companion System

**File:** `app/idle_companion.py`

Natural, spontaneous behavior when user is inactive:

- **Presence Awareness** - Detects when you're away or distracted via vision
- **Context-Aware Thoughts** - Integrates vision data, time of day, conversation mood
- **Emotional Continuity** - Remembers conversation mood for natural flow
- **Mode-Specific Behavior** - Adapts spontaneous thoughts to current mode
- **Rare Speech** - Companion, not chatbot (speaks only when natural)
- **Timing Windows** - 2min/5min/10min/30min silence thresholds with probability
- **Cooldown Management** - Prevents thought spam

**Triggers:**
- User silence for extended periods
- Vision state changes (presence/attention)
- Context-appropriate moments

**Philosophy:** Alisa speaks spontaneously like a companion would - rarely, naturally, when it feels right.

---

### Desktop Understanding

**Integration:** Via WebSocket vision updates from `vision/desktop_understanding.py`

Alisa gains awareness of your work environment:

- **Application Detection** - Knows what apps you're using (VS Code, Chrome, etc.)
- **File Type Recognition** - Identifies current file context (.py, .md, .json, etc.)
- **Task Inference** - Understands if you're coding, browsing, debugging, writing
- **Error Detection** - Spots error patterns on screen (red text, warnings)
- **Smart Offers** - Suggests help with 5-minute cooldown to avoid spam

**Example:** Alisa sees you're coding in VS Code with Python files → Offers coding assistance without being asked.

---

### Desktop Actions

**File:** `app/desktop_actions.py`

**Safety Model:**
- Permission-based execution
- Explicit commands execute directly
- Ambiguous requests ask for confirmation
- Rate limiting and blacklists

**Capabilities:**

#### 🖥️ App Management
```python
open_app(app_name)       # "open chrome", "launch notepad"
close_app(app_name)      # "close chrome"
switch_window(app_name)  # "switch to vscode"
```

#### 🌐 Browser Control
```python
browser_tab("open", url)   # "open tab google.com"
browser_tab("close")       # "close that tab"
browser_navigate(url)      # "go to github.com"
```

#### ⌨️ Keyboard & Mouse
```python
type_text(text)           # "type hello world"
press_key(key)            # "press enter", "ctrl+c"
click(x, y)               # "click" (current position)
scroll(direction, amount) # "scroll down"
```

#### 📁 File Operations
```python
read_file(path)           # "read file notes.txt"
write_note(content, path) # "write note: reminder"
```

#### 🪟 Window Management
```python
minimize_window()         # "minimize this"
maximize_window()         # "maximize window"
```

**Safety Features:**
- **Command Blacklist:** Blocks dangerous commands (rm, format, del, shutdown)
- **Path Restrictions:** No access to system directories (Windows, Program Files)
- **Rate Limiting:** Max 10 actions/minute
- **Permission System:** Explicit vs. request-based execution
- **Error Handling:** Graceful failures with user feedback

**Example Usage:**
```json
{"message": "open chrome"}
// Executes immediately

{"message": "Can you close that tab?"}
// Alisa asks: "Should I close the browser tab?"
```

---

### Task Memory & Habits

**File:** `app/task_memory.py`

Alisa learns your work patterns over time and adapts quietly:

**Learning Capabilities:**

#### 📅 Work Schedule
- Tracks when you're active (hourly patterns)
- Learns peak coding hours
- Identifies typical session lengths
- Recognizes work vs. break times

#### 📱 App Usage Patterns
- Associates apps with task types (VS Code → coding, Chrome → browsing)
- Learns preferred tools for specific tasks
- Recognizes context switches

#### 🔕 Silence Preferences
- Observes when you prefer uninterrupted work
- Learns when you're receptive to conversation
- Adapts interrupt timing based on patterns

#### 🔁 Repeated Tasks
- Recognizes common workflows
- Identifies task sequences
- Learns transition patterns

**Adaptive Behavior:**
- Adjusts timing of suggestions based on learned patterns
- Respects silence windows identified through observation
- Context-aware interruption decisions
- Pattern-based insights without being intrusive

**Data Storage:** 
- JSON files in workspace (auto-created)
- Persistent across sessions
- Privacy-first: all data stays local

**Philosophy:** Alisa observes quietly, learns passively, adapts subtly. No announcements, no questions about preferences - just natural adaptation.

---

## ⚙️ Configuration

### LLM Server

Edit `app/llm_client.py`:

```python
LLM_URL = "http://127.0.0.1:8080/v1/chat/completions"
```

**Supported Servers:**
- llama.cpp (recommended)
- Any OpenAI-compatible API

**LLM Parameters:**
```python
{
    "model": "local",
    "stream": True,
    "temperature": 0.7,
    "repeat_penalty": 1.1
}
```

### System Prompt

Edit `app/prompt.py` to customize:
- Core personality (tsundere girlfriend traits)
- Emotion usage guidelines
- Response style and speech patterns
- Idle behavior rules
- Absolute constraints

**Current Personality:** Anime-style tsundere girlfriend inspired by Alya from Roshidere.

### Conversation Modes

Edit `app/modes.py`:

```python
MODES = {
    "teasing": "You tease gently and act playful.",
    "serious": "You are calm, mature, and direct.",
    "calm": "You speak softly and reassuringly."
}
```

Add custom modes by extending this dictionary.

### Database

**Location:** `backend/alisa_memory.db`

**Schema:** Defined in `app/models.py`:
- `conversation_history` - Chat logs with timestamps
- `memory` - Long-term memory entries (deprecated, kept for compatibility)

**Configuration:** Edit `app/db.py`:

```python
DATABASE_URL = "sqlite:///alisa_memory.db"
```

---

## 🔧 Dependencies

### Core Framework
```
fastapi==0.104.1         # Web framework
uvicorn[standard]==0.24.0  # ASGI server
websockets==12.0          # WebSocket support
pydantic==2.5.0          # Data validation
```

### LLM & HTTP
```
httpx                     # Async HTTP client for LLM streaming
aiohttp==3.9.1           # Alternative HTTP client
python-dotenv            # Environment variables
```

### Database
```
sqlalchemy               # ORM for SQLite
python-multipart==0.0.6  # Form data parsing
```

### Desktop Integration (Phase 10B)
```
pyautogui                # Keyboard/mouse automation
psutil                   # Process management
```

**Full list:** See `requirements.txt`

---

## 🛠️ Development

### Run in Development Mode

```powershell
uvicorn app.main:app --reload
```

Auto-reloads on code changes. Watch console for:
- WebSocket connections/disconnections
- LLM streaming status
- Emotion detection results
- Idle thought triggers (Phase 9B)
- Desktop action executions (Phase 10B)
- Task learning events (Phase 10C)

### View Conversation History

```powershell
python ..\scripts\view_history.py
```

Displays all conversation entries with timestamps.

### Clear Memory

```python
from app.memory_long import clear_history
clear_history()
```

Or via API:
```http
POST /history/clear
```

### Database Inspection

```powershell
sqlite3 alisa_memory.db
.tables
.schema conversation_history
SELECT * FROM conversation_history ORDER BY timestamp DESC LIMIT 10;
.quit
```

---

## 📊 Performance

### Optimizations

- **Async/Await** - Concurrent WebSocket connections
- **Token Streaming** - Real-time response display
- **Connection Pooling** - Efficient database access
- **Token-Based Trimming** - Prevents memory overflow (~3000 tokens max)
- **Lazy Loading** - Data loaded only when needed
- **Background Tasks** - Idle loop runs independently

### Typical Performance

- **LLM First Token:** <100ms (local Llama server)
- **WebSocket Latency:** <10ms
- **Database Query:** <5ms (SQLite on SSD)
- **Memory Load:** <50ms (3000 tokens from DB)
- **Idle Check Interval:** 30 seconds

### Resource Usage

- **Memory:** ~100MB idle, ~300MB during streaming
- **CPU:** <5% idle, 10-20% during LLM streaming
- **Disk:** Minimal writes (conversation history only)

---

## 🐛 Troubleshooting

### LLM Not Responding

**Symptoms:** No response to messages, timeout errors

**Solutions:**
1. Check if LLM server is running on port 8080
2. Verify `LLM_URL` in `app/llm_client.py`
3. Test LLM server: `curl http://127.0.0.1:8080/v1/models`
4. Check console logs for connection errors
5. Ensure LLM model is loaded (check llama-server terminal)

### Database Errors

**Symptoms:** SQLAlchemy errors, "database is locked"

**Solutions:**
1. Delete `alisa_memory.db` to reset database
2. Check write permissions in backend folder
3. Ensure only one backend instance running
4. Close any SQLite browser tools

### WebSocket Disconnects

**Symptoms:** Client disconnects, connection refused

**Solutions:**
1. Check CORS settings in `app/main.py`
2. Verify client uses correct URL: `ws://127.0.0.1:8000/ws/chat`
3. Check firewall settings
4. Restart backend server
5. Check for network errors in browser console

### Desktop Actions Not Working 

**Symptoms:** Actions fail silently, permission errors

**Solutions:**
1. Check console logs for error messages
2. Verify action syntax matches examples above
3. Check rate limiting (max 10 actions/minute)
4. Ensure action isn't blacklisted (no dangerous commands)
5. Run backend with appropriate privileges
6. Verify `pyautogui` is installed

### Task Memory Not Learning 

**Symptoms:** No pattern detection, no adaptive behavior

**Solutions:**
1. Check workspace folder is writable
2. Allow sufficient observation time (hours to days for patterns)
3. Check console logs for learning events
4. Review storage path in `task_memory.py`
5. Ensure JSON files are being created

### Idle Thoughts Not Triggering 

**Symptoms:** No spontaneous speech during silence

**Solutions:**
1. Wait at least 2 minutes of silence
2. Check idle loop is running (console shows "🧠 Phase 9B initialized")
3. Verify vision client is connected (optional but enhances behavior)
4. Check probability settings in `idle_companion.py`
5. Review console for "silent" log messages explaining why not speaking

---

## 🔒 Security Considerations

### API Security

- **CORS:** Configured for localhost only
- **Authentication:** None (local use only)
- **Input Validation:** Pydantic schemas validate all inputs
- **Rate Limiting:** Implemented for desktop actions

### Desktop Actions Security (Phase 10B)

- **Command Blacklist:** Prevents dangerous commands (rm, format, del, shutdown, restart)
- **Path Restrictions:** No access to system directories (C:\Windows, C:\Program Files)
- **Rate Limiting:** Max 10 actions/minute to prevent abuse
- **Permission System:** Explicit commands vs. confirmation requests
- **Fail-Safe:** PyAutoGUI mouse corner abort enabled
- **Action Logging:** All actions tracked with timestamps

### Data Privacy

- **Local Processing:** All LLM inference runs locally
- **No Cloud Uploads:** Conversation data stays on device
- **SQLite Database:** Stored locally in backend folder
- **Vision Data:** Not saved, processed in memory only
- **Task Memory:** Stored locally in JSON files

---

## 📚 Related Documentation

- **[Main README](../README.md)** - Project overview
- **[Codebase Structure](../docs/CODEBASE_STRUCTURE.md)** - Full architecture

---

## 🚀 Next Steps

1. **Customize Personality:** Edit `app/prompt.py` for your preferred style
2. **Add Modes:** Extend `app/modes.py` with custom conversation modes
3. **Enable Phase 10 Features:** Use startup scripts for full integration
4. **Explore Task Patterns:** Review learning data in JSON storage
5. **Build Custom Integrations:** Use WebSocket API for external apps

---

**Version:** 3.0   
**Tested With:** Python 3.10+, Windows 11, Llama.cpp  
**License:** See [LICENSE](../LICENSE)
