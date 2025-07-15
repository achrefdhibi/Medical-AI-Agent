import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConversationManager:
    def __init__(self, conversations_path: str = "conversations"):
        self.conversations_path = conversations_path
        os.makedirs(conversations_path, exist_ok=True)
        logger.info(f"Initialized ConversationManager with path: {conversations_path}")
    
    def save_conversation(self, session_id: str, conversation: List[Dict]):
        """Sauvegarde une conversation en JSON"""
        filename = f"{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.conversations_path, filename)
        
        conversation_data = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "messages": conversation
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(conversation_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved conversation to {filepath}")
    
    def load_conversation(self, session_id: str) -> Optional[List[Dict]]:
        """Charge la dernière conversation d'une session"""
        files = [f for f in os.listdir(self.conversations_path) 
                if f.startswith(session_id) and f.endswith('.json')]
        
        if not files:
            logger.info(f"No conversation found for session_id: {session_id}")
            return None
        
        # Prendre le fichier le plus récent
        latest_file = max(files, key=lambda x: os.path.getmtime(
            os.path.join(self.conversations_path, x)
        ))
        
        with open(os.path.join(self.conversations_path, latest_file), "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"Loaded conversation from {latest_file}")
            return data.get("messages", [])
    
    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Récupère l'historique des conversations"""
        conversation = self.load_conversation(session_id)
        if conversation:
            logger.info(f"Retrieved {len(conversation[-limit:])} messages for session_id: {session_id}")
            return conversation[-limit:]
        return []