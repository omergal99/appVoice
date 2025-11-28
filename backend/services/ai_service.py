"""AI processing service using GPT-5.1"""
# from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
import logging

logger = logging.getLogger(__name__)


class AIService:
    """Handles intelligent query processing with GPT-5.1"""
    
    def __init__(self):
        api_key = os.getenv("EMERGENT_LLM_KEY")
        if not api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment")
        self.api_key = api_key
    
    async def process_query(self, query: str, session_id: str, language: str = "en") -> str:
        """
        Process user query and generate intelligent response
        
        Args:
            query: User's question or statement
            session_id: Unique session identifier
            language: Language code ('en', 'he', etc.)
        
        Returns:
            AI-generated response text
        """
        try:
            # Create system message based on language
            if language == "he":
                system_message = (
                    "אתה עוזר קולי חכם בשם SmartSpeak. "
                    "אתה מתמחה במענה על שאלות טכנולוגיות, תכנות, ארכיטקטורה, אבטחת מידע, ו-Cloud. "
                    "תן תשובות ממוקדות, מקצועיות, וברורות. "
                    "אם השאלה לא טכנולוגית, תן תשובה עוזרת וידידותית."
                )
            else:
                system_message = (
                    "You are SmartSpeak, an intelligent voice assistant. "
                    "You specialize in answering questions about technology, programming, architecture, cybersecurity, and Cloud. "
                    "Provide focused, professional, and clear answers. "
                    "If the question is not technical, give a helpful and friendly response."
                )
            
            # Initialize chat with GPT-5.1
            chat = LlmChat(
                api_key=self.api_key,
                session_id=session_id,
                system_message=system_message
            ).with_model("openai", "gpt-5.1")
            
            # Send user message
            user_message = UserMessage(text=query)
            response = await chat.send_message(user_message)
            
            logger.info(f"AI response generated for session {session_id}")
            
            return response
            
        except Exception as e:
            logger.error(f"AI processing failed: {str(e)}")
            raise Exception(f"Failed to process query: {str(e)}")
