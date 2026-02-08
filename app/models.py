"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class DocumentUploadResponse(BaseModel):
    """Response model for document upload."""
    document_id: str = Field(..., description="Unique identifier for the uploaded document")
    filename: str = Field(..., description="Original filename")
    chunk_count: int = Field(..., description="Number of chunks created from the document")
    upload_time: str = Field(..., description="Timestamp of upload")
    message: str = Field(default="Document uploaded and indexed successfully")


class QueryRequest(BaseModel):
    """Request model for Q&A queries."""
    query: str = Field(..., description="User's question", min_length=1)
    top_k: Optional[int] = Field(default=3, description="Number of relevant chunks to retrieve", ge=1, le=10)


class SourceDocument(BaseModel):
    """Model for source document information."""
    document_id: str
    filename: str
    chunk_index: int
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    content: str


class QueryResponse(BaseModel):
    """Response model for Q&A queries."""
    answer: str = Field(..., description="Generated answer to the query")
    sources: List[SourceDocument] = Field(default=[], description="Source documents used for the answer")
    query: str = Field(..., description="Original query")
    timestamp: str = Field(..., description="Response generation timestamp")


class DocumentInfo(BaseModel):
    """Model for document metadata."""
    document_id: str
    filename: str
    upload_time: str
    chunk_count: int


class DocumentListResponse(BaseModel):
    """Response model for listing documents."""
    documents: List[DocumentInfo]
    total_count: int


class DeleteDocumentResponse(BaseModel):
    """Response model for document deletion."""
    document_id: str
    message: str
    success: bool


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    timestamp: str
    ollama_available: bool
    chroma_available: bool
