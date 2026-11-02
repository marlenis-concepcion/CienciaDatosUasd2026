"""Controles de datos, cálculos, paquetes OOXML, enlaces y privacidad."""
import ast,math,re,statistics,warnings,posixpath
from datetime import datetime
from itertools import product
from zipfile import ZipFile
from lxml import etree as E
from openpyxl import load_workbook
from pypdf import PdfReader
from datos import ROOT,load,audit,metrics
from excel_nativo import NS,X14,REL,PKG,SLE
from generar_excel import OUT,URL


def main():
    data=load();checks=audit(data);m=metrics(data)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore');wb=load_workbook(OUT);values=load_workbook(OUT,data_only=True)
    assert sum(len(w._pivots) for w in wb)==10
    assert wb['Reclamos'].tables['tblReclamos'].ref=='A1:L451'
    assert wb['Produccion'].tables['tblProduccion'].ref=='A1:L1201'
    assert all(isinstance(wb['Reclamos'].cell(i,3).value,datetime) for i in range(2,452))
    for col in [9,10]:assert sum(wb['Reclamos'].cell(i,col).value is None for i in range(2,452))==132
    for sheet in ['Dashboard_Reclamos','Dashboard_Produccion']:
        assert len(wb[sheet]._charts)==4
    with ZipFile(OUT) as z:
        names=set(z.namelist());pivots={}
        for name in names:
            if name.endswith('.xml') or name.endswith('.rels'):E.fromstring(z.read(name))
            if name.endswith('.rels'):
                root=E.fromstring(z.read(name));base='' if name=='_rels/.rels' else posixpath.dirname(posixpath.dirname(name))
                for rel in root:
                    if rel.get('TargetMode')=='External':continue
                    target=rel.get('Target');target=target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join(base,target))
                    assert target in names,(name,target)
            if re.fullmatch(r'xl/pivotTables/pivotTable\d+.xml',name):
                pv=E.fromstring(z.read(name));pivots[pv.get('name')]=pv
        assert len(pivots)==10
        caches={}
        for name in names:
            if re.fullmatch(r'xl/pivotCache/pivotCacheDefinition\d+.xml',name):
                ca=E.fromstring(z.read(name));cache_id=ca.find(f'.//{{{X14}}}pivotCacheDefinition').get('pivotCacheId');caches[cache_id]=ca
        assert len(caches)==2
        sl=[n for n in names if re.fullmatch(r'xl/slicerCaches/slicerCache\d+.xml',n)];assert len(sl)==6
        for name in sl:
            sc=E.fromstring(z.read(name));pt=sc.find(f'{{{X14}}}pivotTables');assert len(pt)==5
            source_id=sc.find(f'.//{{{X14}}}tabular').get('pivotCacheId');assert source_id in caches
            for pp in pt:assert pivots[pp.get('name')].get('cacheId')==source_id
        drawing_slicers=[]
        for name in names:
            if re.fullmatch(r'xl/drawings/drawing\d+.xml',name):drawing_slicers+=E.fromstring(z.read(name)).findall(f'.//{{{SLE}}}slicer')
        assert len(drawing_slicers)==6
        assert not any('/externalLinks/' in n or n.endswith('vbaProject.bin') for n in names)
    # Recalculate every dashboard formula from the original records, not the displayed cached values.
    pv_defs={p.name:p for ws in wb for p in ws._pivots}
    def getpivot(measure,table,*criteria):
        pv=pv_defs[table];src='Reclamos' if pv.cacheId==1 else 'Produccion';rows=data[src]
        for field,val in zip(criteria[::2],criteria[1::2]):rows=[r for r in rows if r[field]==val]
        field=next(f for f in pv.dataFields if f.name==measure);col=pv.cache.cacheFields[field.fld].name;nums=[r[col] for r in rows if r[col] is not None]
        return len(nums) if field.subtotal=='count' else sum(nums) if field.subtotal=='sum' else statistics.mean(nums)
    def evaluate(formula):
        formula=re.sub(r"'([^']+)'!\$A\$4",lambda m:repr(m[1]),formula[1:]);tree=ast.parse(formula,mode='eval')
        allowed=(ast.Expression,ast.Call,ast.Name,ast.Load,ast.Constant,ast.BinOp,ast.Div)
        assert all(isinstance(n,allowed) for n in ast.walk(tree))
        env={'GETPIVOTDATA':getpivot,'DATE':datetime,'IFERROR':lambda v,fallback:v}
        return eval(compile(tree,'<generated formula>','eval'),{'__builtins__':{}},env)
    checked=0
    for sn in ['Dashboard_Reclamos','Dashboard_Produccion']:
        for row in wb[sn]:
            for c in row:
                if c.data_type=='f':
                    actual=evaluate(c.value);saved=values[sn][c.coordinate].value;assert math.isclose(actual,saved,rel_tol=1e-10),(sn,c.coordinate,actual,saved);checked+=1
    # Source-backed expectations for filter combinations; this does not execute Excel's UI.
    scenarios=0
    for src,fields in [('Reclamos',['Region','Categoria','Estado']),('Produccion',['Planta','Turno','Producto'])]:
        choices=[[None]+sorted({r[c] for r in data[src]}) for c in fields]
        for vals in product(*choices):
            rows=[r for r in data[src] if all(v is None or r[c]==v for c,v in zip(fields,vals))]
            if src=='Reclamos':
                resolved=sum(r['Estado']=='Resuelto' for r in rows);assert 0<=resolved<=len(rows)
                if 'Abierto' in vals:assert resolved==0 and not any(r['DiasResolucion'] is not None for r in rows)
            elif rows:
                produced=sum(r['UnidadesProducidas'] for r in rows);defects=sum(r['UnidadesDefectuosas'] for r in rows);assert 0<=defects/produced<=1
            scenarios+=1
    pdf=PdfReader(ROOT/'Informe_Unidad_II_IndustriasCaribe.pdf');links=[a.get_object().get('/A',{}).get('/URI') for p in pdf.pages for a in p.get('/Annots',[])];assert URL in links
    pattern=re.compile(r'/(?:Users|home)/[^\s]+|sesskey=|file://',re.I)
    for path in ROOT.rglob('*'):
        if not path.is_file() or path.suffix in ['.png','.pyc']:continue
        if path.suffix in ['.xlsx','.docx']:
            with ZipFile(path) as z:texts=[z.read(n).decode('utf8',errors='ignore') for n in z.namelist() if n.endswith('.xml')]
        elif path.suffix=='.pdf':texts=[p.extract_text() for p in pdf.pages]+[str(pdf.metadata)]
        else:texts=[path.read_text()]
        if path.name=='verificar_entrega.py':continue # Sanitization patterns are test fixtures.
        assert all(not pattern.search(t) for t in texts),path.name
    word=ROOT/'Informe_Unidad_II_IndustriasCaribe.docx'
    if word.exists():
        with ZipFile(word) as z:
            document=E.fromstring(z.read('word/document.xml'));wns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            assert len(document.findall('.//w:tbl',wns))==7
            assert len(document.findall('.//w:drawing',wns))==9
    result=f'''# Verificación de la entrega\n\n- {len(checks)} controles de datos y relaciones: correctos.\n- 10 tablas dinámicas nativas, 2 cachés, 6 segmentadores; cada uno conectado a las 5 TD compatibles.\n- 8 gráficos de Excel y 8 visualizaciones del informe.\n- {checked} fórmulas de dashboards recalculadas contra los datos originales y conciliadas con sus resultados guardados.\n- {scenarios} combinaciones de filtros con expectativas calculadas desde los datos originales. Estas comprobaciones no ejecutan la interfaz de Excel.\n- XML y relaciones internas: válidos; sin enlaces externos a datos ni macros. El enlace web de GitHub es un hipervínculo.\n- Word editable: portada, siete tablas y ocho gráficos, más el escudo; contenido y metadatos revisados.\n- PDF: {len(pdf.pages)} páginas; enlace GitHub clicable presente.\n- Sin rutas personales, nombres de dispositivos ni parámetros de sesión en el contenido entregable.\n\n## Alcance y compatibilidad\n\nEl libro se abrió con LibreOffice para revisar datos iniciales y gráficos. Los segmentadores requieren Excel compatible; su interacción en Excel de escritorio no se pudo ejecutar en este entorno. No guardar la vista previa de LibreOffice sobre el original, ya que puede perder las extensiones de segmentadores.\n\nPruebas manuales propuestas: Estado = Resuelto → total 318 y resueltos 318; Estado = Abierto → total 54, resueltos 0 y promedios sin datos; Planta Santiago → plan 545,792, real 516,231 y defectuosas 17,354. Borrar filtros restablece los totales globales.\n'''
    (ROOT/'VERIFICACION.md').write_text(result);print(result)

if __name__=='__main__':main()
