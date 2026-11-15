"""Práctica 1 · Gestión de reclamos de Industrias Caribe (Parte C: Python).

Sigue los pasos de la guía: carga el CSV, define la clase AnalizadorReclamos,
calcula los indicadores y construye el dashboard 2 × 2. Se agregan tarjetas
de indicadores y filtros opcionales de Región y Prioridad, equivalentes a los
segmentadores de Power BI y Tableau.

Uso:
    python reclamos_dashboard.py
    python reclamos_dashboard.py --region Este --prioridad Alta
"""
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

CARPETA = Path(__file__).resolve().parent
MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]


# Paso 2. Cargar los datos --------------------------------------------------
def cargar_datos():
    df = pd.read_csv(
        CARPETA / "IndustriasCaribe_Reclamos.csv",
        encoding="utf-8-sig",
        parse_dates=["FechaReclamo"],
    )
    # Los vacíos de DiasResolucion y Satisfaccion_1a5 corresponden a reclamos
    # no resueltos: se conservan como nulos (NaN), no se convierten en cero.
    return df


# Paso 3. Clase para analizar reclamos --------------------------------------
class AnalizadorReclamos:
    """Agrupa los cálculos sobre la tabla de reclamos.

    __init__ es el constructor: se ejecuta al crear el objeto y recibe el
    DataFrame. Lo guarda en el atributo self.df para que todos los métodos
    trabajen sobre los mismos datos sin volver a pasarlos como argumento.
    """

    def __init__(self, datos):
        self.df = datos

    def total_reclamos(self):
        return self.df["ReclamoID"].nunique()

    def reclamos_resueltos(self):
        return self.df.loc[self.df["Estado"] == "Resuelto", "ReclamoID"].nunique()

    def porcentaje_resolucion(self):
        total = self.total_reclamos()
        if total == 0:
            return 0
        return self.reclamos_resueltos() / total * 100

    def reclamos_por_categoria(self):
        return self.df.groupby("Categoria")["ReclamoID"].nunique().sort_values(ascending=False)

    # Métodos añadidos para completar los indicadores del Paso 6.
    def reclamos_por_estado(self):
        orden = ["Abierto", "En proceso", "Resuelto"]
        return self.df.groupby("Estado")["ReclamoID"].nunique().reindex(orden).fillna(0).astype(int)

    def reclamos_por_region(self):
        return self.df.groupby("Region")["ReclamoID"].nunique().sort_values(ascending=False)

    def evolucion_mensual(self):
        # resample("MS") agrupa por mes calendario y mantiene el año, así que
        # enero de 2025 y enero de 2026 quedan separados y en orden.
        return self.df.set_index("FechaReclamo").resample("MS")["ReclamoID"].nunique()

    def dias_promedio_resolucion(self):
        return self.df.loc[self.df["Estado"] == "Resuelto", "DiasResolucion"].mean()

    def satisfaccion_promedio(self):
        return self.df.loc[self.df["Estado"] == "Resuelto", "Satisfaccion_1a5"].mean()


def filtrar(df, region=None, prioridad=None):
    if region:
        df = df[df["Region"] == region]
    if prioridad:
        df = df[df["Prioridad"] == prioridad]
    return df


def tarjeta(ax, titulo, valor):
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, facecolor="#eef4f7", edgecolor="#c9d8e0"))
    ax.text(0.5, 0.64, valor, ha="center", va="center", fontsize=17, fontweight="bold", color="#12455e", transform=ax.transAxes)
    ax.text(0.5, 0.25, titulo, ha="center", va="center", fontsize=9, color="#4a5a63", transform=ax.transAxes)


def construir_dashboard(analizador, subtitulo, salida):
    sns.set_theme(style="whitegrid")
    fig = plt.figure(figsize=(14, 10.5))
    arriba, abajo = fig.subfigures(2, 1, height_ratios=[0.16, 1])
    gk = arriba.add_gridspec(1, 5, wspace=0.12, left=0.03, right=0.97, top=0.92, bottom=0.08)
    gs = abajo.add_gridspec(2, 2, width_ratios=[1.5, 1], hspace=0.38, wspace=0.42, left=0.09, right=0.97, top=0.93, bottom=0.08)

    dias = analizador.dias_promedio_resolucion()
    satis = analizador.satisfaccion_promedio()
    kpis = [
        ("Total de reclamos", f"{analizador.total_reclamos():,}"),
        ("Reclamos resueltos", f"{analizador.reclamos_resueltos():,}"),
        ("% de resolución", f"{analizador.porcentaje_resolucion():.2f}%"),
        ("Días promedio de resolución", "Sin datos" if pd.isna(dias) else f"{dias:.2f}"),
        ("Satisfacción promedio (1-5)", "Sin datos" if pd.isna(satis) else f"{satis:.2f}"),
    ]
    for i, (t, v) in enumerate(kpis):
        tarjeta(arriba.add_subplot(gk[0, i]), t, v)

    ax_cat = abajo.add_subplot(gs[0, 0])
    ax_est = abajo.add_subplot(gs[0, 1])
    ax_mes = abajo.add_subplot(gs[1, 0])
    ax_reg = abajo.add_subplot(gs[1, 1])

    # Reclamos por categoría (barras)
    categoria = analizador.reclamos_por_categoria()
    sns.barplot(x=categoria.values, y=categoria.index, ax=ax_cat, color="#2a7fa5")
    ax_cat.set_title("Reclamos por categoría", fontweight="bold")
    ax_cat.set_xlabel("Reclamos"); ax_cat.set_ylabel("")
    ax_cat.bar_label(ax_cat.containers[0], padding=3); ax_cat.margins(x=0.08)

    # Reclamos por estado (columnas)
    estado = analizador.reclamos_por_estado()
    sns.barplot(x=estado.index, y=estado.values, ax=ax_est, color="#e07b39")
    ax_est.set_title("Reclamos por estado", fontweight="bold")
    ax_est.set_xlabel(""); ax_est.set_ylabel("Reclamos")
    ax_est.bar_label(ax_est.containers[0], padding=3); ax_est.margins(y=0.1)

    # Evolución mensual (líneas), con año en la etiqueta
    mensual = analizador.evolucion_mensual()
    etiquetas = [f"{MESES[d.month - 1]} {str(d.year)[2:]}" for d in mensual.index]
    ax_mes.plot(range(len(mensual)), mensual.values, marker="o", color="#2a7fa5")
    ax_mes.set_xticks(range(len(mensual)), etiquetas, rotation=45)
    ax_mes.set_title("Evolución mensual de reclamos", fontweight="bold")
    ax_mes.set_ylabel("Reclamos")
    for x, y in enumerate(mensual.values):
        ax_mes.annotate(str(y), (x, y), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8)

    # Reclamos por región (barras)
    region = analizador.reclamos_por_region()
    sns.barplot(x=region.values, y=region.index, ax=ax_reg, color="#5a9e6f")
    ax_reg.set_title("Reclamos por región", fontweight="bold")
    ax_reg.set_xlabel("Reclamos"); ax_reg.set_ylabel("")
    ax_reg.bar_label(ax_reg.containers[0], padding=3); ax_reg.margins(x=0.1)

    fig.suptitle(f"Industrias Caribe - Gestión de Reclamos\n{subtitulo}", fontsize=15, fontweight="bold", y=1.04)
    fig.savefig(salida, dpi=150, bbox_inches="tight")
    return fig


def main():
    parser = argparse.ArgumentParser(description="Dashboard de reclamos de Industrias Caribe")
    parser.add_argument("--region", help="Filtrar por región (segmentador)")
    parser.add_argument("--prioridad", help="Filtrar por prioridad: Alta, Media o Baja")
    parser.add_argument("--no-mostrar", action="store_true", help="Solo guardar la imagen")
    args = parser.parse_args()

    df = cargar_datos()
    print(df.head())
    df.info()

    datos = filtrar(df, args.region, args.prioridad)
    if datos.empty:
        raise SystemExit("El filtro no deja reclamos para analizar.")

    # Paso 4. Crear el objeto y calcular indicadores
    analizador = AnalizadorReclamos(datos)
    print("\nTotal:", analizador.total_reclamos())
    print("Resueltos:", analizador.reclamos_resueltos())
    print("Porcentaje resolución:", round(analizador.porcentaje_resolucion(), 2))
    print("Por estado:", analizador.reclamos_por_estado().to_dict())
    print("Días promedio de resolución:", round(analizador.dias_promedio_resolucion(), 2))
    print("Satisfacción promedio:", round(analizador.satisfaccion_promedio(), 2))

    filtros = [f"Región: {args.region}" if args.region else "Todas las regiones",
               f"Prioridad: {args.prioridad}" if args.prioridad else "todas las prioridades"]
    sufijo = "".join(f"_{v.replace(' ', '')}" for v in (args.region, args.prioridad) if v)
    salida = CARPETA / f"Dashboard_Reclamos{sufijo}.png"

    # Paso 5. Crear el dashboard
    construir_dashboard(analizador, " · ".join(filtros) + " · Ene 2025 - Ene 2026", salida)
    print("\nDashboard guardado en", salida.name)
    if not args.no_mostrar:
        plt.show()


if __name__ == "__main__":
    main()
