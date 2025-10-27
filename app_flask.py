from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from rag_utils import answer_query
import datetime
import os
import uuid

# Set up Flask app
app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)  # For session management

@app.route('/')
def landing():
    """Redirect to welcome page"""
    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    """Welcome page with greeting and start chat button"""
    return render_template('welcome.html')

@app.route('/chat')
def chat():
    """Chat interface page"""
    # Initialize session if needed
    if 'chat_id' not in session:
        session['chat_id'] = str(uuid.uuid4())
    if 'user_email' not in session:
        session['user_email'] = "user@example.com"
    if 'chat_history' not in session:
        session['chat_history'] = []
        
        # Add a welcome message to chat history
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        welcome_message = {
            'question': 'Hello',
            'answer': "Welcome to the RAG Publications Assistant! I can answer questions about the publications dataset. How can I help you today?",
            'timestamp': timestamp
        }
        session['chat_history'].append(welcome_message)
        session.modified = True
    
    return render_template('index.html', chat_history=session.get('chat_history', []))

# No document upload or processing functions needed for static data

@app.route('/query', methods=['POST'])
def process_query():
    # Make sure session is initialized
    if 'chat_id' not in session:
        session['chat_id'] = str(uuid.uuid4())
    if 'user_email' not in session:
        session['user_email'] = "user@example.com"
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    data = request.json
    question = data.get('question', '')
    
    if not question.strip():
        return jsonify({'error': 'Question cannot be empty'}), 400
    
    try:
        # No delay needed as we're relying on frontend for typing indicator visibility
        import time
        
        # Use the publications RAG pipeline
        print(f"DEBUG - Processing question: {question}")
        response = answer_query(
            question, 
            top_k=5, 
            user_email=session.get('user_email', "user@example.com"),
            chat_id=session.get('chat_id', "default")
        )
        print("DEBUG - Got response from publications RAG pipeline")
        
        # Create timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Store in session history
        chat_entry = {
            'question': question,
            'answer': response,
            'timestamp': timestamp
        }
        
        session['chat_history'].append(chat_entry)
        session.modified = True
        
        # No delay needed before returning the response
        
        return jsonify({
            'answer': response,
            'timestamp': timestamp
        })
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/clear_history', methods=['POST'])
def clear_history():
    # Clear chat history
    session['chat_history'] = []
    
    # Generate a new chat ID
    session['chat_id'] = str(uuid.uuid4())
    
    # Add a welcome message to chat history
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    welcome_message = {
        'question': 'Hello',
        'answer': "Welcome to the RAG Publications Assistant! I can answer questions about the publications dataset. How can I help you today?",
        'timestamp': timestamp
    }
    session['chat_history'].append(welcome_message)
    
    session.modified = True
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True)