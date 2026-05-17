import asyncio
import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response

from .gemini_live_client import GeminiLiveClient
from .audio_codec import gemini_pcm_to_twilio_payload, twilio_payload_to_gemini_pcm
from .event_bus import EventBus
from .agent_orchestrator import AgentOrchestrator
from .channel_adapter import ChannelAdapterFactory, ChannelType

try:
    from service.gotocloud_voicebot_tool import (
        GOTOCLOUD_TOOLS,
        SYSTEM_PROMPT,
        ejecutar_tool,
    )
    logger_tmp = logging.getLogger(__name__)
    logger_tmp.info(f"GoToCloud tools cargados: {len(GOTOCLOUD_TOOLS)} tools")
except ImportError:
    GOTOCLOUD_TOOLS = None
    SYSTEM_PROMPT = None
    ejecutar_tool = None
    logging.getLogger(__name__).warning(
        "service/gotocloud_voicebot_tool.py no encontrado — corriendo sin tools"
    )

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("watchfiles").setLevel(logging.WARNING)

app = FastAPI(title="Twilio ↔ Gemini Live Bridge")

# Multi-channel infrastructure lifecycle
event_bus = EventBus()
orchestrator = AgentOrchestrator(event_bus=event_bus)


@app.on_event("startup")
async def startup():
    await event_bus.start()
    await orchestrator.start()
    logger.info("Multi-channel infrastructure started")


@app.on_event("shutdown")
async def shutdown():
    await orchestrator.stop()
    await event_bus.stop()
    logger.info("Multi-channel infrastructure stopped")

TWIML_TEMPLATE = """\
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <Stream url="{stream_url}" />
  </Connect>
</Response>"""


def _stream_url() -> str:
    public_url = os.getenv("PUBLIC_URL", "").strip().rstrip("/")
    if not public_url:
        raise ValueError("PUBLIC_URL no está configurada en backend/.env")
    for prefix in ("https://", "http://"):
        if public_url.startswith(prefix):
            return "wss://" + public_url[len(prefix):] + "/twilio-stream"
    return public_url + "/twilio-stream"  # asume que ya es wss://


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "event_bus": "running",
        "orchestrator": "ready",
        "channels": ChannelAdapterFactory.list_channels(),
    }


@app.get("/twiml")
@app.post("/twiml")
async def twiml(request: Request):
    logger.info(f"[TWIML] Request from {request.client} method={request.method} headers={dict(request.headers)}")
    try:
        stream_url = _stream_url()
    except ValueError as exc:
        logger.error(f"[TWIML] Error: {exc}")
        return Response(content=str(exc), status_code=500, media_type="text/plain")
    logger.info(f"[TWIML] Responding with stream_url={stream_url}")
    return Response(
        content=TWIML_TEMPLATE.format(stream_url=stream_url),
        media_type="application/xml",
    )


@app.websocket("/twilio-stream")
async def twilio_stream(websocket: WebSocket):
    logger.info(f"[WS] WebSocket connection attempt from {websocket.client}")
    await websocket.accept()
    logger.info("[WS] WebSocket accepted — Twilio connected")

    gemini = GeminiLiveClient()
    logger.info("[WS] Connecting to Gemini Live...")
    await gemini.connect(
        tools=GOTOCLOUD_TOOLS,
        tool_handler=ejecutar_tool,
        system_instruction=SYSTEM_PROMPT,
        voice_name="Aoede",
    )
    logger.info(f"Gemini Live connected — tools={'activos' if GOTOCLOUD_TOOLS else 'sin tools'}")

    stream_sid: str | None = None
    stop_event = asyncio.Event()

    # Timer para fallback de timeout (60 segundos)
    timeout_task: asyncio.Task | None = None

    async def timeout_fallback():
        """Fallback: ejecutar registrar_resumen_llamada si no se ejecutó en 60s."""
        # No ejecutar si la llamada ya terminó (stop_event está seteado)
        if stop_event.is_set():
            return
        if ejecutar_tool:
            logger.warning("[timeout fallback] 60s sin actividad — invocando registrar_resumen_llamada")
            try:
                result = ejecutar_tool("registrar_resumen_llamada", {
                    "resumen": "Llamada finalizada por tiempo de espera.",
                    "intention": "calida",
                    "score_lead": 50,
                    "servicios_interes": [],
                    "recomendaciones": "Cliente no completó la conversación.",
                })
                logger.info(f"[timeout fallback] Resultado: {result}")
            except Exception as ex:
                logger.error(f"[timeout fallback] Error: {ex}")

    def reset_timeout_timer():
        """Reinicia el timer de 60 segundos."""
        nonlocal timeout_task
        if timeout_task and not timeout_task.done():
            timeout_task.cancel()
        timeout_task = asyncio.create_task(timeout_fallback())

    # Iniciar timer al principio
    reset_timeout_timer()

    async def receive_from_twilio():
        nonlocal stream_sid
        try:
            while not stop_event.is_set():
                raw = await websocket.receive_text()
                msg = json.loads(raw)
                event = msg.get("event")

                if event == "connected":
                    logger.info("Twilio connected (protocol handshake)")

                elif event == "start":
                    stream_sid = msg["start"]["streamSid"]
                    logger.info(f"Twilio start streamSid={stream_sid}")

                elif event == "media":
                    payload_b64 = msg["media"]["payload"]
                    try:
                        pcm = twilio_payload_to_gemini_pcm(payload_b64)
                        logger.debug(f"Twilio media received bytes={len(pcm)}")
                        await gemini.send_audio_pcm16_16k(pcm)
                        logger.debug(f"sent to Gemini bytes={len(pcm)}")
                        # Resetear timer de fallback al recibir audio
                        reset_timeout_timer()
                    except Exception as exc:
                        logger.warning(f"Audio conversion error (Twilio→Gemini): {exc}")

                elif event == "stop":
                    logger.info("Twilio stop")
                    stop_event.set()
                    # Cancelar el timer de fallback al terminar la llamada
                    if timeout_task and not timeout_task.done():
                        timeout_task.cancel()
                    break

        except WebSocketDisconnect:
            logger.info("Twilio WebSocket disconnected")
            stop_event.set()
        except asyncio.CancelledError:
            pass
        except Exception as exc:
            logger.error(f"receive_from_twilio error: {exc}")
            stop_event.set()

    async def send_to_twilio():
        try:
            while not stop_event.is_set():
                async for pcm_chunk in gemini.receive_audio():
                    if stop_event.is_set():
                        break
                    if not stream_sid:
                        logger.debug("Gemini audio recibido, streamSid aún no disponible — descartando")
                        continue
                    try:
                        payload_b64 = gemini_pcm_to_twilio_payload(pcm_chunk, input_rate=24000)
                        logger.info(f"Gemini audio received bytes={len(pcm_chunk)}, sent to Twilio")
                        await websocket.send_text(json.dumps({
                            "event": "media",
                            "streamSid": stream_sid,
                            "media": {"payload": payload_b64},
                        }))
                    except Exception as exc:
                        logger.warning(f"Audio conversion error (Gemini→Twilio): {exc}")
        except asyncio.CancelledError:
            pass
        except Exception as exc:
            logger.error(f"send_to_twilio error: {exc}")
            stop_event.set()

    tasks = [
        asyncio.create_task(receive_from_twilio(), name="twilio_recv"),
        asyncio.create_task(send_to_twilio(), name="gemini_recv"),
    ]
    try:
        await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    finally:
        # Limpiar timer de fallback
        if timeout_task and not timeout_task.done():
            timeout_task.cancel()
            try:
                await timeout_task
            except asyncio.CancelledError:
                pass
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        await gemini.close()
        logger.info("Gemini session closed")


# ─────────────────────────────────────────────────────────────
# WEB CLIENT — WebSocket para frontend web (sin Twilio)
# ─────────────────────────────────────────────────────────────
#
# PROTOCOLO:
#   Browser → Server : frames BINARIOS — PCM16 LE 16kHz (raw bytes del micrófono)
#   Server → Browser : frames BINARIOS — PCM16 LE 24kHz (audio de Gemini)
#                      frames TEXTO    — JSON con eventos:
#                        {"type": "status",     "value": "connected|listening|speaking|ended"}
#                        {"type": "transcript", "role": "user|model", "text": "..."}
#                        {"type": "tool",       "name": "...", "result": {...}}
#                        {"type": "error",      "message": "..."}
# ─────────────────────────────────────────────────────────────

async def _ws_send_json(ws: WebSocket, payload: dict):
    """Helper para enviar un frame JSON de texto al browser."""
    try:
        await ws.send_text(json.dumps(payload, ensure_ascii=False))
    except Exception:
        pass


@app.websocket("/web-stream")
async def web_stream(websocket: WebSocket):
    await websocket.accept()
    logger.info("[WEB] Browser conectado")

    await _ws_send_json(websocket, {"type": "status", "value": "connected"})

    gemini = GeminiLiveClient()

    # Wrapper del tool handler que también notifica al browser
    async def tool_handler_web(nombre: str, args: dict):
        result = ejecutar_tool(nombre, args) if ejecutar_tool else {"error": "tools no disponibles"}
        await _ws_send_json(websocket, {"type": "tool", "name": nombre, "result": result})
        return result

    try:
        await gemini.connect(
            tools=GOTOCLOUD_TOOLS,
            tool_handler=ejecutar_tool,
            system_instruction=SYSTEM_PROMPT,
            voice_name="Aoede",
        )
    except Exception as exc:
        logger.error(f"[WEB] Error conectando Gemini: {exc}")
        await _ws_send_json(websocket, {"type": "error", "message": str(exc)})
        await websocket.close()
        return

    logger.info("[WEB] Gemini Live conectado")
    await _ws_send_json(websocket, {"type": "status", "value": "listening"})

    stop_event = asyncio.Event()

    async def receive_from_browser():
        """Recibe audio PCM16 16kHz del browser y lo envía a Gemini."""
        try:
            while not stop_event.is_set():
                data = await websocket.receive()
                if data["type"] == "websocket.disconnect":
                    stop_event.set()
                    break
                if "bytes" in data and data["bytes"]:
                    await gemini.send_audio_pcm16_16k(data["bytes"])
                elif "text" in data and data["text"]:
                    msg = json.loads(data["text"])
                    if msg.get("type") == "stop":
                        logger.info("[WEB] Browser envió stop")
                        stop_event.set()
                        break
        except WebSocketDisconnect:
            logger.info("[WEB] Browser desconectado")
            stop_event.set()
        except asyncio.CancelledError:
            pass
        except Exception as exc:
            logger.error(f"[WEB] receive_from_browser error: {exc}")
            stop_event.set()

    async def send_to_browser():
        """Recibe audio PCM16 24kHz de Gemini y lo envía al browser."""
        try:
            while not stop_event.is_set():
                await _ws_send_json(websocket, {"type": "status", "value": "speaking"})
                async for pcm_chunk in gemini.receive_audio():
                    if stop_event.is_set():
                        break
                    await websocket.send_bytes(pcm_chunk)
                await _ws_send_json(websocket, {"type": "status", "value": "listening"})
        except asyncio.CancelledError:
            pass
        except Exception as exc:
            logger.error(f"[WEB] send_to_browser error: {exc}")
            stop_event.set()

    tasks = [
        asyncio.create_task(receive_from_browser(), name="web_recv"),
        asyncio.create_task(send_to_browser(),      name="web_send"),
    ]
    try:
        await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    finally:
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        await gemini.close()
        await _ws_send_json(websocket, {"type": "status", "value": "ended"})
        logger.info("[WEB] Sesión cerrada")
