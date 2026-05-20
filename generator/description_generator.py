import json
from llm.model import call_llm


DESCRIPTION_PROMPT = """
You are a senior data analyst. Based ONLY on the column names and data types below,
produce a concise but rich semantic description of what this dataset likely represents.

Guidelines:
- Use professional analytical language.
- Infer the business purpose or domain if it is strongly suggested by the columns.
- Mention key themes such as entities, events, lifecycle stages, or business processes.
- Do NOT hallucinate fields that are not present.
- Do NOT mention uncertainty (avoid phrases like "might be" or "possibly").
- Output ONLY the description sentence.

Columns (JSON):
{columns_json}
"""


def generate_table_description(schema: dict) -> str:
    """
    Generate a rich semantic description of the dataset using column names and types.
    Uses the LLM but keeps the prompt tightly controlled to avoid hallucination.
    """

    # Prepare a compact list of {name, type}
    cols = [
        {"name": c["name"], "type": c["type"]}
        for c in schema["columns"]
    ]

    prompt = DESCRIPTION_PROMPT.format(
        columns_json=json.dumps(cols, indent=2)
    )

    description = call_llm(prompt)

    # Safety: ensure it's a single line, no YAML formatting issues
    return description.strip().replace("\n", " ")
