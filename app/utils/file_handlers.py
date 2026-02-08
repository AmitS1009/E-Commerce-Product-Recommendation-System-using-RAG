"""Utility functions for file handling."""

import os
import uuid
from typing import Tuple
from fastapi import UploadFile, HTTPException


ALLOWED_EXTENSIONS = {'.txt', '.md', '.pdf'}


def generate_document_id() -> str:
    """Generate a unique document ID using UUID4.
    
    Returns:
        str: Unique document identifier
    """
    return str(uuid.uuid4())


def validate_file_extension(filename: str) -> bool:
    """Validate if the file has an allowed extension.
    
    Args:
        filename: Name of the file to validate
        
    Returns:
        bool: True if extension is allowed, False otherwise
    """
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXTENSIONS


async def save_upload_file(upload_file: UploadFile, upload_dir: str) -> Tuple[str, str]:
    """Save uploaded file to disk.
    
    Args:
        upload_file: FastAPI UploadFile object
        upload_dir: Directory to save the file
        
    Returns:
        Tuple of (file_path, document_id)
        
    Raises:
        HTTPException: If file extension not allowed or save fails
    """
    # Validate file extension
    if not validate_file_extension(upload_file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Generate unique document ID
    doc_id = generate_document_id()
    
    # Create upload directory if it doesn't exist
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file with document ID as prefix
    file_extension = os.path.splitext(upload_file.filename)[1]
    filename = f"{doc_id}{file_extension}"
    file_path = os.path.join(upload_dir, filename)
    
    try:
        # Write file to disk
        with open(file_path, "wb") as f:
            content = await upload_file.read()
            f.write(content)
        
        return file_path, doc_id
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}"
        )


def delete_upload_file(file_path: str) -> bool:
    """Delete uploaded file from disk.
    
    Args:
        file_path: Path to the file to delete
        
    Returns:
        bool: True if deletion successful, False otherwise
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False
