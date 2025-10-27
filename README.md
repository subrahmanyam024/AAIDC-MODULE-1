# RAG Publications Assistant

A Flask-based Retrieval Augmented Generation (RAG) assistant for publications data. This application uses vector search with Qdrant and Jina AI embeddings to provide accurate answers to questions about publications.

## Features

- Real-time chat interface with enhanced typing indicators
- Vector search using Qdrant for semantic retrieval
- Jina AI embeddings for high-quality semantic understanding
- Publication data retrieval and summarization
- Chat history memory for contextual conversations
- MySQL database for persistent storage of conversations

## Architecture

The application consists of several components:

- **Flask Backend**: Handles HTTP requests and serves the web interface
- **Embedding Generation**: Creates vector embeddings using Jina AI
- **Vector Database**: Stores and retrieves embeddings using Qdrant
- **LLM Integration**: Uses Cohere for question refinement and answer generation
- **Memory Management**: Stores conversation history in MySQL

## Quick Start

1. Clone the repository
2. Copy `.env.example` to `.env` and add your API keys
3. Install dependencies: `pip install -r requirements.txt`
4. Set up the MySQL database (see [Setup Guide](SETUP.md))
5. Run the application: `python app_flask.py`
6. Open your browser and navigate to `http://localhost:5000`

## Detailed Documentation

- [Setup Guide](SETUP.md)
- [Usage Examples](USAGE.md)

## Sample Inputs and Outputs

### Example 1: Basic Question
**Input**: "What are the latest publications about machine learning?"

**Output**: 
```
Based on the provided context, there are several recent publications about machine learning:

1. "Advances in Neural Network Architectures" which discusses recent developments in neural network design and implementation.

2. "Machine Learning for Time Series Analysis" which explores applications of ML algorithms for analyzing temporal data.

3. "Reinforcement Learning in Robotics" which covers how RL techniques are being applied to robotic systems.

These publications cover various aspects of machine learning including neural networks, time series analysis, and reinforcement learning applications.
```

### Example 2: Follow-up Question
**Input**: "Which one has the most citations?"

**Output**:
```
According to the information in the dataset, "Advances in Neural Network Architectures" has the highest citation count with 127 citations. This publication has been particularly influential in the field of deep learning research.
```

## License

MIT License

## Acknowledgements

- Jina AI for embedding generation
- Qdrant for vector database
- Cohere for language model capabilities
- Flask for the web framework