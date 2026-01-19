'''
This file helps the ML model to find the relevant chunks of data based on queries made by users.
It is basically an internal search tool.
'''

from pathlib import Path
import json
import math
from typing import List

# Configuration

EMBEDDED_FILE = Path("/Users/fiifiattuah/Desktop/ai_data_pipeline/Data/processed/embedded_data.json")
TOP_K = 3

'''
Top-K is a sampling technique that limits the model's choice for the next word 
to a fixed number (K) of the most probable words, discarding the rest.

It makes the output more focused or deterministic as K decreases. 
It helps prevent nonsensical outputs by cutting off less likely options.
'''

# Similarity

'''
Cosine similarity 
'''

def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    '''
    Computes cosine similarity between two vectors. Cosine similarity is a measure
    of how similar two non-zero vectors are. It yields a score between -1 and 1.
    As it focuses on direction rather than magnitude, it is useful for comparing text meaning.
    '''

    dot = sum(a*b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a*a for a in vec_a))
    norm_b = math.sqrt(sum(b*b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0 # This handles zero vectors so that the code does not crash.
    
    return dot / (norm_a * norm_b)

# Retrieving similar chunks

def retrieve(query: str, records: list, top_k: int = TOP_K):
    '''
    Retrieve the top-k most similar chunks for a given query.
    '''

    # Generate embeddings for query using same logic
    from embed import generate_embedding
    query_embedding = generate_embedding(query)

    scored_chunks = []

    for record in records:
        score = cosine_similarity(query_embedding, record["embedding"])
        scored_chunks.append({
            "score": score,
            "document_id": record["document_id"],
            "chunk_id": record["chunk_id"],
            "heading": record.get("heading"),
            "text": record["text"],
        })

    scored_chunks.sort(key =lambda x: x["score"], reverse=True)
    return scored_chunks[:top_k]

# Main 

def main():
    with open(EMBEDDED_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)
    
    query = "machine telemetry latency issue"
    results = retrieve(query, records)

    print(f"Top {TOP_K} results for query: '{query}'\n")
    for idx, result in enumerate(results, start=1):
        print(f"Result {idx} (score={result['score']:.3f})")
        print(f"Document: {result['document_id']}")
        print(f"Section: {result['heading']}")
        print(f"Text: {result['text'][:200]}...")
        print("-" * 40)


if __name__ == "__main__":
    main()

