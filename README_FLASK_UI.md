# Flask Chat UI for RAG Publications Project

This is a modern chat interface built with Flask for the RAG Publications Project. It provides a user-friendly way to interact with the RAG system through a web browser.

## Features

- Modern chat interface with message bubbles
- Markdown support for formatted responses
- Chat history with timestamps
- Example questions for easy starting points
- Responsive design that works on desktop and mobile
- Clear chat functionality
- Typing indicator during response generation

## Installation

1. Make sure you have Flask installed:

```bash
pip install flask
```

2. The Flask UI uses the existing RAG backend, so all dependencies from the main project are required.

## Running the Application

To start the Flask UI:

```bash
python app_flask.py
```

This will start a development server at http://127.0.0.1:5000/

## Project Structure

- `app_flask.py`: The main Flask application
- `templates/index.html`: The HTML template for the chat interface
- `static/css/custom.css`: Additional CSS styling
- `static/js/chat.js`: JavaScript for chat functionality

## How It Works

1. The Flask app serves the chat interface and handles API requests
2. User questions are sent to the backend via AJAX
3. The backend uses the existing RAG pipeline to process questions
4. Responses are returned to the UI and displayed as chat messages
5. Chat history is stored in the session and can be cleared

## Customization

- Edit `static/css/custom.css` to change the appearance
- Modify `static/js/chat.js` to change the behavior
- Update `templates/index.html` to change the structure

## Integration with Existing RAG System

The Flask UI uses the same `answer_query` function from `rag_utils.py` that the Streamlit interface uses, ensuring consistent behavior between the two interfaces.

## Advantages Over Streamlit

- More modern, chat-like interface
- Better control over styling and layout
- Faster response times (no page reloads)
- More professional appearance
- Better mobile experience