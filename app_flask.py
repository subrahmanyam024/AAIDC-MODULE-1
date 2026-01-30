from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from rag_utils import answer_query, qdrant, API_KEY
from embeddings.generate_embeddings import generate_nomic_embeddings_batch
from qdrant_client.http.models import VectorParams, Distance, PointStruct # type: ignore
from memory.memory_manager import get_connection
import datetime
import os
import uuid
import json
import PyPDF2
from docx import Document

# Set up Flask app
app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)  # For session management
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def extract_text_from_file(file_path, filename):
    ext = os.path.splitext(filename)[1].lower()
    text = ""
    
    if ext == '.pdf':
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    elif ext == '.docx':
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    elif ext == '.json':
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    text += str(item) + "\n"
            else:
                text = json.dumps(data)
                
    return text

def chunk_text(text, chunk_size=1000):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1
        if current_length >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
            
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks

@app.route('/')
def landing():
    """Redirect to welcome page"""
    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    """Welcome page with greeting and start chat button"""
    return render_template('welcome.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('welcome'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('welcome'))
    
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process file
        text = extract_text_from_file(file_path, filename)
        chunks = chunk_text(text)
        
        if not chunks:
            return "No text could be extracted from the file.", 400
            
        # Generate embeddings
        embeddings = []
        batch_size = 20
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            batch_embeddings = generate_nomic_embeddings_batch(API_KEY, batch)
            embeddings.extend(batch_embeddings)
            
        # Create unique collection for this user session
        collection_name = "user_" + str(uuid.uuid4())[:8]
        vector_size = len(embeddings[0])
        
        qdrant.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )
        
        points = [
            PointStruct(id=i, vector=embeddings[i], payload={"content": chunks[i]})
            for i in range(len(embeddings))
        ]
        qdrant.upsert(collection_name=collection_name, points=points)
        
        # Store collection name in session
        session['collection_name'] = collection_name
        session['current_file'] = filename
        
        # Initialize chat
        session['chat_id'] = str(uuid.uuid4())
        session['chat_history'] = []
        session.modified = True
        
        return redirect(url_for('chat'))

@app.route('/reset_to_default')
def reset_to_default():
    """Clear session-specific files and reset to default dataset"""
    session.pop('collection_name', None)
    session.pop('current_file', None)
    session['chat_id'] = str(uuid.uuid4())
    session['chat_history'] = []
    session.modified = True
    return redirect(url_for('chat'))

@app.route('/chat')
def chat():
    """Chat interface page"""
    # Initialize session if needed
    if 'chat_id' not in session:
        session['chat_id'] = str(uuid.uuid4())
    if 'user_email' not in session:
        session['user_email'] = "user@example.com"
    
    collection_name = session.get('collection_name')
    filename = session.get('current_file')
    
    if 'chat_history' not in session:
        session['chat_history'] = []
        # No initial message so the welcome/empty state shows up
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
        # Use the publications RAG pipeline
        print(f"DEBUG - Processing question: {question}")
        collection_name = session.get('collection_name', 'publications')
        
        response = answer_query(
            question, 
            top_k=5, 
            user_email=session.get('user_email', "user@example.com"),
            chat_id=session.get('chat_id', "default"),
            collection_name=collection_name
        )
        print(f"DEBUG - Got response from RAG pipeline (Collection: {collection_name})")
        
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
    # Clear chat history and reset session-specific files
    session['chat_history'] = []
    session.pop('collection_name', None)
    session.pop('current_file', None)
    
    # Generate a new chat ID to prevent memory interference
    session['chat_id'] = str(uuid.uuid4())
    
    session.modified = True
    return jsonify({
        'status': 'success'
    })

@app.route('/history', methods=['GET'])
def get_history():
    """Fetch all history for the modal from MySQL"""
    user_email = session.get('user_email', "user@example.com")
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        # Fetch last 10 interactions across all chat IDs for this user
        sql = "SELECT question, response as answer, created_at as timestamp FROM chat_history WHERE email=%s ORDER BY created_at DESC LIMIT 10"
        cursor.execute(sql, (user_email,))
        results = cursor.fetchall()
        
        # Convert datetime to string for JSON serialization
        for row in results:
            if row['timestamp']:
                row['timestamp'] = row['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
                
        cursor.close()
        conn.close()
        
        return jsonify(results)
    except Exception as e:
        print(f"Error fetching history: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True)