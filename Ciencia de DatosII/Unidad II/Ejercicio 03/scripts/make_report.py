from __future__ import annotations

import json

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from inf8239_u02.config import ROOT

REPO = ("https://github.com/marlenis-concepcion/CienciaDatosUasd2026/tree/main/"
        "Ciencia%20de%20DatosII/Unidad%20II/Ejercicio%2003")


def table(rows, styles, widths=None):
    cells = [[Paragraph(str(v), styles["Small"]) for v in row] for row in rows]
    t = Table(cells, repeatRows=1, hAlign="LEFT", colWidths=widths)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dde9f4")),
                           ("GRID", (0, 0), (-1, -1), 0.3, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def params(raw: str) -> str:
    values = json.loads(raw)
    grams = "unigramas y bigramas" if values["tfidf__ngram_range"] == "(1, 2)" else "unigramas"
    hyper = {k.split("__")[1]: v for k, v in values.items() if k.startswith("model__")}
    return f"{grams}, min_df={values['tfidf__min_df']}, " + ", ".join(f"{k}={v}" for k, v in hyper.items())


def main() -> None:
    reports = ROOT / "reports"
    styles = getSampleStyleSheet()
    styles["BodyText"].fontSize, styles["BodyText"].leading, styles["BodyText"].alignment = 9.5, 13.5, TA_LEFT
    styles.add(styles["BodyText"].clone("Small", fontSize=8, leading=10))
    audit = json.loads((reports / "auditoria.json").read_text(encoding="utf-8"))
    metrics = pd.read_csv(reports / "text_metrics.csv")
    cv = pd.read_csv(reports / "busqueda_cv.csv").set_index("modelo")
    errors = pd.read_csv(reports / "error_analysis.csv")
    decision = json.loads((reports / "decision.json").read_text(encoding="utf-8"))
    d = audit["duplicados"]
    p = lambda text: Paragraph(text, styles["BodyText"])
    h = lambda text: Paragraph(text, styles["Heading2"])

    story = [
        Paragraph("Ejercicio 03 · Corpus público y clasificador de texto reproducible", styles["Title"]),
        p("Marlenis Judith Concepción Cuevas · INF-8239-C2 · Unidad II · Docente: Edwin Ramón José Nolasco"),
        p(f'Repositorio: <link href="{REPO}" color="blue">{REPO}</link>'),
        Spacer(1, 8),
        h("1. Corpus, licencia y pregunta"),
        p("<b>Corpus:</b> SMS Spam Collection v.1 (UCI 228), Almeida y Gómez Hidalgo, 2011. Licencia CC BY 4.0. "
          "DOI 10.24432/C5CC84. Descarga automática con verificación SHA-256 del ZIP original. "
          "Se comparó con Sentiment Labelled Sentences (UCI 331, CC BY 4.0, 3000 frases balanceadas); se eligió SMS Spam "
          "porque tiene desbalance real y duplicados, lo que permite evaluar métricas por clase y prevención de fuga."),
        p("<b>Pregunta:</b> ¿puede un clasificador TF-IDF separar spam de mensajes legítimos con un F1 macro claramente "
          "superior a una línea base, sin que los mensajes repetidos inflen el resultado?"),
        h("2. Auditoría y prevención de fuga"),
        p(f"{audit['filas']} mensajes, sin nulos; {audit['distribucion']['ham']} ham (86.6 %) y "
          f"{audit['distribucion']['spam']} spam (13.4 %). Se encontraron {d['duplicados_exactos']} duplicados exactos y "
          f"{d['duplicados_normalizados']} al normalizar minúsculas, dígitos y espacios, sin etiquetas contradictorias. "
          f"Se eliminaron <b>antes</b> de partir: quedan {d['filas_finales']} mensajes. La partición es estratificada 70/15/15 "
          "con semilla 42, y una prueba automática comprueba que ningún texto normalizado se repite entre particiones. "
          "El TF-IDF se ajusta dentro del pipeline, solo con entrenamiento."),
        Image(str(reports / "auditoria.png"), width=460, height=175),
        h("3. Línea base y dos pipelines comparables"),
        p("Línea base: clase más frecuente. Pipelines: TF-IDF + Complement Naive Bayes y TF-IDF + regresión logística "
          "(class_weight='balanced'). Ambos usan la misma rejilla de TF-IDF (unigramas o bigramas, min_df 1 o 2) y la misma "
          "validación cruzada estratificada de 5 pliegues sobre entrenamiento. "
          f"Mejor configuración: Naive Bayes ({params(cv.loc['naive_bayes', 'mejores_parametros'])}) y regresión "
          f"logística ({params(cv.loc['logistic', 'mejores_parametros'])}). "
          f"<b>Decisión:</b> {decision['criterio']}, registrada antes de evaluar en prueba. Resultado: {decision['modelo_elegido']}."),
    ]
    rows = [["Modelo", "F1 macro CV", "F1 macro valid.", "F1 macro test", "Accuracy test", "Precisión spam",
             "Recall spam", "ms/texto", "Tamaño KB"]]
    for _, r in metrics.iterrows():
        cvs = f"{cv.loc[r.modelo, 'f1_macro_cv']:.3f}" if r.modelo in cv.index else "—"
        rows.append([r.modelo, cvs, f"{r.f1_macro_valid:.4f}", f"{r.f1_macro_test:.3f}", f"{r.accuracy_test:.3f}",
                     f"{r.precision_spam_test:.3f}", f"{r.recall_spam_test:.3f}",
                     f"{r.inferencia_ms_por_texto:.3f}", f"{r.tamano_kb:.0f}"])
    story += [Spacer(1, 6), table(rows, styles), Spacer(1, 6),
              p("Validación: 771 mensajes (94 spam). Prueba: 771 mensajes (93 spam)."),
              KeepTogether([h("4. Evaluación"), Image(str(reports / "confusion_text.png"), width=470, height=188)]),
              p("Naive Bayes comete 4 falsos positivos y 4 falsos negativos en prueba (precisión y recall de spam 0.957). "
                "La diferencia con la regresión logística es pequeña: esta ganó en validación cruzada (0.964 frente a 0.961), "
                "perdió en validación por 0.0005 y ordena ligeramente mejor los mensajes según la curva precisión-recall "
                "(AP 0.99 frente a 0.98). No hay evidencia suficiente para afirmar que un pipeline sea superior."),
              h("5. Análisis de 23 errores")]
    summary = errors.groupby("categoria").agg(total=("id", "size"),
                                              ham_como_spam=("real", lambda s: int((s == "ham").sum())),
                                              spam_como_ham=("real", lambda s: int((s == "spam").sum())))
    summary = summary.sort_values("total", ascending=False)
    rows = [["Categoría", "Errores", "Ham → spam", "Spam → ham"]] + [[k, v.total, v.ham_como_spam, v.spam_como_ham]
                                                                    for k, v in summary.iterrows()]
    story += [p("Se analizaron los 8 errores del modelo elegido en prueba y los 15 en validación. Cada mensaje se leyó y se "
                "clasificó; el detalle con explicación está en reports/error_analysis.csv."),
              table(rows, styles, widths=[230, 55, 70, 70]), Spacer(1, 6)]
    examples = [3890, 1430, 1269, 3742]
    rows = [["id", "Real → pred.", "Texto", "Explicación"]]
    for _, r in errors[errors["id"].isin(examples)].iterrows():
        rows.append([r.id, f"{r.real} → {r.predicho}", r.text[:110], r.explicacion])
    story += [table(rows, styles, widths=[32, 62, 180, 250]), Spacer(1, 6),
              p("<b>Lectura:</b> 7 errores son mensajes etiquetados como spam que en realidad son comentarios del foro de origen "
                "(ruido de etiqueta). Otros 7 son mensajes legítimos con vocabulario comercial (free, offer, phone). Los números de "
                "tarificación especial no se aprovechan porque cada número es un token distinto; un rasgo que los agrupe sería una "
                "mejora concreta."),
              h("6. Conclusión y límites"),
              p("TF-IDF con un clasificador lineal resuelve bien este corpus (F1 macro 0.976 frente a 0.468 de la línea base) y "
                "el resultado no depende de duplicados, porque se eliminaron antes de partir. El techo lo marcan la calidad de "
                "las etiquetas y la antigüedad del corpus: el modelo no debe usarse en mensajería actual ni en español sin "
                "reentrenarlo y sin revisión humana."),
              KeepTogether([h("7. Uso de IA"), p("Utilicé Claude Code (Claude Opus 5.5) para adaptar el proyecto base, escribir pruebas, el cuaderno y la redacción. "
                "Verifiqué licencias y DOI en UCI, la composición del corpus en su readme, el SHA-256 y la reproducibilidad de las "
                "métricas; se corrigió la descripción de las fuentes del corpus y una prueba mal construida. Detalle, prompts y "
                "correcciones en docs/DECLARACION_IA.md.")])]
    SimpleDocTemplate(str(reports / "Ejercicio_03.pdf"), rightMargin=40, leftMargin=40, topMargin=34,
                      bottomMargin=34, title="Ejercicio 03 · INF-8239").build(story)
    print("PDF:", reports / "Ejercicio_03.pdf")


if __name__ == "__main__":
    main()
