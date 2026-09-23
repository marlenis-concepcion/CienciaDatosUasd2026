from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
REPO = ("https://github.com/marlenis-concepcion/CienciaDatosUasd2026/tree/main/"
        "Ciencia%20de%20DatosII/Unidad%20IV/Ejercicio%2008")


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
    ["Codex (OpenAI)", "Modelo de OpenAI orientado a código (familia GPT-5-Codex)", "Apoyo complementario",
     "Proponer y revisar código, explicar errores, sugerir pruebas", "Se acepta solo si pasa las pruebas"],
    ["DeepSeek", "DeepSeek-V3 (chat)", "Apoyo complementario", "Explicar conceptos y revisar redacción",
     "Puede inventar referencias: se verificaron en la fuente"],
    ["DeepSeek", "DeepSeek-R1 (razonamiento)", "No usado; recomendado para revisar la lógica de métricas", "Razonamiento paso a paso y depuración lógica",
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
    tests, tests_table = tests_section(styles, "Ejercicio 08")
    p = lambda text: Paragraph(text, styles["BodyText"])
    h = lambda text: Paragraph(text, styles["Heading2"])
    lab = ROOT / "reports/lab13"
    inv = pd.read_csv(ROOT / "docs/data_inventory.csv")
    mr = json.loads((lab / "minimizacion_retencion.json").read_text(encoding="utf-8"))
    manifest = json.loads((lab / "manifest.json").read_text(encoding="utf-8"))
    raci = pd.read_csv(ROOT / "student_inputs/raci.csv")
    perf = pd.read_csv(lab / "monitoreo_desempeno.csv")
    sim = json.loads((lab / "simulacro.json").read_text(encoding="utf-8"))
    ret = mr["simulacion_retencion"]
    inv_rows = [["Columna", "Sensibilidad", "Operativa", "Auditoría", "Finalidad", "Retención"]] + [
        [r.column, r.sensitivity, r.operational_view, r.audit_view, r.purpose, r.retention] for r in inv.itertuples()]
    man_rows = [["Artefacto", "Ruta", "SHA-256 (inicio)"]] + [[k, v["path"], v["sha256"][:16] + "…"] for k, v in manifest.items()]
    raci_rows = [["Actividad", "R", "A", "C", "I"]] + raci.values.tolist()
    perf_rows = [["Corte", "n", "Recall", "Brecha recall", "Brecha FPR", "Alertas"]] + [
        [r.corte, r.n, f"{r.recall:.3f}", f"{r.recall_gap:.3f}", f"{r.fpr_gap:.3f}", r.alertas if isinstance(r.alertas, str) else "—"]
        for r in perf.itertuples()]
    legal = [["Tipo", "Fuente", "Aplicación en gobernanza"],
             ["<b>Obligación legal</b>", "Ley 172-13 (RD); Constitución, arts. 44 y 70",
              "Con datos reales: tratar solo los datos necesarios para la finalidad declarada y atender acceso, "
              "rectificación y supresión (hábeas data)"],
             ["<b>Marco voluntario</b>", "NIST AI RMF 1.0: GOVERN 2.1, MANAGE 2.4, MANAGE 4.1, MANAGE 4.3",
              "Roles documentados (RACI), mecanismo para desactivar el sistema, monitoreo posterior e incidentes comunicados"],
             ["<b>Marco voluntario</b>", "Datasheets (Gebru et al., 2021); Model Cards (Mitchell et al., 2019)",
              "Datasheet y Model Card atadas por hash a los datos y a la decisión"],
             ["<b>Recomendación ética</b>", "Decisión propia",
              "Plazos concretos de retención (12/24/36 meses), umbrales de monitoreo y contención en 24 horas; no son "
              "plazos fijados por la ley"]]
    story = [
        Paragraph("Ejercicio 08 · Expediente de gobernanza y simulacro", styles["Title"]),
        p("Marlenis Judith Concepción Cuevas · INF-8239-C2 · Unidad IV · Docente: Edwin Ramón José Nolasco"),
        p(f'Repositorio: <link href="{REPO}" color="blue">{REPO}</link>'),
        p("Sistema gobernado: la regla transparente elegida en el Ejercicio 07 (<i>previous_incidents ≥ 4 o exposure ≥ 0.6</i>) "
          "para ordenar revisiones humanas de casos territoriales sintéticos."),
        h("1. Inventario, minimización y retención"),
        table(inv_rows, styles, widths=[78, 62, 44, 44, 130, 157]), Spacer(1, 4),
        p(f"<b>Minimización:</b> la vista operativa pasa de {len(mr['columnas_originales'])} a {len(mr['vista_operativa'])} "
          f"columnas ({', '.join(mr['vista_operativa'])}); se retiran {', '.join(mr['columnas_retiradas_de_la_operacion'])}, "
          "que solo existen en la vista de auditoría con acceso restringido. <b>Retención</b> (simulación de revisión al "
          f"{ret['fecha_revision']}): vista operativa a {ret['operativa']['meses']} meses conserva {ret['operativa']['conservados']} "
          f"y elimina {ret['operativa']['eliminados']} casos; vista de auditoría a {ret['auditoria']['meses']} meses conserva "
          f"{ret['auditoria']['conservados']} y elimina {ret['auditoria']['eliminados']}."),
        h("2. Obligación legal, marco voluntario y recomendación ética"),
        table(legal, styles, widths=[95, 170, 250]), Spacer(1, 4),
        h("3. Datasheet y Model Card trazables"),
        p("docs/DATASHEET.md sigue la estructura de Gebru et al. (motivación, composición, recolección, preprocesamiento, usos, "
          "distribución y mantenimiento). docs/MODEL_CARD.md completa las secciones del proyecto base (uso previsto, fuera de "
          "alcance, datos, evaluación global y por grupo con intervalos, Green AI, límites y responsable). Ambas incluyen el "
          "SHA-256 del dataset; una prueba falla si no coincide con el archivo real. El manifiesto registra el hash de cada "
          "artefacto:"),
        table(man_rows, styles, widths=[90, 250, 120]), Spacer(1, 4),
        h("4. RACI y traspaso entre roles"),
        table(raci_rows, styles, widths=[140, 80, 95, 100, 100]), Spacer(1, 4),
        p("Cada actividad tiene un solo responsable A (prueba automática). docs/TRASPASO.md define, para cada traspaso "
          "(Data Engineer → Data Scientist → Product Owner → ML Engineer → Operadores), entregables, criterio de aceptación y "
          "quién firma."),
        h("5. Monitoreo, runbook y simulacro"),
        p("Dos controles: (a) <b>entradas, semanal</b>, sin etiquetas, con el desplazamiento de la media de cada variable de "
          "decisión en errores estándar (umbral ±4) y rangos válidos; (b) <b>desempeño, en ventana de los últimos 100 casos "
          "con resultado</b>, con recall mínimo 0.68 y brecha máxima 0.16. En operación normal ninguna semana genera alertas."),
        table(perf_rows, styles, widths=[70, 35, 50, 70, 60, 230]), Spacer(1, 4),
        Image(str(lab / "monitoreo.png"), width=480, height=181),
        p(f"<b>Simulacro:</b> desde el 1 de diciembre la ingesta registra la exposición multiplicada por 0.1. El control "
          f"semanal lo detecta en la semana del {sim['semana_deteccion']} (z = {sim['z_deteccion']:.1f}) y el runbook pasa a "
          f"<b>{sim['estado']}</b>: orden de llegada con revisión manual, evidencia preservada, comunicación y nueva "
          f"puntuación tras corregir la ingesta. Sin detección, el recall de diciembre caería de {sim['recall_correcto']:.3f} a "
          f"{sim['recall_con_falla']:.3f} y quedarían {sim['casos_alto_riesgo_perdidos_si_nadie_detecta']} casos de alto riesgo "
          f"más sin priorizar; con detección en la primera semana, {sim['casos_alto_riesgo_perdidos_en_primera_semana']}. "
          "Postmortem con causa raíz y acciones con responsable y fecha en reports/lab13/INCIDENT_POSTMORTEM.md; runbook en "
          "docs/RUNBOOK.md."),
        h("6. Decisión final"),
        p("<b>LIMITAR</b> (se mantiene la decisión del Ejercicio 07). La regla puede pasar a un piloto porque el expediente está "
          "completo y el simulacro mostró que una falla se detecta, se contiene y se revierte con responsables definidos. No se "
          "despliega de forma general hasta que cada celda interseccional tenga al menos 30 casos; se retira según las "
          "condiciones de la evaluación de impacto."),
        h("7. Pruebas automatizadas"),
        p(f"{len(tests)} pruebas, todas aprobadas (reports/pruebas.txt): 10 del proyecto base, 13 del Ejercicio 07 y 11 nuevas "
          "de gobernanza. Lista en docs/PRUEBAS.md."),
        tests_table, Spacer(1, 6),
        KeepTogether([h("8. Uso de IA"),
                      p("Utilicé Claude Code (Claude Opus 5.5), Codex (OpenAI) y DeepSeek como apoyo para estructura, código, "
                        "pruebas y redacción. Los plazos de retención, umbrales, RACI y la decisión de contener son decisiones "
                        "propias. Verifiqué los hashes con pruebas automáticas y que el monitor no alerta en semanas normales. "
                        "Corregí un simulacro que no afectaba predicciones y un monitor mensual con falsas alarmas. Detalle en "
                        "docs/AI_USE_DECLARATION.md."), ai_table(styles)])]
    SimpleDocTemplate(str(ROOT / "reports/Ejercicio_08.pdf"), rightMargin=40, leftMargin=40, topMargin=34,
                      bottomMargin=34, title="Ejercicio 08 · INF-8239").build(story)
    print("PDF:", ROOT / "reports/Ejercicio_08.pdf")


if __name__ == "__main__":
    main()
