
import json

# Load Schema for Validation

def load_schema(schema_path):
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


# Validate the schema   
def validate_record(record, schema):
    for field, field_type in schema.items():
        if field not in record:
            raise ValueError(f"Missing required field: {field}")
        
        value = record[field]

        if field_type == "string" and not isinstance(value, str):
            raise TypeError(f"Field '{field}' must be a string!")
        
        if field_type == "integer" and not isinstance(value, int):
            raise TypeError(f"Field '{field}' must be an integer!")
        
        if field_type == "string" and isinstance(value, str) and not value.strip():
            raise TypeError(f"Field '{field}' cannot be empty!")
        
# Validate all records
def validate_records(records, schema):
    for idx, record in enumerate(records):
        try:
            validate_record(record, schema)
        except Exception as e:
            raise ValueError(f"Validation failed at record {idx}: {e}")
# This will stop at the first failure nd tell exactly which record is bad.


