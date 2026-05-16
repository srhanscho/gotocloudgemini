# AGENTS.md — GoToCloud Voicebot (Gemini Live)

AI phone assistant using **Gemini Live API** (voice-to-voice). Hackathon project. Twilio not yet connected.

## Quick start

```powershell
# Create & activate venv (no venv exists yet — first thing to do)
python -m venv venv
venv\Scripts\pip install -r requirements.txt

# Copy credentials
copy .env.example backend\.env  # then edit GEMINI_API_KEY

# Run standalone voice-to-voice (mic → speaker, real-time)
venv\Scripts\python backend\voice_to_voice.py

# Run FastAPI bridge (Twilio endpoint)
venv\Scripts\python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Run text-in / audio-out tests (single or multi turn)
venv\Scripts\python backend\test_gemini_live_text.py
venv\Scripts\python backend\test_gemini_conversation.py

# Run pytest suite (audio codec conversions only)
venv\Scripts\python -m pytest

# Listen to saved PCM audio
ffplay -f s16le -ar 24000 -ac 1 gemini_response.pcm
```

## Architecture

```
backend/
  __init__.py            # makes backend/ a package
  gemini_live_client.py  # GeminiLiveClient — turn-based wrapper (for Twilio path)
  voice_to_voice.py      # Standalone: mic → Gemini → speaker, 3 concurrent tasks
  main.py                # FastAPI app — WebSocket bridge for Twilio
  audio_codec.py         # mulaw 8kHz ↔ PCM16 16kHz ↔ PCM16 24kHz conversions
  test_gemini_live_text.py       # Standalone: 1-turn text → audio save
  test_gemini_conversation.py    # Standalone: multi-turn text → audio per turn
  .env                   # GEMINI_API_KEY, GEMINI_LIVE_MODEL, PUBLIC_URL, PORT
service/
  __init__.py
  gotocloud_voicebot_tool.py  # GoToCloud KB, function tools, and "Camila" system prompt
tests/
  __init__.py
  test_audio_codec.py    # pytest: codec round-trips
```

## Non-obvious facts

- **`.env` is in `backend/`, not project root.** All scripts load it via `load_dotenv(Path(__file__).parent / ".env")`.
- **Files named `test_*.py` in `backend/` are NOT pytest tests.** They're standalone runner scripts (`asyncio.run(main())` at module level). Run them directly with `python`, never `pytest`.
- **`pytest` only discovers `tests/`** (set in `pytest.ini`). No conftest, no fixtures, no mark system.
- **`voice_to_voice.py`** inserts project root into `sys.path` at line 19 to import `service/`. The FastAPI app (`main.py`) uses package-relative imports (`from .gemini_live_client import`). If you add a new script that imports from `service/`, you need the same `sys.path` trick.
- **`main.py`** loads tools conditionally — if `service/gotocloud_voicebot_tool.py` is missing, it runs Gemini without tools (no crash).
- **Audio codec** uses `audioop` (stdlib, zero dependencies). Multi-step: mulaw 8kHz → PCM16 8kHz → ratecv → PCM16 16kHz (Twilio→Gemini), and reverse for Gemini→Twilio.
- **`gemini_live_client.py`** handles tool calls internally inside `receive_audio()` — it executes the handler, sends the function response back, and continues waiting for audio. The caller just iterates chunks.
- **Gemini Live SDK** (`google-genai`): API version must be `v1beta`. Audio input is via `session.send_realtime_input(audio=types.Blob(...))`, not `session.send()`. Text input is `session.send(input=text, end_of_turn=True)`. Output audio is PCM16 24kHz in `response.server_content.model_turn.parts[*].inline_data.data`. Turn boundaries: `turn_complete` / `interrupted`.
- **Service utterances** are in Spanish (Colombian). The system prompt ("Camila") is for a Colombian cloud services company (GoToCloud). The SDK config and voicebot tools mirror this.

## Two usage patterns

| Pattern | Entrypoint | Use case |
|---------|-----------|----------|
| Real-time bidir | `voice_to_voice.py` | Standalone mic→speaker, VAD-driven |
| Turn-based bridge | `main.py` (FastAPI) | Twilio via WebSocket, uses `GeminiLiveClient` |

## Engram + SDD

Agent instructions are in `~/.config/opencode/opencode.json`. The Gentle AI SDD orchestrator (`gentle-orchestrator`) delegates work to sub-agents. Override models, add profile-specific agents, or set permission rules in `opencode.json` (user-level, not repo-level).
