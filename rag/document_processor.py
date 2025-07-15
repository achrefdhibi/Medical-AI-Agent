import pdfplumber
import os
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extrait le texte d'un PDF avec pdfplumber"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            logger.info(f"Extracted text from {pdf_path}")
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction du PDF {pdf_path}: {e}")
        return text
    
    def process_pdfs(self, pdf_directory: str) -> List[Document]:
        """Traite tous les PDFs dans le répertoire"""
        documents = []
        
        pdf_files = {
            "autism.pdf": "autism",
            "diabete.pdf": "diabete", 
            "nutrition.pdf": "nutrition",
            "pcos.pdf": "pcos",
            "psychology.pdf": "psychology",
            "radiology.pdf": "radiology"
        }
        
        for filename, domain in pdf_files.items():
            pdf_path = os.path.join(pdf_directory, filename)
            if os.path.exists(pdf_path):
                text = self.extract_text_from_pdf(pdf_path)
                if text:
                    chunks = self.text_splitter.split_text(text)
                    for i, chunk in enumerate(chunks):
                        doc = Document(
                            page_content=chunk,
                            metadata={
                                "source": filename,
                                "domain": domain,
                                "chunk_id": i
                            }
                        )
                        documents.append(doc)
                    logger.info(f"Processed {filename} into {len(chunks)} chunks")
                else:
                    logger.warning(f"No text extracted from {pdf_path}")
            else:
                logger.warning(f"PDF file not found: {pdf_path}")
        
        return documents