"""Dashboard web interactivo de Industrias Caribe (Streamlit + Plotly).

Reutiliza las clases AnalizadorProduccion y AnalizadorReclamos de las
prácticas, así que las cifras coinciden con los dashboards en PNG y con el
informe. Los filtros de la barra lateral cumplen la función de los
segmentadores de Power BI o los filtros de Tableau.

Ejecutar con Docker (desde la carpeta Practica 3):
    docker compose up --build
y abrir http://localhost:8501
"""
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

BASE = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(BASE / "Practica_Produccion"), str(BASE / "Practica_Reclamos")]
import produccion_dashboard as prod  # noqa: E402
import reclamos_dashboard as rec  # noqa: E402

MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
TN = prod.NOMBRE_TURNO
AZUL, GRIS, NARANJA, VERDE, ROJO = "#2a7fa5", "#b8c4cc", "#e07b39", "#5a9e6f", "#c0504d"

st.set_page_config(page_title="Industrias Caribe · Dashboards", layout="wide")


@st.cache_data
def datos():
    return prod.cargar_datos(), rec.cargar_datos()


def filtro(columna, df, etiqueta, nombres=None):
    opciones = sorted(df[columna].dropna().unique())
    elegidas = st.sidebar.multiselect(etiqueta, opciones, default=opciones, format_func=lambda v: (nombres or {}).get(v, v))
    return df[df[columna].isin(elegidas)]


def kpis(valores):
    for col, (t, v) in zip(st.columns(len(valores)), valores):
        col.metric(t, v)


df_p, df_r = datos()
st.title("Industrias Caribe S.A.")
vista = st.sidebar.radio("Dashboard", ["Producción 2025", "Reclamos"])
st.sidebar.markdown("**Filtros**")

if vista == "Producción 2025":
    d = filtro("Planta", df_p, "Planta")
    d = filtro("Turno", d, "Turno", TN)
    d = filtro("Producto", d, "Producto")
    if d.empty:
        st.warning("Los filtros no dejan lotes para analizar.")
        st.stop()
    a = prod.AnalizadorProduccion(d)
    st.subheader(f"Control y eficiencia de producción · {len(d):,} lotes")
    kpis([("Producción total", f"{a.produccion_total():,.0f}"),
          ("Producción planificada", f"{a.produccion_planificada():,.0f}"),
          ("Cumplimiento del plan", f"{a.cumplimiento_plan():.2f}%"),
          ("Tasa de defectos", f"{a.tasa_defectos():.2f}%"),
          ("Costo total", f"RD${a.costo_total() / 1e6:,.2f} M"),
          ("Costo por unidad", f"RD${a.costo_por_unidad():.2f}")])

    c1, c2 = st.columns(2)
    m = a.mensual().reset_index()
    m["MesTxt"] = m["Mes"].apply(lambda p: MESES[p.month - 1])
    fig = go.Figure()
    fig.add_scatter(x=m["MesTxt"], y=m["UnidadesPlanificadas"], name="Planificada", mode="lines+markers", line=dict(color=GRIS, dash="dash"))
    fig.add_scatter(x=m["MesTxt"], y=m["UnidadesProducidas"], name="Real", mode="lines+markers", line=dict(color=AZUL))
    fig.update_layout(title="Producción real vs. planificada por mes", hovermode="x unified", yaxis_title="Unidades")
    c1.plotly_chart(fig, width="stretch")

    pl = a.resumen_por("Planta").reset_index()
    fig = px.bar(pl, x="Planta", y="UnidadesProducidas", text_auto=",.0f", title="Unidades producidas por planta",
                 hover_data={"Cumplimiento_%": ":.2f", "TasaDefectos_%": ":.2f", "CostoUnidad_DOP": ":.2f"}, color_discrete_sequence=[AZUL])
    c2.plotly_chart(fig, width="stretch")

    c3, c4 = st.columns(2)
    pr = a.resumen_por("Producto").reset_index().sort_values("TasaDefectos_%")
    fig = px.bar(pr, x="TasaDefectos_%", y="Producto", orientation="h", text_auto=".2f", title="Tasa de defectos por producto (%)",
                 color_discrete_sequence=[ROJO])
    fig.add_vline(x=a.tasa_defectos(), line_dash="dot", annotation_text=f"promedio {a.tasa_defectos():.2f}%")
    c3.plotly_chart(fig, width="stretch")

    tu = a.resumen_por("Turno").reindex([t for t in prod.TURNOS if t in d["Turno"].unique()]).reset_index()
    tu["Turno"] = tu["Turno"].map(TN)
    fig = px.bar(tu, x="Turno", y="UnidadesProducidas", text_auto=",.0f", title="Producción por turno",
                 hover_data={"TasaDefectos_%": ":.2f", "Cumplimiento_%": ":.2f"}, color_discrete_sequence=[NARANJA])
    c4.plotly_chart(fig, width="stretch")

    c5, c6 = st.columns(2)
    pc = a.resumen_por("Producto").reset_index().sort_values("CostoProduccion_DOP")
    fig = px.bar(pc, x="CostoProduccion_DOP", y="Producto", orientation="h", text_auto=",.0f", title="Costo de producción por producto (RD$)",
                 hover_data={"CostoUnidad_DOP": ":.2f"}, color_discrete_sequence=[VERDE])
    c5.plotly_chart(fig, width="stretch")

    filas = []
    for col in ("Planta", "Turno"):
        g = a.resumen_por(col)
        for k, v in g.iterrows():
            filas.append({"Grupo": TN.get(k, k), "Cumplimiento": f"{v['Cumplimiento_%']:.2f}%",
                          "Defectos": f"{v['TasaDefectos_%']:.2f}%", "Costo/unidad": f"RD${v['CostoUnidad_DOP']:.2f}"})
    c6.markdown("**Indicadores por planta y turno**")
    c6.dataframe(pd.DataFrame(filas), hide_index=True, width="stretch")

    with st.expander("Respuestas a las preguntas gerenciales (según los filtros)"):
        for k, v in prod.preguntas_gerenciales(a).items():
            st.markdown(f"- **{k}:** {v}")

else:
    d = filtro("Region", df_r, "Región")
    d = filtro("Prioridad", d, "Prioridad")
    if d.empty:
        st.warning("Los filtros no dejan reclamos para analizar.")
        st.stop()
    a = rec.AnalizadorReclamos(d)
    dias, sat = a.dias_promedio_resolucion(), a.satisfaccion_promedio()
    st.subheader("Gestión de reclamos · enero 2025 a enero 2026")
    kpis([("Total de reclamos", f"{a.total_reclamos():,}"),
          ("Reclamos resueltos", f"{a.reclamos_resueltos():,}"),
          ("% de resolución", f"{a.porcentaje_resolucion():.2f}%"),
          ("Días promedio de resolución", "Sin datos" if pd.isna(dias) else f"{dias:.2f}"),
          ("Satisfacción promedio (1-5)", "Sin datos" if pd.isna(sat) else f"{sat:.2f}")])

    c1, c2 = st.columns(2)
    cat = a.reclamos_por_categoria().sort_values().reset_index(name="Reclamos")
    c1.plotly_chart(px.bar(cat, x="Reclamos", y="Categoria", orientation="h", text_auto=True, title="Reclamos por categoría",
                           color_discrete_sequence=[AZUL]), width="stretch")
    est = a.reclamos_por_estado().reset_index(name="Reclamos")
    c2.plotly_chart(px.bar(est, x="Estado", y="Reclamos", text_auto=True, title="Reclamos por estado",
                           color_discrete_sequence=[NARANJA]), width="stretch")

    c3, c4 = st.columns(2)
    mes = a.evolucion_mensual().reset_index(name="Reclamos")
    mes["Mes"] = mes["FechaReclamo"].apply(lambda f: f"{MESES[f.month - 1]} {f.year}")
    c3.plotly_chart(px.line(mes, x="Mes", y="Reclamos", markers=True, title="Evolución mensual de reclamos",
                            color_discrete_sequence=[AZUL]), width="stretch")
    reg = a.reclamos_por_region().sort_values().reset_index(name="Reclamos")
    c4.plotly_chart(px.bar(reg, x="Reclamos", y="Region", orientation="h", text_auto=True, title="Reclamos por región",
                           color_discrete_sequence=[VERDE]), width="stretch")

st.caption("Fuente: CSV de Industrias Caribe (UASDVirtual). Tasas calculadas como razones de sumas. "
           "Tiempo y satisfacción solo sobre reclamos resueltos.")
