from typing import Dict, Any, List, TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from .memory import AgentMemory
from .tools import MedicalTools
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MedicalAgentState(TypedDict):
    query: str
    domain: str
    context: str
    response: str
    memory_context: str
    conversation_history: List[Dict]

class MedicalAgent:
    def __init__(self, session_id: str, retriever):
        self.session_id = session_id
        self.memory = AgentMemory(session_id)
        self.tools = MedicalTools(retriever)
        self.llm = ChatGroq(
            groq_api_key=Config.GROQ_API_KEY,
            model_name=Config.GROQ_MODEL,
            temperature=0.1
        )
        self.workflow = self._create_workflow()
        logger.info(f"Initialized MedicalAgent for session_id: {session_id}")
    
    def _create_workflow(self) -> StateGraph:
        """Crée le workflow LangGraph"""
        workflow = StateGraph(MedicalAgentState)
        
        # Définir les nœuds
        workflow.add_node("process_query", self.process_query)
        workflow.add_node("identify_domain", self.identify_domain)
        workflow.add_node("retrieve_context", self.retrieve_context)
        workflow.add_node("generate_response", self.generate_response)
        workflow.add_node("update_memory", self.update_memory)
        
        # Définir les edges ( hya l5at l yorbet ma bin neud w neud )
        workflow.add_edge(START, "process_query") 
        workflow.add_edge("process_query", "identify_domain")
        workflow.add_edge("identify_domain", "retrieve_context")
        workflow.add_edge("retrieve_context", "generate_response")
        workflow.add_edge("generate_response", "update_memory")
        workflow.add_edge("update_memory", END)
        
        logger.info("Created LangGraph workflow")
        return workflow.compile()
    
    def process_query(self, state: MedicalAgentState) -> Dict[str, Any]: # noeud 
        """Traite la requête initiale"""
        memory_context = self.memory.get_context()
        logger.info(f"Processed query: {state.get('query', '')}")
        return {"memory_context": memory_context}
    
    def identify_domain(self, state: MedicalAgentState) -> Dict[str, Any]: # noeud 
        """Identifie le domaine médical"""
        query = state.get("query", "")
        try:
            domain = self.tools.identify_medical_domain(query=query)
        except Exception as e:
            logger.error(f"Error identifying domain: {e}")
            # Fallback: identifier le domaine par défaut ou basé sur des mots-clés
            domain = "general"
        logger.info(f"Identified domain: {domain}")
        return {"domain": domain}
    
    def retrieve_context(self, state: MedicalAgentState) -> Dict[str, Any]:  # noeud 
        """Récupère le contexte pertinent"""
        query = state.get("query", "")
        domain = state.get("domain", "")
        try:
            context = self.tools.search_medical_docs(query=query, domain=domain)
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            context = "Aucun contexte disponible"
        logger.info(f"Retrieved context for query: {query}, domain: {domain}")
        return {"context": context}
    
    def generate_response(self, state: MedicalAgentState) -> Dict[str, Any]: # noeud LLM pour géneré réponse 
        """Génère la réponse"""
        query = state.get("query", "")
        memory_context = state.get("memory_context", "")
        domain = state.get("domain", "")
        context = state.get("context", "")
        
        prompt = f"""
        Tu es un assistant médical spécialisé. Réponds à la question suivante en utilisant le contexte fourni.
        
        Contexte de la conversation:
        {memory_context}
        
        Domaine identifié: {domain}
        
        Contexte des documents:
        {context}
        
        Question: {query}
        
        Instructions:
        - Utilise uniquement les informations des documents fournis
        - Sois précis et factuel
        - Indique les sources quand possible
        - Si les informations sont insuffisantes, dis-le clairement
        - Adapte ta réponse au contexte conversationnel
        
        Réponse:
        """
        
        messages = [HumanMessage(content=prompt)]
        response = self.llm.invoke(messages)
        logger.info(f"Generated response for query: {query}")
        return {"response": response.content}
    
    def update_memory(self, state: MedicalAgentState) -> Dict[str, Any]:
        """Met à jour la mémoire"""
        query = state.get("query", "")
        response = state.get("response", "")
        domain = state.get("domain", "")
        
        self.memory.add_message("user", query, domain)
        self.memory.add_message("assistant", response, domain)
        self.memory.save_memory()
        logger.info(f"Updated memory for session_id: {self.session_id}")
        return {}
    
    def chat(self, query: str) -> str:
        """Interface principale pour le chat"""
        initial_state: MedicalAgentState = {
            "query": query,
            "domain": "",
            "context": "",
            "response": "",
            "memory_context": "",
            "conversation_history": []
        }
        
        result = self.workflow.invoke(initial_state)
        logger.info(f"Chat completed for query: {query}")
        return result.get("response", "")