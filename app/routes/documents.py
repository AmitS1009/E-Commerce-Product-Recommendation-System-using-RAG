"""API routes for document management."""

from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
from typing import List

from app.models import (
    DocumentUploadResponse,
    DocumentListResponse,
    DocumentInfo,
    DeleteDocumentResponse
)
from app.utils.file_handlers import save_upload_file, delete_upload_file
from app.services.document_processor import DocumentProcessor
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore
from app.config import settings

# Initialize router
router = APIRouter(prefix="/api/documents", tags=["documents"])

# Initialize services (these will be shared across requests)
document_processor = DocumentProcessor(
    chunk_size=settings.chunk_size,
    chunk_overlap=settings.chunk_overlap
)
embedding_service = EmbeddingService(model_name=settings.embedding_model)
vector_store = VectorStore(
    persist_directory=settings.chroma_persist_dir,
    collection_name=settings.chroma_collection_name
)


@router.post("/upload", response_model=DocumentUploadResponse, status_code=201)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and index a document.
    
    Supports: .txt, .md, .pdf files
    
    Process:
    1. Save uploaded file
    2. Extract text and create chunks
    3. Generate embeddings
    4. Store in vector database
    
    Returns:
        DocumentUploadResponse with document ID and metadata
    """
    try:
        # Save the uploaded file
        file_path, doc_id = await save_upload_file(file, settings.upload_dir)
        
        # Process the document (extract text and chunk)
        chunks, metadata = document_processor.process_document(
            file_path=file_path,
            document_id=doc_id,
            filename=file.filename
        )
        
        if not chunks:
            # Clean up file if no chunks were created
            delete_upload_file(file_path)
            raise HTTPException(
                status_code=400,
                detail="No text content could be extracted from the document"
            )
        
        # Generate embeddings for all chunks
        embeddings = embedding_service.generate_embeddings(chunks)
        
        # Store in vector database
        vector_store.add_documents(
            chunks=chunks,
            embeddings=embeddings,
            document_id=doc_id,
            filename=file.filename,
            upload_time=metadata['upload_time']
        )
        
        return DocumentUploadResponse(
            document_id=doc_id,
            filename=file.filename,
            chunk_count=len(chunks),
            upload_time=metadata['upload_time']
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document: {str(e)}"
        )


@router.get("", response_model=DocumentListResponse)
async def list_documents():
    """
    List all indexed documents.
    
    Returns:
        DocumentListResponse with list of all documents and total count
    """
    try:
        documents = vector_store.list_documents()
        
        # Convert to DocumentInfo models
        doc_infos = [
            DocumentInfo(
                document_id=doc['document_id'],
                filename=doc['filename'],
                upload_time=doc['upload_time'],
                chunk_count=doc['chunk_count']
            )
            for doc in documents
        ]
        
        return DocumentListResponse(
            documents=doc_infos,
            total_count=len(doc_infos)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list documents: {str(e)}"
        )


@router.delete("/{document_id}", response_model=DeleteDocumentResponse)
async def delete_document(document_id: str):
    """
    Delete a document from the vector store.
    
    Args:
        document_id: Unique identifier of the document to delete
        
    Returns:
        DeleteDocumentResponse with deletion status
    """
    try:
        # Delete from vector store
        deleted_count = vector_store.delete_document(document_id)
        
        if deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail=f"Document with ID {document_id} not found"
            )
        
        # Note: We're not deleting the physical file from uploads/
        # to maintain audit trail. You can add file deletion if needed.
        
        return DeleteDocumentResponse(
            document_id=document_id,
            message=f"Successfully deleted document and {deleted_count} chunks",
            success=True
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete document: {str(e)}"
        )
