"""Informe técnico del trabajo final (PDF) a partir de reports/ y docs/."""
from __future__ import annotations

import json

import joblib
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from tutoria_dss.config import ROOT, load_config
from tutoria_dss.data import load, split
from tutoria_dss.dss import prioritize
from tutoria_dss.fairness import audit_groups
from tutoria_dss.models import contributions, predict_risk

REPO = ("https://github.com/marlenis-concepcion/CienciaDatosUasd2026/tree/main/"
        "Ciencia%20de%20DatosII/Unidad%20IV/Trabajo%20final")


def table(rows, styles, widths=None):
    cells = [[Paragraph(str(v), styles["Small"]) for v in row] for row in rows]
    t = Table(cells, repeatRows=1, hAlign="LEFT", colWidths=widths)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dde9f4")),
                           ("GRID", (0, 0), (-1, -1), 0.3, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


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
    p = lambda text: Paragraph(text, styles["BodyText"])
    h = lambda text: Paragraph(text, styles["Heading2"])
    r = ROOT / "reports"
    cfg = load_config()
    audit = json.loads((r / "auditoria.json").read_text(encoding="utf-8"))
    valid, test = pd.read_csv(r / "validacion.csv"), pd.read_csv(r / "prueba.csv")
    decision3 = json.loads((r / "decision.json").read_text(encoding="utf-8"))
    final = json.loads((r / "decision_final.json").read_text(encoding="utf-8"))
    mitig = pd.read_csv(r / "mitigacion_validacion.csv")
    fair = pd.read_csv(r / "equidad.csv")
    errors = pd.read_csv(r / "errores_perfil.csv", index_col=0)
    tests = pd.read_csv(ROOT / "docs/pruebas.csv")

    model = joblib.load(ROOT / "models/logistica.joblib")
    cohort = split(load(), cfg["random_state"])["test"]
    example = prioritize(cohort, predict_risk(model, cohort), cfg["capacity_share"], contributions(model, cohort),
                         audit_groups(cohort)["edad"]).head(6)

    comp = [["Alternativa", "Recall cap. valid.", "Recall cap. prueba", "Precisión cap. prueba", "AUC prueba", "AP prueba"]]
    vt = valid.set_index("alternativa")
    for row in test.itertuples():
        comp.append([f"<b>{row.alternativa}</b>" if row.alternativa == decision3["alternativa_elegida"] else row.alternativa,
                     f"{vt.loc[row.alternativa, 'recall_capacidad']:.3f}", f"{row.recall_capacidad:.3f}",
                     f"{row.precision_capacidad:.2f}", f"{row.auc:.3f}", f"{row.average_precision:.3f}"])
    mit = [["Alternativa", "Recall cap. valid.", "Brecha género", "Brecha edad"]] + [
        [f"<b>{m.alternativa}</b>" if m.alternativa == final["alternativa_elegida"] else m.alternativa,
         f"{m.recall_capacidad:.3f}", f"{m.brecha_genero:.3f}", f"{m.brecha_edad:.3f}"] for m in mitig.itertuples()]
    pt = final["prueba_todas"]
    mit_test = [["Alternativa (prueba)", "Recall cap.", "Precisión cap.", "Brecha género", "Brecha edad"]] + [
        [k, f"{v['recall_capacidad']:.3f}", f"{v['precision_capacidad']:.2f}", f"{v['brechas']['genero']:.3f}",
         f"{v['brechas']['edad']:.3f}"] for k, v in pt.items()]
    groups = fair[(fair.alternativa == final["alternativa_elegida"]) & (fair.dimension != "genero×edad")]
    grp = [["Dimensión", "Grupo", "Abandonos", "Tasa", "Recall cap.", "n ≥ 30"]] + [
        [g.dimension, g.grupo, g.abandonos, f"{g.tasa_abandono:.2f}", f"{g.recall_capacidad:.3f}",
         "sí" if g.n_suficiente else "no"] for g in groups.itertuples()]
    ex = [["Prioridad", "Estudiante", "Riesgo", "Apoyo sugerido", "Por qué"]] + [
        [e.prioridad, e.student_id, f"{e.riesgo:.3f}", e.apoyo_sugerido, e.por_que] for e in example.itertuples()]
    err = [["Variable (media)", "Abandonos alcanzados", "Abandonos no alcanzados"]] + [
        [i, f"{v['alcanzado']:.2f}", f"{v['no alcanzado']:.2f}"] for i, v in errors.iterrows()]
    trows = [["#", "Prueba", "Área", "Qué comprueba", "Por qué"]] + [
        [t.n, t.prueba.replace("_", " "), t.area, t.comprueba, t.por_que] for t in tests.itertuples()]
    g = final["green_ai"]

    story = [
        Paragraph("Trabajo final · DSS de alerta temprana para tutoría universitaria", styles["Title"]),
        p("Marlenis Judith Concepción Cuevas · INF-8239-C2 Ciencia de Datos II · Docente: Edwin Ramón José Nolasco · "
          "Modalidad B (DSS) · Individual"),
        p(f'Repositorio (versión etiquetada <b>trabajo-final-v1.0</b>): <link href="{REPO}" color="blue">{REPO}</link>'),
        h("1. Problema y decisor"),
        p("Al terminar el primer semestre, la coordinación de tutorías tiene cupos para el 15 % de la cohorte y debe decidir a "
          "quién contactar primero y con qué apoyo. El DSS propone una lista priorizada, un tipo de apoyo por reglas explícitas "
          "y una explicación por estudiante; <b>la coordinación decide</b> y registra su decisión (aceptar, modificar o "
          "rechazar, con motivo y responsable). No se usa para sancionar, excluir ni condicionar becas."),
        h("2. Datos y partición"),
        p(f"UCI 697, <i>Predict Students' Dropout and Academic Success</i> (Realinho et al., 2021; CC BY 4.0; DOI "
          f"10.24432/C5MC89). {audit['filas']} estudiantes de Portugal, sin nulos ni duplicados; abandono "
          f"{100 * audit['tasa_abandono']:.1f} %. Se descarga con verificación SHA-256 y no se redistribuye. Solo se usan las "
          f"{audit['variables_modelo']} variables conocidas al final del primer semestre: las sensibles (género, edad, "
          "nacionalidad, estado civil, internacional, beca) y las del segundo semestre quedan fuera del modelo. Partición "
          "estratificada 70/15/15, semilla 42. Tasa de abandono: 45 % en hombres y 25 % en mujeres; 39 % sin beca y 12 % con beca."),
        h("3. Baseline y modelo candidato"),
        p(f"Baseline: regla sin aprendizaje (unidades no aprobadas del primer semestre, matrícula atrasada y deuda). Candidato: "
          f"regresión logística en pipeline (one-hot y estandarización ajustados solo en entrenamiento), C = {decision3['C']:g} "
          "elegido por validación cruzada de 5 pliegues. Métrica principal: <b>recall a capacidad</b>, la proporción de abandonos "
          "reales que reciben tutoría con los cupos disponibles."),
        table(comp, styles, widths=[90, 70, 70, 80, 60, 60]), Spacer(1, 4),
        p(f"Regla fijada en validación: {decision3['regla']}. Recall máximo posible en prueba con 100 cupos: "
          f"{decision3['techo_recall_capacidad_prueba']:.3f}; la logística llega a 0.455."),
        h("4. Análisis de errores"),
        table(err, styles, widths=[200, 110, 120]), Spacer(1, 4),
        p("Los abandonos que el sistema no alcanza aprobaron en promedio 3.4 unidades con nota 9.0, y el 84 % tenía la "
          "matrícula al día (frente al 43 % de los alcanzados): es un abandono «silencioso» que no se ve en las señales académicas y requiere otros canales "
          "(entrevistas, encuesta de bienestar)."),
        h("5. DSS: priorización, apoyo y explicación"),
        p("Reglas de apoyo: deuda o matrícula atrasada → orientación financiera + tutoría; ninguna unidad aprobada → tutoría "
          "académica intensiva; resto → seguimiento del tutor. La explicación lista las tres variables que más suben el riesgo "
          "con su valor real. Ejemplo de la lista que ve la coordinación (cohorte de prueba):"),
        table(ex, styles, widths=[45, 55, 40, 120, 255]), Spacer(1, 4),
        p("La aplicación Streamlit (<i>app/streamlit_app.py</i>) permite cambiar los cupos, activar el reparto por edad y "
          "registrar cada decisión en <i>reports/decisiones_coordinacion.csv</i>."),
        h("6. Auditoría responsable"),
        p("En prueba, con cupos globales, la logística alcanzaba al 29 % de los abandonos de estudiantes de ≤ 20 años frente al "
          "55 % de los mayores de 25 (brecha 0.26): la tasa de abandono cambia mucho con la edad y los jóvenes casi no entraban "
          "en la lista. Mitigaciones evaluadas en validación:"),
        table(mit, styles, widths=[130, 90, 80, 80]), Spacer(1, 4),
        p("Solo el reparto de cupos por franja de edad (en proporción al abandono esperado por el propio modelo) cumple la brecha "
          "máxima de 0.15. El modelo sigue sin usar la edad; la edad solo reparte cupos de un apoyo voluntario. <b>Es una "
          "decisión de valores de la autora</b>. Resultado en prueba:"),
        table(mit_test, styles, widths=[130, 70, 75, 75, 75]), Spacer(1, 4),
        KeepTogether([table(grp, styles, widths=[60, 70, 60, 50, 60, 50]),
                      Image(str(r / "equidad.png"), width=470, height=163)]),
        p(f"<b>Decisión: {final['decision'].upper()}.</b> Cumple el recall mínimo (0.35) y las brechas observadas (género "
          f"{final['brechas']['genero']:.3f}, edad {final['brechas']['edad']:.3f}), pero el límite superior del intervalo "
          f"bootstrap del 95 % llega a {final['limite_superior_ic95']['edad']:.3f} en edad, por encima de 0.15. Se propone un "
          "piloto con revisión humana de cada propuesta. Becarios: 27 abandonos (menos de 30), no se usan para decidir."),
        h("7. Green AI"),
        p(f"Entrenamiento: {g['segundos_entrenamiento']:.3f} s; inferencia: {g['ms_por_estudiante']:.4f} ms por estudiante; "
          f"modelo de {g['tamano_modelo_kb']:.1f} KB y {g['parametros']} parámetros ({g['hardware']}). La logística está cerca "
          "del techo de recall a capacidad, por lo que un modelo más costoso no se justifica."),
        h("8. Reproducibilidad, Git y documentación"),
        p("Ejecución: <i>uv sync</i>, descarga, entrenamiento, auditoría, informe y pruebas (README). Evidencia Git: issues #1–#6 "
          "por semana, una rama y un pull request revisado por semana (#7–#12) y la etiqueta trabajo-final-v1.0. Documentos: "
          "alcance, Dataset Card, Model Card, declaración de IA y guion de demostración (docs/)."),
        h("9. Pruebas automatizadas"),
        p(f"{len(tests)} pruebas, todas aprobadas (el mínimo para un equipo individual es 6). Lista en docs/pruebas.csv."),
        table(trows, styles, widths=[24, 116, 60, 155, 160]), Spacer(1, 6),
        h("10. Límites"),
        p("Datos de una institución portuguesa: no representan a la UASD; los códigos de carrera e ingreso son de esa "
          "institución. Una sola partición y una semilla. La mitigación por edad requiere validación ética y jurídica antes de "
          "cualquier uso real (en la República Dominicana, Ley 172-13 para datos personales)."),
        h("11. Referencias"),
        p("Realinho, V., Vieira Martins, M., Machado, J. y Baptista, L. (2021). Predict Students' Dropout and Academic Success "
          "[Dataset]. UCI. https://doi.org/10.24432/C5MC89 · Realinho, V. et al. (2022). Predicting Student Dropout and Academic "
          "Success. Data, 7(11), 146. https://doi.org/10.3390/data7110146 · Mitchell, M. et al. (2019). Model Cards for Model "
          "Reporting. FAT*. · NIST (2023). AI RMF 1.0, NIST AI 100-1."),
        KeepTogether([h("12. Uso de IA"),
                      p("Utilicé Claude Code (Claude Opus 5.5), Codex (OpenAI) y DeepSeek como apoyo para estructura, código, "
                        "pruebas y redacción. Capacidad, compuertas, reglas de apoyo y reparto por edad son decisiones propias. "
                        "Detalle en docs/AI_USE_DECLARATION.md."), ai_table(styles)])]
    SimpleDocTemplate(str(r / "Informe_Trabajo_Final.pdf"), rightMargin=38, leftMargin=38, topMargin=34, bottomMargin=34,
                      title="Trabajo final · INF-8239").build(story)
    print("PDF:", r / "Informe_Trabajo_Final.pdf")


if __name__ == "__main__":
    main()
