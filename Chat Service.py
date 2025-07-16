import logging
from typing import Dict, Any
from ..ml.nlp_processor import NLPProcessor

class ChatService:
    def __init__(self):
        self.nlp_processor = NLPProcessor()
        self.conversation_context = {}  # Stores conversation state
        self.logger = logging.getLogger(__name__)

    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming chat message and generate response"""
        try:
            # Extract user intent and entities
            user_id = message.get('user_id', 'anonymous')
            text = message.get('text', '')
            
            # Process with NLP pipeline
            nlp_result = self.nlp_processor.process(text)
            
            # Generate response based on intent
            response = self._generate_response(nlp_result, user_id)
            
            # Update conversation context
            self._update_context(user_id, nlp_result)
            
            return {
                "text": response,
                "intent": nlp_result.get('intent'),
                "entities": nlp_result.get('entities'),
                "sentiment": nlp_result.get('sentiment')
            }
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            return {"text": "Sorry, I encountered an error. Please try again."}

    def _generate_response(self, nlp_result: Dict[str, Any], user_id: str) -> str:
        """Generate appropriate response based on NLP analysis"""
        # Implementation would use intent and entities to craft response
        return f"I understand you're asking about {nlp_result.get('intent')}. Here's what I can tell you..."

    def _update_context(self, user_id: str, nlp_result: Dict[str, Any]):
        """Maintain conversation context for each user"""
        if user_id not in self.conversation_context:
            self.conversation_context[user_id] = []
        self.conversation_context[user_id].append(nlp_result)