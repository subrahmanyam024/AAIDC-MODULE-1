import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'rag_assistant')
    )

def insert_interaction(email, chat_id, question, response):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO chat_history (email, chat_id, question, response) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (email, chat_id, question, response))
    conn.commit()
    cursor.close()
    conn.close()

def get_last_questions(email, chat_id, limit=3):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT question FROM chat_history WHERE email=%s AND chat_id=%s ORDER BY created_at DESC LIMIT %s"
    cursor.execute(sql, (email, chat_id, limit))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row[0] for row in results]



if __name__ == "__main__":
    # Test insertion
    insert_interaction("user@test.com", "chat001", "What is RAG?", "It stands for Retrieval-Augmented Generation.")
    # Test retrieval
    print(get_last_questions("user@test.com", "chat001", 3))
