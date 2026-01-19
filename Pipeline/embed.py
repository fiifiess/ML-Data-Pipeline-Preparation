'''
This code turns the chunks into numerical features that a machine learning system can use.
I am very well aware there are transformers LLMs and other embedding models out there.
This provides a simulated experience.
THIS MODEL CAN ALWAYS BE SWAPPED WITH A REAL EMBEDDING MODEL IF RESULTS ARE NOT SATISFACTORY!
'''

from pathlib import Path
import json
import math

INPUT_FILE = Path("/Users/fiifiattuah/Desktop/ai_data_pipeline/Data/Processed/ingested_data.json")
OUTPUT_FILE = Path("/Users/fiifiattuah/Desktop/ai_data_pipeline/Data/Processed/embedded_data.json")
EMBEDDING_DIM = 8

def generate_embedding(text, dim = EMBEDDING_DIM):
    '''
    This will generate a placeholder embedding vector for text.
    This simulates real embeddings without external APIs or ML Models.
    Alternatives for this could be a transformer, a vector model, or an API call.
    '''

    vector = [0.0] * dim

    for i, char in enumerate(text):
        vector[i % dim] += ord(char) #ord(char) is a numerical value of each character. it is a form of tokenization. 

    # Normalize vector
    norm = math.sqrt(sum(v * v for v in vector)) 
    if norm > 0:
        vector = [v / norm for v in vector]

    return vector

def main():
    # Load ingested chunks
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)

    # Generate embeddings
    for record in records:
        record["embedding"] = generate_embedding(record["text"])
        record["embedding_dim"] = EMBEDDING_DIM

    # Save enriched output
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    print(f"Generated embeddings for {len(records)} chunks.")
    #now records are text, validated, vectorized and have metadata. Ready to use for ML.

if __name__ == "__main__":
    main()