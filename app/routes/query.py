"""API routes for Q&A queries."""

from fastapi import APIRouter, HTTPException

from app.models import QueryRequest, QueryResponse
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.rag_pipeline import RAGPipeline
from app.config import settings

# Initialize router
router = APIRouter(prefix="/api", tags=["query"])

# Initialize services
embedding_service = EmbeddingService(model_name=settings.embedding_model)
vector_store = VectorStore(
    persist_directory=settings.chroma_persist_dir,
    collection_name=settings.chroma_collection_name
)
rag_pipeline = RAGPipeline(
    ollama_base_url=settings.ollama_base_url,
    model_name=settings.ollama_model
)


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Ask a question about the indexed documents.
    
    Process:
    1. Generate embedding for the query
    2. Retrieve relevant chunks from vector store
    3. Generate answer using RAG pipeline
    
    Args:
        request: QueryRequest with user's question
        
    Returns:
        QueryResponse with answer and source documents
    """
    try:
        # Check if there are any documents indexed
        if vector_store.get_chunk_count() == 0:
            raise HTTPException(
                status_code=400,
                detail="No documents have been indexed yet. Please upload documents first."
            )
        
        # Generate embedding for the query
        query_embedding = embedding_service.generate_embedding(request.query)
        
        # Retrieve relevant documents from vector store
        top_k = request.top_k if request.top_k else settings.top_k_results
        search_results = vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )
        
        # Generate response using RAG pipeline
        response_data = rag_pipeline.generate_response(
            query=request.query,
            search_results=search_results
        )
        
        # Convert to response model
        return QueryResponse(**response_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process query: {str(e)}"
        )
