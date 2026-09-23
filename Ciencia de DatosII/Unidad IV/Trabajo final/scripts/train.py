"""Semana 3: búsqueda de C, comparación en validación, decisión, evaluación única en prueba y errores."""
from __future__ import annotations

import json

import joblib
import numpy as np

from tutoria_dss.baseline import rule_score
from tutoria_dss.config import ROOT, load_config
from tutoria_dss.data import load, split
from tutoria_dss.evaluation import choose, compare, error_profile
from tutoria_dss.models import predict_risk, tune


def main() -> None:
    cfg = load_config()
    share, seed = cfg["capacity_share"], cfg["random_state"]
    reports, models = ROOT / "reports", ROOT / "models"
    reports.mkdir(exist_ok=True)
    models.mkdir(exist_ok=True)
    parts = split(load(), seed)
    model, search, seconds = tune(parts["train"], seed)
    search.to_csv(reports / "busqueda_C.csv", index=False)
    joblib.dump(model, models / "logistica.joblib")
    rng = np.random.default_rng(seed)
    scores = lambda d: {"aleatorio": rng.random(len(d)), "reglas": rule_score(d), "logistica": predict_risk(model, d)}
    valid = compare(parts["valid"]["abandono"].to_numpy(), scores(parts["valid"]), share)
    valid.to_csv(reports / "validacion.csv", index=False)
    chosen = choose(valid)
    ceiling = min(1.0, np.ceil(share * len(parts["test"])) / parts["test"]["abandono"].sum())
    decision = {"alternativa_elegida": chosen, "regla": "mayor recall a capacidad en validación; desempate por "
                "average precision", "C": float(model.named_steps["model"].C), "segundos_busqueda": seconds,
                "techo_recall_capacidad_prueba": float(ceiling), "tomada_antes_de_prueba": True}
    (reports / "decision.json").write_text(json.dumps(decision, indent=2, ensure_ascii=False), encoding="utf-8")
    test = compare(parts["test"]["abandono"].to_numpy(), scores(parts["test"]), share)
    test.to_csv(reports / "prueba.csv", index=False)
    error_profile(parts["test"], predict_risk(model, parts["test"]), share).to_csv(reports / "errores_perfil.csv")
    print(valid.round(3).to_string(index=False), "\n", test.round(3).to_string(index=False), "\n", decision)


if __name__ == "__main__":
    main()
