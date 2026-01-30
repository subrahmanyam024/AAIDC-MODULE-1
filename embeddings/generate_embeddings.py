import json
import re
import requests
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient # type: ignore
from qdrant_client.http.models import VectorParams, Distance, PointStruct # type: ignore

# Load environment variables
load_dotenv()

def clean_and_truncate(text, max_len=4000):
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:max_len]

def generate_nomic_embeddings_batch(api_key, texts, model_name="nomic-embed-text-v1", task_type="search_document"):
    print(f"Generating embeddings for {len(texts)} texts using {model_name} (Task: {task_type})")
    
    if not texts:
        print("ERROR: Empty texts list provided to generate_nomic_embeddings_batch")
        return []
    
    url = "https://api-atlas.nomic.ai/v1/embedding/text"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "texts": texts,
        "model": model_name,
        "task_type": task_type
    }
    
    try:
        print(f"Sending request to Nomic API with first text: {texts[0][:50]}...")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        embeddings = result.get("embeddings", [])
        print(f"Successfully generated {len(embeddings)} embeddings")
        
        return embeddings
    except Exception as e:
        print(f"ERROR: Embedding batch failed: {e}")
        return []

def main(api_key, qdrant_url, qdrant_api_key):
    # Use relative path for better portability
    data_dir = "data"
    json_file = os.path.join(data_dir, "project_1_publications.json")
    
    # Get the absolute path based on the current script location
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    abs_json_file = os.path.join(script_dir, json_file)
    
    print(f"Loading publications from: {abs_json_file}")
    with open(abs_json_file, "r", encoding="utf-8") as f:
        publications = json.load(f)

    chunks = []
    for pub in publications:
        title = pub.get("title")
        description = pub.get("publication_description")
        if title and description:
            cleaned_desc = clean_and_truncate(description)
            chunk = f"{title}: {cleaned_desc}"
            chunks.append(chunk)

    print(f"Total document chunks to embed: {len(chunks)}")

    embeddings = []
    batch_size = 20 # Nomic supports larger batches
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"Embedding batch from index {i} to {i + len(batch) - 1}")
        batch_embeddings = generate_nomic_embeddings_batch(api_key, batch)
        if not batch_embeddings:
            print(f"Skipping batch from {i} due to failure.")
            continue
        embeddings.extend(batch_embeddings)

    if len(embeddings) == 0:
        raise ValueError("No embeddings were generated; aborting.")

    vector_size = len(embeddings[0])
    print(f"Single embedding vector size: {vector_size}")

    qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    collection_name = "publications"

    try:
        print(f"Attempting to delete existing collection '{collection_name}'")
        qdrant.delete_collection(collection_name)
    except Exception as e:
        print(f"Note: Could not delete collection (might not exist): {e}")

    print(f"Creating collection '{collection_name}'")
    qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )

    upload_count = min(len(embeddings), len(chunks))
    points = [
        PointStruct(id=i, vector=embeddings[i], payload={"content": chunks[i]})
        for i in range(upload_count)
    ]

    qdrant.upsert(collection_name=collection_name, points=points)
    print(f"Uploaded {upload_count} vectors to Qdrant collection '{collection_name}'.")

    return qdrant, api_key  # Return clients for reuse



if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    # Get credentials from environment variables
    API_KEY = os.getenv('NOMIC_API_KEY')
    QDRANT_URL = os.getenv('QDRANT_URL')
    QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
    
    if not API_KEY or not QDRANT_URL or not QDRANT_API_KEY:
        print("Error: Missing environment variables. Please set NOMIC_API_KEY, QDRANT_URL, and QDRANT_API_KEY in your .env file.")
        exit(1)
        
    main(API_KEY, QDRANT_URL, QDRANT_API_KEY)