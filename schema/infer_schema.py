import polars as pl
import re
from datetime import datetime

def to_snake_case(name: str) -> str:
    name = re.sub(r'[^0-9a-zA-Z]+', '_', name)
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower().strip('_')


def detect_date_format(value: str):
    """Try common date formats and return the matching one in your contract style."""
    if value is None:
        return None

    formats = {
        "%Y-%m-%d": "yyyy-MM-dd",
        "%d/%m/%Y": "d/M/yyyy",
        "%m/%d/%Y": "M/d/yyyy",
        "%Y/%m/%d": "yyyy/M/d",
        "%d-%m-%Y": "d-M-yyyy",
        "%m-%d-%Y": "M-d-yyyy",
        "%Y%m%d": "yyyyMMdd",
    }

    for fmt_in, fmt_out in formats.items():
        try:
            datetime.strptime(value, fmt_in)
            return fmt_out
        except Exception:
            pass

    return None


def map_polars_to_contract_type(dtype):
    if dtype in (pl.Int8, pl.Int16, pl.Int32, pl.Int64):
        return "long"
    if dtype in (pl.Float32, pl.Float64):
        return "double"
    if dtype == pl.Boolean:
        return "boolean"
    if dtype == pl.Date:
        return "date"
    if dtype == pl.Datetime:
        return "timestamp"
    return "string"


def infer_schema(csv_path: str, sample_size: int = 20):
    df = pl.read_csv(csv_path)

    columns = []
    for col in df.columns:
        series = df[col]

        snake = to_snake_case(col)
        contract_type = map_polars_to_contract_type(series.dtype)

        # detect date format only if string
        fmt = None
        if contract_type == "string":
            sample_values = (
                df[col]
                .drop_nulls()
                .head(sample_size)
                .to_list()
            )
            for v in sample_values:
                detected = detect_date_format(str(v))
                if detected:
                    contract_type = "date"
                    fmt = detected
                    break

        nullable = series.null_count() > 0

        columns.append({
            "name": snake,
            "type": contract_type,
            "nullable": nullable,
            "format": fmt,
        })

    return {
        "object": csv_path.split("/")[-1].replace(".csv", ""),
        "columns": columns,
    }
