"""AI processing service using GPT"""
import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

class AIService:
    """Handles intelligent query processing"""
    
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY") or os.getenv("OPENAI_API_KEY")
        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            logger.info("AIService: OpenAI GPT client initialized")
        else:
            logger.warning("AIService: No API key - using mock mode")
    
    async def process_query(self, query: str, session_id: str, language: str = "en") -> str:
        """Process user query"""
        if not self.client:
            # MOCK MODE
            logger.info(f"AI MOCK: {query[:30]}...")
            mock_responses = {
                "en": "Docker containers package apps with dependencies. Microservices = independent services via API.",
                "he": "[translate:קונטיינרים של Docker מארזים אפליקציות עם תלויות. מיקרו-שירותים = שירותים עצמאיים דרך API. ]"
            }
            return mock_responses.get(language, mock_responses["en"])
        
        # REAL OpenAI GPT
        try:
            system_message = (
                "You are SmartSpeak, a technical voice assistant expert in programming, architecture, cloud, and cybersecurity."
                if language == "en" else
                "[translate:אתה SmartSpeak, עוזר קולי מומחה בתכנות, ארכיטקטורה, ענן ואבטחת מידע.]"
            )
            
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",  # or gpt-5.1 later
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": query}
                ],
                max_tokens=300
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"GPT failed: {str(e)}")
            raise Exception(f"AI processing failed: {str(e)}")
