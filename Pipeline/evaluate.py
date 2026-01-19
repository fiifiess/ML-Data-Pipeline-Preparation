'''
Currently, we can ingest, chunk data, embed the data, and retrieve the data.
But this helps us evaluate how well the process has gone. 
'''


from pathlib import Path
import json
from typing import List, Dict
from retrieve import retrieve, rerank_results
from tfidf_retrieve import build_tfidf_index, retrieve_tfidf

# Configuration

PROJECT_ROOT = Path(__file__).resolve().parents[1]

#EMBEDDED_FILE = Path("/Users/fiifiattuah/Desktop/ai_data_pipeline/Data/processed/embedded_data.json")
EMBEDDED_FILE = PROJECT_ROOT / "Data/Processed/embedded_data.json"
TOP_K = 3

# Evaluation queries with expected documents

EVAL_QUERIES = [
    {"query": "machine telemetry latency issue",
     "relevant_docs": ["telemetry_data_latency_runbook.md"]},
    {"query": "dashboard access problems for operators",
     "relevant_docs": ["dashboard_access_service_overview.md"]},
    {"query": "machine log search outage",
     "relevant_docs": ["machine_log_search_outage.md"]}
]

# Normalization for file names

def normalize(doc_id: str) -> str:
    return doc_id.replace("-", "_").lower()

# Evaluation Metrics

def precision_at_k(results: List[Dict], relevant_docs: List[str], k: int) -> float:
    '''
    Computes precision @ K
    '''

    top_k = results[:k]
    hits = sum(1 for r in top_k if normalize(r["document_id"]) in map(normalize, relevant_docs))
    return hits / k

# Main Evaluation Loop

def main():
    with open (EMBEDDED_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)

    total_precision = 0.0

    print("Retrieval Evaluation Results\n")

    vectorizer, tfidf_matrix = build_tfidf_index(records)

    for item in EVAL_QUERIES:
        query = item["query"]
        relevant_docs = item["relevant_docs"]

        results = retrieve(query, records, TOP_K)
        results = rerank_results(query, results)

        tfidf_results = retrieve_tfidf(
            query,
            records,
            vectorizer,
            tfidf_matrix,
            TOP_K
        )
        
        p_at_k = precision_at_k(results, relevant_docs, TOP_K)
        p_tfidf = precision_at_k(tfidf_results, relevant_docs, TOP_K)

        total_precision += p_at_k

        print(f"Query: {query}")
        print(f"Precision@{TOP_K}: {p_at_k:.2f}")
        print(f"Precision_TF-IDF@{TOP_K}: {p_tfidf:.2f}")
        print("Top results:")

        for r in results:
            print(f" - {r['document_id']} (score = {r['score']: .3f})")
        print("-" * 40)

        avg_precision = total_precision / len(EVAL_QUERIES)
        print(f"Average Precision@{TOP_K}: {avg_precision:.2f}")

        

if __name__ == "__main__":
    main()