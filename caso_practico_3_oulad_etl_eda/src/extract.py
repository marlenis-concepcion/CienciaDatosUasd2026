import pandas as pd

from src.config import CSV_FILES, RAW_DATA_DIR


def to_snake_case(name):
    result = []
    for char in name:
        if char.isupper() and result:
            result.append("_")
        result.append(char.lower())
    return "".join(result)


def load_raw_tables(raw_dir=RAW_DATA_DIR):
    tables = {}
    for table_name, file_name in CSV_FILES.items():
        path = raw_dir / file_name
        if not path.exists():
            raise FileNotFoundError(f"No se encontro el archivo requerido: {path}")

        df = pd.read_csv(path)
        df.columns = [to_snake_case(column.strip()) for column in df.columns]
        tables[table_name] = df
    return tables
