import faiss
import numpy as np
import pickle
import os
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
from langchain.schema import Document
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        logger.info(f"Initializing VectorStore with model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        self.index = None
        self.documents = []
        self.embeddings = None
    
    def create_embeddings(self, documents: List[Document]) -> np.ndarray:
        """Crée les embeddings pour les documents"""
        texts = [doc.page_content for doc in documents]
        embeddings = self.embedding_model.encode(texts)
        logger.info(f"Created embeddings for {len(documents)} documents")
        return embeddings
    
    def build_index(self, documents: List[Document]):
        """Construit l'index FAISS"""
        self.documents = documents
        self.embeddings = self.create_embeddings(documents)
        
        # Créer l'index FAISS
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings.astype('float32'))
        logger.info(f"Built FAISS index with dimension {dimension}")
    
    def save_index(self, path: str):
        """Sauvegarde l'index et les documents"""
        os.makedirs(path, exist_ok=True)
        
        # Sauvegarder l'index FAISS
        faiss.write_index(self.index, os.path.join(path, "faiss_index"))
        
        # Sauvegarder les documents
        with open(os.path.join(path, "documents.pkl"), "wb") as f:
            pickle.dump(self.documents, f)
        logger.info(f"Saved index and documents to {path}")
    
    def load_index(self, path: str):
        """Charge l'index et les documents"""
        index_path = os.path.join(path, "faiss_index")
        docs_path = os.path.join(path, "documents.pkl")
        
        if os.path.exists(index_path) and os.path.exists(docs_path):
            self.index = faiss.read_index(index_path)
            with open(docs_path, "rb") as f:
                self.documents = pickle.load(f)
            logger.info(f"Loaded index and documents from {path}")
            return True
        logger.warning(f"Index or documents not found at {path}")
        return False
    
    def search(self, query: str, k: int = 5) -> List[Tuple[Document, float]]:
        """Recherche les documents les plus similaires"""
        if self.index is None:
            logger.warning("No index loaded for search")
            return []
        
        # Encoder la requête
        query_embedding = self.embedding_model.encode([query])
        
        # Rechercher dans l'index
        scores, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # Retourner les documents avec leurs scores
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):
                results.append((self.documents[idx], scores[0][i]))
        
        logger.info(f"Search returned {len(results)} results for query: {query}")
        return results