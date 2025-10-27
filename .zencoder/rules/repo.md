---
description: Repository Information Overview
alwaysApply: true
---

# RAG Publications Project Information

## Summary
A Retrieval-Augmented Generation (RAG) application with dual interfaces: a Streamlit app and a Flask web application. The system allows users to query publications data and upload documents (PDF, DOCX, TXT) for question answering. It uses Jina AI for embeddings, Qdrant for vector storage, and Cohere for LLM capabilities with conversation memory.

## Structure
- **app.py**: Main Streamlit application entry point for querying publications
- **app_flask.py**: Flask web application with document upload functionality
- **rag_utils.py**: Core RAG functionality and utilities shared by both interfaces
- **data/**: Contains publication dataset in JSON format
- **embeddings/**: Module for generating embeddings using Jina AI
- **llm/**: Module for LLM interaction with Cohere
- **memory/**: Module for chat history persistence using MySQL database
- **retrieval/**: Module for retrieving relevant chunks from vector store
- **templates/**: HTML templates for the Flask web interface
- **static/**: CSS and JavaScript files for the web interface
- **uploads/**: Directory for storing uploaded documents

## Language & Runtime
**Language**: Python
**Version**: Python 3.10 (based on venv structure)
**Package Manager**: pip

## Dependencies
**Main Dependencies**:
- Flask/Streamlit: Web frameworks for different interfaces
- PyPDF2/pdfminer.six: PDF text extraction with fallback mechanism
- python-docx: DOCX document processing
- qdrant_client: Vector database client for similarity search
- langchain_cohere: LLM integration for answer generation
- mysql.connector: Database connection for conversation memory
- requests: HTTP client for API calls to embedding services

**External Services**:
- Jina AI: For embeddings generation (API key required)
- Qdrant: Vector database for storing embeddings (cloud instance)
- Cohere: LLM provider for question answering
- MySQL: Database for conversation memory persistence

## Document Processing
**Supported Formats**: PDF, DOCX, TXT, DOC
**PDF Extraction**: Uses PyPDF2 with pdfminer.six as fallback for problematic PDFs
**Text Processing**: Cleans and truncates text, splits into paragraph chunks
**Vector Storage**: Creates document-specific Qdrant collections for each upload

## RAG Pipeline
**Embedding Generation**: Jina AI embeddings API (jina-embeddings-v2-base-en model)
**Vector Database**: Qdrant Cloud with collection per document
**Retrieval**: Semantic search with cosine similarity for top-k chunks
**Context Building**: Combines retrieved chunks into unified context
**Question Refinement**: Uses conversation history to create standalone questions
**Answer Generation**: Cohere LLM with context-based prompting
**Fallback Mechanism**: Uses text search when vector search fails

## Web Interfaces
**Streamlit App**: 
- Run with: `streamlit run app.py`
- Simple chat interface for querying publications dataset
- Chat history panel with reload functionality

**Flask App**:
- Run with: `python app_flask.py`
- Document upload functionality with multiple format support
- Modern chat interface with message bubbles
- Markdown support for formatted responses
- Session-based chat history

## Build & Installation
```bash
# Install required packages
pip install flask streamlit PyPDF2 python-docx qdrant-client langchain-cohere python-dotenv mysql-connector-python requests pdfminer.six

# Set up MySQL database
# Create database named 'rag_assistant' with a 'chat_history' table

# Run Flask application
python app_flask.py

# Or run Streamlit application
streamlit run app.py
```

## Database Configuration
**Type**: MySQL
**Connection**: Local database (localhost)
**Database Name**: rag_assistant
**Tables**: chat_history (stores user questions, AI responses, chat IDs, and timestamps)