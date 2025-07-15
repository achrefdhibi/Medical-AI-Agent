from typing import Dict, List
from langchain.tools import tool
from rag.retriever import MedicalRetriever
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MedicalTools:
    def __init__(self, retriever: MedicalRetriever):
        self.retriever = retriever
        logger.info("Initialized MedicalTools")
    
    @tool
    def search_medical_docs(self, query: str, domain: str = None) -> str:
        """Recherche dans les documents médicaux"""
        context = self.retriever.get_context_for_query(query, domain)
        logger.info(f"Searched medical docs for query: {query}, domain: {domain}")
        return context
    
    @tool
    def summarize_medical_info(self, text: str) -> str:
        """Résume les informations médicales"""
        sentences = text.split('.')
        if len(sentences) <= 3:
            logger.info("Text too short for summarization")
            return text
        
        summary = '. '.join(sentences[:3]) + '.'
        logger.info("Generated summary")
        return summary
    
    @tool
    def identify_medical_domain(self, query: str) -> str:
        """Identifie le domaine médical d'une requête"""
        domains = {
            "autism": ["autism", "autisme", "tsa", "spectre autistique"],
            "diabete": ["diabète", "diabetes", "glycémie", "insuline"],
            "nutrition": ["nutrition", "alimentation", "régime", "nutriments"],
            "pcos": ["pcos", "ovaires polykystiques", "sopk"],
            "psychology": ["psychologie", "mental", "comportement", "thérapie"],
            "radiology": ["radiologie", "imagerie", "scanner", "irm", "radio"]
        }
        
        query_lower = query.lower()
        for domain, keywords in domains.items():
            if any(keyword in query_lower for keyword in keywords):
                logger.info(f"Identified domain: {domain} for query: {query}")
                return domain
        
        logger.info(f"No specific domain identified for query: {query}, using 'general'")
        return "general"