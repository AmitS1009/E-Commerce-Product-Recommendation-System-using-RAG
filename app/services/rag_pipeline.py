"""RAG pipeline service integrating retrieval and generation."""

import ollama
from typing import List, Dict
from datetime import datetime


class RAGPipeline:
    """Retrieval Augmented Generation pipeline."""
    
    def __init__(
        self,
        ollama_base_url: str = "http://localhost:11434",
        model_name: str = "llama3.2"
    ):
        """Initialize the RAG pipeline.
        
        Args:
            ollama_base_url: Base URL for Ollama API
            model_name: Name of the Ollama model to use
        """
        self.ollama_base_url = ollama_base_url
        self.model_name = model_name
        self.client = ollama.Client(host=ollama_base_url)
    
    def _build_context(self, search_results: Dict) -> str:
        """Build context string from search results.
        
        Args:
            search_results: Results from vector store search
            
        Returns:
            Formatted context string
        """
        if not search_results['documents'] or not search_results['documents'][0]:
            return "No relevant context found."
        
        contexts = []
        documents = search_results['documents'][0]
        metadatas = search_results['metadatas'][0]
        
        for i, (doc, metadata) in enumerate(zip(documents, metadatas)):
            context_piece = f"[Source {i+1}: {metadata['filename']}]\n{doc}\n"
            contexts.append(context_piece)
        
        return "\n".join(contexts)
    
    def _build_prompt(self, query: str, context: str) -> str:
        """Build the prompt for the LLM.
        
        Args:
            query: User's question
            context: Retrieved context from documents
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are a helpful AI assistant for an e-commerce platform. Answer the user's question based on the provided context from product documents.

Context from documents:
{context}

User Question: {query}

Instructions:
- Answer the question using ONLY the information from the context above
- If the context doesn't contain enough information to answer, say "I don't have enough information in the documents to answer this question."
- Be concise and accurate
- If referencing specific products or features, mention the source document

Answer:"""
        
        return prompt
    
    def generate_response(
        self,
        query: str,
        search_results: Dict
    ) -> Dict:
        """Generate response using RAG.
        
        Args:
            query: User's question
            search_results: Results from vector store search
            
        Returns:
            Dictionary containing answer and metadata
        """
        # Build context from retrieved documents
        context = self._build_context(search_results)
        
        # Build prompt
        prompt = self._build_prompt(query, context)
        
        # Generate response using Ollama
        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.7,
                    "num_predict": 512,
                }
            )
            
            answer = response['response'].strip()
            
        except Exception as e:
            answer = f"Error generating response: {str(e)}"
        
        # Extract source information
        sources = []
        if search_results['documents'] and search_results['documents'][0]:
            documents = search_results['documents'][0]
            metadatas = search_results['metadatas'][0]
            distances = search_results['distances'][0] if 'distances' in search_results else [0] * len(documents)
            
            for doc, metadata, distance in zip(documents, metadatas, distances):
                # Convert distance to similarity score (1 - distance for cosine)
                similarity_score = 1.0 - distance if distance <= 1.0 else 0.0
                
                sources.append({
                    "document_id": metadata['document_id'],
                    "filename": metadata['filename'],
                    "chunk_index": metadata['chunk_index'],
                    "relevance_score": round(similarity_score, 3),
                    "content": doc[:200] + "..." if len(doc) > 200 else doc
                })
        
        return {
            "answer": answer,
            "sources": sources,
            "query": query,
            "timestamp": datetime.now().isoformat()
        }
    
    def check_ollama_available(self) -> bool:
        """Check if Ollama is available and the model exists.
        
        Returns:
            True if Ollama is available, False otherwise
        """
        try:
            # Try to list models to check connection
            models = self.client.list()
            
            # Check if our model is available
            model_names = [model['name'] for model in models.get('models', [])]
            
            # Check for exact match or partial match (e.g., llama3.2:latest)
            model_available = any(
                self.model_name in name or name.startswith(self.model_name)
                for name in model_names
            )
            
            return model_available
            
        except Exception as e:
            print(f"Ollama check failed: {str(e)}")
            return False
