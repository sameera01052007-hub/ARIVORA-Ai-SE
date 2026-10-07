import re
import hashlib
from pathlib import Path
from typing import Dict, Any
from gtts import gTTS

from config import VOICE_DIR

class VoiceService:
    """
    ARIVORA AI Voice & Multilingual Speech Synthesis Engine.
    Generates audio explanations in Tamil, Tanglish, English, Hindi, Telugu, Malayalam, Kannada, etc.
    using Google Text-to-Speech (gTTS).
    """

    LANG_MAP = {
        "tamil": "ta", "ta": "ta", "தமிழ்": "ta",
        "tanglish": "ta", "thanglish": "ta", "ta-en": "ta", "tamil+english": "ta", "தாங்க்லீஷ்": "ta",
        "english": "en", "en": "en",
        "hindi": "hi", "hi": "hi", "हिंदी": "hi",
        "telugu": "te", "te": "te", "తెలుగు": "te",
        "malayalam": "ml", "ml": "ml", "മലയാളം": "ml",
        "kannada": "kn", "kn": "kn", "கன்னடம்": "kn", "கன்னடா": "kn",
        "bengali": "bn", "bn": "bn",
        "marathi": "mr", "mr": "mr",
        "french": "fr", "fr": "fr",
        "spanish": "es", "es": "es",
        "german": "de", "de": "de"
    }

    def __init__(self):
        self.voice_dir = VOICE_DIR

    def generate_speech(self, text: str, language: str = "en") -> Dict[str, Any]:
        """
        Synthesizes an audio MP3 from text in any supported language (Tamil, Tanglish, English, Hindi, etc.).
        Caches previously generated audio using content hash.
        """
        clean_text = re.sub(r"[\*#_`~=\+\-\|\{\}\[\]\(\)]", " ", text)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        # Keep speech snippet concise for fast synthesis (first 400 chars)
        speech_snippet = clean_text[:400]

        lang_lower = (language or "en").lower().strip()
        lang_code = self.LANG_MAP.get(lang_lower, "en")

        # Accent TLD optimization
        tld = "co.in" if lang_code in ["en", "ta", "hi"] else "com"

        # Content hash for caching
        content_hash = hashlib.md5(f"{speech_snippet}_{lang_code}".encode("utf-8")).hexdigest()[:12]
        filename = f"arivora_ai_{lang_code}_{content_hash}.mp3"
        output_path = self.voice_dir / filename

        if not output_path.exists():
            try:
                tts = gTTS(text=speech_snippet, lang=lang_code, tld=tld, slow=False)
                tts.save(str(output_path))
            except Exception as e:
                # Fallback attempt with default Indian English accent if primary fails
                try:
                    tts = gTTS(text=speech_snippet, lang="en", tld="co.in", slow=False)
                    tts.save(str(output_path))
                except Exception as ex:
                    return {
                        "success": False,
                        "error": str(ex),
                        "filename": None,
                        "audio_url": None
                    }

        lang_display_names = {
            "ta": "Tamil / Tanglish",
            "en": "English",
            "hi": "Hindi",
            "te": "Telugu",
            "ml": "Malayalam",
            "kn": "Kannada"
        }

        return {
            "success": True,
            "filename": filename,
            "audio_url": f"/api/voice-audio/{filename}",
            "language": lang_display_names.get(lang_code, language.title()),
            "text_spoken": speech_snippet
        }

    def save_uploaded_voice_note(self, file_bytes: bytes, filename: str, username: str) -> str:
        """Saves a student or faculty recorded audio note."""
        safe_user = re.sub(r"[^a-zA-Z0-9_-]", "_", username)
        user_voice_dir = self.voice_dir / safe_user
        user_voice_dir.mkdir(parents=True, exist_ok=True)

        safe_filename = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)
        target = user_voice_dir / safe_filename
        with open(target, "wb") as f:
            f.write(file_bytes)

        return str(target.name)

voice_service = VoiceService()
