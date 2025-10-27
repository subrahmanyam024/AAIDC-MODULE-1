# Setup Guide for RAG Publications Assistant

This guide will walk you through the process of setting up the RAG Publications Assistant on your local machine.

## Prerequisites

- Python 3.8 or higher
- MySQL Server
- Git

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/RAG_Publications_Project.git
cd RAG_Publications_Project
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment:

- On Windows:
```bash
venv\Scripts\activate
```

- On macOS/Linux:
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit the `.env` file and add your API keys:

```
# Cohere API key
COHERE_API_KEY=your_cohere_api_key_here

# Jina AI and Qdrant credentials
JINA_API_KEY=your_jina_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here

# Database configuration
DB_HOST=localhost
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_NAME=rag_assistant
```

### 5. Set Up MySQL Database

1. Log in to MySQL:

```bash
mysql -u root -p
```

2. Create the database:

```sql
CREATE DATABASE rag_assistant;
USE rag_assistant;
```

3. Create the chat history table:

```sql
CREATE TABLE chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    chat_id VARCHAR(255) NOT NULL,
    question TEXT NOT NULL,
    response TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

4. Exit MySQL:

```sql
EXIT;
```

### 6. Generate Embeddings

Run the embedding generation script to create vector embeddings for the publications data:

```bash
python -m embeddings.generate_embeddings
```

This will:
1. Load the publications data from `data/project_1_publications.json`
2. Generate embeddings using Jina AI
3. Store the embeddings in Qdrant

### 7. Run the Application

Start the Flask application:

```bash
python app_flask.py
```

The application will be available at `http://localhost:5000`.

## Troubleshooting

### Database Connection Issues

If you encounter database connection issues:

1. Verify your MySQL credentials in the `.env` file
2. Ensure MySQL service is running
3. Check that the database and table are created correctly

### API Key Issues

If you encounter API key issues:

1. Verify that your API keys are correctly set in the `.env` file
2. Check that you have active subscriptions for Jina AI, Qdrant, and Cohere
3. Ensure you have sufficient quota/credits for the services

### Embedding Generation Issues

If embedding generation fails:

1. Check your Jina AI API key
2. Verify that the data file exists at `data/project_1_publications.json`
3. Ensure you have internet connectivity to reach the Jina AI API

## Additional Configuration

### Customizing the Number of Retrieved Documents

You can adjust the number of documents retrieved for each query by modifying the `top_k` parameter in `rag_utils.py`:

```python
def answer_query(user_question, top_k=5, ...):
```

Increase the value for more comprehensive (but potentially less focused) answers, or decrease it for more concise responses.

### Adjusting the LLM Parameters

You can modify the LLM parameters in `llm/llm_handler.py` to adjust the behavior of the language model.