import streamlit as st
import os
from datetime import datetime
from config import Config
from rag.document_processor import DocumentProcessor
from rag.vector_store import VectorStore
from rag.retriever import MedicalRetriever
from agents.medical_agent import MedicalAgent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_rag_system():
    """Initialise le système RAG"""
    logger.info("Initializing RAG system")
    vector_store = VectorStore()
    
    # Charger l'index existant ou le créer
    if not vector_store.load_index(Config.VECTORSTORE_PATH):
        logger.info("Creating vector index")
        processor = DocumentProcessor()
        documents = processor.process_pdfs(Config.PDF_PATH)
        
        if documents:
            vector_store.build_index(documents)
            vector_store.save_index(Config.VECTORSTORE_PATH)
            st.success(f"Index créé avec {len(documents)} documents")
            logger.info(f"Created index with {len(documents)} documents")
        else:
            st.error("Aucun document trouvé dans le dossier PDFs")
            logger.error("No documents found in PDF directory")
            return None
    
    retriever = MedicalRetriever(vector_store)
    logger.info("Initialized RAG system successfully")
    return retriever

def main():
    st.set_page_config(
        page_title="Assistant Médical AI",
        page_icon="🏥",
        layout="wide"
    )
    
    st.title("🏥 Assistant Médical AI")
    st.write("Assistant spécialisé en Autism, Diabète, Nutrition, PCOS, Psychologie et Radiologie")
    
    # Initialisation
    if 'retriever' not in st.session_state:
        st.session_state.retriever = initialize_rag_system()
    
    if 'session_id' not in st.session_state:
        st.session_state.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    if 'agent' not in st.session_state and st.session_state.retriever:
        st.session_state.agent = MedicalAgent(
            st.session_state.session_id,
            st.session_state.retriever
        )
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Informations")
        st.write(f"Session: {st.session_state.session_id}")
        st.write(f"Messages: {len(st.session_state.messages)}")
        
        st.header("🔧 Configuration")
        domains = st.multiselect(
            "Domaines disponibles:",
            ["autism", "diabete", "nutrition", "pcos", "psychology", "radiology"],
            default=["autism", "diabete", "nutrition", "pcos", "psychology", "radiology"]
        )
        
        if st.button("Nouvelle Session"):
            st.session_state.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            st.session_state.messages = []
            st.session_state.agent = MedicalAgent(
                st.session_state.session_id,
                st.session_state.retriever
            )
            st.rerun()
    
    # Interface de chat
    if st.session_state.retriever is None:
        st.error("Système RAG non initialisé. Vérifiez vos fichiers PDF.")
        logger.error("RAG system not initialized")
        return
    
    # Afficher les messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input utilisateur
    if query := st.chat_input("Posez votre question médicale..."):
        # Afficher la question
        with st.chat_message("user"):
            st.markdown(query)
        st.session_state.messages.append({"role": "user", "content": query})
        logger.info(f"User query: {query}")
        
        # Générer la réponse
        with st.chat_message("assistant"):
            with st.spinner("Recherche d'informations..."):
                try:
                    response = st.session_state.agent.chat(query)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    logger.info(f"Generated response: {response}")
                except Exception as e:
                    error_msg = f"Erreur lors de la génération de la réponse: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    logger.error(error_msg)

if __name__ == "__main__":
    main()