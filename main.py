import argparse
import logging
import os
import yaml

from schema.infer_schema import infer_schema
from llm.agent_loop import agent_enrich_schema
from generator.description_generator import generate_table_description
from generator.template_engine import apply_template
from generator.column_ordering import order_columns_with_llm


# ---------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def load_reference(path: str) -> str:
    logger.info(f"Loading reference contract from: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def derive_output_path(csv_path: str, output_dir: str = "output") -> str:
    """
    Convert CSV filename → YAML filename and place it in the output directory.
    Example: data/Leads.csv → output/Leads.yaml
    """
    base = os.path.basename(csv_path)
    name, _ = os.path.splitext(base)
    yaml_name = f"{name}.yaml"
    return os.path.join(output_dir, yaml_name)


def save_output(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    logger.info(f"Saving generated contract to: {path}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def pretty_yaml(data: dict) -> str:
    """
    Render YAML with extra spacing:
    - blank line between top-level sections
    - blank line between each column block
    """
    raw = yaml.safe_dump(data, sort_keys=False)
    lines = raw.split("\n")
    output = []
    inside_columns = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Detect entering columns block
        if stripped == "columns:":
            inside_columns = True
            output.append(line)
            continue

        # Add blank line before each column item
        if inside_columns and stripped.startswith("- "):
            output.append("")  # blank line
            output.append(line)
            continue

        # Detect leaving columns block
        if inside_columns and stripped == "":
            inside_columns = False

        # Add blank line between top-level keys
        if not inside_columns and stripped and not line.startswith(" "):
            if output and output[-1] != "":
                output.append("")  # blank line before new section

        output.append(line)

    return "\n".join(output)


# ---------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Generate a YAML data contract from a CSV file.")
    parser.add_argument("--csv", required=True, help="Path to input CSV file")
    parser.add_argument("--reference", required=True, help="Path to reference contract YAML")
    parser.add_argument("--output", default=None, help="Optional override for output file path")

    parser.add_argument(
        "--order-columns",
        action="store_true",
        help="Use LLM to reorder columns using data modeling best practices"
    )

    args = parser.parse_args()

    logger.info("Starting contract generation pipeline")
    logger.info(f"CSV file: {args.csv}")
    logger.info(f"Reference contract: {args.reference}")

    # Step 1: Infer schema
    logger.info("Inferring schema from CSV...")
    schema = infer_schema(args.csv)

    # Add object/table name from CSV filename
    base = os.path.basename(args.csv)
    table_name, _ = os.path.splitext(base)
    schema["object"] = table_name

    logger.info(f"Inferred {len(schema['columns'])} columns")
    logger.info(f"Object/table name set to: {table_name}")

    # Step 2: Optional column enrichment
    logger.info("Enriching column descriptions (optional)...")
    schema = agent_enrich_schema(schema)

    # Step 3: Optional column ordering
    if args.order_columns:
        logger.info("Reordering columns using LLM best practices...")
        schema["columns"] = order_columns_with_llm(schema["columns"])
    else:
        logger.info("Keeping original CSV column order")

    # Step 4: Generate rich semantic table description
    logger.info("Generating semantic table description...")
    description = generate_table_description(schema)

    # Step 5: Load reference template
    reference_yaml = load_reference(args.reference)

    # Step 6: Apply template engine
    logger.info("Applying template engine...")
    patched_contract = apply_template(schema, reference_yaml, description)

    # Step 7: Determine output path
    output_path = args.output or derive_output_path(args.csv)

    # Step 8: Save final YAML with pretty formatting
    final_yaml = pretty_yaml(patched_contract)
    save_output(output_path, final_yaml)

    logger.info("Pipeline complete")
    logger.info(f"Contract saved to: {output_path}")


if __name__ == "__main__":
    main()
