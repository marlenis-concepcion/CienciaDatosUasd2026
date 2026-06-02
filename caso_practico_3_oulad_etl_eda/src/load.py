import psycopg

from src.config import PostgresConfig


LOAD_ORDER = [
    "courses",
    "assessments",
    "student_info",
    "student_registration",
    "vle",
    "student_assessment",
    "student_vle",
]


def load_tables(tables, config=PostgresConfig(), schema="oulad"):
    with psycopg.connect(**config.connect_kwargs()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SET search_path TO {schema}")
            for table_name in LOAD_ORDER:
                df = tables[table_name]
                columns = list(df.columns)
                placeholders = ", ".join(["%s"] * len(columns))
                sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                cursor.executemany(sql, df.where(df.notna(), None).itertuples(index=False, name=None))
        connection.commit()
