# reporting/voice_alert.py
"""ElevenLabs voice alert integration for RANZR.

Provides a simple wrapper to generate speech from a warning message using the
ElevenLabs API and play it back locally.
"""

import os
import requests
import tempfile
import subprocess

# Load API key from configuration (expects config/settings.yaml to define it)
def _load_api_key():
    try:
        import yaml
        config_path = os.path.join(os.path.dirname(__file__), "..", "config", "settings.yaml")
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        return cfg.get("elevenlabs_api_key")
    except Exception:
        raise RuntimeError("Unable to load ElevenLabs API key from config/settings.yaml")

def generate_voice_alert(message: str, voice_id: str = "EXAVITQu4vr4xnSDxMaL") -> None:
    """Generate and play a voice alert.

    Parameters
    ----------
    message: str
        The text to be spoken.
    voice_id: str, optional
        ElevenLabs voice identifier. Defaults to a generic voice.
    """
    api_key = _load_api_key()
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": message,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.75, "similarity_boost": 0.75},
    }
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    # Save audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(response.content)
        tmp_path = tmp_file.name
    # Play the audio (cross‑platform). Here we use the default system player.
    try:
        if os.name == "nt":
            import ctypes
            # Convert paths to forward slash for mciSendString safety against escape characters
            safe_path = tmp_path.replace('\\', '/')
            
            # Play the audio in the background without launching Windows Media Player
            ctypes.windll.winmm.mciSendStringW(f'open "{safe_path}" type mpegvideo alias ranzraudio', None, 0, None)
            ctypes.windll.winmm.mciSendStringW('play ranzraudio wait', None, 0, None)
            ctypes.windll.winmm.mciSendStringW('close ranzraudio', None, 0, None)
            
            # Clean up the temporary MP3 file after speaking is done
            try:
                os.remove(tmp_path)
            except Exception:
                pass
        else:
            subprocess.run(["open", tmp_path])  # macOS; adjust for Linux if needed
    finally:
        pass
