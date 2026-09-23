"""Semana 5: auditoría por grupo e interseccional, incertidumbre, Green AI y decisión con compuertas."""
from __future__ import annotations

import json
from time import perf_counter

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tutoria_dss.baseline import rule_score
from tutoria_dss.config import ROOT, load_config
from tutoria_dss.data import load, split
from tutoria_dss.evaluation import top_k_mask
from scipy.stats import rankdata

from tutoria_dss.fairness import (allocate_by_group, audit_groups, by_group, choose_mitigation,
                                  gate_decision, recall_gap)
from tutoria_dss.models import build_logistic, predict_risk
from tutoria_dss.data import allowed_features


def main() -> None:
    cfg = load_config()
    share, gates, seed = cfg["capacity_share"], cfg["gates"], cfg["random_state"]
    reports = ROOT / "reports"
    parts = split(load(), seed)
    model = joblib.load(ROOT / "models/logistica.joblib")

    def alternatives(part: pd.DataFrame) -> dict[str, np.ndarray]:
        risk, rules = predict_risk(model, part), rule_score(part)
        edad = audit_groups(part)["edad"]
        return {"logistica": top_k_mask(risk, share), "reglas": top_k_mask(rules, share),
                "hibrido_rangos": top_k_mask(rankdata(risk) + rankdata(rules), share),
                "logistica_cupos_edad": allocate_by_group(risk, edad, share)}

    # 1) Validación: elegir la mitigación antes de mirar la prueba.
    valid = parts["valid"]
    vg, vy = audit_groups(valid), valid["abandono"].to_numpy()
    rows = []
    for name, sel in alternatives(valid).items():
        rows.append({"alternativa": name, "recall_capacidad": float((sel & (vy == 1)).sum() / vy.sum()),
                     "precision_capacidad": float(vy[sel].mean()),
                     **{f"brecha_{d}": recall_gap(by_group(vy, sel, vg[d], gates["min_group_size"]))
                        for d in ["genero", "edad", "beca"]}})
    valid_table = pd.DataFrame(rows)
    valid_table.to_csv(reports / "mitigacion_validacion.csv", index=False)
    chosen = choose_mitigation(valid_table, gates)

    # 2) Prueba: auditoría completa de todas las alternativas; decisión con compuertas para la elegida.
    test = parts["test"]
    groups, y = audit_groups(test), test["abandono"].to_numpy()
    tables, summary = [], {}
    for name, selected in alternatives(test).items():
        gaps = {}
        for dim in ["genero", "edad", "beca"]:
            t = by_group(y, selected, groups[dim], gates["min_group_size"]).assign(dimension=dim, alternativa=name)
            tables.append(t)
            gaps[dim] = recall_gap(t)
        inter = groups["genero"] + " | " + groups["edad"]
        tables.append(by_group(y, selected, inter, gates["min_group_size"]).assign(dimension="genero×edad",
                                                                                    alternativa=name))
        recall = float((selected & (y == 1)).sum() / y.sum())
        summary[name] = {"recall_capacidad": recall, "precision_capacidad": float(y[selected].mean()), "brechas": gaps}
    rng = np.random.default_rng(seed)
    chosen_upper = {}
    for dim in ["genero", "edad", "beca"]:
        values = []
        for _ in range(500):
            idx = rng.integers(0, len(y), len(y))
            sel = alternatives(test.iloc[idx])[chosen]
            values.append(recall_gap(by_group(y[idx], sel, groups[dim].to_numpy()[idx], gates["min_group_size"])))
        chosen_upper[dim] = float(np.percentile(values, 97.5))
    decision = gate_decision(summary[chosen]["recall_capacidad"], summary[chosen]["brechas"], chosen_upper, gates)
    audit = pd.concat(tables, ignore_index=True)
    audit.to_csv(reports / "equidad.csv", index=False)

    # Green AI: costo de entrenar e inferir en CPU.
    train = parts["train"]
    start = perf_counter()
    build_logistic(C=float(model.named_steps["model"].C)).fit(train[allowed_features()], train["abandono"])
    fit_seconds = perf_counter() - start
    start = perf_counter()
    for _ in range(20):
        predict_risk(model, test)
    infer_ms = 1000 * (perf_counter() - start) / (20 * len(test))
    green = {"segundos_entrenamiento": fit_seconds, "ms_por_estudiante": infer_ms,
             "tamano_modelo_kb": (ROOT / "models/logistica.joblib").stat().st_size / 1024,
             "parametros": int(model.named_steps["model"].coef_.size + 1), "hardware": "CPU Apple M1 Pro"}
    final = {"alternativa_elegida": chosen, "regla": "choose_mitigation en validación", **decision,
             "prueba_todas": summary, "green_ai": green,
             "nota": "El reparto de cupos por edad no usa la edad en el modelo; es una decisión de valores de la autora."}
    (reports / "decision_final.json").write_text(json.dumps(final, indent=2, ensure_ascii=False), encoding="utf-8")

    figure, axes = plt.subplots(1, 2, figsize=(11, 3.8), sharex=True)
    for axis, name in zip(axes, ["logistica", chosen]):
        plot = audit[(audit.alternativa == name) & (audit.dimension != "genero×edad")]
        labels = plot["dimension"] + ": " + plot["grupo"]
        axis.barh(labels, plot["recall_capacidad"], color=["#4c78a8" if ok else "#bbbbbb" for ok in plot["n_suficiente"]])
        axis.axvline(summary[name]["recall_capacidad"], color="black", ls="--", lw=1, label="global")
        axis.set_title(f"{name} · prueba", fontsize=9)
        axis.set_xlabel("recall a capacidad")
        axis.legend(fontsize=7)
    figure.tight_layout()
    figure.savefig(reports / "equidad.png", dpi=160)
    plt.close(figure)
    print(audit.round(3).to_string(index=False))
    print(valid_table.round(3).to_string(index=False))
    print(json.dumps(final, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
