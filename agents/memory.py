from typing import Dict, List, Optional
from utils.conversation_manager import ConversationManager
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentMemory:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.conversation_manager = ConversationManager()
        self.short_term_memory = []
        self.long_term_memory = {}
        self.load_memory()
        logger.info(f"Initialized AgentMemory for session_id: {session_id}")
    
    def load_memory(self):
        """Charge la mémoire depuis les conversations sauvegardées"""
        history = self.conversation_manager.get_conversation_history(self.session_id)
        self.short_term_memory = history
        
        # Extraire des patterns de la mémoire à long terme
        self.extract_long_term_patterns()
        logger.info(f"Loaded memory with {len(self.short_term_memory)} messages")
    
    def extract_long_term_patterns(self):
        """Extrait des patterns récurrents pour la mémoire à long terme"""
        domains_discussed = set()
        for msg in self.short_term_memory:
            if "domain" in msg:
                domains_discussed.add(msg["domain"])
        
        self.long_term_memory["preferred_domains"] = list(domains_discussed)
        self.long_term_memory["conversation_count"] = len(self.short_term_memory)
        logger.info(f"Extracted long-term patterns: {self.long_term_memory}")
    
    def add_message(self, role: str, content: str, domain: str = None):
        """Ajoute un message à la mémoire"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "domain": domain
        }
        self.short_term_memory.append(message)
        
        # Garder seulement les 20 derniers messages en mémoire courte
        if len(self.short_term_memory) > 20:
            self.short_term_memory = self.short_term_memory[-20:]
        logger.info(f"Added message to memory: {role} - {domain}")
    
    def get_context(self) -> str:
        """Obtient le contexte conversationnel"""
        context = "Historique de la conversation:\n"
        for msg in self.short_term_memory[-5:]:  # 5 derniers messages
            context += f"{msg['role']}: {msg['content']}\n"
        
        if self.long_term_memory.get("preferred_domains"):
            context += f"\nDomaines préférés: {', '.join(self.long_term_memory['preferred_domains'])}\n"
        
        logger.info("Generated conversation context")
        return context
    
    def save_memory(self):
        """Sauvegarde la mémoire"""
        self.conversation_manager.save_conversation(self.session_id, self.short_term_memory)
        logger.info(f"Saved memory for session_id: {self.session_id}")