"""Text-to-Speech service using OpenAI TTS"""
# from emergentintegrations.llm.openai import OpenAITextToSpeech
import os
import logging
import base64

logger = logging.getLogger(__name__)


class TTSService:
    """Handles text-to-speech conversion"""
    
    def __init__(self):
        api_key = os.getenv("EMERGENT_LLM_KEY")
        if not api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment")
        self.tts = OpenAITextToSpeech(api_key=api_key)
    
    async def text_to_speech(self, text: str, voice: str = "nova") -> str:
        """
        Convert text to speech audio
        
        Args:
            text: Text to convert to speech
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
        
        Returns:
            Base64-encoded audio data
        """
        try:
            # Generate speech with TTS-1 (faster for real-time)
            audio_base64 = await self.tts.generate_speech_base64(
                text=text,
                model="tts-1",
                voice=voice,
                response_format="mp3"
            )
            
            logger.info(f"TTS generated successfully with voice: {voice}")
            
            return audio_base64
            
        except Exception as e:
            logger.error(f"TTS generation failed: {str(e)}")
            raise Exception(f"Failed to generate speech: {str(e)}")
