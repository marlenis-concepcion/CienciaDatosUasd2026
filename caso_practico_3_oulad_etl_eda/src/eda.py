from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.config import PROCESSED_DATA_DIR, PROJECT_DIR


OUTPUT_FIGURES = PROJECT_DIR / "outputs" / "figures"
OUTPUT_TABLES = PROJECT_DIR / "outputs" / "tables"


def generate_eda(features_path=PROCESSED_DATA_DIR / "student_course_features.csv"):
    if not Path(features_path).exists():
        raise FileNotFoundError(
            "Primero ejecute el ETL para crear data/processed/student_course_features.csv"
        )

    OUTPUT_FIGURES.mkdir(parents=True, exist_ok=True)
    OUTPUT_TABLES.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(features_path)
    summary = df.groupby(["code_module", "code_presentation", "final_result"]).size()
    summary = summary.reset_index(name="students")
    summary.to_csv(OUTPUT_TABLES / "resumen_resultados_por_curso.csv", index=False)

    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="final_result", order=df["final_result"].value_counts().index)
    plt.title("Distribucion de resultados finales")
    plt.xlabel("Resultado final")
    plt.ylabel("Cantidad de estudiantes")
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES / "grafico_01_distribucion_resultados.png", dpi=150)
    plt.close()

    if "total_clicks_student_course" in df.columns:
        plt.figure(figsize=(8, 5))
        sns.boxplot(data=df, x="final_result", y="total_clicks_student_course")
        plt.title("Interaccion VLE por resultado final")
        plt.xlabel("Resultado final")
        plt.ylabel("Total de clics")
        plt.tight_layout()
        plt.savefig(OUTPUT_FIGURES / "grafico_02_clicks_por_resultado.png", dpi=150)
        plt.close()

    return {
        "rows": len(df),
        "summary_table": str(OUTPUT_TABLES / "resumen_resultados_por_curso.csv"),
        "figures_dir": str(OUTPUT_FIGURES),
    }


if __name__ == "__main__":
    print(generate_eda())

