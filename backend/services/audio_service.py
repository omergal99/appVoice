"""Speech-to-Text service using OpenAI Whisper"""
import os
import logging
from io import BytesIO
from typing import Dict, Any
from openai import OpenAI

logger = logging.getLogger(__name__)

class AudioService:
    """Handles audio transcription using Whisper"""
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY") or os.getenv("OPENAI_API_KEY")
        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            logger.info("AudioService: OpenAI Whisper client initialized")
        else:
            logger.warning("AudioService: No API key - using mock mode")
    
    async def transcribe_audio(self, audio_data: bytes, language: str = None) -> dict:
        """Transcribe audio to text"""
        if not self.client:
            # MOCK MODE - Demo responses
            logger.info("AudioService MOCK: Transcribing...")
            mock_texts = {
                "en": "What is Docker? Demo transcription.",
                "he": "[translate:מה זה Docker? תמלול לדוגמה.]",
                None: "Explain REST API."
            }
            return {
                "text": mock_texts.get(language, mock_texts["en"]),
                "language": language or "auto"
            }
        
        # REAL OpenAI Whisper
        try:
            audio_file = BytesIO(audio_data)
            audio_file.name = "audio.webm"
            
            response = await self.client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1",
                response_format="json",
                language=language
            )
            
            logger.info(f"Whisper transcription: {response.text[:50]}...")
            return {
                "text": response.text,
                "language": getattr(response, 'language', language or "auto")
            }
        except Exception as e:
            logger.error(f"Whisper failed: {str(e)}")
            raise Exception(f"Transcription failed: {str(e)}")
