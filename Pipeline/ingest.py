'''
This file ...
* Reads Markdown files
* Splits them into logical “chunks” 
* Converts each chunk into a structured record using the data's schema
* Stores the structured output (we can store as JSON for now)
''' 

# Imports

import os 
import json
from pathlib import Path
from validate import load_schema, validate_records
# os and Path let us navigate folders safely.
# json lets us store structured records.

# Path Definitions

RAW_DIR = Path("/Users/fiifiattuah/Desktop/ai_data_pipeline/Data/Raw") # points to Markdown files.
OUTPUT_FILE = Path("/Users/fiifiattuah/Desktop/ai_data_pipeline/Data/Processed/ingested_data.json") # clean and structured records come here
SCHEMA_FILE = Path("/Users/fiifiattuah/Desktop/ai_data_pipeline/Data/Schema/document_schema.json")
# Using Path rather than strings avoids OS path issues.

# Loading files

def load_markdown_files(directory):
    files = list(directory.glob("*.md"))    # only reads .md files, ignores others.
    data = []
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:   # avoids errors with special characters
            content = f.read()
            data.append({"filename": file_path.name, "content": content})   # wraps file in a dictionary with filename and content
    return data

def chunk_text(text, chunk_size = 500):
    '''
    Splits text into chunks of chunk_size words.
    Some ML systems have token limits so chunks is helpful.
    '''

    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk_text = " ".join(words[i:i + chunk_size])
        chunks.append(chunk_text)
    return chunks


def chunk_text_by_heading(text):
    '''
    Splits text into chunks separated by headings.
    '''
        
    lines = text.splitlines()
    chunks = []
    current_chunk = []

    for line in lines:
        if (line.startswith('##') or line.startswith('###')) and current_chunk:
            # Save previous chunk
            chunks.append("\n".join(current_chunk).strip())
            current_chunk = [line]
        else:
            current_chunk.append(line)
    if current_chunk:
        chunks.append("\n".join(current_chunk).strip())
    
    return chunks


# Converting to Structured Records

def build_records(raw_dir: Path):
    markdown_files = list(raw_dir.glob("*.md"))
    records = []
    for file in markdown_files:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        chunks = chunk_text_by_heading(content)
        for idx, chunk in enumerate(chunks):
            record = {
                "document_id": file.name, #["filename"],    #keeps traceability
                "chunk_id": str(idx),                    #helps debugging later
                "text": chunk,                      #chunk content
                "source_file": "manufacturing_docs"      #optional metadata
            }
            records.append(record)
    return records

# Save records

def save_records(records, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)   #ensures folder exists
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)                     #readable JSON, easy to inspect

# Main Execution

if __name__ == "__main__":
    files_data = load_markdown_files(RAW_DIR)
    records = build_records(files_data)

    schema = load_schema(SCHEMA_FILE)
    validate_records(records, schema)

    save_records(records, OUTPUT_FILE)
    print(f"Ingested {len(records)} chunks from {len(files_data)} files.")



