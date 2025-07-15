from typing import List, Dict
from langchain.schema import Document
from .vector_store import VectorStore
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MedicalRetriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        logger.info("Initialized MedicalRetriever")
    
    def retrieve_relevant_docs(self, query: str, domain: str = None, k: int = 5) -> List[Document]:
        """Récupère les documents pertinents pour une requête"""
        results = self.vector_store.search(query, k=k*2)  # Récupérer plus pour filtrer
        
        relevant_docs = []
        for doc, score in results:
            # Filtrer par domaine si spécifié
            if domain and doc.metadata.get("domain") != domain:
                continue
            
            # Seuil de pertinence
            if score < 1.0:  # Ajuster selon les besoins
                relevant_docs.append(doc)
        
        logger.info(f"Retrieved {len(relevant_docs)} relevant documents for query: {query}")
        return relevant_docs[:k]
    
    def get_context_for_query(self, query: str, domain: str = None) -> str:
        """Obtient le contexte formaté pour une requête"""
        docs = self.retrieve_relevant_docs(query, domain)
        
        context = ""
        for doc in docs:
            context += f"Source: {doc.metadata.get('source', 'Unknown')}\n"
            context += f"Domaine: {doc.metadata.get('domain', 'Unknown')}\n"
            context += f"Contenu: {doc.page_content}\n\n"
        
        logger.info(f"Generated context for query: {query}")
        return context