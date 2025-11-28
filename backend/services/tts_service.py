"""Text-to-Speech service using OpenAI TTS"""
import os
import logging
import base64
from openai import OpenAI

logger = logging.getLogger(__name__)

class TTSService:
    """Handles text-to-speech conversion"""
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY") or os.getenv("OPENAI_API_KEY")
        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            logger.info("TTSService: OpenAI TTS client initialized")
        else:
            logger.warning("TTSService: No API key - using mock mode")
    
    async def text_to_speech(self, text: str, voice: str = "nova") -> bytes:
        """Convert text to speech audio"""
        if not self.client:
            # MOCK MODE - 1 second silence WAV
            logger.info(f"TTS MOCK: {text[:50]}...")
            # Valid WAV base64 (silence)
            return base64.b64decode("UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAo")
        
        # REAL OpenAI TTS
        try:
            response = await self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text[:4000]  # Max length
            )
            logger.info(f"TTS generated {len(response.content)} bytes")
            return response.content
        except Exception as e:
            logger.error(f"TTS failed: {str(e)}")
            raise Exception(f"TTS failed: {str(e)}")
