# Usage Guide for RAG Publications Assistant

This guide provides examples and best practices for using the RAG Publications Assistant.

## Getting Started

After setting up the application following the [Setup Guide](SETUP.md), you can access the chat interface by navigating to `http://localhost:5000` in your web browser.

## Basic Usage

### Starting a New Chat

1. Open your browser and navigate to `http://localhost:5000`
2. You'll be greeted with a welcome message
3. Type your question in the input box at the bottom of the screen
4. Press Enter or click the Send button to submit your question
5. The typing indicator will appear while the system processes your query
6. The answer will be displayed in the chat interface

### Clearing Chat History

To start a new conversation:

1. Click the "Clear Chat" button at the top of the chat interface
2. This will reset the conversation and create a new chat session
3. Your previous conversation will still be stored in the database

## Example Queries

Here are some example queries you can try with the RAG Publications Assistant:

### General Queries

- "What publications are available about machine learning?"
- "Show me the most recent publications in the database"
- "What are the top-cited publications?"
- "List publications by author John Smith"
- "What publications discuss neural networks?"

### Specific Queries

- "What does the publication 'Advances in Neural Network Architectures' discuss?"
- "Who are the authors of 'Machine Learning for Time Series Analysis'?"
- "When was 'Reinforcement Learning in Robotics' published?"
- "How many citations does 'Quantum Computing Applications' have?"
- "What are the key findings in 'Climate Change Prediction Models'?"

### Follow-up Queries

The system maintains conversation context, so you can ask follow-up questions:

Initial query: "Tell me about publications on deep learning"
Follow-up: "Which one has the most citations?"
Follow-up: "What are its key findings?"

## Advanced Usage

### Adjusting Result Precision

The default configuration retrieves the top 5 most relevant documents for each query. If you want more comprehensive answers, you can modify the code in `rag_utils.py` to increase this number:

```python
# In rag_utils.py
def answer_query(user_question, top_k=10, ...):  # Increased from 5 to 10
```

### Using with Different Data

While the system is pre-configured to work with the publications dataset, you can adapt it to work with other datasets:

1. Prepare your data in a similar JSON format
2. Update the data loading path in `embeddings/generate_embeddings.py`
3. Run the embedding generation script to create embeddings for your new data
4. The system will now answer questions based on your custom dataset

## Best Practices

1. **Be Specific**: The more specific your question, the more accurate the answer will be.

2. **Use Natural Language**: You can ask questions in natural language rather than using keywords.

3. **Context Matters**: The system maintains conversation context, so you can ask follow-up questions without repeating all the details.

4. **Check Sources**: The system retrieves information from the publications database. If you need information outside this dataset, it may not be able to provide accurate answers.

5. **Clear Chat for New Topics**: When switching to a completely new topic, it's best to clear the chat history to avoid context confusion.

## Troubleshooting

### Slow Responses

If you're experiencing slow responses:

1. Check your internet connection, as the system uses external APIs
2. Reduce the number of retrieved documents (top_k parameter)
3. Ensure you're not hitting API rate limits

### Irrelevant Answers

If you're getting irrelevant answers:

1. Try rephrasing your question to be more specific
2. Check if the information you're looking for is actually in the publications dataset
3. Try increasing the number of retrieved documents (top_k parameter)

### Typing Indicator Issues

If the typing indicator isn't displaying properly:

1. Make sure JavaScript is enabled in your browser
2. Try refreshing the page
3. Check for any console errors in your browser's developer tools