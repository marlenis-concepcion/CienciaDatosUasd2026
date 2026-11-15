"""Práctica 2 · Control y eficiencia de producción de Industrias Caribe (Python).

Explora IndustriasCaribe_Produccion.csv, calcula los indicadores exigidos con la
clase AnalizadorProduccion, construye el dashboard y responde las preguntas
gerenciales. Los filtros opcionales equivalen a los segmentadores de Power BI.

Todas las tasas son razones de sumas (por ejemplo, defectuosas totales entre
producidas totales), no promedios de las tasas de cada lote.

Uso:
    python produccion_dashboard.py
    python produccion_dashboard.py --planta "Planta Santiago" --turno Noche
"""
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

CARPETA = Path(__file__).resolve().parent
MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
TURNOS = ["Manana", "Tarde", "Noche"]
NOMBRE_TURNO = {"Manana": "Mañana", "Tarde": "Tarde", "Noche": "Noche"}
SUMAS = ["UnidadesPlanificadas", "UnidadesProducidas", "UnidadesDefectuosas", "CostoProduccion_DOP"]


def cargar_datos():
    df = pd.read_csv(CARPETA / "IndustriasCaribe_Produccion.csv", encoding="utf-8-sig", parse_dates=["Fecha"])
    return df


def explorar(df):
    """A. Exploración: estructura, calidad y rango de los datos."""
    print("Registros:", len(df), "| Columnas:", df.shape[1])
    print("Período:", df["Fecha"].min().date(), "a", df["Fecha"].max().date())
    print("Valores nulos:", int(df.isna().sum().sum()), "| LoteID duplicados:", int(df["LoteID"].duplicated().sum()))
    print("Plantas:", sorted(df["Planta"].unique()))
    print("Turnos:", sorted(df["Turno"].unique()))
    print("Productos:", sorted(df["Producto"].unique()))
    sobre = (df["UnidadesProducidas"] > df["UnidadesPlanificadas"]).sum()
    print(f"Lotes que superan lo planificado: {sobre} de {len(df)} (se conservan: son datos válidos)")
    print(df[SUMAS].describe().round(2))


class AnalizadorProduccion:
    """Indicadores de producción sobre un DataFrame de lotes.

    El constructor guarda los datos en self.df; cada método calcula un
    indicador a partir de esas mismas filas, de modo que el objeto puede
    crearse con todo el dataset o con un subconjunto filtrado.
    """

    def __init__(self, datos):
        self.df = datos

    # B. Indicadores ---------------------------------------------------------
    def produccion_total(self):
        return self.df["UnidadesProducidas"].sum()

    def produccion_planificada(self):
        return self.df["UnidadesPlanificadas"].sum()

    def cumplimiento_plan(self):
        plan = self.produccion_planificada()
        return self.produccion_total() / plan * 100 if plan else float("nan")

    def tasa_defectos(self):
        prod = self.produccion_total()
        return self.df["UnidadesDefectuosas"].sum() / prod * 100 if prod else float("nan")

    def costo_total(self):
        return self.df["CostoProduccion_DOP"].sum()

    def costo_por_unidad(self):
        prod = self.produccion_total()
        return self.costo_total() / prod if prod else float("nan")

    # Resúmenes por dimensión -----------------------------------------------
    def resumen_por(self, columna):
        g = self.df.groupby(columna)[SUMAS].sum()
        g["Lotes"] = self.df.groupby(columna)["LoteID"].nunique()
        g["Cumplimiento_%"] = g["UnidadesProducidas"] / g["UnidadesPlanificadas"] * 100
        g["TasaDefectos_%"] = g["UnidadesDefectuosas"] / g["UnidadesProducidas"] * 100
        g["CostoUnidad_DOP"] = g["CostoProduccion_DOP"] / g["UnidadesProducidas"]
        return g

    def mensual(self):
        g = self.resumen_por(self.df["Fecha"].dt.to_period("M"))
        g.index.name = "Mes"
        return g


def preguntas_gerenciales(a):
    """D. Respuestas calculadas a partir de los datos."""
    planta, turno, prod, mes = a.resumen_por("Planta"), a.resumen_por("Turno"), a.resumen_por("Producto"), a.mensual()
    r = {}
    p = planta["UnidadesProducidas"].idxmax()
    r["Planta con mayor volumen"] = f"{p}: {planta.loc[p, 'UnidadesProducidas']:,.0f} unidades"
    p = planta["Cumplimiento_%"].idxmax()
    r["Planta con mejor cumplimiento"] = f"{p}: {planta.loc[p, 'Cumplimiento_%']:.2f}%"
    t = turno["TasaDefectos_%"].idxmax()
    r["Turno con mayor proporción de defectos"] = f"{NOMBRE_TURNO.get(t, t)}: {turno.loc[t, 'TasaDefectos_%']:.2f}%"
    c = prod["CostoProduccion_DOP"].idxmax()
    u = prod["CostoUnidad_DOP"].idxmax()
    r["Producto con mayor costo total"] = f"{c}: RD${prod.loc[c, 'CostoProduccion_DOP']:,.2f}"
    r["Producto con mayor costo por unidad"] = f"{u}: RD${prod.loc[u, 'CostoUnidad_DOP']:.2f}"
    mx, mn = mes["UnidadesProducidas"].idxmax(), mes["UnidadesProducidas"].idxmin()
    r["Evolución 2025"] = (f"máximo en {MESES[mx.month - 1]} ({mes.loc[mx, 'UnidadesProducidas']:,.0f}), "
                           f"mínimo en {MESES[mn.month - 1]} ({mes.loc[mn, 'UnidadesProducidas']:,.0f}); "
                           f"cumplimiento mensual entre {mes['Cumplimiento_%'].min():.2f}% y {mes['Cumplimiento_%'].max():.2f}%")
    return r


def tarjeta(ax, titulo, valor):
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, facecolor="#eef4f7", edgecolor="#c9d8e0"))
    ax.text(0.5, 0.62, valor, ha="center", va="center", fontsize=15, fontweight="bold", color="#12455e", transform=ax.transAxes)
    ax.text(0.5, 0.24, titulo, ha="center", va="center", fontsize=9, color="#4a5a63", transform=ax.transAxes)


def miles(x, _=None):
    return f"{x / 1e3:,.0f} mil" if abs(x) >= 1e3 else f"{x:,.0f}"


def construir_dashboard(a, subtitulo, salida):
    sns.set_theme(style="whitegrid")
    plt.rcParams["text.parse_math"] = False  # "RD$" es moneda, no una fórmula
    fig = plt.figure(figsize=(15, 15))
    arriba, abajo = fig.subfigures(2, 1, height_ratios=[0.11, 1])
    gk = arriba.add_gridspec(1, 6, wspace=0.1, left=0.03, right=0.97, top=0.92, bottom=0.06)
    kpis = [("Producción total", f"{a.produccion_total():,.0f}"),
            ("Producción planificada", f"{a.produccion_planificada():,.0f}"),
            ("Cumplimiento del plan", f"{a.cumplimiento_plan():.2f}%"),
            ("Tasa de defectos", f"{a.tasa_defectos():.2f}%"),
            ("Costo total", f"RD${a.costo_total() / 1e6:,.2f} M"),
            ("Costo por unidad producida", f"RD${a.costo_por_unidad():.2f}")]
    for i, (t, v) in enumerate(kpis):
        tarjeta(arriba.add_subplot(gk[0, i]), t, v)

    gs = abajo.add_gridspec(3, 2, hspace=0.42, wspace=0.32, left=0.1, right=0.97, top=0.95, bottom=0.05)
    azul, gris, naranja, verde, rojo = "#2a7fa5", "#b8c4cc", "#e07b39", "#5a9e6f", "#c0504d"

    # 1. Producción real frente a planificada por mes
    ax = abajo.add_subplot(gs[0, 0])
    m = a.mensual()
    x = range(len(m))
    etiquetas = [MESES[p.month - 1] for p in m.index]
    ax.plot(x, m["UnidadesPlanificadas"], marker="o", linestyle="--", color=gris, label="Planificada")
    ax.plot(x, m["UnidadesProducidas"], marker="o", color=azul, label="Real")
    ax.set_xticks(list(x), etiquetas)
    ax.yaxis.set_major_formatter(miles)
    ax.set_title("Producción real vs. planificada por mes", fontweight="bold")
    ax.legend(loc="upper left", fontsize=9)

    # 2. Unidades producidas por planta
    ax = abajo.add_subplot(gs[0, 1])
    pl = a.resumen_por("Planta").sort_values("UnidadesProducidas", ascending=False)
    ax.bar(pl.index.str.replace("Planta ", ""), pl["UnidadesProducidas"], color=azul)
    for i, (u, c) in enumerate(zip(pl["UnidadesProducidas"], pl["Cumplimiento_%"])):
        ax.text(i, u, f"{u:,.0f}\n({c:.2f}% del plan)", ha="center", va="bottom", fontsize=9)
    ax.yaxis.set_major_formatter(miles); ax.margins(y=0.18)
    ax.set_title("Unidades producidas por planta", fontweight="bold")

    # 3. Tasa de defectos por producto
    ax = abajo.add_subplot(gs[1, 0])
    pr = a.resumen_por("Producto").sort_values("TasaDefectos_%")
    ax.barh(pr.index, pr["TasaDefectos_%"], color=rojo)
    media = a.tasa_defectos()
    ax.axvline(media, color="#333", linestyle=":", linewidth=1)
    ax.text(media, -0.75, f" promedio {media:.2f}%", fontsize=8, va="center")
    for i, v in enumerate(pr["TasaDefectos_%"]):
        ax.text(v, i, f" {v:.2f}%", va="center", fontsize=9)
    ax.set_xlim(pr["TasaDefectos_%"].min() * 0.9, pr["TasaDefectos_%"].max() * 1.06)
    ax.set_title("Tasa de defectos por producto (%)", fontweight="bold")
    ax.set_xlabel("Eje recortado para resaltar diferencias pequeñas", fontsize=8, color="#666")

    # 4. Producción por turno
    ax = abajo.add_subplot(gs[1, 1])
    tu = a.resumen_por("Turno").reindex([t for t in TURNOS if t in a.df["Turno"].unique()])
    ax.bar([NOMBRE_TURNO[t] for t in tu.index], tu["UnidadesProducidas"], color=naranja)
    for i, (u, d) in enumerate(zip(tu["UnidadesProducidas"], tu["TasaDefectos_%"])):
        ax.text(i, u, f"{u:,.0f}\n({d:.2f}% defectos)", ha="center", va="bottom", fontsize=9)
    ax.yaxis.set_major_formatter(miles); ax.margins(y=0.18)
    ax.set_title("Producción por turno", fontweight="bold")

    # 5. Costo de producción por producto
    ax = abajo.add_subplot(gs[2, 0])
    pc = a.resumen_por("Producto").sort_values("CostoProduccion_DOP")
    ax.barh(pc.index, pc["CostoProduccion_DOP"] / 1e6, color=verde)
    for i, (c, cu) in enumerate(zip(pc["CostoProduccion_DOP"], pc["CostoUnidad_DOP"])):
        ax.text(c / 1e6, i, f" RD${c / 1e6:,.2f} M · RD${cu:.2f}/u", va="center", fontsize=9)
    ax.set_xlim(0, pc["CostoProduccion_DOP"].max() / 1e6 * 1.45)
    ax.set_title("Costo de producción por producto (millones RD$)", fontweight="bold")

    # 6. Indicadores de cumplimiento, defectos y costo por unidad
    ax = abajo.add_subplot(gs[2, 1]); ax.axis("off")
    filas, datos = [], []
    for col, orden in (("Planta", None), ("Turno", TURNOS)):
        g = a.resumen_por(col)
        if orden:
            g = g.reindex([t for t in orden if t in g.index])
        for k, v in g.iterrows():
            filas.append(NOMBRE_TURNO.get(k, k) if col == "Turno" else k)
            datos.append([f"{v['Cumplimiento_%']:.2f}%", f"{v['TasaDefectos_%']:.2f}%", f"RD${v['CostoUnidad_DOP']:.2f}"])
    filas.append("Total"); datos.append([f"{a.cumplimiento_plan():.2f}%", f"{a.tasa_defectos():.2f}%", f"RD${a.costo_por_unidad():.2f}"])
    tabla = ax.table(cellText=datos, rowLabels=filas, colLabels=["Cumplimiento", "Defectos", "Costo/unidad"], cellLoc="center", bbox=[0.3, 0.08, 0.7, 0.8])
    tabla.auto_set_font_size(False); tabla.set_fontsize(10)
    for (r, c), cell in tabla.get_celld().items():
        cell.set_edgecolor("#c9d8e0")
        if r == 0 or c == -1:
            cell.set_text_props(fontweight="bold"); cell.set_facecolor("#eef4f7")
    ax.set_title("Indicadores por planta y turno", fontweight="bold")

    fig.suptitle(f"Industrias Caribe - Control y eficiencia de producción 2025\n{subtitulo}", fontsize=16, fontweight="bold", y=1.03)
    fig.savefig(salida, dpi=150, bbox_inches="tight")
    return fig


def main():
    parser = argparse.ArgumentParser(description="Dashboard de producción de Industrias Caribe")
    parser.add_argument("--planta"); parser.add_argument("--turno"); parser.add_argument("--producto")
    parser.add_argument("--no-mostrar", action="store_true", help="Solo guardar la imagen")
    args = parser.parse_args()

    df = cargar_datos()
    explorar(df)
    datos = df
    for col, val in (("Planta", args.planta), ("Turno", args.turno), ("Producto", args.producto)):
        if val:
            datos = datos[datos[col] == val]
    if datos.empty:
        raise SystemExit("El filtro no deja lotes para analizar.")

    a = AnalizadorProduccion(datos)
    print("\nIndicadores")
    print(f"  Producción total:        {a.produccion_total():,.0f}")
    print(f"  Producción planificada:  {a.produccion_planificada():,.0f}")
    print(f"  Cumplimiento del plan:   {a.cumplimiento_plan():.2f}%")
    print(f"  Tasa de defectos:        {a.tasa_defectos():.2f}%")
    print(f"  Costo total:             RD${a.costo_total():,.2f}")
    print(f"  Costo por unidad:        RD${a.costo_por_unidad():.2f}")
    for col in ("Planta", "Turno", "Producto"):
        print(f"\nPor {col}\n", a.resumen_por(col).round(2).to_string())
    print("\nPreguntas gerenciales")
    for k, v in preguntas_gerenciales(a).items():
        print(f"  {k}: {v}")

    filtros = [v for v in (args.planta, args.turno, args.producto) if v]
    subtitulo = " · ".join(filtros) if filtros else "Todas las plantas, turnos y productos · 1,200 lotes"
    sufijo = "".join("_" + v.replace(" ", "") for v in filtros)
    salida = CARPETA / f"Dashboard_Produccion{sufijo}.png"
    construir_dashboard(a, subtitulo, salida)
    a.resumen_por("Producto").round(4).to_csv(CARPETA / f"indicadores_por_producto{sufijo}.csv", encoding="utf-8-sig")
    print("\nDashboard guardado en", salida.name)
    if not args.no_mostrar:
        plt.show()


if __name__ == "__main__":
    main()
