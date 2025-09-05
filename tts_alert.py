# TTS wrapper using espeak (or print fallback)
import subprocess, sys

class TTSWrapper:
    def __init__(self, voice="en"):
        self.voice = voice

    def speak(self, text):
        try:
            subprocess.run(["espeak", text], check=False)
        except Exception:
            # fallback
            print("[TTS]", text)
