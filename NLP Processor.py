from transformers import pipeline
from typing import Dict, Any
import logging

class NLPProcessor:
    def __init__(self):
        # Initialize pre-trained models
        self.intent_classifier = pipeline(
            "text-classification",
            model="bert-base-uncased",
            tokenizer="bert-base-uncased"
        )
        self.ner_model = pipeline(
            "ner",
            model="dslim/bert-base-NER",
            tokenizer="dslim/bert-base-NER"
        )
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.logger = logging.getLogger(__name__)

    def process(self, text: str) -> Dict[str, Any]:
        """Process text through NLP pipeline"""
        try:
            # Intent classification
            intent_result = self.intent_classifier(text)
            
            # Named entity recognition
            entities = self.ner_model(text)
            
            # Sentiment analysis
            sentiment = self.sentiment_analyzer(text)
            
            return {
                "text": text,
                "intent": intent_result[0]['label'],
                "intent_score": intent_result[0]['score'],
                "entities": [{"entity": e['entity'], "word": e['word']} for e in entities],
                "sentiment": sentiment[0]['label'],
                "sentiment_score": sentiment[0]['score']
            }
        except Exception as e:
            self.logger.error(f"NLP processing error: {str(e)}")
            return {
                "text": text,
                "intent": "unknown",
                "entities": [],
                "sentiment": "neutral"
            }