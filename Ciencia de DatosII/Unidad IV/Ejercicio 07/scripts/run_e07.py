"""Ejercicio 07: evaluación de impacto (LAB11) y auditoría de equidad con mitigación y decisión (LAB12)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from inf8239_u04.data import load_data, temporal_split
from inf8239_u04.evaluation import (bootstrap_gaps, candidates, choose, final_decision, flag_small_cells,
                                    intersectional)
from inf8239_u04.fairness import audit
from inf8239_u04.governance import load_config

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts/lab11_impact.py")], check=True, cwd=ROOT)
    out = ROOT / "reports/lab12"
    out.mkdir(parents=True, exist_ok=True)
    gates = load_config()["gates"]
    df = load_data()
    table, predictions, info = candidates(df)
    table.to_csv(out / "candidatos.csv", index=False)
    chosen, reason = choose(table, gates)
    _, test = temporal_split(df)
    y, groups = test.target.to_numpy(), test.protected_group.to_numpy()

    detail = {}
    for name in [chosen, "logistica_0.50"]:
        pred = predictions[name]
        _, by_group, _ = audit(y, pred, groups)
        _, by_age, _ = audit(y, pred, test.age_band)
        _, inter, _ = audit(y, pred, intersectional(test))
        inter = flag_small_cells(inter)
        suffix = "" if name == chosen else "_logistica"
        by_group.to_csv(out / f"por_grupo{suffix}.csv")
        by_age.to_csv(out / f"por_edad{suffix}.csv")
        inter.to_csv(out / f"interseccional{suffix}.csv")
        detail[name] = {"ci": bootstrap_gaps(y, pred, groups), "small": int((~inter["n_suficiente"]).sum())}
    (out / "bootstrap.json").write_text(json.dumps({k: v["ci"] for k, v in detail.items()}, indent=2), encoding="utf-8")

    test_row = table[(table.etapa == "prueba") & (table.candidato == chosen)].iloc[0]
    decision = {"candidato_elegido": chosen, "razon_eleccion": reason, **info,
                **final_decision(test_row, detail[chosen]["ci"], gates, detail[chosen]["small"]),
                "modelo_ml_logistica": final_decision(
                    table[(table.etapa == "prueba") & (table.candidato == "logistica_0.50")].iloc[0],
                    detail["logistica_0.50"]["ci"], gates, detail["logistica_0.50"]["small"]),
                "tomada_con_validacion": True}
    (out / "decision.json").write_text(json.dumps(decision, indent=2, ensure_ascii=False), encoding="utf-8")

    test_table = table[table.etapa == "prueba"].set_index("candidato")
    figure, axes = plt.subplots(1, 2, figsize=(11, 3.8))
    test_table[["recall", "fpr", "accuracy"]].plot.barh(ax=axes[0])
    axes[0].axvline(gates["min_recall"], color="red", ls="--", lw=1)
    axes[0].set_title("Prueba (línea: recall mínimo 0.68)")
    test_table[["recall_gap", "fpr_gap", "selection_gap"]].plot.barh(ax=axes[1])
    axes[1].axvline(gates["max_recall_gap"], color="red", ls="--", lw=1)
    axes[1].set_title("Brechas G1–G2 (línea: tolerancia 0.16)")
    for axis in axes:
        axis.legend(fontsize=7)
    figure.tight_layout()
    figure.savefig(out / "candidatos.png", dpi=160)
    plt.close(figure)
    print(table.round(3).to_string(index=False))
    print(json.dumps(decision, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
