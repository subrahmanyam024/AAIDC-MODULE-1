# RAG Publications Assistant

A professional Flask-based Retrieval-Augmented Generation (RAG) assistant for analyzing publication content. This application uses Nomic embeddings, Qdrant vector database, and Cohere/OpenRouter LLMs to provide intelligent, context-aware answers.

## 🚀 Features

- **Dynamic Context Isolation**: Unique session management (`chat_id`) prevents memory interference when switching between different publications.
- **Persistent Chat History**: All interactions are stored in MySQL, accessible via a dedicated "History Modal" in the UI.
- **Multi-Format Support**: Upload and query PDF, DOCX, TXT, and JSON files seamlessly.
- **Advanced UI/UX**: 
  - Real-time typing indicators with pulsing animations.
  - Light/Dark mode toggle with complete CSS variable integration.
  - Streamlined chat bubbles with feedback icons.
  - Floating background particles and glassmorphism effects.
- **Nomic Embeddings**: High-quality semantic understanding using `nomic-embed-text-v1`.

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Vector DB**: Qdrant
- **Embeddings**: Nomic AI
- **LLM**: ChatCohere (via LangChain)
- **Database**: MySQL (for persistent memory)
- **Frontend**: Bootstrap 5, FontAwesome, Marked.js (Markdown support)

## 📋 Prerequisites

- Python 3.8+
- MySQL Server
- Qdrant (Cloud or Local)
- API Keys: Nomic, Cohere (or OpenRouter)

## ⚙️ Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd RAG_Publications_Project
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**:
   Create a `.env` file in the root directory:
   ```env
   NOMIC_API_KEY=your_nomic_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_key
   COHERE_API_KEY=your_cohere_key
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=rag_assistant
   ```

4. **Database Setup**:
   ```sql
   CREATE DATABASE rag_assistant;
   USE rag_assistant;
   CREATE TABLE chat_history (
       id INT AUTO_INCREMENT PRIMARY KEY,
       email VARCHAR(255),
       chat_id VARCHAR(255),
       question TEXT,
       response TEXT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

5. **Run the App**:
   ```bash
   python app_flask.py
   ```

## 📂 Project Structure

- `app_flask.py`: Main entry point and routes.
- `rag_utils.py`: RAG pipeline orchestration.
- `memory/`: MySQL memory management logic.
- `llm/`: LLM handler for question refinement and generation.
- `embeddings/`: Nomic embedding generation logic.
- `static/`: CSS, JS, and UI assets.
- `templates/`: HTML templates for the interface.

## 🛡️ License

MIT License
