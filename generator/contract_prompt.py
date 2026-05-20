CONTRACT_PROMPT = """
You are an expert data engineer responsible for generating a clean, production-ready
YAML data contract.

You will be given:
1. A reference contract that shows the exact structure, formatting, and style.
2. An inferred schema (JSON) containing column names, types, nullability, and formats.
3. Optional metadata such as table name, schema name, primary keys, and tags.

Your task:
- Produce a final YAML contract that strictly follows the structure and formatting
  of the reference contract.
- Use the inferred schema to populate the `columns:` section.
- Use metadata when provided; otherwise fall back to reasonable defaults.
- Omit the `format:` field for any column where the value is null.
- Do NOT hallucinate columns or metadata.
- Do NOT reorder keys unless the reference contract does so.
- The output MUST be valid YAML.

Reference contract:
-------------------
{reference_contract}

Inferred schema (JSON):
-----------------------
{schema_json}

Metadata (JSON):
----------------
{metadata_json}

Now generate the final YAML contract below.
Only output YAML. Do not include explanations.
"""
