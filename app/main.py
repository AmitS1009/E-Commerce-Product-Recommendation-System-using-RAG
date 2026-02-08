"""FastAPI application setup."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from app.config import settings
from app.models import HealthResponse
from app.routes import documents, query
from app.services.vector_store import VectorStore
from app.services.rag_pipeline import RAGPipeline

# Create FastAPI application
app = FastAPI(
    title="E-Commerce Product Recommendation System",
    description="Document-Based Q&A System using RAG (Retrieval Augmented Generation)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents.router)
app.include_router(query.router)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "E-Commerce Product Recommendation System API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """
    Health check endpoint.
    
    Checks:
    - API status
    - Ollama availability
    - ChromaDB availability
    
    Returns:
        HealthResponse with system status
    """
    # Check ChromaDB
    chroma_available = True
    try:
        vector_store = VectorStore(
            persist_directory=settings.chroma_persist_dir,
            collection_name=settings.chroma_collection_name
        )
        _ = vector_store.get_chunk_count()
    except Exception:
        chroma_available = False
    
    # Check Ollama
    ollama_available = True
    try:
        rag = RAGPipeline(
            ollama_base_url=settings.ollama_base_url,
            model_name=settings.ollama_model
        )
        ollama_available = rag.check_ollama_available()
    except Exception:
        ollama_available = False
    
    return HealthResponse(
        status="healthy" if (chroma_available and ollama_available) else "degraded",
        timestamp=datetime.now().isoformat(),
        ollama_available=ollama_available,
        chroma_available=chroma_available
    )


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    print("=" * 60)
    print("E-Commerce Product Recommendation System - Starting")
    print("=" * 60)
    print(f"Ollama URL: {settings.ollama_base_url}")
    print(f"Ollama Model: {settings.ollama_model}")
    print(f"ChromaDB Path: {settings.chroma_persist_dir}")
    print(f"Embedding Model: {settings.embedding_model}")
    print("=" * 60)
    
    # Ensure upload directory exists
    import os
    os.makedirs(settings.upload_dir, exist_ok=True)
    print(f"✓ Upload directory ready: {settings.upload_dir}")
    
    # Initialize ChromaDB (will create if doesn't exist)
    try:
        vector_store = VectorStore(
            persist_directory=settings.chroma_persist_dir,
            collection_name=settings.chroma_collection_name
        )
        chunk_count = vector_store.get_chunk_count()
        doc_count = vector_store.get_document_count()
        print(f"✓ ChromaDB initialized: {doc_count} documents, {chunk_count} chunks")
    except Exception as e:
        print(f"⚠ ChromaDB initialization warning: {str(e)}")
    
    print("=" * 60)
    print("API is ready! Visit http://localhost:8000/docs for API documentation")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("\nShutting down E-Commerce Product Recommendation System...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
