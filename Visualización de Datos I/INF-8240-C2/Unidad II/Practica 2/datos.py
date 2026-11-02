"""Carga y validación del caso académico sin rutas absolutas."""
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
import csv, hashlib
ROOT=Path(__file__).resolve().parent
SUBJECT=ROOT.parents[1]

def load():
    result={}
    for key in ['Reclamos','Produccion','Ventas']:
        path=SUBJECT/f'IndustriasCaribe_{key}.csv'
        if not path.exists():path=SUBJECT/'Unidad II'/f'IndustriasCaribe_{key}.csv'
        with path.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
        for row in rows:
            for col,val in list(row.items()):
                if not val.strip(): row[col]=None
                elif col.startswith('Fecha'): row[col]=datetime.fromisoformat(val)
                elif col in ['DiasResolucion','Satisfaccion_1a5','UnidadesPlanificadas','UnidadesProducidas','UnidadesDefectuosas','Unidades']: row[col]=int(val)
                elif col in ['CostoProduccion_DOP','PrecioUnitario_DOP','DescuentoPct','IngresoNeto_DOP']: row[col]=float(val)
            if key in ['Reclamos','Produccion']:
                date=row['FechaReclamo' if key=='Reclamos' else 'Fecha']
                row['MesReclamo' if key=='Reclamos' else 'MesProduccion']=date.replace(day=1)
                row['Universo']='Todos'
        result[key]=rows
    return result

def aggregate(rows,field,columns):
    groups=defaultdict(lambda:[0]*len(columns))
    for row in rows:
        for i,c in enumerate(columns): groups[row[field]][i]+=row[c]
    return dict(sorted(groups.items()))

def audit(data):
    r,p,v=(data[k] for k in ['Reclamos','Produccion','Ventas']); sales={x['VentaID']:x for x in v}
    checks=[]
    def check(name,actual,expected):
        assert actual==expected,(name,actual,expected)
        checks.append((name,actual,expected,'Correcto'))
    for name,rows,col,n in [('Reclamos',r,'ReclamoID',450),('Produccion',p,'LoteID',1200),('Ventas',v,'VentaID',3000)]:
        check(f'Registros {name}',len(rows),n);check(f'ID únicos {name}',len({x[col] for x in rows}),n)
    check('Resueltos',sum(x['Estado']=='Resuelto' for x in r),318)
    for c in ['DiasResolucion','Satisfaccion_1a5']:
        check(f'Con dato {c}',sum(x[c] is not None for x in r),318)
        check(f'Vacíos {c}',sum(x[c] is None for x in r),132)
    check('Resueltos sin ambos valores',sum(x['Estado']=='Resuelto' and (x['DiasResolucion'] is None or x['Satisfaccion_1a5'] is None) for x in r),0)
    check('No resueltos con valores registrados',sum(x['Estado']!='Resuelto' and (x['DiasResolucion'] is not None or x['Satisfaccion_1a5'] is not None) for x in r),0)
    check('Satisfacción fuera de 1 a 5',sum(x['Satisfaccion_1a5'] is not None and not 1<=x['Satisfaccion_1a5']<=5 for x in r),0)
    check('Días negativos',sum(x['DiasResolucion'] is not None and x['DiasResolucion']<0 for x in r),0)
    check('VentaID ausente',sum(x['VentaID'] not in sales for x in r),0)
    check('Producto distinto de venta asociada',sum(x['ProductoID']!=sales[x['VentaID']]['ProductoID'] for x in r),0)
    check('Región distinta de venta asociada',sum(x['Region']!=sales[x['VentaID']]['Region'] for x in r),0)
    check('Reclamos anteriores a su venta',sum(x['FechaReclamo']<sales[x['VentaID']]['Fecha'] for x in r),0)
    check('Producción con campos vacíos',sum(any(x is None for x in row.values()) for row in p),0)
    check('Unidades inconsistentes',sum(x['UnidadesPlanificadas']<=0 or x['UnidadesProducidas']<=0 or not 0<=x['UnidadesDefectuosas']<=x['UnidadesProducidas'] for x in p),0)
    return checks

def metrics(data):
    r,p=data['Reclamos'],data['Produccion']; cols=['UnidadesPlanificadas','UnidadesProducidas','UnidadesDefectuosas']
    totals=[sum(x[c] for x in p) for c in cols]
    return dict(total=len(r),resolved=sum(x['Estado']=='Resuelto' for x in r),days=sum(x['DiasResolucion'] or 0 for x in r)/318,satisfaction=sum(x['Satisfaccion_1a5'] or 0 for x in r)/318,categories=Counter(x['Categoria'] for x in r),states=Counter(x['Estado'] for x in r),months=Counter(x['MesReclamo'] for x in r),totals=totals,plants=aggregate(p,'Planta',cols),products=aggregate(p,'Producto',cols),production_months=aggregate(p,'MesProduccion',cols),shifts=aggregate(p,'Turno',cols),overplan=sum(x[cols[1]]>x[cols[0]] for x in p))
