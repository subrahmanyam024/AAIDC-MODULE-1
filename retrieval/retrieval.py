def retrieve_relevant_chunks(qdrant_client, query_embedding, top_k=5, collection_name="publications"):
    print(f"DEBUG - Retrieving from collection: {collection_name}")
    
    # Verify collection exists
    if not qdrant_client.collection_exists(collection_name):
        print(f"ERROR - Collection {collection_name} does not exist!")
        
        # Check if publications collection exists as fallback
        if collection_name != "publications" and qdrant_client.collection_exists("publications"):
            print(f"DEBUG - Falling back to 'publications' collection")
            collection_name = "publications"
        else:
            print("ERROR - No valid collection found!")
            return []
    
    # Get collection info to verify it has points
    try:
        collection_info = qdrant_client.get_collection(collection_name)
        points_count = collection_info.points_count
        print(f"DEBUG - Collection {collection_name} has {points_count} points")
        
        if points_count == 0:
            print(f"WARNING - Collection {collection_name} exists but has no points!")
            if collection_name != "publications" and qdrant_client.collection_exists("publications"):
                print(f"DEBUG - Falling back to 'publications' collection due to empty collection")
                collection_name = "publications"
                collection_info = qdrant_client.get_collection(collection_name)
                points_count = collection_info.points_count
                print(f"DEBUG - Publications collection has {points_count} points")
    except Exception as e:
        print(f"ERROR - Failed to get collection info: {e}")
    
    try:
        print(f"DEBUG - Searching collection {collection_name} with vector of length {len(query_embedding)}")
        results = qdrant_client.search(collection_name=collection_name, query_vector=query_embedding, limit=top_k)
        print(f"DEBUG - Retrieved {len(results)} results from {collection_name}")
        
        # Extract content from payload
        chunks = []
        for i, res in enumerate(results):
            try:
                content = res.payload.get("content")
                score = res.score
                print(f"DEBUG - Result {i+1}: score={score:.4f}, content_length={len(content) if content else 0}")
                if content:
                    chunks.append(content)
            except Exception as e:
                print(f"ERROR - Error extracting content from result: {e}")
        
        print(f"DEBUG - Extracted {len(chunks)} content chunks")
        
        # Print sample of first chunk if available
        if chunks and len(chunks) > 0:
            print(f"DEBUG - First chunk sample: {chunks[0][:100]}...")
        
        return chunks
    except Exception as e:
        print(f"ERROR - Error searching collection {collection_name}: {e}")
        return []
