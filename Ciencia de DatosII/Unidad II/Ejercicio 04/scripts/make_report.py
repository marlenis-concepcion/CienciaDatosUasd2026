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
        "Ciencia%20de%20DatosII/Unidad%20II/Ejercicio%2004")
NAMES = {"baseline": "Línea base", "dense": "Denso (base)", "cnn": "CNN pequeña (base)", "cnn_flatten": "CNN Flatten"}


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
    tests, tests_table = tests_section(styles, "Ejercicio 04")
    p = lambda text: Paragraph(text, styles["BodyText"])
    h = lambda text: Paragraph(text, styles["Heading2"])
    m = json.loads((reports / "cv_metrics.json").read_text(encoding="utf-8"))
    a = json.loads((reports / "auditoria.json").read_text(encoding="utf-8"))
    d = json.loads((reports / "decision.json").read_text(encoding="utf-8"))
    per_class = pd.read_csv(reports / "metricas_por_clase.csv")
    conf = pd.read_csv(reports / "confusiones_principales.csv")

    rows = [["Modelo", "F1 valid.", "F1 test", "Accuracy test", "Parámetros", "Épocas", "Entrenamiento s",
             "Inferencia ms/img", "Tamaño KB"]]
    for key in ["baseline", "dense", "cnn", "cnn_flatten"]:
        v = m[key]
        rows.append([f"<b>{NAMES[key]}</b>" if key == d["modelo_elegido"] else NAMES[key], f"{v['f1_macro_valid']:.3f}",
                     f"{v['f1_macro']:.3f}", f"{v['accuracy']:.3f}", f"{v['parametros']:,}", v.get("epocas", "—"),
                     f"{v['segundos_entrenamiento']:.1f}" if "segundos_entrenamiento" in v else "—",
                     f"{v['inferencia_ms_por_imagen']:.3f}" if "inferencia_ms_por_imagen" in v else "—",
                     f"{v['tamano_kb']:.0f}" if "tamano_kb" in v else "—"])
    classes = [["Clase", "Precisión", "Recall", "F1", "Errores"]] + [
        [r.clase, f"{r.precision:.3f}", f"{r.recall:.3f}", f"{r.f1:.3f}", r.errores] for r in per_class.itertuples()]
    confusions = [["Real", "Predicha", "Errores"]] + [[r.real, r.predicha, r.errores] for r in conf.head(5).itertuples()]
    story = [
        Paragraph("Ejercicio 04 · Clasificador visual con CNN y Model Card", styles["Title"]),
        p("Marlenis Judith Concepción Cuevas · INF-8239-C2 · Unidad II · Docente: Edwin Ramón José Nolasco"),
        p(f'Repositorio: <link href="{REPO}" color="blue">{REPO}</link>'),
        h("1. Auditoría y partición reproducible"),
        p(f"Fashion-MNIST (Xiao, Rasul y Vollgraf, 2017; licencia MIT), cargado con tf.keras. {a['forma_entrenamiento'][0]:,} "
          f"imágenes de entrenamiento y {a['forma_prueba'][0]:,} de prueba de 28×28, balanceadas (6000 y 1000 por clase). "
          f"La auditoría por hash no encontró duplicados en entrenamiento ({a['duplicados_en_entrenamiento']}), ni en prueba "
          f"({a['duplicados_en_prueba']}), ni imágenes de entrenamiento repetidas en prueba ({a['entrenamiento_repetido_en_prueba']}). "
          "La validación son 6000 imágenes estratificadas del entrenamiento oficial (semilla 42, índices guardados); la prueba "
          "oficial se usó una sola vez, después de fijar la decisión."),
        Image(str(reports / "muestras.png"), width=480, height=112),
        h("2. Línea base y CNN"),
        p("Se comparan la clase más frecuente, el modelo denso y la CNN pequeña del proyecto base, y una CNN propia que "
          "sustituye el promedio global por Flatten + Dense(128). Todos usan Adam, lotes de 128 y parada temprana sobre la "
          "pérdida de validación (paciencia 2), con un máximo de 30 épocas. Con las 8 épocas del proyecto base, la CNN pequeña "
          "obtuvo F1 0.785 en prueba, por debajo del denso; las curvas muestran que no había convergido."),
        KeepTogether([Image(str(reports / "curvas.png"), width=480, height=173)]),
        h("3. Costo, tamaño y decisión técnica"),
        table(rows, styles, widths=[78, 44, 40, 50, 56, 36, 60, 60, 48]), Spacer(1, 6),
        p(f"<b>Regla fijada antes de la prueba:</b> {d['regla'][0].lower() + d['regla'][1:]}. {d['razon']} La CNN Flatten gana +0.04 de F1 macro "
          "frente al denso, a cambio de 8 veces más parámetros, 4 veces más inferencia y 5 MB en disco. En CPU (Apple M1 Pro, "
          "TensorFlow 2.21) la inferencia sigue por debajo de 0.1 ms por imagen, por lo que el costo es aceptable."),
        KeepTogether([h("4. Métricas, curvas y errores por clase"),
                      Table([[table(classes, styles), table(confusions, styles)]], colWidths=[290, 220],
                            style=[("VALIGN", (0, 0), (-1, -1), "TOP")])]),
        Spacer(1, 6),
        KeepTogether([Image(str(reports / "confusion_cnn.png"), width=330, height=286)]),
        KeepTogether([Image(str(reports / "cnn_errors.png"), width=430, height=242)]),
        p("Shirt es la clase más débil (recall 0.728): se confunde con T-shirt/top, Coat y Pullover, prendas con la misma "
          "silueta a 28×28 píxeles. Los errores de calzado (Ankle boot → Sneaker) son el otro grupo relevante. Trouser, Bag, "
          "Sandal y Sneaker superan 0.95 de F1."),
        h("5. Model Card y reproducibilidad"),
        p("La Model Card (MODEL_CARD.md) documenta uso previsto, usos fuera de alcance, datos, métricas por clase, costo, "
          "límites y monitoreo. "
          "Los modelos "
          "guardados reproducen las métricas al recargarlos en el cuaderno."),
        h("6. Pruebas automatizadas"),
        p(f"{len(tests)} pruebas, todas aprobadas (reports/pruebas.txt): 3 del proyecto base y 6 propias sobre partición, "
          "fuga, contrato de los modelos, decisión y conteo de errores. Lista completa en docs/PRUEBAS.md."),
        tests_table, Spacer(1, 6),
        h("7. Uso de IA"),
        p("Utilicé Claude Code (Claude Opus 5.5), Codex (OpenAI) y DeepSeek como apoyo. Con Claude Code adapté el proyecto base, propuse la CNN Flatten y escribí las "
          "pruebas, el cuaderno y la redacción. Verifiqué la corrida de 8 épocas, la reproducción de métricas desde los modelos "
          "guardados, la partición y las pruebas; se corrigió la regla de decisión y la partición de validación. Detalle en "
          "docs/DECLARACION_IA.md."),
        ai_table(styles),
    ]
    SimpleDocTemplate(str(reports / "Ejercicio_04.pdf"), rightMargin=40, leftMargin=40, topMargin=34, bottomMargin=34,
                      title="Ejercicio 04 · INF-8239").build(story)
    print("PDF:", reports / "Ejercicio_04.pdf")


if __name__ == "__main__":
    main()
