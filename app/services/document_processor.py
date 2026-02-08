"""Document processing service for text extraction and chunking."""

import os
from typing import List, Tuple
from datetime import datetime
from pypdf import PdfReader


class DocumentProcessor:
    """Handles document upload, text extraction, and chunking."""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """Initialize document processor.
        
        Args:
            chunk_size: Size of each text chunk in characters
            chunk_overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from different file formats.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Extracted text content
            
        Raises:
            ValueError: If file format is not supported
        """
        _, ext = os.path.splitext(file_path.lower())
        
        if ext == '.pdf':
            return self._extract_from_pdf(file_path)
        elif ext in ['.txt', '.md']:
            return self._extract_from_text(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
    
    def _extract_from_text(self, file_path: str) -> str:
        """Extract text from text/markdown file.
        
        Args:
            file_path: Path to text file
            
        Returns:
            File contents
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            raise ValueError(f"Failed to read text file: {str(e)}")
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks.
        
        Uses a sliding window approach to create chunks with overlap
        for better context preservation.
        
        Args:
            text: Text to chunk
            
        Returns:
            List of text chunks
        """
        if not text:
            return []
        
        chunks = []
        text_length = len(text)
        
        # Calculate step size (chunk_size - overlap)
        step = self.chunk_size - self.chunk_overlap
        
        # Create chunks using sliding window
        for i in range(0, text_length, step):
            chunk = text[i:i + self.chunk_size]
            
            # Only add non-empty chunks
            if chunk.strip():
                chunks.append(chunk.strip())
            
            # Break if we've reached the end
            if i + self.chunk_size >= text_length:
                break
        
        return chunks
    
    def process_document(self, file_path: str, document_id: str, filename: str) -> Tuple[List[str], dict]:
        """Process a document: extract text and create chunks.
        
        Args:
            file_path: Path to the document file
            document_id: Unique identifier for the document
            filename: Original filename
            
        Returns:
            Tuple of (chunks, metadata)
        """
        # Extract text from document
        text = self.extract_text(file_path)
        
        # Create chunks
        chunks = self.chunk_text(text)
        
        # Create metadata
        metadata = {
            "document_id": document_id,
            "filename": filename,
            "chunk_count": len(chunks),
            "upload_time": datetime.now().isoformat(),
            "file_path": file_path
        }
        
        return chunks, metadata
