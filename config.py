import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    VECTORSTORE_PATH = "data/vectorstore"
    CONVERSATIONS_PATH = "conversations"
    PDF_PATH = "data/pdfs"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    GROQ_MODEL = "llama3-70b-8192"  # ou "mixtral-8x7b-32768"

    def __init__(self):
        # Ensure directories exist
        for path in [self.VECTORSTORE_PATH, self.CONVERSATIONS_PATH, self.PDF_PATH]:
            os.makedirs(path, exist_ok=True)
            logger.info(f"Ensured directory exists: {path}")

# Instantiate Config to ensure directories are created
Config()