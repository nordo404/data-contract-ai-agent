import yaml
from llm.model import call_llm


ORDER_PROMPT = """
You are a senior data modeler. Reorder the columns below using best practices:
1. Identifier fields first (id, key, uuid, pk, fk)
2. Core entity attributes next (names, emails, measures, amounts, categories)
3. Flags/booleans next
4. Dates/timestamps next
5. Audit fields last (created_at, updated_at, deleted_at)

Rules:
- Do NOT rename columns.
- Do NOT add or remove columns.
- Output ONLY a JSON array of column names in the new order.
- Do NOT output YAML.
- Do NOT output markdown.
- Do NOT use code fences.
- Do NOT include explanations or comments.

Example of the ONLY valid output format:
["id", "customer_id", "first_name", "last_name"]

Columns:
{columns_yaml}
"""


def order_columns_with_llm(columns: list) -> list:
    """
    Ask the LLM to reorder columns using data modeling best practices.
    Returns a list of column dicts in the new order.
    """

    col_names = [c["name"] for c in columns]
    prompt = ORDER_PROMPT.format(columns_yaml=yaml.safe_dump(col_names))

    llm_output = call_llm(prompt)

    try:
        ordered_names = yaml.safe_load(llm_output)
        if not isinstance(ordered_names, list):
            return columns
    except Exception:
        return columns

    # Rebuild column list in new order
    name_to_col = {c["name"]: c for c in columns}
    return [name_to_col[name] for name in ordered_names if name in name_to_col]
