"""API routes for voice assistant"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from services.audio_service import AudioService
from services.ai_service import AIService
from services.tts_service import TTSService
from models.conversation import Message, Conversation
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/voice", tags=["voice"])

# Initialize services
audio_service = AudioService()
ai_service = AIService()
tts_service = TTSService()


class ProcessQueryRequest(BaseModel):
    text: str
    session_id: str
    language: str = "en"


class SpeakRequest(BaseModel):
    text: str
    voice: str = "nova"


class VoiceResponse(BaseModel):
    text: str
    audio: str  # base64


@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribe audio file to text
    """
    try:
        audio_data = await file.read()
        result = await audio_service.transcribe_audio(audio_data)
        return result
    except Exception as e:
        logger.error(f"Transcription endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process")
async def process_query(request: ProcessQueryRequest):
    """
    Process user query and return AI response
    """
    try:
        response_text = await ai_service.process_query(
            query=request.text,
            session_id=request.session_id,
            language=request.language
        )
        return {"response": response_text}
    except Exception as e:
        logger.error(f"Process query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/speak")
async def text_to_speech(request: SpeakRequest):
    """
    Convert text to speech audio
    """
    try:
        audio_base64 = await tts_service.text_to_speech(
            text=request.text,
            voice=request.voice
        )
        return {"audio": audio_base64}
    except Exception as e:
        logger.error(f"TTS endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask", response_model=VoiceResponse)
async def voice_ask(file: UploadFile = File(...), language: str = "auto"):
    """
    Complete voice flow: transcribe -> process -> speak
    """
    try:
        session_id = str(uuid.uuid4())
        
        # 1. Transcribe audio
        audio_data = await file.read()
        transcription = await audio_service.transcribe_audio(audio_data, language if language != "auto" else None)
        user_text = transcription["text"]
        
        # 2. Process with AI
        response_text = await ai_service.process_query(
            query=user_text,
            session_id=session_id,
            language=language if language != "auto" else "en"
        )
        
        # 3. Convert to speech
        audio_base64 = await tts_service.text_to_speech(response_text)
        
        return VoiceResponse(text=response_text, audio=audio_base64)
        
    except Exception as e:
        logger.error(f"Voice ask error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}")
async def get_conversation_history(session_id: str):
    """
    Get conversation history for a session
    """
    # This endpoint is for future use when implementing persistent storage
    return {"messages": [], "session_id": session_id}
