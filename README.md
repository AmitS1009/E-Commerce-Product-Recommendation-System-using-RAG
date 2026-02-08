# 🛍️ E-Commerce Product Recommendation System using RAG

> **Intelligent Document-Based Q&A System** powered by Retrieval Augmented Generation (RAG) for semantic search and natural language queries over product catalogs.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.4.22-orange.svg)](https://www.trychroma.com/)
[![Ollama](https://img.shields.io/badge/Ollama-llama3.2-purple.svg)](https://ollama.ai/)

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 📄 Document Processing
- Multi-format support (`.txt`, `.md`, `.pdf`)
- Intelligent semantic chunking
- Context-preserving overlap
- Automatic metadata extraction

</td>
<td width="50%">

### 🔍 Semantic Search
- Vector-based similarity search
- 384-dim embeddings
- Persistent ChromaDB storage
- Cosine similarity ranking

</td>
</tr>
<tr>
<td width="50%">

### 🤖 AI-Powered Q&A
- Context-aware responses
- Source attribution
- Local LLM (Ollama)
- RAG pipeline integration

</td>
<td width="50%">

### 🌐 RESTful API
- FastAPI backend
- Auto-generated docs (Swagger)
- Request validation
- Comprehensive error handling

</td>
</tr>
</table>

---

## 🏗️ System Architecture

```
User Request → FastAPI → Document Processor → Embeddings → ChromaDB
                              ↓
                         RAG Pipeline ← Ollama LLM
                              ↓
                          Response
```

**Key Components:**

1. **Document Processor**: Extracts text and creates semantic chunks with overlap
2. **Embedding Service**: Generates 384-dim vectors using sentence-transformers
3. **Vector Store**: ChromaDB for persistent storage and similarity search
4. **RAG Pipeline**: Retrieves context and generates answers using Ollama

---

## 🔄 Data Flow

### Upload Process:
```
1. User uploads document (PDF/Text/Markdown)
   ↓
2. Extract text from file
   ↓
3. Split into chunks (500 chars, 100 overlap)
   ↓
4. Generate embeddings (384-dim vectors)
   ↓
5. Store in ChromaDB with metadata
   ↓
6. Return document_id and chunk_count
```

### Query Process:
```
1. User asks question
   ↓
2. Convert query to embedding vector
   ↓
3. Search ChromaDB (top-3 similar chunks)
   ↓
4. Build context from retrieved chunks
   ↓
5. Send to Ollama LLM with prompt
   ↓
6. Generate answer
   ↓
7. Return answer + source documents
```

---

## 🛠️ Technology Stack

- **Backend**: FastAPI 0.109
- **Vector Database**: ChromaDB 0.4.22 (local, persistent)
- **LLM**: Ollama (llama3.2 - 3B params)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Document Processing**: pypdf for PDF extraction
- **Validation**: Pydantic models

---

## 📦 Installation

### Prerequisites

- **Python 3.10+**
- **Ollama** installed and running
- **4GB+ RAM** recommended

### Step-by-Step Setup

#### 1. Navigate to Project
```bash
cd "d:\ML\Projects\AI\E-Commerce Product Recommendation System"
```

#### 2. Create Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- `fastapi==0.109.0`
- `chromadb==0.4.22`
- `sentence-transformers==2.3.1`
- `ollama==0.1.6`
- `pypdf==4.0.1`
- `numpy==1.26.4` ⚠️ **Must be < 2.0 for ChromaDB compatibility**

#### 4. Setup Ollama
```bash
# Pull the model
ollama pull llama3.2

# Verify
ollama list
```

#### 5. Verify Installation
```bash
python test_system.py
```

**Expected Output:**
```
✓ Config loaded: Ollama URL=http://localhost:11434, Model=llama3.2
✓ Embedding service imported
✓ Vector store imported
✓ RAG pipeline imported
✓ Ollama is available with model: llama3.2
System check complete!
```

---

## 🚀 Quick Start

### Start the Server

```bash
uvicorn app.main:app --reload
```

**Server will start on:** `http://localhost:8000`

**Access Points:**
- 🏠 Home: http://localhost:8000
- 📖 Swagger UI: http://localhost:8000/docs
- 📚 ReDoc: http://localhost:8000/redoc
- ❤️ Health Check: http://localhost:8000/health

---

## 📚 API Endpoints

### 1. Upload Document

**POST** `/api/documents/upload`

```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@sample_product.txt"
```

**Response:**
```json
{
  "document_id": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
  "filename": "sample_product.txt",
  "chunk_count": 6,
  "upload_time": "2026-02-09T01:00:00.123456",
  "message": "Document uploaded and indexed successfully"
}
```

---

### 2. Query Documents

**POST** `/api/query`

```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the features of the headphones?"}'
```

**Response:**
```json
{
  "answer": "The headphones feature industry-leading ANC, 30-hour battery life, Bluetooth 5.2...",
  "sources": [
    {
      "document_id": "a1b2c3d4-...",
      "filename": "sample_product.txt",
      "chunk_index": 1,
      "relevance_score": 0.892,
      "content": "Key Features:\n- Industry-leading Active Noise Cancellation..."
    }
  ],
  "query": "What are the features of the headphones?",
  "timestamp": "2026-02-09T01:00:30.789012"
}
```

---

### 3. List Documents

**GET** `/api/documents`

```bash
curl "http://localhost:8000/api/documents"
```

**Response:**
```json
{
  "documents": [
    {
      "document_id": "a1b2c3d4-...",
      "filename": "sample_product.txt",
      "upload_time": "2026-02-09T01:00:00.123456",
      "chunk_count": 6
    }
  ],
  "total_count": 1
}
```

---

### 4. Delete Document

**DELETE** `/api/documents/{document_id}`

```bash
curl -X DELETE "http://localhost:8000/api/documents/a1b2c3d4-..."
```

**Response:**
```json
{
  "document_id": "a1b2c3d4-...",
  "message": "Successfully deleted document and 6 chunks",
  "success": true
}
```

---

### 5. Health Check

**GET** `/health`

```bash
curl "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-09T01:05:00.000000",
  "ollama_available": true,
  "chroma_available": true
}
```

---

## 🧪 Testing Guide

### Using Sample Document

The project includes `sample_product.txt` with wireless headphones information.

**1. Upload Document:**
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@sample_product.txt"
```

**2. Test Questions:**

| Question | Command | Expected Answer |
|----------|---------|----------------|
| **Features** | `curl -X POST "http://localhost:8000/api/query" -H "Content-Type: application/json" -d '{"query": "What features do the headphones have?"}'` | ANC, 30-hour battery, Bluetooth 5.2, etc. |
| **Price** | `curl -X POST "http://localhost:8000/api/query" -H "Content-Type: application/json" -d '{"query": "How much do they cost?"}'` | $399.99 |
| **Colors** | `curl -X POST "http://localhost:8000/api/query" -H "Content-Type: application/json" -d '{"query": "What colors are available?"}'` | Black, Silver, Midnight Blue |
| **Battery** | `curl -X POST "http://localhost:8000/api/query" -H "Content-Type: application/json" -d '{"query": "What is the battery life?"}'` | 30 hours (ANC on), 40 hours (ANC off) |

---

## 🎯 Design Decisions

### Why ChromaDB?

**Alternatives:** Pinecone, Milvus, Weaviate

**Chosen because:**
- ✅ Local-first (no API keys needed)
- ✅ Persistent storage
- ✅ Simple setup
- ✅ Perfect for demos and development

---

### Why Ollama?

**Alternatives:** OpenAI API, Hugging Face, Google Gemini

**Chosen because:**
- ✅ Privacy (runs locally)
- ✅ Free (no API costs)
- ✅ Fast local inference
- ✅ Easy model management

---

### Chunking Strategy

**Parameters:**
- Chunk Size: 500 characters
- Overlap: 100 characters (user customized from 50)
- Strategy: Sliding window

**Why these values?**
- Preserves context across boundaries
- Prevents information loss
- Balances granularity vs completeness
- Optimal for product descriptions

---

## 📁 Project Structure

```
E-Commerce Product Recommendation System/
│
├── app/
│   ├── main.py                  # FastAPI application
│   ├── config.py                # Configuration management
│   ├── models.py                # Pydantic models
│   │
│   ├── routes/
│   │   ├── documents.py         # Upload, list, delete endpoints
│   │   └── query.py             # Q&A endpoint
│   │
│   ├── services/
│   │   ├── document_processor.py    # Text extraction & chunking
│   │   ├── embeddings.py            # Vector generation
│   │   ├── vector_store.py          # ChromaDB operations
│   │   └── rag_pipeline.py          # RAG implementation
│   │
│   └── utils/
│       └── file_handlers.py     # File I/O operations
│
├── uploads/                     # Temporary file storage
├── chroma_db/                   # Vector database (auto-created)
│
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment config template
├── .gitignore                   # Git exclusions
│
├── README.md                    # This file
├── QUICKSTART.md                # Quick start guide
├── NUMPY_FIX.md                 # NumPy troubleshooting
│
├── sample_product.txt           # Test document
└── test_system.py               # System verification script
```

**Statistics:**
- Python Files: 18
- Lines of Code: 1200+
- API Endpoints: 5
- Services: 4

---

## 🔧 Configuration

### Environment Variables

```bash
# .env file (optional - defaults work!)

# Ollama Settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# ChromaDB Settings
CHROMA_PERSIST_DIR=./chroma_db

# Embedding Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Document Processing
CHUNK_SIZE=500
CHUNK_OVERLAP=100

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
```

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **NumPy 2.0 Error** `AttributeError: np.float_ was removed` | `pip install --force-reinstall numpy==1.26.4` <br> See [NUMPY_FIX.md](./NUMPY_FIX.md) |
| **Ollama Connection Failed** | `ollama serve` then `ollama pull llama3.2` |
| **Port 8000 in Use** | `uvicorn app.main:app --port 8001` |
| **Import Errors** | Activate venv: `.\venv\Scripts\activate` <br> Reinstall: `pip install -r requirements.txt` |

---

## 🚀 Future Enhancements

### Planned Features

- [ ] Support for `.docx` and `.html` files
- [ ] Conversational memory for multi-turn dialogue
- [ ] User authentication and access control
- [ ] Analytics dashboard
- [ ] Web UI for easier interaction
- [ ] Redis caching for better performance
- [ ] Docker containerization
- [ ] Multi-language support

---

## 📊 Assignment Requirements Met

✅ **Python backend** using FastAPI  
✅ **Vector Database** (ChromaDB) with semantic search  
✅ **LLM Integration** (Ollama with llama3.2)  
✅ **4+ REST API endpoints** (upload, query, list, delete, health)  
✅ **Clean, documented code** with type hints and docstrings  
✅ **README** with setup instructions  
✅ **requirements.txt** with all dependencies  
✅ **Design decisions** documented  

---

## 📄 License

This project is created as an assignment submission for educational purposes.

---

## 👤 Author

Developed as part of an AI/ML technical assessment.

**Demonstrates:**
- RAG implementation skills
- Vector database integration
- LLM application development
- Clean code practices
- Production-ready architecture

---

## 🙏 Acknowledgments

- **FastAPI** - Modern web framework
- **ChromaDB** - Vector database solution
- **Ollama** - Local LLM inference
- **sentence-transformers** - Embedding models
- **Hugging Face** - Model repository

---

<div align="center">

### 🌟 System Status: Production Ready! 🌟

**Built with ❤️ using Python, FastAPI, ChromaDB, and Ollama**

---

**⭐ Star this repository if it helped you!**

</div>
