# 🎙️ Voice - Alisa Assistant

Voice input/output system with speech recognition, text-to-speech, and optional RVC voice conversion.

**Last Updated:** January 17, 2026

---

## 📋 Overview

The voice module provides natural conversation capabilities:

- **Speech-to-Text (STT)** - Faster Whisper for accurate, low-latency transcription
- **Text-to-Speech (TTS)** - Microsoft Edge TTS with customizable voices
- **RVC Voice Conversion** - Optional anime-style voice transformation (advanced)
- **Audio Processing** - Real-time audio capture and playback via PyGame
- **Multiple Interfaces** - Text chat with voice output OR full voice conversation
- **Overlay Integration** - Synchronized avatar animations via WebSocket
- **Emotion Support** - Text cleaning and emotion extraction for natural speech

---

## 🚀 Quick Start

### Text Chat (Text Input + Voice Output)

Best for: Development, testing, or when you don't want to speak

```powershell
# From project root
.\scripts\start_text_chat.ps1

# Or manually
cd voice
pip install -r requirements.txt
python text_chat.py
```

**Features:**
- Type messages in terminal
- Hear Alisa's voice responses
- Avatar animations (if overlay running)
- No microphone required

### Voice Chat (Full Voice Conversation)

Best for: Natural conversation, hands-free interaction

```powershell
# From project root
.\scripts\start_voice.ps1

# Or manually
cd voice
python voice_chat_optimized.py
```

**Features:**
- Press Enter to speak into microphone
- Automatic speech recognition
- Voice responses with avatar sync
- Continuous conversation loop

### Requirements

- **Backend server** running on `ws://127.0.0.1:8000/ws/chat`
- **Microphone** (for voice input mode)
- **Audio output device** (speakers/headphones)
- **Python 3.10+**

---

## 📁 Structure

```
voice/
├── text_chat.py             # Text input + voice output interface
├── voice_chat_optimized.py  # Full voice conversation interface
├── voice_input.py           # Faster Whisper STT engine
├── voice_output_edge.py     # Edge TTS (recommended, default)
├── voice_output_rvc.py      # Edge TTS + RVC conversion (advanced)
├── voice_config.py          # Voice customization settings
├── install_voice.ps1        # Automated dependency installer
├── rvc/                     # RVC voice conversion (optional)
│   ├── inferencer.py        # RVC inference wrapper
│   ├── weights/             # Model weights (.pth files)
│   └── index/               # Feature index (.index files)
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## 🎤 Speech-to-Text (STT)

### Technology: Faster Whisper

Faster Whisper is an optimized implementation of OpenAI's Whisper model for speech recognition.

**Features:**
- ✅ High accuracy transcription
- ✅ Fast inference (~1-2 seconds per utterance)
- ✅ GPU acceleration support (CUDA)
- ✅ Multiple language support
- ✅ Works offline (no API calls)
- ✅ Noise robustness

**Model Sizes:**

| Model | Size | Accuracy | Speed (CPU) | Speed (GPU) |
|-------|------|----------|-------------|-------------|
| `tiny` | 75 MB | Fair | Very Fast | Very Fast |
| `base` | 142 MB | Good | Fast | Fast |
| `small` | 466 MB | **Recommended** | Moderate | Fast |
| `medium` | 1.5 GB | Great | Slow | Moderate |
| `large` | 2.9 GB | Best | Very Slow | Moderate |

**Default:** `small` (best balance of accuracy and speed)

### Configuration

Edit `voice_input.py`:

```python
# Model selection
MODEL_SIZE = "small"  # Change to "base", "medium", "large"

# Audio settings
SAMPLE_RATE = 16000  # Hz (standard for Whisper)
DURATION = 5         # Recording duration in seconds

# Device
DEVICE = "cpu"       # or "cuda" for GPU acceleration
COMPUTE_TYPE = "int8"  # or "float16" for GPU
```

### Usage Example

```python
from voice_input import record_audio, speech_to_text

# Record from microphone
record_audio()

# Transcribe
text = speech_to_text()
print(f"You said: {text}")
```

### GPU Acceleration

**For NVIDIA GPUs (CUDA):**
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

Then update `voice_input.py`:
```python
DEVICE = "cuda"
COMPUTE_TYPE = "float16"
```

**Performance Improvement:**
- CPU: ~3-5 seconds per utterance
- GPU: ~1-2 seconds per utterance

---

## 🗣️ Text-to-Speech (TTS)

### Technology: Microsoft Edge TTS

Edge TTS provides natural-sounding voices using Microsoft's neural text-to-speech.

**Features:**
- ✅ Natural, human-like voices
- ✅ Low latency (~500ms generation)
- ✅ No API key required (free)
- ✅ 200+ voices in 100+ languages
- ✅ SSML support for prosody control
- ✅ Offline capable after initial download

### Default Voice

**`en-US-AnaNeural`** - Young, bright, energetic English voice (recommended for Alisa)

### Available Voice Options

Edit `voice_config.py` to select your preferred voice:

#### English Voices (Sorted by Cuteness)

| Voice ID | Description | Best For |
|----------|-------------|----------|
| `ana` | Young, bright, energetic | ⭐ **Recommended** - Most anime-like |
| `jenny` | Neural, clear, professional | Natural conversation |
| `aria` | Friendly, conversational | Casual chat |
| `michelle` | Young adult, clear | Professional but friendly |

#### Japanese Voices (Maximum Kawaii 🎌)

| Voice ID | Description | Best For |
|----------|-------------|----------|
| `nanami` | High pitch, most anime-like | ⭐ Ultimate anime experience |
| `aoi` | Cute, youthful | Authentic Japanese voice |

#### Chinese Voices (Cute Options 🎎)

| Voice ID | Description | Best For |
|----------|-------------|----------|
| `xiaoxiao` | Sweet, young-sounding | Mandarin speakers |
| `xiaoyi` | Cute, friendly | Alternative Chinese option |

### Configuration

Edit `voice_config.py`:

```python
# Select voice
SELECTED_VOICE = "ana"  # Change to any voice from VOICE_OPTIONS

# Speech properties
SPEECH_RATE = "+15%"  # Speed: -50% to +100%
PITCH_SHIFT = "+10Hz"  # Pitch: -20Hz to +20Hz

# Emotion-specific prosody (optional)
EMOTION_PROSODY = {
    "happy": {"rate": "+15%", "pitch": "+8Hz"},
    "sad": {"rate": "-10%", "pitch": "-5Hz"},
    "angry": {"rate": "+20%", "pitch": "+10Hz"},
    "neutral": {"rate": "+10%", "pitch": "+5Hz"},
}
```

### List All Available Voices

```powershell
edge-tts --list-voices | Select-String "Neural"
```

### Usage Example

```python
from voice_output_edge import speak_async
import asyncio

# Speak text asynchronously
asyncio.run(speak_async("Hello! I'm Alisa!"))
```

---

## 🎨 RVC Voice Conversion (Advanced)

### What is RVC?

RVC (Retrieval-based Voice Conversion) transforms TTS output into anime-style character voices.

**Process Flow:**
```
Text → Edge TTS (base voice) → RVC Model → Anime Voice
```

**Use Cases:**
- Transform into specific anime character voice
- Create unique, personalized voice
- Match voice to avatar style

### Prerequisites

- **Trained RVC Model** - `.pth` file (model weights)
- **Feature Index** - `.index` file (voice characteristics)
- **PyTorch** - For neural network inference
- **GPU Recommended** - CPU conversion is slow (~5-10 seconds)

### Setup RVC

#### 1. Obtain RVC Model

**Option A: Train Your Own**
- Use [RVC-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)
- Record 10-30 minutes of target voice audio
- Train model (requires GPU, takes hours)
- Export `.pth` and `.index` files

**Option B: Download Pre-trained**
- Find community-trained models online
- Ensure licensing compliance
- Download matching `.pth` and `.index` files

#### 2. Place Model Files

```
voice/rvc/
├── weights/
│   └── alisa.pth          # Your model weights
└── index/
    └── alisa.index        # Your feature index
```

#### 3. Configure Paths

Edit `voice_output_rvc.py`:

```python
MODEL_PATH = "rvc/weights/alisa.pth"
INDEX_PATH = "rvc/index/alisa.index"
```

#### 4. Use RVC Voice

Edit chat scripts to import RVC version:

```python
# In text_chat.py or voice_chat_optimized.py
from voice_output_rvc import speak  # Instead of voice_output_edge
```

### Performance

| Hardware | Conversion Time | Recommendation |
|----------|-----------------|----------------|
| CPU | 5-10 seconds | Not recommended |
| GPU (CUDA) | 1-2 seconds | ✅ Recommended |

### Troubleshooting RVC

**Issue:** Slow conversion on CPU  
**Solution:** Install CUDA or skip RVC, use Edge TTS only

**Issue:** Model not loading  
**Solution:** Check `.pth` and `.index` file paths are correct

**Issue:** Voice quality poor  
**Solution:** Try different base voice or retrain with more data

---

## 💬 Chat Interfaces

### Text Chat (`text_chat.py`)

**Best For:**
- Development and testing
- When microphone unavailable
- Quiet environments
- Precise input control

**Features:**
- ✅ Type messages in terminal
- ✅ Receive voice responses
- ✅ Emotion display and cleaning
- ✅ Avatar animation sync
- ✅ Mode switching (`/mode <name>`)
- ✅ Precise timing control for speech

**Interface:**
```
You: Hello Alisa!
Alisa: Oh, look who finally decided to talk to me. [token streaming...]
💭 Emotion: teasing
🎤 Speaking: Oh, look who finally decided to talk to me.
✅ Speech completed
```

**Commands:**
- Type message and press Enter
- `/mode <name>` - Switch conversation mode
- `exit`, `quit`, `bye` - End chat

### Voice Chat (`voice_chat_optimized.py`)

**Best For:**
- Natural conversation
- Hands-free interaction
- Accessibility
- Immersive experience

**Features:**
- ✅ Press Enter to speak
- ✅ Automatic speech recognition
- ✅ Voice output with avatar sync
- ✅ Emotion emoji display
- ✅ Continuous conversation loop
- ✅ Clean console output (no token spam)

**Interface:**
```
🎤 Press ENTER to speak...
[User presses Enter]
🎤 Listening...
📝 You said: What are you doing?
Just coding. Not like I need your help or anything. 😏
[Alisa speaks response]
```

**Commands:**
- Press Enter to start recording
- Speak for ~5 seconds
- Say "exit", "quit", "bye" to end

### Comparison

| Feature | Text Chat | Voice Chat |
|---------|-----------|------------|
| Input | Keyboard | Microphone |
| Output | Voice + Text | Voice + Text |
| Speed | Instant | ~2-5 seconds |
| Convenience | High precision | Hands-free |
| Use Case | Development | Natural interaction |
| Microphone | Not required | Required |

---

## 🔌 Overlay Integration

### How It Works

Voice modules communicate with overlay via WebSocket messages for synchronized animations.

**Message Flow:**
```
Voice Module → Backend → Overlay
[SPEECH_START] -----> Mouth opens, starts animating
[SPEECH_END] -------> Mouth closes, animation stops
```

### Timing Synchronization

**Critical Feature:** `speak_with_timing()` function ensures perfect sync:

1. **Generate TTS audio** (500ms-1s)
2. **Load audio into PyGame**
3. **Start playback** 🎵
4. **Send `[SPEECH_START]`** (mouth animation begins NOW)
5. **Wait for playback to finish**
6. **Send `[SPEECH_END]`** (mouth animation stops)

This ensures avatar mouth moves exactly when audio plays, not before/after.

### Safety Features

- **30-second timeout** - Auto-stops animation if stuck
- **Duplicate prevention** - Ignores multiple start signals
- **Error handling** - Graceful fallback if overlay unavailable
- **Temporary file cleanup** - Prevents disk filling

### Code Example

```python
async def speak_with_timing(text, ws):
    # Generate TTS
    await tts_generate(text, output_file)
    
    # Load and start playback
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    
    # NOW send animation signal
    await ws.send("[SPEECH_START]")
    
    # Wait for audio to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    # Stop animation
    await ws.send("[SPEECH_END]")
```

---

## 🎭 Emotion Processing

### Text Cleaning

Voice modules clean LLM responses before speaking:

**Input:**
```
<emotion=teasing>teasing
Hmph. I wasn't waiting for you or anything...
```

**Cleaned Output:**
```
Hmph. I wasn't waiting for you or anything...
```

### Cleaning Rules

1. **Remove emotion tags:** `<emotion=...>` stripped
2. **Remove standalone emotion words:** "teasing" at start removed
3. **Preserve content:** Actual message preserved
4. **Whitespace normalization:** Extra spaces/newlines cleaned

### Implementation

```python
def clean_text_for_speech(text: str) -> str:
    # Remove <emotion=...> tags
    text = re.sub(r'<emotion=[^>]+>', '', text)
    
    # List of emotion words
    emotions = ['happy', 'calm', 'teasing', 'serious', 'sad', 'neutral']
    
    # Remove emotion word at start if followed by content
    for emotion in emotions:
        pattern = r'^\s*\b' + re.escape(emotion) + r'\b[\s\n]+'
        match = re.match(pattern, text, flags=re.IGNORECASE)
        if match and text[match.end():].strip():
            text = text[match.end():]
            break
    
    # Clean whitespace
    return ' '.join(text.split()).strip()
```

### Emotion Display

**Text Chat:**
```
💭 Emotion: teasing
```

**Voice Chat:**
```
Message content... 😏
```

Emoji mapping in `voice_chat_optimized.py`:
```python
EMOTION_EMOJI = {
    'happy': '😊',
    'calm': '😌',
    'teasing': '😏',
    'serious': '😐',
    'sad': '😢',
    'neutral': '🙂'
}
```

---

## ⚙️ Configuration

### Voice Customization

Edit `voice_config.py`:

```python
# Voice selection
SELECTED_VOICE = "ana"  # Options: ana, jenny, nanami, xiaoxiao

# Speed adjustment
SPEECH_RATE = "+15%"  # Range: -50% to +100%
# +15% = slightly faster, cuter
# +0% = normal speed
# -10% = slower, more dramatic

# Pitch adjustment
PITCH_SHIFT = "+10Hz"  # Range: -20Hz to +20Hz
# +10Hz = higher pitch, cuter
# +0Hz = natural pitch
# -5Hz = lower pitch, more serious
```

### Microphone Configuration

Test available microphones:

```python
import sounddevice as sd
print(sd.query_devices())
```

Select specific device in `voice_input.py`:

```python
# Use device ID from query_devices()
sd.default.device = 1  # Change to your mic index
```

### Audio Output Configuration

Select output device:

```python
import sounddevice as sd

# List devices
print(sd.query_devices())

# Set output
sd.default.device = (None, 2)  # (input, output)
```

### Performance Tuning

**For Speed:**
```python
# voice_input.py
MODEL_SIZE = "base"  # Faster than "small"
DURATION = 3  # Shorter recording

# voice_config.py
SPEECH_RATE = "+20%"  # Speak faster
```

**For Quality:**
```python
# voice_input.py
MODEL_SIZE = "small"  # Better accuracy
DURATION = 5  # Longer recording window

# voice_config.py
SPEECH_RATE = "+0%"  # Natural speed
```

---

## 🔧 Dependencies

### Core Dependencies

```
edge-tts>=6.1.0         # Text-to-speech engine
pygame>=2.5.0           # Audio playback
websockets              # Backend communication
```

### Speech Recognition Dependencies

```
faster-whisper>=0.10.0  # Speech-to-text engine
sounddevice>=0.4.0      # Microphone input
scipy>=1.10.0           # Audio processing
numpy>=1.24.0           # Array operations
```

### Optional (RVC) Dependencies

```
torch                   # Neural network inference
librosa>=0.10.0        # Audio processing
soundfile>=0.12.0      # Audio file I/O
```

### Installation

**Quick Install:**
```powershell
cd voice
pip install -r requirements.txt
```

**Automated Install:**
```powershell
.\install_voice.ps1
```

**GPU Support (NVIDIA):**
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

---

## 🐛 Troubleshooting

### Microphone Not Working

**Symptoms:** "Could not record audio", no speech detected

**Solutions:**
1. **Check permissions:** Windows Settings → Privacy → Microphone → Allow apps
2. **Test microphone:** `python -c "import sounddevice; print(sounddevice.query_devices())"`
3. **Verify not muted:** Check Windows sound settings
4. **Try different device:** Edit `voice_input.py` device ID
5. **Test recording:** `python voice_input.py` standalone

### No Audio Output

**Symptoms:** No voice heard, silent playback

**Solutions:**
1. **Check volume:** System volume and app volume
2. **Test speakers:** Windows sound test
3. **Test Edge TTS:** `edge-tts --text "Test" --voice en-US-AnaNeural --write-media test.mp3`
4. **Check pygame:** Ensure pygame.mixer initialized
5. **Try different output:** Change audio output device in Windows

### Voice Recognition Inaccurate

**Symptoms:** Transcription wrong, gibberish output

**Solutions:**
1. **Upgrade model:** `MODEL_SIZE = "small"` or `"medium"`
2. **Reduce noise:** Quiet environment, close to mic
3. **Speak clearly:** Enunciate, moderate pace
4. **Adjust duration:** `DURATION = 7` for longer input
5. **Check language:** Set `LANGUAGE = "en"` explicitly
6. **Use GPU:** Faster model allows larger size

### TTS Voice Sounds Robotic

**Symptoms:** Unnatural, stilted speech

**Solutions:**
1. **Try different voice:** `SELECTED_VOICE = "jenny"` or `"nanami"`
2. **Adjust rate:** `SPEECH_RATE = "+0%"` (slower = more natural)
3. **Adjust pitch:** `PITCH_SHIFT = "+0Hz"` (reset to neutral)
4. **Check text:** Punctuation affects prosody
5. **Use RVC:** Anime-style conversion (if configured)

### RVC Conversion Slow

**Symptoms:** 5-10 second delay before speech

**Solutions:**
1. **Use GPU:** Install CUDA, update to `device="cuda"`
2. **Smaller model:** Use lighter RVC model if available
3. **Skip RVC:** Use Edge TTS only: `from voice_output_edge import speak`
4. **Pre-cache:** Generate common phrases ahead of time

### WebSocket Connection Failed

**Symptoms:** "Connection error", "Backend not running"

**Solutions:**
1. **Start backend:** `uvicorn backend.app.main:app --reload`
2. **Check URL:** Verify `WS_URL = "ws://127.0.0.1:8000/ws/chat"`
3. **Firewall:** Allow Python through Windows Firewall
4. **Port in use:** Check nothing else on port 8000
5. **Test connection:** `curl http://127.0.0.1:8000` should return status

### Overlay Animation Desync

**Symptoms:** Mouth animates before/after speech

**Solutions:**
1. **Use `speak_with_timing()`:** Ensures correct timing
2. **Check WebSocket:** Verify `[SPEECH_START]` received
3. **Restart overlay:** Close and reopen overlay
4. **Check logs:** Look for timing messages in console
5. **Audio delay:** Adjust `pygame.mixer.init(buffer=512)` if needed

### High CPU Usage

**Symptoms:** 100% CPU, system slowdown

**Solutions:**
1. **Use smaller model:** `MODEL_SIZE = "tiny"` or `"base"`
2. **Close other apps:** Free up CPU resources
3. **Reduce duration:** `DURATION = 3` for shorter recording
4. **Enable caching:** Reuse detections when possible
5. **Use GPU:** Offload processing from CPU

---

## 📊 Performance

### Typical Latency

| Operation | CPU | GPU (CUDA) |
|-----------|-----|------------|
| Text Input → Voice Output | 1-2s | 1-2s |
| Voice Input → Transcription | 3-5s | 1-2s |
| Voice → Voice (Full Cycle) | 4-7s | 2-4s |
| With RVC Conversion | +5-10s | +1-2s |

### Resource Usage

| Component | CPU % | Memory (MB) | Notes |
|-----------|-------|-------------|-------|
| Faster Whisper (small) | 10-30% | 400-600 | During transcription |
| Edge TTS | <5% | 50-100 | Very efficient |
| PyGame Audio | <5% | 20-50 | Minimal overhead |
| RVC Conversion | 40-80% | 1000-2000 | CPU-intensive |
| RVC (GPU) | <10% | 1500-2500 | GPU offload |

### Optimization Tips

**For Lowest Latency:**
```python
MODEL_SIZE = "base"
SPEECH_RATE = "+20%"
# Skip RVC
```

**For Best Quality:**
```python
MODEL_SIZE = "medium"
SPEECH_RATE = "+0%"
# Use RVC with GPU
```

**For Battery Saving:**
```python
MODEL_SIZE = "tiny"
DURATION = 3
# Use Edge TTS only
```

---

## 🎯 Use Cases

### 1. Development Companion

```powershell
.\scripts\start_text_chat.ps1
```

Type questions while coding, get spoken explanations without breaking focus.

### 2. Study Assistant

```powershell
.\scripts\start_text_chat.ps1
/mode study
```

Ask complex questions, hear detailed explanations with emotion.

### 3. Hands-Free Interaction

```powershell
.\scripts\start_voice.ps1
```

Speak while working with hands occupied, ideal for hardware projects or cooking.

### 4. Accessibility

Voice chat enables interaction for users with:
- Visual impairments (audio responses)
- Mobility limitations (hands-free input)
- Typing difficulties (speech input)

### 5. Immersive Roleplay

```powershell
.\scripts\start_voice.ps1
/mode chill
```

Natural conversation with anime-style voice and animated avatar.

---

## 💡 Tips & Best Practices

### For Best Voice Recognition

- **Position:** 6-12 inches from microphone
- **Environment:** Quiet room, minimal background noise
- **Speech:** Clear enunciation, moderate pace
- **Microphone:** Use quality mic, not laptop built-in
- **Settings:** Start with `base` model, upgrade if needed

### For Natural Speech Output

- **Voice Selection:** Try multiple voices to find favorite
- **Speed:** Slightly faster (+10-15%) sounds more natural
- **Pitch:** Small adjustments (+5-10Hz) for personality
- **Punctuation:** Use in prompts to control prosody
- **Emotion:** Let LLM include emotion tags for variety

### For Performance

- **GPU:** Massive improvement for Whisper and RVC
- **Model Size:** `base` for speed, `small` for balance
- **Caching:** Reuse common phrases if possible
- **Background:** Close unnecessary applications
- **Updates:** Keep dependencies updated

### For Development

- **Text Chat First:** Easier debugging than voice
- **Logging:** Enable verbose logs for troubleshooting
- **Testing:** Use `test_voice.py` for isolated tests
- **Gradual:** Add voice after text interface works

---

## 🧪 Testing

### Test TTS Only

```powershell
python -c "from voice_output_edge import speak; speak('Hello, this is a test!')"
```

### Test STT Only

```powershell
python voice_input.py
```

Speaks into mic, shows transcription.

### Test Full Voice Loop

```powershell
python voice_chat_optimized.py
```

End-to-end voice conversation test.

### Test Overlay Sync

1. Start backend
2. Start overlay
3. Start text_chat
4. Type message
5. Verify mouth moves with audio

---

## 📚 Related Documentation

- **[Main README](../README.md)** - Project overview
- **[Backend README](../backend/README.md)** - WebSocket protocol
- **[Overlay README](../overlay/README.md)** - Avatar animation system
- **[Codebase Structure](../docs/CODEBASE_STRUCTURE.md)** - Full architecture

---

## 🚀 Future Enhancements

### Planned Features

- [ ] Wake word detection ("Hey Alisa")
- [ ] Voice activity detection (auto-record when speaking)
- [ ] Multiple language support
- [ ] Voice emotion detection
- [ ] Voice cloning fine-tuning
- [ ] Real-time voice conversion
- [ ] Background noise cancellation

### Potential Improvements

- [ ] Streaming TTS (lower latency)
- [ ] Whisper v3 integration
- [ ] Custom voice training guide
- [ ] Voice preset system
- [ ] Audio effects (reverb, echo)
- [ ] Multi-speaker support

---

**Version:** 2.0  
**Status:** Stable ✅  
**Tested With:** Python 3.10+, Windows 10/11, Edge TTS 6.1+, Faster Whisper 0.10+  
**License:** See [LICENSE](../LICENSE)
