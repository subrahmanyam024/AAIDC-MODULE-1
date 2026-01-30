---
description: Repository Information Overview
alwaysApply: true
---

# RAG Publications Assistant Information

## Summary
A Flask-based Retrieval-Augmented Generation (RAG) assistant designed for analyzing publication content. It leverages Nomic embeddings, Qdrant vector database, and Cohere/OpenRouter LLMs to provide context-aware answers. The system supports dynamic file uploads (PDF, DOCX, TXT, JSON) and maintains persistent chat history using MySQL.

## Structure
- **Root**: Contains main application files (`app_flask.py`, `rag_utils.py`), configuration files, and documentation.
- **embeddings/**: Logic for generating vector embeddings using the Nomic API.
- **llm/**: Interface for LLM interaction, supporting ChatCohere and OpenAI-compatible endpoints.
- **memory/**: Manages persistent conversation history via MySQL.
- **retrieval/**: Handles semantic search and chunk retrieval from Qdrant.
- **templates/**: HTML templates for the web interface (Landing, Welcome, and Chat).
- **static/**: CSS and JavaScript assets for the frontend UI.
- **data/**: Contains the default publication dataset (`project_1_publications.json`).
- **uploads/**: Destination for user-uploaded documents during processing.

## Language & Runtime
**Language**: Python  
**Version**: 3.x  
**Framework**: Flask 2.3.3  
**Package Manager**: pip

## Dependencies
**Main Dependencies**:
- `flask`: Web framework
- `qdrant-client`: Vector database interaction
- `langchain-cohere` & `langchain-core`: LLM orchestration
- `mysql-connector-python`: MySQL database connectivity
- `PyPDF2`, `python-docx`, `pdfminer.six`: Document parsing
- `python-dotenv`: Environment variable management
- `openai`: Fallback LLM client

## Build & Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and DB credentials

# Run the application
python app_flask.py
```

## Main Files & Resources
- **app_flask.py**: Main entry point and Flask route definitions.
- **rag_utils.py**: Core RAG pipeline logic orchestration.
- **memory/memory_manager.py**: Database schema interaction for chat history.
- **llm/llm_handler.py**: LLM prompt engineering and API management.
- **data/project_1_publications.json**: Initial dataset for the assistant.

## Testing & Validation
The project does not include a formal testing framework (like pytest). Validation is performed via:
- Manual testing scripts within `if __name__ == "__main__":` blocks in `memory_manager.py`, `rag_backend.py`, and `llm_handler.py`.
- Debug print statements within the Flask application flow.

## Database Configuration
**MySQL**:
- Table: `chat_history`
- Schema: `(email, chat_id, question, response, created_at)`
- Purpose: Stores persistent user interactions for context-aware querying.

**Qdrant**:
- Purpose: Vector storage for publication chunks and user-uploaded document segments.
- Distance Metric: Cosine
- Embeddings: `nomic-embed-text-v1`
