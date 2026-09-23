from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import yaml
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
REPO = ("https://github.com/marlenis-concepcion/CienciaDatosUasd2026/tree/main/"
        "Ciencia%20de%20DatosII/Unidad%20IV/Ejercicio%2007")


def table(rows, styles, widths=None):
    cells = [[Paragraph(str(v), styles["Small"]) for v in row] for row in rows]
    t = Table(cells, repeatRows=1, hAlign="LEFT", colWidths=widths)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dde9f4")),
                           ("GRID", (0, 0), (-1, -1), 0.3, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def tests_section(styles, title: str):
    """Genera docs/PRUEBAS.md y la tabla del PDF desde docs/pruebas.csv."""
    tests = pd.read_csv(ROOT / "docs/pruebas.csv")
    lines = [f"# Pruebas automatizadas · {title}", "",
             f"{len(tests)} pruebas; se ejecutan con `uv run pytest -q` y el resultado queda en `reports/pruebas.txt`.",
             "Cada fila indica qué comprueba la prueba, por qué se hizo y qué criterio de la rúbrica respalda.", "",
             "| # | Prueba | Origen | Criterio | Qué comprueba | Por qué |", "|---|---|---|---|---|---|"]
    lines += [f"| {r.n} | `{r.archivo}::{r.prueba}` | {r.origen} | {r.criterio} | {r.comprueba} | {r.por_que} |"
              for r in tests.itertuples()]
    (ROOT / "docs/PRUEBAS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    rows = [["#", "Prueba", "Qué comprueba", "Por qué se hizo"]] + [
        [r.n, f"{r.prueba.replace('_', ' ')}<br/><i>{r.origen} · {r.criterio}</i>", r.comprueba, r.por_que]
        for r in tests.itertuples()]
    return tests, table(rows, styles, widths=[22, 138, 173, 182])


AI_MODELS = [
    ["Herramienta", "Modelo", "Uso en esta práctica", "Para qué sirve", "Límite y control"],
    ["Claude Code (Anthropic)", "<b>Claude Opus 5.5</b>", "<b>Usado.</b> Agente en VS Code: código, pruebas, cuaderno, "
     "documentación, ejecución y PDF", "Tareas largas de varios pasos sobre un repositorio", "Todo se verificó con pruebas y reportes"],
    ["Claude (Anthropic)", "Claude Sonnet 5", "No usado", "Programación cotidiana, equilibrio velocidad-calidad",
     "Menos profundidad en tareas largas"],
    ["Claude (Anthropic)", "Claude Haiku 4.5", "No usado", "Tareas rápidas y baratas: resúmenes, clasificación",
     "No indicado para diseño experimental"],
    ["Codex (OpenAI)", "Modelo configurado en Codex (versión a verificar)", "Apoyo complementario",
     "Proponer y revisar código, explicar errores, sugerir pruebas", "Se acepta solo si pasa las pruebas"],
    ["DeepSeek", "DeepSeek-V3 (chat)", "Apoyo complementario", "Explicar conceptos y revisar redacción",
     "Puede inventar referencias: se verificaron en la fuente"],
    ["DeepSeek", "DeepSeek-R1 (razonamiento)", "No consta su uso", "Razonamiento paso a paso y depuración lógica",
     "No sustituye la ejecución"],
]


RESPONSIBILITIES = [
    ["Responsabilidad", "Quién"],
    ["Valores del análisis (daño prioritario, tolerancias, compuertas, decisiones de uso)", "La autora"],
    ["Elección de datos y verificación de licencias y referencias", "La autora, con apoyo de las herramientas"],
    ["Borradores de código, pruebas y redacción", "Herramientas de IA"],
    ["Ejecución de pruebas y comprobación de cada cifra contra reports/", "La autora, con Claude Code"],
    ["Defensa oral y respuesta a preguntas técnicas", "La autora"],
]


def ai_table(styles):
    """Modelos de IA con uso real, función y límite; los valores del análisis los decide la autora."""
    return KeepTogether([table(AI_MODELS, styles, widths=[78, 88, 120, 120, 110]), Spacer(1, 6),
                         Paragraph("<b>Reparto de responsabilidades</b>", styles["BodyText"]),
                         table(RESPONSIBILITIES, styles, widths=[330, 186])])


def main() -> None:
    styles = getSampleStyleSheet()
    styles["BodyText"].fontSize, styles["BodyText"].leading, styles["BodyText"].alignment = 9.5, 13.5, TA_LEFT
    styles.add(styles["BodyText"].clone("Small", fontSize=8, leading=10))
    tests, tests_table = tests_section(styles, "Ejercicio 07")
    p = lambda text: Paragraph(text, styles["BodyText"])
    h = lambda text: Paragraph(text, styles["Heading2"])
    impact = yaml.safe_load((ROOT / "student_inputs/lab11_impact.yml").read_text(encoding="utf-8"))
    stake = pd.read_csv(ROOT / "student_inputs/stakeholders.csv")
    risks = pd.read_csv(ROOT / "reports/lab11/risk_register_scored.csv")
    cand = pd.read_csv(ROOT / "reports/lab12/candidatos.csv")
    inter = pd.read_csv(ROOT / "reports/lab12/interseccional.csv")
    by_group = pd.read_csv(ROOT / "reports/lab12/por_grupo.csv", index_col=0)
    by_age = pd.read_csv(ROOT / "reports/lab12/por_edad.csv", index_col=0)
    ci = json.loads((ROOT / "reports/lab12/bootstrap.json").read_text(encoding="utf-8"))
    d = json.loads((ROOT / "reports/lab12/decision.json").read_text(encoding="utf-8"))

    impact_rows = [["Campo", "Contenido"]] + [[k.replace("_", " "), v] for k, v in impact.items()]
    stake_rows = [["Interesado", "Beneficio", "Daño", "Poder", "Participación"]] + stake.values.tolist()
    risk_rows = [["ID", "Escenario", "Prob.", "Imp.", "Prioridad", "Control", "Responsable", "NIST AI RMF"]] + [
        [r.id, r.scenario, r.likelihood_1_4, r.impact_1_4, r.priority, r.control, r.owner, r.rmf_subcategory]
        for r in risks.itertuples()]
    legal = [["Tipo", "Fuente", "Aplicación en este sistema"],
             ["<b>Obligación legal</b>", "Ley 172-13 de protección de datos personales (RD, 2013)",
              "Con datos reales: finalidad declarada, datos mínimos; el esquema rechaza identificadores directos"],
             ["<b>Obligación legal</b>", "Constitución RD, arts. 39 (igualdad), 44 (intimidad) y 70 (hábeas data)",
              "El grupo protegido no decide; no se perfila; apelación y rectificación documentadas"],
             ["<b>Marco voluntario</b>", "NIST AI RMF 1.0 (NIST AI 100-1, 2023)",
              "Cada riesgo vinculado a una subcategoría de GOVERN, MAP, MEASURE o MANAGE"],
             ["<b>Marco voluntario</b>", "Model Cards (Mitchell et al., 2019); Datasheets (Gebru et al., 2021)",
              "Documentación de datos y modelo (se completa en el Ejercicio 08)"],
             ["<b>Recomendación ética</b>", "Criterio propio", "Preferir la alternativa menos intrusiva si rinde igual; "
              "no decidir con celdas de menos de 30 casos; supervisión humana y apelación"]]
    stage = cand[cand.etapa == "prueba"]
    valid = cand[cand.etapa == "validacion"].set_index("candidato")
    cand_rows = [["Candidato", "Recall valid.", "Recall test", "FPR test", "Accuracy", "Selección",
                  "Brecha recall", "Brecha FPR", "Brecha selección"]] + [
        [f"<b>{r.candidato}</b>" if r.candidato == d["candidato_elegido"] else r.candidato,
         f"{valid.loc[r.candidato, 'recall']:.3f}", f"{r.recall:.3f}", f"{r.fpr:.3f}", f"{r.accuracy:.3f}",
         f"{r.selection_rate:.3f}", f"{r.recall_gap:.3f}", f"{r.fpr_gap:.3f}", f"{r.selection_gap:.3f}"]
        for r in stage.itertuples()]
    group_rows = [["Grupo o edad", "n", "Recall", "FPR", "Precisión", "Selección"]] + [
        [str(r.Index), int(r.count), f"{r.recall:.3f}", f"{r.fpr:.3f}", f"{r.precision:.3f}", f"{r.selection_rate:.3f}"]
        for r in pd.concat([by_group, by_age]).itertuples()]
    inter_rows = [["Grupo | edad", "n", "Recall", "FPR", "n ≥ 30"]] + [
        [r[0], int(r.count), f"{r.recall:.3f}", f"{r.fpr:.3f}", "sí" if r.n_suficiente else "no"]
        for r in inter.itertuples(index=False)]
    rule = ci[d["candidato_elegido"]]
    story = [
        Paragraph("Ejercicio 07 · Evaluación de impacto y auditoría de equidad", styles["Title"]),
        p("Marlenis Judith Concepción Cuevas · INF-8239-C2 · Unidad IV · Docente: Edwin Ramón José Nolasco"),
        p(f'Repositorio: <link href="{REPO}" color="blue">{REPO}</link>'),
        p("Sistema: <i>Territorial Review DSS - Synthetic</i> (proyecto base del curso). Datos sintéticos: 640 casos, "
          "sin personas reales. El sistema ordena casos para revisión humana; no decide intervenciones."),
        h("1. Finalidad, interesados y proporcionalidad"),
        table(impact_rows, styles, widths=[110, 405]), Spacer(1, 6),
        table(stake_rows, styles, widths=[80, 110, 125, 40, 160]), Spacer(1, 6),
        p("<b>Proporcionalidad.</b> Necesidad: el volumen obliga a ordenar la revisión. Idoneidad: la regla transparente "
          "alcanza recall 0.75 en prueba. Menor intrusión: usa solo incidentes previos y exposición, sin edad, zona ni "
          "grupo. Equilibrio: envía más casos a revisión (FPR 0.37), aceptado porque el daño prioritario es el falso "
          "negativo; la carga se vigila (R06)."),
        h("2. Obligación legal, marco voluntario y recomendación ética"),
        table(legal, styles, widths=[95, 170, 250]), Spacer(1, 4),
        p("Análisis académico, no asesoría jurídica. Matriz completa y referencias en docs/MARCO_NORMATIVO.md."),
        h("3. Registro de riesgos y NIST AI RMF"),
        table(risk_rows, styles, widths=[24, 130, 28, 26, 42, 140, 60, 65]), Spacer(1, 4),
        p("Prioridad = probabilidad × impacto (1–4). Las subcategorías se contrastaron con el texto de NIST AI 100-1."),
        h("4. Auditoría global, por grupo e interseccional"),
        p("Partición temporal del proyecto base: 480 casos de entrenamiento (los últimos 120 como validación) y 160 de "
          "prueba posteriores. El grupo protegido se excluye del modelo y se usa solo para auditar. Tasa base en prueba: "
          "0.49 en G1 y 0.73 en G2; por eso la métrica principal es la igualdad de oportunidades (recall), no la paridad "
          "de selección."),
        table(cand_rows, styles, widths=[92, 50, 48, 44, 48, 48, 52, 52, 60]), Spacer(1, 6),
        Image(str(ROOT / "reports/lab12/candidatos.png"), width=500, height=173),
        KeepTogether([p(f"<b>Regla elegida por grupo y edad (prueba):</b>"), table(group_rows, styles, widths=[70, 40, 60, 60, 60, 60])]),
        Spacer(1, 6),
        KeepTogether([p("<b>Interseccional (grupo × edad):</b> 7 de 8 celdas tienen menos de 30 casos; sus valores no "
                        "se usan para decidir."), table(inter_rows, styles, widths=[90, 40, 60, 60, 50])]),
        Spacer(1, 4),
        p(f"<b>Incertidumbre (bootstrap, 1000 remuestreos):</b> brecha de recall de la regla entre "
          f"{rule['recall_gap'][0]:.3f} y {rule['recall_gap'][1]:.3f}; brecha de FPR entre {rule['fpr_gap'][0]:.3f} y "
          f"{rule['fpr_gap'][1]:.3f}. Para la regresión logística, la brecha de recall llega a "
          f"{ci['logistica_0.50']['recall_gap'][1]:.3f}."),
        h("5. Mitigación, trade-offs y decisión"),
        p("Mitigaciones evaluadas: (a) umbral global ajustado en validación (0.56), que reduce la brecha de FPR pero baja "
          "el recall por debajo de 0.70; (b) ThresholdOptimizer de Fairlearn con igualdad de probabilidades, que reduce "
          "la brecha de recall a 0.07 pero sube el FPR a 0.44 y <b>necesita el grupo protegido al decidir</b>, por lo que "
          "se descarta (art. 39 de la Constitución y riesgo R04); (c) sustituir el modelo por la regla transparente."),
        p(f"<b>Regla de elección fijada en validación:</b> {d['razon_eleccion']}"),
        p(f"<b>Decisión final: {d['decision'].upper()}.</b> La regla cumple las compuertas en prueba (recall 0.750, "
          "brechas 0.011 y 0.010), pero el extremo superior del intervalo supera la tolerancia de 0.16 y la mayoría de "
          "celdas interseccionales son pequeñas. Se usa la regla solo para ordenar revisiones humanas en un piloto "
          "limitado, con apelación y monitoreo mensual; <b>no se utiliza el modelo de regresión logística</b>. "
          "Registro completo en reports/lab11/DECISION_RECORD.md."),
        h("6. Pruebas automatizadas"),
        p(f"{len(tests)} pruebas, todas aprobadas (reports/pruebas.txt): 10 del proyecto base y 13 propias. Lista en "
          "docs/PRUEBAS.md."),
        tests_table, Spacer(1, 6),
        h("7. Referencias"),
        p("Ley No. 172-13 sobre protección de datos personales (2013). · Constitución de la República Dominicana (2015), "
          "arts. 39, 44 y 70. · NIST (2023). AI RMF 1.0, NIST AI 100-1. doi:10.6028/NIST.AI.100-1 · Bird et al. (2020). "
          "Fairlearn, MSR-TR-2020-32. · Hardt, Price y Srebro (2016). Equality of Opportunity in Supervised Learning, "
          "NeurIPS. · Mitchell et al. (2019). Model Cards for Model Reporting, FAT*. · Gebru et al. (2021). Datasheets "
          "for Datasets, CACM 64(12)."),
        KeepTogether([h("8. Uso de IA"),
                      p("Utilicé Claude Code (Claude Opus 5.5), Codex (OpenAI) y DeepSeek como apoyo para estructura, código, "
                        "pruebas y redacción. Los valores del análisis (daño prioritario, tolerancias, preferir la alternativa "
                        "menos intrusiva, no usar el grupo protegido al decidir) son decisiones propias. Verifiqué las "
                        "subcategorías del NIST AI RMF en el documento oficial y la Ley 172-13 y la Constitución en fuentes "
                        "oficiales. Se corrigieron dos scripts del proyecto base que no ejecutaban. Detalle en "
                        "docs/AI_USE_DECLARATION.md."), ai_table(styles)])]
    SimpleDocTemplate(str(ROOT / "reports/Ejercicio_07.pdf"), rightMargin=40, leftMargin=40, topMargin=34,
                      bottomMargin=34, title="Ejercicio 07 · INF-8239").build(story)
    print("PDF:", ROOT / "reports/Ejercicio_07.pdf")


if __name__ == "__main__":
    main()
