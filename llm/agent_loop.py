import yaml
from llm.model import call_llm


def is_valid_yaml(text: str) -> bool:
    """Check if the LLM output is valid YAML."""
    try:
        yaml.safe_load(text)
        return True
    except Exception:
        return False


def enrich_column_descriptions(schema: dict, max_retries: int = 2) -> dict:
    """
    Optional: Ask the LLM to generate column descriptions.
    This does NOT modify structure — only adds a 'description' field per column.
    """

    columns = schema["columns"]

    # Build a compact prompt
    prompt = f"""
You are a data analyst. For each column below, generate a short, clear description
of what the field represents. Do NOT hallucinate fields. Output valid YAML only.

columns:
{yaml.safe_dump(columns)}
"""

    for attempt in range(max_retries):
        llm_output = call_llm(prompt)

        if not is_valid_yaml(llm_output):
            continue

        try:
            enriched = yaml.safe_load(llm_output)
            # Expecting: { "columns": [ {name, type, description}, ... ] }
            if "columns" in enriched:
                return enriched["columns"]
        except Exception:
            pass

    # If enrichment fails, return original columns unchanged
    return columns


def agent_enrich_schema(schema: dict) -> dict:
    """
    Main entry point for the agent loop in the new architecture.
    Only enriches column descriptions (optional).
    """

    enriched_columns = enrich_column_descriptions(schema)

    # Return a new schema dict with enriched columns
    return {
        **schema,
        "columns": enriched_columns
    }
