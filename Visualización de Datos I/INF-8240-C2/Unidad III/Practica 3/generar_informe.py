"""Genera el informe ejecutivo de dos páginas (Word) de la Unidad III.

Los números se calculan con las mismas clases de los dashboards, de modo que el
informe no repite cifras escritas a mano. Requiere haber ejecutado antes
produccion_dashboard.py para que exista Dashboard_Produccion.png.
"""
import sys
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

UNIDAD = Path(__file__).resolve().parent
sys.path[:0] = [str(UNIDAD / "Practica_Produccion"), str(UNIDAD / "Practica_Reclamos")]
import produccion_dashboard as prod  # noqa: E402
import reclamos_dashboard as rec  # noqa: E402

LOGO = UNIDAD.parent.parent / "Unidad I" / "Practica 1" / "recursos" / "uasd_logo.png"
DASH = UNIDAD / "Practica_Produccion" / "Dashboard_Produccion.png"
SALIDA = UNIDAD / "Informe_Ejecutivo_Unidad_III.docx"
URL = ("https://github.com/marlenis-concepcion/CienciaDatosUasd2026/tree/main/"
       "Visualizaci%C3%B3n%20de%20Datos%20I/INF-8240-C2/Unidad%20III/Practica%203")
AZUL = RGBColor.from_string("12455E")
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
TN = prod.NOMBRE_TURNO


def n0(v):
    return f"{v:,.0f}"


def sombrear(celda, color):
    pr = celda._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), color)
    pr.append(shd)


def enlace(parrafo, texto, url, tam=None):
    """Agrega un hipervínculo clicable al párrafo."""
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    h = OxmlElement("w:hyperlink"); h.set(qn("r:id"), parrafo.part.relate_to(url, RT.HYPERLINK, is_external=True))
    r = OxmlElement("w:r"); pr = OxmlElement("w:rPr")
    c = OxmlElement("w:color"); c.set(qn("w:val"), "126782"); pr.append(c)
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); pr.append(u)
    if tam:
        sz = OxmlElement("w:sz"); sz.set(qn("w:val"), str(int(tam * 2))); pr.append(sz)
    r.append(pr); t = OxmlElement("w:t"); t.text = texto; r.append(t); h.append(r); parrafo._p.append(h)


def datos_informe():
    a = prod.AnalizadorProduccion(prod.cargar_datos())
    pl, tu, pr, me = a.resumen_por("Planta"), a.resumen_por("Turno"), a.resumen_por("Producto"), a.mensual()
    sd, st = pl.loc["Planta Santo Domingo"], pl.loc["Planta Santiago"]
    d = dict(a=a, pl=pl, tu=tu, pr=pr, me=me)
    d["faltante"] = a.produccion_planificada() - a.produccion_total()
    d["lotes"] = len(a.df)
    d["sobre"] = int((a.df["UnidadesProducidas"] > a.df["UnidadesPlanificadas"]).sum())
    # Unidades defectuosas que se evitarían si Santo Domingo igualara la tasa de Santiago.
    d["def_evitables"] = sd["UnidadesDefectuosas"] - sd["UnidadesProducidas"] * st["TasaDefectos_%"] / 100
    # Ahorro si Santo Domingo produjera al costo unitario de Santiago.
    d["ahorro_sd"] = (sd["CostoUnidad_DOP"] - st["CostoUnidad_DOP"]) * sd["UnidadesProducidas"]
    r = rec.AnalizadorReclamos(rec.cargar_datos())
    d["rec"] = dict(total=r.total_reclamos(), res=r.reclamos_resueltos(), est=r.reclamos_por_estado().to_dict(),
                    dias=r.dias_promedio_resolucion(), sat=r.satisfaccion_promedio(), pct=r.porcentaje_resolucion())
    return d


def construir():
    d = datos_informe()
    a, pl, tu, pr, me = d["a"], d["pl"], d["tu"], d["pr"], d["me"]

    doc = Document()
    cp = doc.core_properties
    cp.author = "Marlenis Judith Concepción Cuevas"; cp.last_modified_by = ""
    cp.title = "Informe ejecutivo · Producción 2025 · Industrias Caribe"; cp.subject = "Visualización de Datos I · INF-8240-C2 · Unidad III"
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.left_margin = sec.right_margin = Inches(0.75); sec.top_margin = sec.bottom_margin = Inches(0.6)
    st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    st.paragraph_format.space_after = Pt(4); st.paragraph_format.line_spacing = 1.08

    def titulo(texto):
        p = doc.add_paragraph(); r = p.add_run(texto); r.bold = True; r.font.size = Pt(12); r.font.color.rgb = AZUL
        p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(3); p.paragraph_format.keep_with_next = True
        return p

    def parrafo(*partes, estilo=None):
        p = doc.add_paragraph(style=estilo)
        for parte in partes:
            if isinstance(parte, tuple):
                p.add_run(parte[0]).bold = True
            else:
                p.add_run(parte)
        return p

    # Encabezado
    enc = doc.add_table(rows=1, cols=2); enc.alignment = WD_TABLE_ALIGNMENT.CENTER
    c0, c1 = enc.rows[0].cells
    c0.width, c1.width = Inches(0.9), Inches(6.1)
    if LOGO.exists():
        c0.paragraphs[0].add_run().add_picture(str(LOGO), width=Inches(0.75))
    p = c1.paragraphs[0]; r = p.add_run("Informe ejecutivo · Control y eficiencia de producción 2025"); r.bold = True; r.font.size = Pt(15); r.font.color.rgb = AZUL
    p = c1.add_paragraph(); p.add_run("Industrias Caribe S.A. · Para: Gerencia de Operaciones").font.size = Pt(10)
    p = c1.add_paragraph()
    r = p.add_run(f"Visualización de Datos I (INF-8240-C2) · Unidad III · Marlenis Judith Concepción Cuevas · {date.today().day} de {MESES[date.today().month - 1]} de {date.today().year}")
    r.font.size = Pt(9); r.font.color.rgb = RGBColor.from_string("555555")
    p = c1.add_paragraph(); r = p.add_run("Código y dashboards: "); r.font.size = Pt(9)
    enlace(p, "GitHub · CienciaDatosUasd2026 / Unidad III / Practica 3", URL, tam=9)

    titulo("Resumen")
    parrafo(f"Durante 2025 las plantas de Santo Domingo y Santiago produjeron ", (f"{n0(a.produccion_total())} unidades",),
            f" de {n0(a.produccion_planificada())} planificadas, un ", (f"cumplimiento del {a.cumplimiento_plan():.2f}%",),
            f". Quedaron sin producir {n0(d['faltante'])} unidades del plan. La ", (f"tasa de defectos fue {a.tasa_defectos():.2f}%",),
            f" y el ", (f"costo total RD${a.costo_total() / 1e6:,.2f} millones",), f", equivalente a RD${a.costo_por_unidad():.2f} por unidad producida. "
            "Plantas y turnos rinden de forma parecida; las mayores oportunidades están en la planificación de los meses pico, "
            "la calidad y el costo unitario de la Planta Santo Domingo.")

    titulo("Indicadores clave")
    filas = [("Producción total", "Σ UnidadesProducidas", n0(a.produccion_total())),
             ("Producción planificada", "Σ UnidadesPlanificadas", n0(a.produccion_planificada())),
             ("Cumplimiento del plan", "Producidas ÷ Planificadas × 100", f"{a.cumplimiento_plan():.2f}%"),
             ("Tasa de defectos", "Defectuosas ÷ Producidas × 100", f"{a.tasa_defectos():.2f}%"),
             ("Costo total", "Σ CostoProduccion_DOP", f"RD${a.costo_total():,.2f}"),
             ("Costo por unidad producida", "Costo total ÷ Producidas", f"RD${a.costo_por_unidad():.2f}")]
    t = doc.add_table(rows=1, cols=3); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(["Indicador", "Fórmula", "Resultado 2025"]):
        c = t.rows[0].cells[i]; c.text = ""; c.paragraphs[0].add_run(h).bold = True; sombrear(c, "EEF4F7")
    for f in filas:
        cells = t.add_row().cells
        for i, v in enumerate(f):
            cells[i].text = v
            if i == 2:
                cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for row in t.rows:
        for c, w in zip(row.cells, (2.1, 2.9, 2.0)):
            c.width = Inches(w)
            for pp in c.paragraphs:
                pp.paragraph_format.space_after = Pt(0)
                for rr in pp.runs:
                    rr.font.size = Pt(9.5)

    titulo("Dashboard (Python: pandas, matplotlib y seaborn)")
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(DASH), width=Inches(4.35))
    cap = doc.add_paragraph(f"Fuente: IndustriasCaribe_Produccion.csv, {n0(d['lotes'])} lotes de enero a diciembre de 2025, sin valores nulos ni lotes duplicados. "
                            f"Se conservan los {d['sobre']} lotes que superaron su plan. Las tasas son razones de sumas.")
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in cap.runs:
        r.font.size = Pt(8); r.font.color.rgb = RGBColor.from_string("555555")

    # Página 2
    doc.add_page_break()
    titulo("Hallazgos: respuestas a las preguntas gerenciales")
    p_vol = pl["UnidadesProducidas"].idxmax(); p_otra = pl["UnidadesProducidas"].idxmin()
    p_cum = pl["Cumplimiento_%"].idxmax(); p_cum2 = pl["Cumplimiento_%"].idxmin()
    t_def = tu["TasaDefectos_%"].idxmax(); t_min = tu["TasaDefectos_%"].idxmin()
    c_tot = pr["CostoProduccion_DOP"].idxmax(); c_u = pr["CostoUnidad_DOP"].idxmax()
    mx, mn = me["UnidadesProducidas"].idxmax(), me["UnidadesProducidas"].idxmin()
    cmx, cmn = me["Cumplimiento_%"].idxmax(), me["Cumplimiento_%"].idxmin()
    h1 = me.loc[me.index.month <= 6, "UnidadesProducidas"].sum(); h2 = me.loc[me.index.month > 6, "UnidadesProducidas"].sum()
    hall = [
        (("¿Qué planta produce más? ",), f"{p_vol}, con {n0(pl.loc[p_vol, 'UnidadesProducidas'])} unidades frente a {n0(pl.loc[p_otra, 'UnidadesProducidas'])} de {p_otra} "
         f"({pl.loc[p_vol, 'UnidadesProducidas'] / a.produccion_total() * 100:.1f}% del total). La diferencia es pequeña."),
        (("¿Cuál cumple mejor el plan? ",), f"{p_cum}, con {pl.loc[p_cum, 'Cumplimiento_%']:.2f}% frente a {pl.loc[p_cum2, 'Cumplimiento_%']:.2f}%. "
         f"Sin embargo, tiene más defectos ({pl.loc[p_cum, 'TasaDefectos_%']:.2f}% frente a {pl.loc[p_cum2, 'TasaDefectos_%']:.2f}%) y mayor costo por unidad "
         f"(RD${pl.loc[p_cum, 'CostoUnidad_DOP']:.2f} frente a RD${pl.loc[p_cum2, 'CostoUnidad_DOP']:.2f})."),
        (("¿Qué turno tiene más defectos? ",), f"{TN[t_def]}, con {tu.loc[t_def, 'TasaDefectos_%']:.2f}% de unidades defectuosas; el más bajo es "
         f"{TN[t_min]} ({tu.loc[t_min, 'TasaDefectos_%']:.2f}%), que además produce más ({n0(tu.loc[t_min, 'UnidadesProducidas'])} unidades)."),
        (("¿Qué producto cuesta más? ",), f"{c_tot} tiene el mayor costo total (RD${pr.loc[c_tot, 'CostoProduccion_DOP'] / 1e6:,.2f} M), porque es el de mayor volumen. "
         f"Por unidad, el más caro es {c_u} (RD${pr.loc[c_u, 'CostoUnidad_DOP']:.2f})."),
        (("¿Cómo evoluciona la producción? ",), f"Sube con fuerza en junio y julio, baja de septiembre a noviembre y alcanza su máximo en {MESES[mx.month - 1]} "
         f"({n0(me.loc[mx, 'UnidadesProducidas'])} unidades); el mínimo fue {MESES[mn.month - 1]} ({n0(me.loc[mn, 'UnidadesProducidas'])}). "
         f"El segundo semestre produjo {(h2 / h1 - 1) * 100:.1f}% más que el primero. El cumplimiento osciló entre {me.loc[cmn, 'Cumplimiento_%']:.2f}% "
         f"({MESES[cmn.month - 1]}) y {me.loc[cmx, 'Cumplimiento_%']:.2f}% ({MESES[cmx.month - 1]}): el plan nunca se cumplió completo en ningún mes."),
    ]
    for neg, txt in hall:
        p = parrafo(neg, txt, estilo="List Bullet"); p.paragraph_format.space_after = Pt(3)

    titulo("Conclusiones")
    rng_cum = pl["Cumplimiento_%"].max() - pl["Cumplimiento_%"].min()
    for txt in [
        f"El desempeño es estable: entre plantas el cumplimiento difiere solo {rng_cum:.2f} puntos y entre turnos menos de medio punto. No hay una planta o turno que falle de forma aislada.",
        f"La brecha principal es de planificación: cada mes se programa más de lo que las plantas producen ({n0(d['faltante'])} unidades en el año), sobre todo en los meses pico.",
        "Santo Domingo cumple un poco mejor el plan, pero lo hace con más defectos y a mayor costo por unidad; Santiago es la referencia de eficiencia.",
    ]:
        doc.add_paragraph(txt, style="List Bullet").paragraph_format.space_after = Pt(3)

    titulo("Recomendaciones")
    reco = [
        (("1. Planificar según la capacidad real. ",), f"Ajustar el plan mensual al cumplimiento histórico (~{a.cumplimiento_plan():.0f}%) y reforzar personal y mantenimiento antes de junio, julio y diciembre, "
         f"para cerrar la brecha de {n0(d['faltante'])} unidades."),
        (("2. Programa de calidad focalizado. ",), f"Priorizar la Planta Santo Domingo, el turno {TN[t_def]} y los productos {pr['TasaDefectos_%'].idxmax()} y "
         f"{pr['TasaDefectos_%'].nlargest(2).index[1]}. Si Santo Domingo igualara la tasa de Santiago se evitarían unas {n0(d['def_evitables'])} unidades defectuosas al año."),
        (("3. Reducir el costo unitario. ",), f"Replicar en Santo Domingo las prácticas de Santiago (insumos, tiempos y consumo energético): igualar su costo por unidad ahorraría cerca de "
         f"RD${d['ahorro_sd'] / 1e6:,.2f} millones al año. Revisar en especial {c_u}."),
    ]
    for neg, txt in reco:
        parrafo(neg, txt).paragraph_format.space_after = Pt(3)

    rr = d["rec"]
    titulo("Práctica 1 · Verificación del dashboard de reclamos")
    parrafo(f"El dashboard de reclamos reproduce los valores de control: {rr['total']} reclamos, {rr['res']} resueltos ({rr['pct']:.2f}%), "
            f"{rr['est'].get('En proceso', 0)} en proceso y {rr['est'].get('Abierto', 0)} abiertos; {rr['dias']:.2f} días promedio de resolución y "
            f"satisfacción de {rr['sat']:.2f}/5, ambos sobre los reclamos resueltos. Los 132 vacíos se conservaron como nulos.")

    titulo("Archivos fuente")
    parrafo("Practica_Produccion/produccion_dashboard.py (clase AnalizadorProduccion y dashboard) · Practica_Reclamos/reclamos_dashboard.py "
            "(clase AnalizadorReclamos) · dashboard_web/app.py (dashboard interactivo con Docker) · generar_informe.py (este informe) · "
            "Dashboard_Produccion.png y Dashboard_Reclamos.png.")
    p = parrafo(("Repositorio en GitHub: ",)); enlace(p, URL, URL)

    doc.save(SALIDA)
    print("Informe guardado en", SALIDA.name)


if __name__ == "__main__":
    construir()
