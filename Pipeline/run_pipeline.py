'''
This is the entry point for the AI Data Pipeline
This is the script that wires together all the pipeline stages in the right order.
'''

from pathlib import Path
import json

from ingest import build_records
from validate import load_schema, validate_records
from embed import generate_embedding

# Configuration
'''
Old paths. Revert to this if you start having issues.
RAW_DATA_DIR = Path("/Users/fiifiattuah/Desktop/ai_data_pipeline/Data/Raw")
SCHEMA_PATH = Path("/Users/fiifiattuah/Desktop/ai_data_pipeline/Data/Schema/document_schema.json")
OUTPUT_PATH = Path("/Users/fiifiattuah/Desktop/ai_data_pipeline/Data/Processed/embedded_data.json")
'''

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "Data"
RAW_DATA_DIR = DATA_DIR / "Raw"
PROCESSED_DIR = DATA_DIR / "Processed"
SCHEMA_DIR = DATA_DIR / "Schema"
SCHEMA_PATH = SCHEMA_DIR / "Document_schema.json"
OUTPUT_PATH = PROCESSED_DIR / "embedded_data.json"


# Pipeline Runner

def run_pipeline():
    print("Starting AI Data Pipeline...\n")
    # 1. Ingest
    print("[1/4] Ingesting markdown files...")
    records = build_records(RAW_DATA_DIR)
    print(f" Ingested {len(records)} records")

    # 2. Validate
    print("[2/4] Validating records against schema...")
    schema = load_schema(SCHEMA_PATH)
    validate_records(records, schema)
    print(" Validation passed") 

    # 3. Embed
    print("[3/4] Generating embeddings...")
    for record in records:
        record["embedding"] = generate_embedding(record["text"])
    print(" Embeddings generated")

    # 4. Store
    print("[4/4] Writing embedded records to disk...")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    print("\nPipeline completed successfully.")
    print(f"Output written to: {OUTPUT_PATH}")

if __name__ == "__main__":
    run_pipeline()