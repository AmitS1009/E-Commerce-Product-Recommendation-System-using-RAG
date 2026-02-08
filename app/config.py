"""Configuration management for the RAG application."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Ollama Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    
    # ChromaDB Configuration
    chroma_persist_dir: str = "./chroma_db"
    chroma_collection_name: str = "ecommerce_docs"
    
    # Embedding Model Configuration
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Document Processing Configuration
    chunk_size: int = 500
    chunk_overlap: int = 100
    upload_dir: str = "./uploads"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Retrieval Configuration
    top_k_results: int = 3
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
