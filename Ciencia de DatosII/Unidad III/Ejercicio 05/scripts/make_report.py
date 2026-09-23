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
        "Ciencia%20de%20DatosII/Unidad%20III/Ejercicio%2005")


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
    reports = ROOT / "reports"
    styles = getSampleStyleSheet()
    styles["BodyText"].fontSize, styles["BodyText"].leading, styles["BodyText"].alignment = 9.5, 13.5, TA_LEFT
    styles.add(styles["BodyText"].clone("Small", fontSize=8, leading=10))
    tests, tests_table = tests_section(styles, "Ejercicio 05")
    p = lambda text: Paragraph(text, styles["BodyText"])
    h = lambda text: Paragraph(text, styles["Heading2"])
    summary = json.loads((reports / "resumen.json").read_text(encoding="utf-8"))
    a, part = summary["auditoria"], summary["particion"]
    d = json.loads((reports / "decision.json").read_text(encoding="utf-8"))
    valid = pd.read_csv(reports / "validacion.csv").set_index("modelo")
    test = pd.read_csv(reports / "resultados_test.csv")
    cold = pd.read_csv(reports / "usuarios_frios_resultados.csv")
    grid = pd.read_csv(reports / "busqueda_factorizacion.csv")
    activity = pd.read_csv(reports / "errores_por_actividad.csv")
    examples = pd.read_csv(reports / "ejemplos_sin_aciertos.csv")

    rows = [["Modelo", "NDCG@10 valid.", "Pareto", "NDCG@10 test", "Precision@10", "Recall@10", "Hit@10",
             "Cobertura", "Novedad"]]
    for r in test.itertuples():
        name = f"<b>{r.modelo}</b>" if r.modelo == d["modelo_elegido"] else r.modelo
        v = valid.loc[r.modelo]
        rows.append([name, f"{v['ndcg@10']:.4f}", "sí" if v["pareto"] else "no", f"{r._5:.4f}", f"{r._3:.4f}",
                     f"{r._4:.4f}", f"{r._6:.3f}", f"{r.cobertura:.3f}", f"{r.novedad:.2f}"])
    grid_rows = [["Factores", "Épocas", "NDCG@10 valid.", "RMSE valid.", "Segundos"]] + [
        [int(g.factores), int(g.epocas), f"{g._3:.4f}", f"{g.rmse_valid:.4f}", f"{g.segundos:.1f}"] for g in grid.itertuples()]
    cold_rows = [["Escenario (61 usuarios fríos)", "NDCG@10", "Hit@10", "Cobertura"]] + [
        [c.modelo, f"{c._5:.3f}", f"{c._6:.3f}", f"{c.cobertura:.4f}"] for c in cold.itertuples()]
    act_rows = [["Actividad", "Usuarios", "Historial mediano", "NDCG@10", "Hit@10", "Sin aciertos"]] + [
        [x.actividad, x.usuarios, f"{x.historial_mediano:.0f}", f"{x.ndcg:.3f}", f"{x.hit:.3f}", x.sin_aciertos]
        for x in activity.itertuples()]
    ex_rows = [["Usuario", "Historial", "Géneros que le gustan", "Géneros recomendados", "Géneros relevantes en test"]] + [
        [e.userId, e.historial, e.generos_que_le_gustan, e.generos_recomendados, e.generos_relevantes_en_test]
        for e in examples.head(3).itertuples()]
    story = [
        Paragraph("Ejercicio 05 · Motor recomendador reproducible", styles["Title"]),
        p("Marlenis Judith Concepción Cuevas · INF-8239-C2 · Unidad III · Docente: Edwin Ramón José Nolasco"),
        p(f'Repositorio: <link href="{REPO}" color="blue">{REPO}</link>'),
        h("1. Datos, licencia y auditoría"),
        p(f"MovieLens ml-latest-small (GroupLens; Harper y Konstan, 2015, DOI 10.1145/2827872). Uso para investigación, no "
          "comercial y con cita; <b>no se redistribuye</b>: data/ está fuera de Git y el script descarga el ZIP y verifica su "
          f"SHA-256. {a['valoraciones']:,} valoraciones de {a['usuarios']} usuarios sobre {a['peliculas_valoradas']:,} películas "
          f"({a['desde']} a {a['hasta']}); densidad {100 * a['densidad']:.1f} %; sin nulos ni duplicados usuario-película. "
          f"Cola larga: el 10 % de películas más valoradas reúne el {a['porcentaje_valoraciones_en_top10pct_peliculas']:.0f} % "
          f"de las valoraciones y {a['peliculas_con_una_valoracion']:,} películas tienen una sola."),
        Image(str(reports / "auditoria.png"), width=480, height=136),
        h("2. Corte temporal y usuarios fríos"),
        p(f"Se reservan {part['usuarios_frios']} usuarios (10 %, semilla 42) que no entran al entrenamiento. Para los "
          f"{part['usuarios_calidos']} restantes, {part['regla']}: {part['train']:,} / {part['valid']:,} / {part['test']:,} "
          "valoraciones. Una prueba automática verifica que el pasado de cada usuario queda en entrenamiento y el futuro en prueba. "
          "Relevante = rating ≥ 4. En la prueba final se reentrena con entrenamiento + validación."),
        h("3. Popularidad, contenido y factorización"),
        p("Popularidad: media ponderada por número de valoraciones. Contenido: perfil TF-IDF de géneros ponderado por el rating "
          "del usuario. Factorización: SGD del proyecto base; los factores y las épocas se eligen por NDCG@10 en validación. "
          "Más épocas bajan el RMSE pero empeoran el ranking: predecir bien el rating no equivale a ordenar bien."),
        table(grid_rows, styles, widths=[60, 50, 80, 70, 60]), Spacer(1, 6),
        h("4. Tabla principal: ranking, cobertura, novedad e híbrido"),
        table(rows, styles, widths=[78, 58, 38, 58, 56, 52, 40, 52, 44]), Spacer(1, 4),
        p(f"RMSE de la factorización en prueba: {summary['rmse_test_factorizacion']:.3f}. El "
          f"{100 * summary['fraccion_relevantes_alcanzables']:.1f} % de los ítems relevantes de prueba está en el catálogo "
          "recomendable; el resto son películas nuevas que ningún modelo colaborativo puede recomendar."),
        KeepTogether([h("5. Híbrido y decisión Pareto"),
                      Image(str(reports / "pareto.png"), width=330, height=213),
                      p(f"<b>Regla fijada en validación:</b> {d['regla']}. {d['razon']} "
                        "En prueba la factorización queda ligeramente por encima en NDCG (0.062 frente a 0.059), pero el "
                        "híbrido recomienda un 35 % más del catálogo y con más novedad. Se mantiene la decisión de validación: "
                        "cambiarla después de ver la prueba sería ajustar el modelo a la prueba.")]),
        h("6. Usuarios fríos y errores"),
        table(cold_rows, styles, widths=[220, 60, 60, 60]), Spacer(1, 4),
        p("Sin historial, el fallback es la popularidad. Con 5 valoraciones iniciales, el contenido basado solo en géneros no la "
          "supera, así que el fallback se mantiene hasta que el usuario acumule historial. Estos valores no se comparan con los de "
          "usuarios cálidos, porque la verdad incluye toda la historia del usuario."),
        table(act_rows, styles, widths=[110, 50, 80, 55, 50, 60]), Spacer(1, 4),
        table(ex_rows, styles, widths=[45, 45, 135, 135, 135]), Spacer(1, 4),
        p("El error se concentra en los usuarios con menos historia: 124 de 139 del cuartil menos activo no reciben ningún acierto. "
          "Los ejemplos muestran el patrón: el modelo recomienda los géneros del pasado del usuario, pero en el periodo de prueba "
          "sus gustos cambian (aventura, ciencia ficción, musical), algo que ni el contenido ni la factorización anticipan."),
        h("7. Límites"),
        p("Evaluación offline con valoraciones explícitas: no mide clics ni satisfacción real. Solo se usan géneros como contenido. "
          "Una sola semilla. La popularidad reforzada por el sistema puede aumentar la concentración del catálogo. System Card en "
          "docs/SYSTEM_CARD.md y Dataset Card en docs/DATASET_CARD.md."),
        h("8. Pruebas automatizadas"),
        p(f"{len(tests)} pruebas, todas aprobadas (reports/pruebas.txt): 7 del proyecto base y 6 propias. Una de ellas detectó un "
          "error real que se corrigió. Lista completa en docs/PRUEBAS.md."),
        tests_table, Spacer(1, 6),
        KeepTogether([h("9. Uso de IA"),
                      p("Utilicé Claude Code (Claude Opus 5.5), Codex (OpenAI) y DeepSeek como apoyo. Con Claude Code diseñé la "
                        "partición temporal y los usuarios fríos, extendí el proyecto base con métricas de ranking, novedad, "
                        "Pareto e híbridos, y escribí las pruebas, el cuaderno y la redacción. Verifiqué la licencia y la cita "
                        "en el README de MovieLens, el SHA-256, las pruebas y que la corrección del error no alteró las métricas. "
                        "Detalle en docs/DECLARACION_IA.md."), ai_table(styles)])]
    SimpleDocTemplate(str(reports / "Ejercicio_05.pdf"), rightMargin=40, leftMargin=40, topMargin=34, bottomMargin=34,
                      title="Ejercicio 05 · INF-8239").build(story)
    print("PDF:", reports / "Ejercicio_05.pdf")


if __name__ == "__main__":
    main()
