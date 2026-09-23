"""Ejercicio 08 (LAB13): inventario, minimización, retención, trazabilidad, RACI, monitoreo y simulacro."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from inf8239_u04.data import load_data, temporal_split
from inf8239_u04.governance import load_config, validate_raci
from inf8239_u04.lifecycle import (apply_retention, build_manifest, check_inputs, check_performance, load_inventory,
                                   minimize, respond, rule, write_json)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/lab13"
INCIDENT_START = "2026-12-01"
SCALE_BUG = 0.1  # la ingesta empieza a registrar exposure en otra escala


def weekly(df: pd.DataFrame) -> list[tuple[str, pd.DataFrame]]:
    return [(str(w.start_time.date()), b) for w, b in df.groupby(df.received_date.dt.to_period("W"))]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = load_config()
    limits, retention = cfg["monitoring"], cfg["retention"]
    df = load_data()
    train, test = temporal_split(df)

    # 1) Inventario, minimización y retención.
    inventory = load_inventory()
    operational, audit_view = minimize(df, inventory, "operational"), minimize(df, inventory, "audit")
    as_of = "2027-06-30"
    kept_op, deleted_op = apply_retention(operational, as_of, retention["operational_cases_months"])
    kept_audit, deleted_audit = apply_retention(audit_view, as_of, retention["audit_view_months"])
    write_json(OUT / "minimizacion_retencion.json", {
        "columnas_originales": list(df.columns), "vista_operativa": list(operational.columns),
        "vista_auditoria": list(audit_view.columns),
        "columnas_retiradas_de_la_operacion": sorted(set(df.columns) - set(operational.columns)),
        "simulacion_retencion": {"fecha_revision": as_of,
                                 "operativa": {"meses": retention["operational_cases_months"], "conservados": len(kept_op),
                                               "eliminados": deleted_op},
                                 "auditoria": {"meses": retention["audit_view_months"], "conservados": len(kept_audit),
                                               "eliminados": deleted_audit}}})

    # 2) RACI y decisión del proyecto base (compuertas sobre la regresión logística).
    raci = pd.read_csv(ROOT / "student_inputs/raci.csv")
    validate_raci(raci)
    subprocess.run([sys.executable, str(ROOT / "scripts/lab13_governance.py")], check=True, cwd=ROOT,
                   capture_output=True)

    # 3) Monitoreo normal: entradas por semana y desempeño en ventana móvil de 100 casos.
    rows = []
    for week, batch in weekly(test):
        check = check_inputs(batch, train, limits)
        rows.append({"semana": week, "escenario": "normal", "n": check["n"], "z_exposure": check["z_exposure"],
                     "z_previous_incidents": check["z_previous_incidents"], "alertas": "; ".join(check["alerts"]),
                     "estado": respond(check)})
    perf_rows = []
    for month_end in ["2026-10-31", "2026-11-30", "2026-12-31"]:
        window = test[test.received_date <= month_end].tail(limits["min_window"])
        perf = check_performance(window, rule(window), limits)
        perf_rows.append({"corte": month_end, **{k: v for k, v in perf.items() if k != "alerts"},
                          "alertas": "; ".join(perf["alerts"])})

    # 4) Simulacro: desde el 1 de diciembre exposure llega multiplicada por 0.1 (cambio de escala en la ingesta).
    faulty = test.copy()
    affected = faulty.received_date >= INCIDENT_START
    faulty.loc[affected, "exposure"] *= SCALE_BUG
    timeline = []
    for week, batch in weekly(faulty[affected]):
        check = check_inputs(batch, train, limits)
        rows.append({"semana": week, "escenario": "incidente", "n": check["n"], "z_exposure": check["z_exposure"],
                     "z_previous_incidents": check["z_previous_incidents"], "alertas": "; ".join(check["alerts"]),
                     "estado": respond(check)})
        timeline.append((week, check, respond(check)))
    monitoring = pd.DataFrame(rows)
    monitoring.to_csv(OUT / "monitoreo_entradas.csv", index=False)
    pd.DataFrame(perf_rows).to_csv(OUT / "monitoreo_desempeno.csv", index=False)

    good, bad = test[affected], faulty[affected]
    first_week = weekly(bad)[0][1]
    good_first = good.loc[first_week.index]
    fn = lambda part, pred: int(((part.target == 1) & (pred == 0)).sum())
    impact = {
        "casos_afectados_diciembre": int(affected.sum()), "positivos_reales": int(good.target.sum()),
        "falsos_negativos_con_datos_correctos": fn(good, rule(good)),
        "falsos_negativos_si_nadie_detecta": fn(good, rule(bad)),
        "casos_alto_riesgo_perdidos_si_nadie_detecta": fn(good, rule(bad)) - fn(good, rule(good)),
        "casos_alto_riesgo_perdidos_en_primera_semana": fn(good_first, rule(first_week)) - fn(good_first, rule(good_first)),
        "recall_correcto": float(check_performance(good, rule(good), limits)["recall"]),
        "recall_con_falla": float(check_performance(good, rule(bad), limits)["recall"]),
        "semana_deteccion": timeline[0][0], "z_deteccion": timeline[0][1]["z_exposure"], "estado": timeline[0][2],
    }
    write_json(OUT / "simulacro.json", impact)
    postmortem = f"""# Postmortem · simulacro de incidente de datos

Simulacro ejecutado por `scripts/run_e08.py` sobre la línea temporal sintética. Valores calculados en `reports/lab13/simulacro.json`.

- **Escenario:** desde el {INCIDENT_START} la ingesta registra `exposure` multiplicada por {SCALE_BUG} (cambio de unidad no comunicado).
- **Detección:** semana del {impact['semana_deteccion']}; `check_inputs` mide un desplazamiento de la media de exposure de {impact['z_deteccion']:.1f} errores estándar (umbral ±{limits['max_abs_z']}). Ninguna semana normal superó |z| = {monitoring[monitoring.escenario == 'normal'][['z_exposure', 'z_previous_incidents']].abs().max().max():.1f}.
- **Clasificación:** severidad alta (deriva de una variable de decisión). Estado del runbook: **{impact['estado']}**.
- **Contención:** el ML Engineer desactiva el orden sugerido y pasa a orden de llegada con revisión manual; autoriza el Institutional Owner (RACI: Respuesta a incidentes).
- **Evidencia preservada:** lote afectado, alertas (`monitoreo_entradas.csv`), hashes (`manifest.json`) y commit del código.
- **Impacto medido:** {impact['casos_afectados_diciembre']} casos en diciembre con {impact['positivos_reales']} de alto riesgo. Si nadie lo detectara, el recall caería de {impact['recall_correcto']:.3f} a {impact['recall_con_falla']:.3f} y se dejarían sin priorizar {impact['casos_alto_riesgo_perdidos_si_nadie_detecta']} casos de alto riesgo más; al detectarlo en la primera semana, la pérdida se limita a {impact['casos_alto_riesgo_perdidos_en_primera_semana']} caso(s), que se revisan de inmediato al volver a puntuar.
- **Comunicación:** interna el mismo día; el Product Owner informa a las comunidades de las zonas con casos reordenados y ofrece revisión prioritaria en 5 días hábiles.
- **Reversión:** volver a la versión anterior de la ingesta, volver a puntuar todos los casos desde el {INCIDENT_START} y revisar primero los casos de alto riesgo reordenados.
- **Causa raíz:** cambio de unidad en la fuente sin contrato de datos que fijara la escala.

## Acciones correctivas
| Acción | Responsable | Fecha límite |
|---|---|---|
| Añadir la escala y el rango esperado de `exposure` al contrato de datos | Data Engineer | 2026-12-15 |
| Prueba automática de deriva en cada carga (`check_inputs`) antes de puntuar | ML Engineer | 2026-12-15 |
| Protocolo de aviso de cambios de fuente entre proveedor de datos y Data Engineer | Product Owner | 2026-12-31 |
| Revisión del postmortem y cierre | Institutional Owner | 2027-01-08 |
"""
    (OUT / "INCIDENT_POSTMORTEM.md").write_text(postmortem, encoding="utf-8")

    figure, axis = plt.subplots(figsize=(9, 3.4))
    for scenario, style in [("normal", "-o"), ("incidente", "-s")]:
        part = monitoring[monitoring.escenario == scenario]
        axis.plot(pd.to_datetime(part.semana), part.z_exposure, style, label=f"exposure · {scenario}")
    normal = monitoring[monitoring.escenario == "normal"]
    axis.plot(pd.to_datetime(normal.semana), normal.z_previous_incidents, "--", color="grey", label="previous_incidents · normal")
    for sign in (-1, 1):
        axis.axhline(sign * limits["max_abs_z"], color="red", ls="--", lw=1)
    axis.set_ylabel("desplazamiento de la media (z)")
    axis.set_title("Monitoreo semanal de entradas: operación normal y simulacro")
    axis.legend(fontsize=7)
    figure.tight_layout()
    figure.savefig(OUT / "monitoreo.png", dpi=160)
    plt.close(figure)

    # 5) Manifiesto de trazabilidad (al final, para incluir los documentos vigentes).
    write_json(OUT / "manifest.json", build_manifest({
        "dataset": ROOT / "data/territorial_risk_synthetic.csv", "configuracion": ROOT / "configs/governance.yml",
        "inventario": ROOT / "docs/data_inventory.csv", "raci": ROOT / "student_inputs/raci.csv",
        "decision_e07": ROOT / "reports/lab12/decision.json", "datasheet": ROOT / "docs/DATASHEET.md",
        "model_card": ROOT / "docs/MODEL_CARD.md", "runbook": ROOT / "docs/RUNBOOK.md"}))
    print(monitoring.round(2).to_string(index=False))
    print(pd.DataFrame(perf_rows).round(3).to_string(index=False))
    print(impact)


if __name__ == "__main__":
    main()
