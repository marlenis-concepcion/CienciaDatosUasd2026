"""Exporta las hojas Ventas y Produccion a CSV para el artifact."""
import csv
from pathlib import Path
import openpyxl

BASE = Path(__file__).resolve().parent
EXCEL = next(d / "IndustriasCaribe_Tablas.xlsx" for d in (BASE.parent, BASE.parent.parent, BASE.parent.parent.parent)
             if (d / "IndustriasCaribe_Tablas.xlsx").exists())
wb = openpyxl.load_workbook(EXCEL, data_only=True)
for hoja, cols in {
    "Ventas": ["VentaID", "Fecha", "Producto", "Region", "Canal", "Unidades", "PrecioUnitario_DOP", "DescuentoPct", "IngresoNeto_DOP"],
    "Produccion": ["LoteID", "Fecha", "Producto", "Planta", "Turno", "UnidadesPlanificadas", "UnidadesProducidas", "UnidadesDefectuosas", "CostoProduccion_DOP"],
}.items():
    it = wb[hoja].iter_rows(values_only=True)
    hdr = list(next(it))
    idx = [hdr.index(c) for c in cols]
    with open(BASE / f"{hoja}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in it:
            if all(v is None for v in r): continue
            w.writerow([r[i].strftime("%Y-%m-%d") if hasattr(r[i], "strftime") else r[i] for i in idx])
