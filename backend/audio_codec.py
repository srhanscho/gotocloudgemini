import audioop
import base64


def twilio_payload_to_gemini_pcm(payload_b64: str) -> bytes:
    """
    Twilio base64 mulaw 8kHz → PCM16 16kHz para Gemini.
    """
    mulaw_8k = base64.b64decode(payload_b64)
    pcm_8k = audioop.ulaw2lin(mulaw_8k, 2)              # mulaw → PCM16 8kHz
    pcm_16k, _ = audioop.ratecv(pcm_8k, 2, 1, 8000, 16000, None)  # 8kHz → 16kHz
    return pcm_16k


def gemini_pcm_to_twilio_payload(pcm: bytes, input_rate: int = 24000) -> str:
    """
    PCM16 de Gemini (default 24kHz) → base64 mulaw 8kHz para Twilio.
    """
    pcm_8k, _ = audioop.ratecv(pcm, 2, 1, input_rate, 8000, None)  # input_rate → 8kHz
    mulaw_8k = audioop.lin2ulaw(pcm_8k, 2)              # PCM16 → mulaw
    return base64.b64encode(mulaw_8k).decode("ascii")
