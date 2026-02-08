# E-Commerce Product Recommendation System using RAG

An intelligent Document-Based Q&A System that enables semantic search and question answering over product documents using Retrieval Augmented Generation (RAG).

## Features

- **Document Upload & Processing**: Support for `.txt`, `.md`, and `.pdf` files
- **Semantic Search**: Vector-based similarity search using ChromaDB
- **Intelligent Q&A**: Context-aware responses using Ollama LLM (llama3.2)
- **RESTful API**: Clean FastAPI endpoints with automatic Swagger documentation
- **Production-Ready**: Error handling, validation, type hints, and comprehensive logging

## Technology Stack

- **Backend**: FastAPI
- **Vector Database**: ChromaDB (local, persistent)
- **LLM**: Ollama (llama3.2)
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Document Processing**: pypdf for PDF extraction

## Architecture

<img width="966" height="917" alt="image" src="https://github.com/user-attachments/assets/73ab31a6-619b-41bd-a8fe-6f5348a16f61" />
<img width="974" height="339" alt="image" src="https://github.com/user-attachments/assets/266d72e5-6124-46d5-913a-4fb924107b3d" />

**Key Components:**
1. **Document Processor**: Extracts text and creates semantic chunks
2. **Embedding Service**: Generates 384-dim vectors
3. **Vector Store**: ChromaDB for persistent storage
4. **RAG Pipeline**: Retrieves context and generates answers

## Prerequisites

- Python 3.10 or higher
- Ollama installed and running
- 4GB+ RAM recommended

## Installation

### 1. Setup Ollama

Download and install Ollama from [ollama.com](https://ollama.com/download)

```bash
# Pull the llama3.2 model
ollama pull llama3.2

# Verify
ollama list
```

### 2. Clone Repository

```bash
cd "d:\ML\Projects\AI\E-Commerce Product Recommendation System"
```

### 3. Create Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Verify Installation

```bash
python test_system.py
```

Expected output:
```
✓ Config loaded: Ollama URL=http://localhost:11434, Model=llama3.2
✓ Embedding service imported
✓ Vector store imported
✓ RAG pipeline imported
✓ Ollama is available with model: llama3.2
System check complete!
```

## Running the Application

Start the server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

**Access Points:**
- API Documentation (Swagger): http://localhost:8000/docs
- Alternative Docs (ReDoc): http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## API Endpoints

### 1. Upload Document

**`POST /api/documents/upload`**

Upload and index a document for semantic search.

```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@sample_product.txt"
```

Response:
```json
{
  "document_id": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
  "filename": "sample_product.txt",
  "chunk_count": 6,
  "upload_time": "2026-02-09T01:00:00",
  "message": "Document uploaded and indexed successfully"
}
```

### 2. Query Documents

**`POST /api/query`**

Ask natural language questions about indexed documents.

```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the features of the headphones?"}'
```

Response:
```json
{
  "answer": "The headphones feature industry-leading ANC, 30-hour battery life...",
  "sources": [
    {
      "document_id": "a1b2c3d4-...",
      "filename": "sample_product.txt",
      "chunk_index": 1,
      "relevance_score": 0.892,
      "content": "Key Features: Industry-leading Active Noise Cancellation..."
    }
  ],
  "query": "What are the features of the headphones?",
  "timestamp": "2026-02-09T01:00:30"
}
```

### 3. List Documents

**`GET /api/documents`**

Retrieve all indexed documents.

```bash
curl "http://localhost:8000/api/documents"
```

### 4. Delete Document

**`DELETE /api/documents/{document_id}`**

Remove a document from the vector store.

```bash
curl -X DELETE "http://localhost:8000/api/documents/a1b2c3d4-..."
```

### 5. Health Check

**`GET /health`**

Check system status.

```bash
curl "http://localhost:8000/health"
```

## Testing

The project includes a sample document `sample_product.txt` for testing.

### Upload Sample Document

```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@sample_product.txt"
```

### Test Queries

**Ask about features:**
```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What features do the headphones have?"}'
```

**Ask about price:**
```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "How much do they cost?"}'
```

**Ask about colors:**
```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What colors are available?"}'
```

**Ask about battery:**
```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the battery life?"}'
```

## Project Structure

```
E-Commerce Product Recommendation System/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic models
│   ├── routes/
│   │   ├── documents.py     # Document endpoints
│   │   └── query.py         # Query endpoint
│   ├── services/
│   │   ├── document_processor.py   # Text extraction & chunking
│   │   ├── embeddings.py           # Vector generation
│   │   ├── vector_store.py         # ChromaDB operations
│   │   └── rag_pipeline.py         # RAG implementation
│   └── utils/
│       └── file_handlers.py        # File I/O utilities
├── uploads/                 # Uploaded files
├── chroma_db/              # Vector database
├── requirements.txt
├── .env.example
├── README.md
├── sample_product.txt
└── test_system.py
```

## Assignment Requirements

✅ Python backend using FastAPI  
✅ Vector Database (ChromaDB)  
✅ LLM Integration (Ollama)  
✅ REST API endpoints (4+)  
✅ Clean, documented code  
✅ README with setup instructions  
✅ requirements.txt  
✅ Design decisions explained  


**Built with Python, FastAPI, ChromaDB, and Ollama**
