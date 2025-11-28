"""Speech-to-Text service using OpenAI Whisper"""
# from emergentintegrations.llm.openai import OpenAISpeechToText
import os
import logging
from io import BytesIO

logger = logging.getLogger(__name__)


class AudioService:
    """Handles audio transcription using Whisper"""
    
    def __init__(self):
        api_key = os.getenv("EMERGENT_LLM_KEY")
        if not api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment")
        self.stt = OpenAISpeechToText(api_key=api_key)
    
    async def transcribe_audio(self, audio_data: bytes, language: str = None) -> dict:
        """
        Transcribe audio to text
        
        Args:
            audio_data: Audio file bytes
            language: Optional language code ('en', 'he', etc.)
        
        Returns:
            dict with 'text' and optional 'language'
        """
        try:
            audio_file = BytesIO(audio_data)
            audio_file.name = "audio.webm"  # Whisper needs a filename
            
            # Transcribe with Whisper
            response = await self.stt.transcribe(
                file=audio_file,
                model="whisper-1",
                response_format="json",
                language=language  # None for auto-detection
            )
            
            logger.info(f"Transcription successful: {response.text[:50]}...")
            
            return {
                "text": response.text,
                "language": language or "auto"
            }
            
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            raise Exception(f"Failed to transcribe audio: {str(e)}")
