import copy
import yaml


def apply_template(schema: dict, reference_yaml: str, description: str) -> dict:
    """
    Patch the reference YAML template with:
      - object name (from CSV filename)
      - table.name (same as object)
      - table.description (LLM-generated)
      - columns (entire block replaced with inferred schema)

    Everything else in the reference YAML remains untouched.
    """

    # Load reference YAML into a Python dict
    ref = yaml.safe_load(reference_yaml)

    # Deep copy to avoid mutating the original reference
    patched = copy.deepcopy(ref)

    object_name = schema["object"]

    # -------------------------------
    # 1. Replace object
    # -------------------------------
    patched["object"] = object_name

    # -------------------------------
    # 2. Replace table.name
    # -------------------------------
    if "table" not in patched:
        patched["table"] = {}

    patched["table"]["name"] = object_name

    # -------------------------------
    # 3. Replace table.description
    # -------------------------------
    patched["table"]["description"] = description

    # -------------------------------
    # 4. Replace columns block entirely
    # -------------------------------
    patched["columns"] = []

    for col in schema["columns"]:
        col_block = {
            "name": col["name"],
            "type": col["type"],
            "nullable": True,
        }
        if col.get("format"):
            col_block["format"] = col["format"]

        patched["columns"].append(col_block)

    return patched
