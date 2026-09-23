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
        "Ciencia%20de%20DatosII/Unidad%20III/Ejercicio%2006")
NAMES = {"media": "Imagen media", "pca_16": "PCA 16", "ae_16": "AE 16 (base)", "vae_2": "VAE 2 (base)",
         "vae_16": "VAE 16", "real_prueba": "Real (prueba)"}


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


def main() -> None:
    reports = ROOT / "reports"
    styles = getSampleStyleSheet()
    styles["BodyText"].fontSize, styles["BodyText"].leading, styles["BodyText"].alignment = 9.5, 13.5, TA_LEFT
    styles.add(styles["BodyText"].clone("Small", fontSize=8, leading=10))
    tests, tests_table = tests_section(styles, "Ejercicio 06")
    p = lambda text: Paragraph(text, styles["BodyText"])
    h = lambda text: Paragraph(text, styles["Heading2"])
    rec = pd.read_csv(reports / "reconstruccion.csv")
    gen = pd.read_csv(reports / "generacion.csv")
    m = json.loads((reports / "metricas.json").read_text(encoding="utf-8"))
    d = json.loads((reports / "decision.json").read_text(encoding="utf-8"))
    fmt = lambda v, f: "—" if pd.isna(v) else format(v, f)
    rows = [["Modelo", "MSE píxel (test)", "BCE imagen (test)", "Pérdida valid.", "Parámetros", "Épocas", "Segundos", "KB"]]
    for r in rec.itertuples():
        name = f"<b>{NAMES[r.modelo]}</b>" if r.modelo == d["modelo_elegido"] else NAMES[r.modelo]
        rows.append([name, f"{r.mse_pixel:.4f}", f"{r.bce_por_imagen:.1f}", fmt(r.perdida_valid, ".1f"),
                     f"{int(r.parametros):,}", fmt(r.epocas, ".0f"), f"{r.segundos:.1f}", fmt(r.tamano_kb, ".0f")])
    grows = [["Conjunto", "Confianza juez", "Clases", "Entropía", "Dispersión", "Dist. vecino train", "Posibles copias"]]
    for r in gen.itertuples():
        grows.append([NAMES.get(r.conjunto, r.conjunto), f"{r.confianza_media:.3f}", r.clases_cubiertas,
                      f"{r.entropia_clases:.3f}", f"{r.dispersion:.2f}", f"{r.dist_vecino_train_mediana:.2f}",
                      f"{100 * r.posibles_copias:.1f} %"])
    story = [
        Paragraph("Ejercicio 06 · VAE, evaluación y Model Card", styles["Title"]),
        p("Marlenis Judith Concepción Cuevas · INF-8239-C2 · Unidad III · Docente: Edwin Ramón José Nolasco"),
        p(f'Repositorio: <link href="{REPO}" color="blue">{REPO}</link>'),
        h("1. Datos, particiones y líneas base"),
        p("Fashion-MNIST (Xiao, Rasul y Vollgraf, 2017; licencia MIT), descargado con tf.keras; no se usa MovieLens. "
          "Validación: 6000 imágenes aleatorias del entrenamiento oficial (semilla 42, índices guardados); entrenamiento: 54 000; "
          "prueba: 10 000 oficiales, usadas solo para medir reconstrucción y como referencia de memoria. Líneas base: la imagen "
          "media (no aprende nada) y PCA con 16 componentes (compresión lineal del mismo tamaño que el AE). Se comparan con el AE "
          "y el VAE 2 del proyecto base y con un VAE de latente 16. Parada temprana sobre la pérdida de validación."),
        h("2. Tabla principal de resultados"),
        table(rows, styles, widths=[80, 62, 62, 56, 62, 40, 50, 40]), Spacer(1, 6),
        p(f"<b>Decisión fijada en validación:</b> {d['regla'][0].lower() + d['regla'][1:]}. {d['razon']} La pérdida total (reconstrucción + KL) "
          "es una cota de la verosimilitud y es comparable entre dimensiones latentes."),
        KeepTogether([h("3. Reconstrucción, muestreo e interpolación"),
                      Image(str(reports / "reconstruccion.png"), width=470, height=236)]),
        Image(str(reports / "muestras.png"), width=470, height=123),
        Image(str(reports / "interpolacion.png"), width=470, height=150),
        p("El VAE 16 conserva la forma y parte de la textura; el VAE 2 produce siluetas borrosas. La interpolación entre un "
          "Sneaker y un Ankle boot reales pasa en el espacio latente por calzado plausible, mientras que la mezcla de píxeles "
          "superpone las dos imágenes."),
        KeepTogether([Image(str(reports / "espacio_latente.png"), width=300, height=231),
                      p("En 2 dimensiones el calzado, los pantalones y los bolsos se separan; Pullover, Coat y Shirt se solapan, "
                        "lo que explica por qué el VAE 2 no genera Pullover.")]),
        KeepTogether([h("4. Fidelidad, diversidad y memoria"), table(grows, styles, widths=[72, 62, 40, 52, 55, 80, 70])]),
        Spacer(1, 6),
        p(f"1000 muestras de N(0, I) por modelo. <b>Fidelidad:</b> confianza de un clasificador juez entrenado solo con "
          f"entrenamiento (exactitud {m['generacion']['exactitud_juez_prueba']:.3f} en prueba). <b>Diversidad:</b> clases "
          "cubiertas, entropía del reparto de clases (1 = uniforme) y distancia media entre pares. <b>Memoria:</b> distancia al "
          "vecino más cercano de entrenamiento; una posible copia es una muestra más cercana que el 95 % de las imágenes reales "
          f"de prueba (umbral {m['generacion']['umbral_copia']:.2f}). El VAE 16 no memoriza (0.5 %). El 19 % del VAE 2 no son "
          "copias de imágenes concretas: son prototipos simples y borrosos, cercanos a muchas prendas lisas."),
        h("5. Costo, límites y conclusión"),
        p("El VAE 16 cuesta casi lo mismo que el VAE 2 (207 920 frente a 202 516 parámetros; 44 s frente a 41 s en CPU, Apple M1 "
          "Pro) y mejora reconstrucción, diversidad y memoria. Límites: las muestras siguen siendo menos nítidas que las reales "
          "(confianza 0.63 frente a 0.90); las medidas de fidelidad dependen del juez; una sola semilla; los modelos llegaron al "
          "máximo de épocas. Generar datos sintéticos no garantiza privacidad. Model Card completa en MODEL_CARD.md."),
        h("6. Pruebas automatizadas"),
        p(f"{len(tests)} pruebas, todas aprobadas (reports/pruebas.txt): 4 del proyecto base y 8 propias. Lista completa en "
          "docs/PRUEBAS.md."),
        tests_table, Spacer(1, 6),
        KeepTogether([h("7. Uso de IA"),
                      p("Utilicé Claude Code (Claude Opus 5.5), Codex (OpenAI) y DeepSeek como apoyo. Con Claude Code adapté el "
                        "proyecto base, añadí las líneas base, el VAE 16, la validación y las medidas de fidelidad, diversidad y "
                        "memoria, y escribí las pruebas, el cuaderno y la redacción. Verifiqué que los modelos recargados "
                        "reproducen las métricas, las figuras y las pruebas; se corrigió una prueba con tolerancia numérica "
                        "incorrecta. Detalle en AI_USE_DECLARATION.md.")])]
    SimpleDocTemplate(str(reports / "Ejercicio_06.pdf"), rightMargin=40, leftMargin=40, topMargin=34, bottomMargin=34,
                      title="Ejercicio 06 · INF-8239").build(story)
    print("PDF:", reports / "Ejercicio_06.pdf")


if __name__ == "__main__":
    main()
