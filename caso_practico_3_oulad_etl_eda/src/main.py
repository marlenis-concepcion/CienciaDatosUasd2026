from src.config import AUDIT_DATA_DIR, PROCESSED_DATA_DIR
from src.extract import load_raw_tables
from src.quality import find_duplicate_keys, profile_tables, validate_domains
from src.transform import add_student_features, clean_tables


def main():
    tables = load_raw_tables()
    cleaned = clean_tables(tables)

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Perfil inicial de tablas:")
    for row in profile_tables(cleaned):
        print(row)

    duplicates = find_duplicate_keys(cleaned)
    domains = validate_domains(cleaned)

    for name, df in duplicates.items():
        path = AUDIT_DATA_DIR / f"duplicados_{name}.csv"
        df.to_csv(path, index=False)
        print(f"Duplicados detectados en {name}: {path}")

    for name, df in domains.items():
        path = AUDIT_DATA_DIR / f"dominio_invalido_{name.replace('.', '_')}.csv"
        df.to_csv(path, index=False)
        print(f"Dominio invalido detectado en {name}: {path}")

    features = add_student_features(cleaned)
    features.to_csv(PROCESSED_DATA_DIR / "student_course_features.csv", index=False)
    print("Archivo procesado creado: data/processed/student_course_features.csv")


if __name__ == "__main__":
    main()
