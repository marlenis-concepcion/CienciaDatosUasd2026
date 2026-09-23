from __future__ import annotations

import json

import matplotlib.pyplot as plt
import pandas as pd

from inf8239_u02.config import ROOT, settings
from inf8239_u02.data import deduplicate, load_dataset, normalize_text, sha256, validate_dataframe


def audit() -> dict:
    df = load_dataset()
    validate_dataframe(df, settings.text_column, settings.target_column)
    text = df[settings.text_column].astype(str)
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    _, dedup = deduplicate(df, settings.text_column, settings.target_column)
    keys = text.map(normalize_text)
    repeated = (
        df.assign(clave=keys)
        .groupby("clave")
        .agg(veces=("id", "size"), label=(settings.target_column, "first"), ejemplo=(settings.text_column, "first"))
        .query("veces > 1")
        .sort_values("veces", ascending=False)
    )
    repeated.head(15).to_csv(reports / "duplicados_frecuentes.csv", index=False)
    lengths = df.assign(caracteres=text.str.len(), palabras=text.str.split().str.len())
    summary = {
        "archivo": str(settings.dataset_path.relative_to(ROOT)),
        "sha256_csv": sha256(settings.dataset_path),
        "filas": int(df.shape[0]),
        "columnas": list(df.columns),
        "nulos": {c: int(v) for c, v in df.isna().sum().items()},
        "distribucion": {k: int(v) for k, v in df[settings.target_column].value_counts().items()},
        "proporcion": {k: round(float(v), 4) for k, v in df[settings.target_column].value_counts(normalize=True).items()},
        "duplicados": dedup,
        "grupos_repetidos": int(len(repeated)),
        "caracteres_por_clase": {
            k: {m: round(float(v), 1) for m, v in g["caracteres"].describe(percentiles=[0.5, 0.9]).items()}
            for k, g in lengths.groupby(settings.target_column)
        },
    }
    (reports / "auditoria.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    figure, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    counts = df[settings.target_column].value_counts()
    axes[0].bar(counts.index, counts.values, color=["#4c78a8", "#e45756"])
    axes[0].set_title("Mensajes por clase (antes de deduplicar)")
    for i, v in enumerate(counts.values):
        axes[0].text(i, v, str(v), ha="center", va="bottom")
    for label, color in [("ham", "#4c78a8"), ("spam", "#e45756")]:
        axes[1].hist(lengths.loc[lengths[settings.target_column] == label, "caracteres"],
                     bins=40, alpha=0.6, label=label, color=color, range=(0, 400))
    axes[1].set_title("Longitud en caracteres por clase")
    axes[1].set_xlabel("caracteres")
    axes[1].legend()
    figure.tight_layout()
    figure.savefig(reports / "auditoria.png", dpi=160)
    plt.close(figure)
    return summary


def main() -> None:
    summary = audit()
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
