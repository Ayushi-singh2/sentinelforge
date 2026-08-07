# SentinelForge

AI-powered Retrieval-Augmented Generation (RAG) API and dashboard.

## Features

- FastAPI backend
- RAG pipeline
- ChromaDB vector storage
- Sentence Transformers embeddings
- API key authentication
- Request middleware
- Prompt injection protection
- Source citations
- React dashboard

## Technologies

- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- React
- Vite

## Running the Backend

cd backend
.\.venv\Scripts\activate
uvicorn app.main:app --reload

## Running the Frontend

cd frontend
npm install
npm run dev

## Testing

python -m tests.test_auth
python -m tests.test_middleware
python -m tests.test_e2e