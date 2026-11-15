"""Agrega Ventas y Produccion de IndustriasCaribe_Tablas.xlsx para el storytelling."""
import json
from collections import defaultdict
from pathlib import Path
import openpyxl

BASE = Path(__file__).resolve().parent
EXCEL = next(d / "IndustriasCaribe_Tablas.xlsx" for d in (BASE.parent, BASE.parent.parent, BASE.parent.parent.parent)
             if (d / "IndustriasCaribe_Tablas.xlsx").exists())
wb = openpyxl.load_workbook(EXCEL, data_only=True)

def rows(name):
    it = wb[name].iter_rows(values_only=True)
    hdr = next(it)
    return [dict(zip(hdr, r)) for r in it if any(v is not None for v in r)]

ventas, prod = rows("Ventas"), rows("Produccion")
issues = defaultdict(int)
for r in ventas:
    for k, v in r.items():
        if v is None: issues[f"Ventas.{k} nulo"] += 1
    if isinstance(r["Unidades"], (int, float)) and r["Unidades"] <= 0: issues["Ventas.Unidades<=0"] += 1
for r in prod:
    for k, v in r.items():
        if v is None: issues[f"Produccion.{k} nulo"] += 1

def num(v):
    return float(v) if isinstance(v, (int, float)) else 0.0

out = {"n_ventas": len(ventas), "n_lotes": len(prod), "issues": dict(issues)}
dates = [r["Fecha"] for r in ventas if r["Fecha"]] + [r["Fecha"] for r in prod if r["Fecha"]]
out["rango"] = [min(dates).strftime("%Y-%m-%d"), max(dates).strftime("%Y-%m-%d")]

m = defaultdict(lambda: defaultdict(float))
for r in ventas:
    if not r["Fecha"]: continue
    k = r["Fecha"].strftime("%Y-%m")
    m[k]["ingreso"] += num(r["IngresoNeto_DOP"]); m[k]["vendidas"] += num(r["Unidades"]); m[k]["n"] += 1
for r in prod:
    if not r["Fecha"]: continue
    k = r["Fecha"].strftime("%Y-%m")
    m[k]["producidas"] += num(r["UnidadesProducidas"]); m[k]["planificadas"] += num(r["UnidadesPlanificadas"])
    m[k]["defectuosas"] += num(r["UnidadesDefectuosas"]); m[k]["costo"] += num(r["CostoProduccion_DOP"])
out["mensual"] = [{"mes": k, **{a: round(b, 2) for a, b in v.items()}} for k, v in sorted(m.items())]

def group(data, key, fields):
    g = defaultdict(lambda: defaultdict(float))
    for r in data:
        for f, src in fields.items():
            g[r[key]][f] += num(r[src]) if src else 1
    return {k: {a: round(b, 2) for a, b in v.items()} for k, v in g.items()}

out["prod_ventas"] = group(ventas, "Producto", {"ingreso": "IngresoNeto_DOP", "vendidas": "Unidades", "n": None})
out["prod_prod"] = group(prod, "Producto", {"producidas": "UnidadesProducidas", "planificadas": "UnidadesPlanificadas", "defectuosas": "UnidadesDefectuosas", "costo": "CostoProduccion_DOP"})
out["region"] = group(ventas, "Region", {"ingreso": "IngresoNeto_DOP", "vendidas": "Unidades"})
out["canal"] = group(ventas, "Canal", {"ingreso": "IngresoNeto_DOP", "vendidas": "Unidades"})
out["planta"] = group(prod, "Planta", {"producidas": "UnidadesProducidas", "planificadas": "UnidadesPlanificadas", "defectuosas": "UnidadesDefectuosas", "costo": "CostoProduccion_DOP"})
out["turno"] = group(prod, "Turno", {"producidas": "UnidadesProducidas", "planificadas": "UnidadesPlanificadas", "defectuosas": "UnidadesDefectuosas"})
desc = defaultdict(lambda: [0.0, 0.0])
for r in ventas:
    desc[r["DescuentoPct"]][0] += num(r["IngresoNeto_DOP"]); desc[r["DescuentoPct"]][1] += num(r["Unidades"])
out["descuento"] = {str(k): [round(a, 2), b] for k, (a, b) in desc.items()}

(BASE / "resumen.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(json.dumps(out, ensure_ascii=False, indent=1))
