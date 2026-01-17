# 🎭 Overlay - Alisa Assistant

Animated avatar overlay window with transparent background and emotion-based animations.

**Last Updated:** January 17, 2026

---

## 📋 Overview

The overlay displays Alisa's animated avatar on your desktop with:

- **Transparent Window** - Always-on-top, borderless overlay with click-through transparency
- **6 Emotion Expressions** - neutral, happy, teasing, serious, calm, sad
- **Smooth Animations** - Talking mouth animation synced with speech
- **Auto Blinking** - Natural, random blinking every 2-5 seconds
- **Draggable Interface** - Click and drag to reposition anywhere
- **Real-time Updates** - Emotion and speech sync via WebSocket from backend
- **Thread-Safe Architecture** - Safe control from voice modules and WebSocket
- **Auto-Reconnect** - Maintains connection even if backend restarts

---

## 🚀 Quick Start

### Install Dependencies

```powershell
cd overlay
pip install -r requirements.txt
```

### Start Overlay

```powershell
# From project root
.\scripts\start_overlay.ps1

# Or manually
cd overlay
python main.py
```

**Requires:** Backend server running on `ws://127.0.0.1:8000/ws/chat`

**Note:** The overlay will auto-reconnect if backend is started later.

---

## 📁 Structure

```
overlay/
├── main.py                  # Entry point & WebSocket client
├── avatar_window.py         # Tkinter UI & animation rendering
├── avatar_controller.py     # Thread-safe control API
├── check_images.py          # Asset verification utility
├── test_animations.py       # Animation testing script
├── assets/                  # Avatar images (PNG with alpha)
│   ├── base.png            # Neutral expression
│   ├── happy.png           # Happy expression
│   ├── teasing.png         # Teasing expression
│   ├── serious.png         # Serious expression
│   ├── calm.png            # Calm expression
│   ├── sad.png             # Sad expression
│   ├── eyes_closed.png     # Blinking layer (overlay)
│   └── mouth_open.png      # Talking layer (overlay)
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## 🎨 Emotion System

### Available Emotions

| Emotion | Description | Use Case | Backend Trigger |
|---------|-------------|----------|-----------------|
| `neutral` | Default calm expression | Standard state | Default/fallback |
| `happy` | Bright, cheerful smile | Joy, excitement | `<emotion=happy>` |
| `teasing` | Playful, mischievous look | Tsundere moments | `<emotion=teasing>` |
| `serious` | Focused, mature expression | Important topics | `<emotion=serious>` |
| `calm` | Soft, peaceful look | Relaxation, peace | `<emotion=calm>` |
| `sad` | Downcast, empathetic expression | Sadness, empathy | `<emotion=sad>` |

### How It Works

1. **Backend Detection:** LLM includes `<emotion=name>` tag in response
2. **Extraction:** Backend extracts emotion and sends `[EMOTION]name` via WebSocket
3. **Overlay Receives:** WebSocket listener catches emotion message
4. **Thread-Safe Update:** Uses `root.after()` to safely update from WebSocket thread
5. **Expression Change:** Base image switches to new emotion face
6. **Persistence:** Emotion remains until next change

---

## 💬 Animation System

### Talking Animation

**Trigger:** `[SPEECH_START]` message from backend or voice modules

**Behavior:**
- Toggles `mouth_open.png` layer on/off
- 500ms cycle: 200ms open, 300ms closed
- Loops until `[SPEECH_END]` received
- Synced with voice output timing

**Safety Features:**
- 30-second auto-timeout prevents stuck animation
- Duplicate start signals ignored
- Returns to neutral face when stopped

**Example Flow:**
```
[SPEECH_START] → mouth animates → [SPEECH_END] → returns to neutral
```

### Blinking Animation

**Trigger:** Automatic timer (every 3 seconds)

**Behavior:**
- Overlays `eyes_closed.png` layer briefly
- 150ms duration per blink
- Independent of talking state
- Pauses during talking to avoid conflicts

**Timing:**
- Check interval: 3000ms
- Blink duration: 150ms
- Continuous loop

### Layer Compositing

The avatar uses a layered rendering approach:

```
Final Display = base.png (current emotion)
              + eyes_closed.png (if blinking)
              + mouth_open.png (if talking)
```

**Technical Details:**
- Base layer: Current emotion face (persistent)
- Overlay layer: Temporary effects (eyes/mouth)
- All images: RGBA PNG format with transparency
- Size: 400x400 pixels (configurable)

---

## 🎮 Controls

### Window Interaction

- **Drag:** Left-click and drag anywhere to move window
- **Close:** Right-click on avatar window
- **Position:** Remembers position within session (not persisted)

### Window Properties

- **Always On Top:** Stays above all other windows
- **Transparent Background:** White color-keyed transparency
- **Borderless:** No title bar or window controls
- **Click-Through:** Text area is transparent, avatar image catches clicks

---

## 🔌 WebSocket Protocol

### Messages Received

The overlay listens for these messages from backend:

| Message | Action | Notes |
|---------|--------|-------|
| `[EMOTION]<name>` | Change emotion | e.g., `[EMOTION]happy` |
| `[SPEECH_START]` | Start talking animation | From voice/text chat |
| `[SPEECH_END]` | Stop talking animation | From voice/text chat |
| `[END]` | LLM response complete | Ignored by overlay |
| `<token>` | LLM streaming text | Ignored by overlay |

### Connection Management

**Auto-Reconnect:**
- Reconnect delay: 2 seconds
- Infinite retry attempts
- Graceful handling of backend restarts

**Error Handling:**
- Connection closed: Auto-reconnect
- Connection refused: Wait and retry
- Unexpected errors: Log and reconnect

**Console Output:**
```
✅ Connected to backend at ws://127.0.0.1:8000/ws/chat
🔵 [WS RECEIVED] [EMOTION]teasing
🎤 [OVERLAY] Speech started - animating mouth
🤐 [OVERLAY] Speech ended - stopping mouth
```

---

## 🧵 Thread-Safe Architecture

### Why Thread-Safety Matters

Tkinter runs in the main thread and is **not thread-safe**. The overlay receives WebSocket messages in a background thread, requiring safe communication.

### Implementation

**WebSocket Thread:**
```python
async def listen_to_backend(self):
    # Runs in background thread
    async with websockets.connect(WS_URL) as ws:
        msg = await ws.recv()
        # Thread-safe update:
        avatar_window.root.after(0, lambda: handle_message(msg))
```

**Main Thread:**
```python
# Tkinter mainloop runs here
root.mainloop()
```

**Safe Methods:**
- `safe_start_talking()` - Queue talking animation
- `safe_stop_talking()` - Queue stop animation
- `safe_on_emotion(emotion)` - Queue emotion change

**How It Works:**
1. WebSocket thread receives message
2. Uses `root.after(0, callback)` to queue in main thread
3. Main thread executes callback safely
4. No race conditions or crashes

### Controller API

**File:** `avatar_controller.py`

Public functions for external control:

```python
on_speech_start()  # Start talking (from voice modules)
on_speech_end()    # Stop talking (from voice modules)
on_emotion(emotion)  # Change emotion (from backend)
```

These functions ensure thread-safe updates from any module.

---

## 🎨 Customization

### Change Avatar Images

1. **Create/Edit Images:**
   - **Format:** PNG with RGBA (transparency support)
   - **Dimensions:** 400x400 pixels (or consistent size)
   - **Alignment:** All layers must align perfectly when overlaid
   - **Background:** Transparent (alpha channel)

2. **Replace Assets:**
   ```
   overlay/assets/
   ├── base.png          # Neutral expression (base)
   ├── happy.png         # Happy face
   ├── teasing.png       # Teasing face
   ├── serious.png       # Serious face
   ├── calm.png          # Calm face
   ├── sad.png           # Sad face
   ├── eyes_closed.png   # Blinking overlay (aligned to eyes)
   └── mouth_open.png    # Talking overlay (aligned to mouth)
   ```

3. **Add New Emotions:**
   - Create new emotion PNG (e.g., `excited.png`)
   - Add to `faces` dict in `avatar_window.py`:
     ```python
     faces = {
         "neutral": ImageTk.PhotoImage(load("base.png").convert("RGBA")),
         "excited": ImageTk.PhotoImage(load("excited.png").convert("RGBA")),
         # ...
     }
     ```
   - Add to backend `emotion.py` validation
   - Update system prompt in `backend/app/prompt.py`

### Adjust Window Properties

Edit `avatar_window.py`:

```python
# Window size
WINDOW_SIZE = 400  # Change to your preferred size

# Position (default spawn location)
root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}+50+50")  # +X+Y

# Transparency
root.attributes("-transparentcolor", "white")  # Color to make transparent
```

### Adjust Animation Timings

Edit `avatar_window.py`:

```python
# Blink duration
root.after(150, lambda: end_blink())  # 150ms blink

# Blink interval
root.after(3000, animate_blink)  # 3 seconds between blinks

# Mouth animation cycle
root.after(200, close_mouth)  # Mouth open 200ms
root.after(500, animate_mouth)  # Total cycle 500ms

# Safety timeout
talking_timeout_id = root.after(30000, stop_talking)  # 30 seconds
```

---

## 🔧 Dependencies

### Required Packages

```
pillow>=10.0.0     # Image processing & manipulation
websockets>=12.0   # WebSocket client
tkinter            # GUI framework (built-in with Python)
```

### Installation

```powershell
pip install -r requirements.txt
```

**Note:** `tkinter` comes pre-installed with most Python distributions.

---

## 🛠️ Development

### Test Animations

```powershell
python test_animations.py
```

**What it does:**
- Cycles through all 6 emotions (2 seconds each)
- Tests talking animation for 5 seconds
- Demonstrates blinking
- Right-click to close

**Use for:**
- Verifying emotion images are correct
- Testing animation timing
- Checking layer alignment

### Verify Assets

```powershell
python check_images.py
```

**Output:**
```
=== Checking Image Properties ===

base.png:
  Mode: RGBA
  Size: (400, 400)
  Format: PNG
  Has transparency: True
  Has visible content: True

eyes_closed.png:
  Mode: RGBA
  Size: (400, 400)
  Format: PNG
  Has transparency: True
  Has visible content: True
```

**Use for:**
- Ensuring all required images exist
- Verifying transparency is present
- Checking image formats and sizes

### Custom WebSocket Server

Edit `main.py`:

```python
WS_URL = "ws://your-server:port/ws/chat"
```

### Debugging

**Enable verbose logging:**

Edit `main.py` to log all messages:

```python
async def listen_to_backend(self):
    # ...
    msg = await ws.recv()
    print(f"🔵 [WS DEBUG] {msg}")  # Log everything
```

**Check connection:**
```python
# In main.py, add before websockets.connect():
print(f"Attempting to connect to: {WS_URL}")
```

---

## 🐛 Troubleshooting

### Window Not Appearing

**Symptoms:** Overlay doesn't show up on screen

**Solutions:**
1. Check if backend is running: `http://127.0.0.1:8000`
2. Verify images exist in `assets/` folder (use `check_images.py`)
3. Check console for error messages
4. Ensure Windows 10/11 for transparency support
5. Try moving window (might be off-screen): Edit spawn position in code

### Images Not Loading

**Symptoms:** Blank window, errors in console

**Solutions:**
1. Run `check_images.py` to verify all assets exist
2. Ensure PNGs are valid and not corrupted
3. Check file permissions (read access required)
4. Verify image dimensions are consistent
5. Ensure files are named correctly (case-sensitive on some systems)

### Animations Not Working

**Symptoms:** No mouth movement, no blinking, no emotion changes

**Solutions:**
1. **Talking not animating:**
   - Check WebSocket connection (console shows "Connected")
   - Verify backend sends `[SPEECH_START]` (enable debug logging)
   - Test with `test_animations.py`
   - Check if safety timeout triggered (30s limit)

2. **Blinking not working:**
   - Check if `eyes_closed.png` exists
   - Verify alignment with base images
   - Look for errors in console

3. **Emotions not changing:**
   - Check if emotion images exist in `assets/`
   - Verify backend sends `[EMOTION]<name>` messages
   - Enable debug logging in `main.py`
   - Test with `test_animations.py`

### WebSocket Connection Issues

**Symptoms:** "Could not connect to backend" messages

**Solutions:**
1. Start backend first: `uvicorn backend.app.main:app --reload`
2. Verify backend is on port 8000
3. Check firewall settings
4. Ensure no other app is using port 8000
5. Try restarting both backend and overlay

### Window Behind Other Windows

**Symptoms:** Overlay doesn't stay on top

**Solutions:**
1. Restart overlay
2. Check `root.attributes("-topmost", True)` is set
3. Click window to bring to front
4. Some fullscreen apps may override topmost

### High CPU Usage

**Symptoms:** Excessive CPU usage from overlay

**Solutions:**
1. Check for infinite loops in console logs
2. Reduce animation update frequency
3. Ensure images are appropriately sized (not huge)
4. Close overlay when not needed

### Transparency Not Working

**Symptoms:** White background visible instead of transparent

**Solutions:**
1. Windows 10/11 required for color-key transparency
2. Verify `root.attributes("-transparentcolor", "white")` is set
3. Ensure background elements in images are actually transparent
4. Check DWM (Desktop Window Manager) is running

---

## 📊 Performance

### Resource Usage

- **CPU:** <2% idle, ~3-5% during animations
- **Memory:** 50-100 MB (depends on image sizes)
- **GPU:** Minimal (basic 2D compositing)
- **Network:** <1 KB/s (WebSocket messages only)

### Response Times

- **Emotion Change:** <10ms after WebSocket message
- **Speech Start/Stop:** <10ms after signal
- **Blink Animation:** 150ms duration
- **Mouth Animation:** 500ms cycle (200ms open, 300ms closed)

### Optimization Tips

1. **Image Size:** Keep images at 400x400 or smaller
2. **File Format:** PNG with optimized compression
3. **Update Frequency:** Don't update faster than 60 FPS
4. **Resource Cleanup:** Close overlay when not in use

---

## 💡 Tips & Best Practices

### Positioning

- **Multiple Monitors:** Window spawns on primary monitor by default
- **Off-Screen Recovery:** Edit spawn position in code if window is lost
- **Common Positions:** 
  - Bottom-right: `geometry(f"+{screen_width-450}+{screen_height-450}")`
  - Top-left: `geometry(f"+50+50")` (default)
  - Center: Calculate based on screen dimensions

### Asset Creation

- **Vector Graphics:** Use SVG → PNG conversion for scalability
- **Layer Alignment:** Use guides in image editor to ensure perfect overlay
- **Transparency:** Save with alpha channel, not indexed transparency
- **File Size:** Compress PNGs to reduce memory usage

### Integration

- **Voice Modules:** Use `avatar_controller.py` functions
- **Custom Modules:** Import controller and call thread-safe methods
- **External Control:** Send WebSocket messages to backend

### Performance

- **Close When Idle:** Save resources by closing overlay if not actively watching
- **Reduce Size:** Smaller window = less GPU/CPU usage
- **Optimize Images:** Use tools like TinyPNG to reduce file sizes

---

## 🔗 Integration with Other Modules

### Voice Output Integration

**File:** `voice/voice_output_edge.py`

Voice modules can directly control the avatar:

```python
import sys
sys.path.append("../overlay")
import avatar_controller

# Start talking animation when TTS begins
avatar_controller.on_speech_start()

# Stop animation when TTS ends
avatar_controller.on_speech_end()
```

### Backend Integration

**File:** `backend/app/ws.py`

Backend broadcasts control messages:

```python
# Send emotion
await broadcast_message(f"[EMOTION]{emotion}")

# Start talking
await broadcast_message("[SPEECH_START]")

# Stop talking
await broadcast_message("[SPEECH_END]")
```

### Custom Module Integration

```python
# Import controller (thread-safe)
from overlay import avatar_controller

# Change emotion
avatar_controller.on_emotion("happy")

# Control speech
avatar_controller.on_speech_start()
# ... do TTS ...
avatar_controller.on_speech_end()
```

---

## 📚 Related Documentation

- **[Main README](../README.md)** - Project overview
- **[Backend README](../backend/README.md)** - Emotion system and WebSocket protocol
- **[Voice README](../voice/README.md)** - Voice output integration
- **[Codebase Structure](../docs/CODEBASE_STRUCTURE.md)** - Full architecture

---

## 🚀 Future Enhancements

### Potential Features

- [ ] Persistent window position (save/load from config)
- [ ] Mouse-over tooltips or reactions
- [ ] Idle animations (subtle movements when not talking)
- [ ] Multiple avatar skins/themes
- [ ] Size adjustment via UI (not just code)
- [ ] System tray integration (minimize to tray)
- [ ] Desktop widget mode (pinned to desktop)
- [ ] Emotion transition animations (smooth morphing)

### Customization Ideas

- **Live2D Integration:** Replace static images with Live2D model
- **Eye Tracking:** Avatar looks at mouse cursor
- **Weather Reactions:** Changes expression based on local weather
- **Time of Day:** Different expressions for morning/night
- **Screen Recording:** Disable during screen capture

---

**Version:** 2.0  
**Status:** Stable ✅  
**Tested With:** Python 3.10+, Windows 10/11  
**License:** See [LICENSE](../LICENSE)
