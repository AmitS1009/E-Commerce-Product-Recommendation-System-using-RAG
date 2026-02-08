"""Vector store service using ChromaDB."""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
from datetime import datetime


class VectorStore:
    """Service for managing document vectors in ChromaDB."""
    
    def __init__(self, persist_directory: str, collection_name: str = "ecommerce_docs"):
        """Initialize the vector store.
        
        Args:
            persist_directory: Directory for ChromaDB persistence
            collection_name: Name of the ChromaDB collection
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize ChromaDB client and collection."""
        print(f"Initializing ChromaDB at: {self.persist_directory}")
        
        # Create persistent client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )
        
        print(f"ChromaDB collection '{self.collection_name}' initialized")
    
    def add_documents(
        self,
        chunks: List[str],
        embeddings: List[List[float]],
        document_id: str,
        filename: str,
        upload_time: str
    ):
        """Add document chunks to the vector store.
        
        Args:
            chunks: List of text chunks
            embeddings: List of embedding vectors
            document_id: Unique document identifier
            filename: Original filename
            upload_time: ISO format timestamp of upload
        """
        if not chunks or not embeddings:
            return
        
        # Create unique IDs for each chunk
        chunk_ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
        
        # Create metadata for each chunk
        metadatas = [
            {
                "document_id": document_id,
                "filename": filename,
                "chunk_index": i,
                "upload_time": upload_time,
                "total_chunks": len(chunks)
            }
            for i in range(len(chunks))
        ]
        
        # Add to collection
        self.collection.add(
            ids=chunk_ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas
        )
        
        print(f"Added {len(chunks)} chunks for document {document_id}")
    
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 3
    ) -> Dict:
        """Search for similar documents using vector similarity.
        
        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            
        Returns:
            Dictionary with search results
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        return results
    
    def delete_document(self, document_id: str) -> int:
        """Delete all chunks associated with a document.
        
        Args:
            document_id: Document identifier to delete
            
        Returns:
            Number of chunks deleted
        """
        # Query all chunks with this document_id
        results = self.collection.get(
            where={"document_id": document_id}
        )
        
        if not results['ids']:
            return 0
        
        # Delete all matching chunks
        self.collection.delete(
            ids=results['ids']
        )
        
        deleted_count = len(results['ids'])
        print(f"Deleted {deleted_count} chunks for document {document_id}")
        
        return deleted_count
    
    def list_documents(self) -> List[Dict]:
        """List all unique documents in the vector store.
        
        Returns:
            List of document metadata dictionaries
        """
        # Get all items from collection
        all_items = self.collection.get()
        
        if not all_items['metadatas']:
            return []
        
        # Group by document_id
        documents = {}
        for metadata in all_items['metadatas']:
            doc_id = metadata['document_id']
            if doc_id not in documents:
                documents[doc_id] = {
                    "document_id": doc_id,
                    "filename": metadata['filename'],
                    "upload_time": metadata['upload_time'],
                    "chunk_count": metadata.get('total_chunks', 0)
                }
        
        return list(documents.values())
    
    def get_document_count(self) -> int:
        """Get total number of unique documents.
        
        Returns:
            Number of documents
        """
        return len(self.list_documents())
    
    def get_chunk_count(self) -> int:
        """Get total number of chunks in the collection.
        
        Returns:
            Number of chunks
        """
        return self.collection.count()
