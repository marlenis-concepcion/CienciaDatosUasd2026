"""Genera libro con datos, fórmulas cacheadas, 10 TD, 6 slicers y 8 gráficos."""
from collections import Counter
from datetime import datetime
from pathlib import Path
import statistics
import xlsxwriter
from datos import ROOT,load,audit,metrics
from excel_nativo import inject

URL='https://github.com/marlenis-concepcion/CienciaDatosUasd2026/tree/main/Visualizaci%C3%B3n%20de%20Datos%20I/INF-8240-C2/Unidad%20II/Practica%202'
OUT=ROOT/'Marlenis_Concepcion_IndustriasCaribe.xlsx'
BLUE='#126782';TEAL='#219EBC';GOLD='#E9A23B';PURPLE='#7B6BA8';BG='#F2F6F8'

def build():
    data=load();checks=audit(data);m=metrics(data)
    book=xlsxwriter.Workbook(OUT);book.set_properties({'title':'Unidad II · Industrias Caribe S.A.','author':'Marlenis Judith Concepción Cuevas','subject':'Visualización de Datos I · INF-8240-C2','comments':'Datos originales de la consigna UASDVirtual. Sin macros ni conexiones externas.'})
    f={
      'head':book.add_format({'bold':True,'bg_color':BLUE,'font_color':'white','text_wrap':True,'valign':'vcenter','border':1,'border_color':'white'}),
      'title':book.add_format({'bold':True,'font_size':22,'font_color':BLUE,'valign':'vcenter'}),
      'body':book.add_format({'font_size':11,'text_wrap':True,'valign':'top'}),
      'note':book.add_format({'font_size':10,'font_color':'#4E6170','text_wrap':True,'valign':'top'}),
      'int':book.add_format({'num_format':'#,##0','border':1,'border_color':'#DFE7EC'}),
      'num':book.add_format({'num_format':'0.00','border':1,'border_color':'#DFE7EC'}),
      'pct':book.add_format({'num_format':'0.00%','border':1,'border_color':'#DFE7EC'}),
      'date':book.add_format({'num_format':'yyyy-mm-dd'}),
      'month':book.add_format({'num_format':'mmm yyyy'}),
      'text':book.add_format({'border':1,'border_color':'#DFE7EC'}),
      'khead':book.add_format({'bold':True,'font_size':11,'font_color':BLUE,'bg_color':'#E5F1F5','align':'center'}),
      'kint':book.add_format({'font_size':25,'bold':True,'font_color':BLUE,'bg_color':'#E5F1F5','align':'center','num_format':'#,##0'}),
      'knum':book.add_format({'font_size':25,'bold':True,'font_color':BLUE,'bg_color':'#E5F1F5','align':'center','num_format':'0.00'}),
      'kpct':book.add_format({'font_size':25,'bold':True,'font_color':BLUE,'bg_color':'#E5F1F5','align':'center','num_format':'0.00%'}),
    }
    sheets={}
    def sheet(name,title=None,dashboard=False):
        ws=book.add_worksheet(name);sheets[name]=ws;ws.hide_gridlines(2);ws.freeze_panes(4,1);ws.set_column('A:A',27);ws.set_column('B:H',19);ws.set_landscape();ws.set_paper(9);ws.fit_to_pages(1,1);ws.set_margins(.25,.25,.35,.35)
        if title:ws.merge_range('A1:H2',title,f['title'])
        if dashboard:
            ws.set_column('A:X',8);ws.set_default_row(15);ws.freeze_panes(0,0);ws.print_area('A1:X58');ws.set_zoom(80);ws.set_header('&CIndustrias Caribe S.A. · INF-8240-C2');ws.set_footer('&LMarlenis Judith Concepción Cuevas&R&P / &N')
        return ws
    guide=sheet('Inicio','Industrias Caribe S.A. · Unidad II')
    guide.set_column('A:A',27);guide.set_column('B:H',18)
    notes=[('Estudiante','Marlenis Judith Concepción Cuevas'),('Materia','Visualización de Datos I · INF-8240-C2'),('Contenido','450 reclamos, 1,200 lotes de producción y 3,000 ventas. Datos de la actividad UASDVirtual.'),('Uso','Abrir Dashboard_Reclamos y Dashboard_Produccion en Excel de escritorio con soporte de segmentadores. Todos los filtros se entregan sin selección restrictiva.'),('Filtros de reclamos','Region, Categoria y Estado. Cada segmentador se conecta a las 5 TD de reclamos. Total, resueltos, días y satisfacción se calculan desde TD; los gráficos consultan las mismas TD.'),('Filtros de producción','Planta, Turno y Producto. Cada segmentador se conecta a las 5 TD de producción. Las tasas usan razón de sumas; no promedio de porcentajes.'),('Multiselección','Ctrl/Cmd o botón multiselección del segmentador. Usar el icono de borrar filtro para volver al total. No confundir 54 Abierto con los 132 aún no resueltos.'),('Datos actualizados','Datos > Actualizar todo si se editan los registros originales. Los resultados iniciales están guardados para su revisión. Se conservaron los 132 vacíos; no son ceros.'),('Compatibilidad','Los segmentadores requieren un visor que soporte esta función. No guardar este libro con bibliotecas o visores que eliminen extensiones de segmentadores. El PDF muestra la vista global sin filtros.'),('Tasas y límites','Tasa de defectos = suma defectuosas / suma producidas. Cumplimiento = suma producidas / suma planificadas. Los reclamos no se presentan como tasa por producto ni como deterioro causal.'),('Fuentes','CSV originales de la consigna; no se utilizó el archivo Ventas copy, que es idéntico al original.'),('Privacidad','Se usaron rutas relativas. No se incluyen rutas de equipo, nombres de dispositivos, credenciales ni direcciones de sesión de Moodle.')]
    for row,(label,text) in enumerate(notes,4):guide.write(row,0,label,f['head']);guide.merge_range(row,1,row,7,text,f['body']);guide.set_row(row,50 if row not in [4,5] else 25)
    guide.write_url('A19',URL,string='GitHub · Solución completa de la práctica')
    # Importación tipada: las fechas son valores de Excel y los vacíos permanecen vacíos.
    for key,table_name in [('Reclamos','tblReclamos'),('Produccion','tblProduccion'),('Ventas','tblVentas')]:
        rows=data[key];cols=list(rows[0]);ws=sheet(key);ws.freeze_panes(1,1);ws.set_column(0,len(cols)-1,19);ws.set_column(4,5,26)
        columns=[]
        for c in cols:
            col={'header':c}
            if c.startswith('Fecha'):col['format']=f['date']
            if c in ['MesReclamo','MesProduccion']:
                base='FechaReclamo' if key=='Reclamos' else 'Fecha';col['formula']=f'=DATE(YEAR([@{base}]),MONTH([@{base}]),1)';col['format']=f['month']
            columns.append(col)
        ws.add_table(0,0,len(rows),len(cols)-1,{'name':table_name,'columns':columns,'style':'Table Style Medium 2','data':[[row[c] for c in cols] for row in rows]})
        # Override the calculated-column cells to include reliable cached month values.
        for r,row in enumerate(rows,1):
            for j,c in enumerate(cols):
                if c in ['MesReclamo','MesProduccion']:
                    base='FechaReclamo' if key=='Reclamos' else 'Fecha';serial=(row[c]-datetime(1899,12,30)).days
                    ws.write_formula(r,j,f'=DATE(YEAR([@{base}]),MONTH([@{base}]),1)',f['month'],serial)
    datasets={key:{'rows':data[key],'table':'tbl'+key} for key in ['Reclamos','Produccion']}
    pivots=[]
    def aggregate(rows,col,fn):
        vals=[x[col] for x in rows if x[col] is not None]
        return len(vals) if fn=='count' else sum(vals) if fn=='sum' else statistics.mean(vals) if vals else 0
    def pivot(name,source,row,measures,col=None,values=None,colvalues=None):
        rows=data[source];values=values or sorted({x[row] for x in rows});colvalues=colvalues or (sorted({x[col] for x in rows}) if col else [])
        p={'name':name,'source':source,'row':row,'metrics':measures,'values':values,'col':col,'colvalues':colvalues};pivots.append(p);ws=sheet(name,name.replace('_',' '));ws.write('A3','Tabla dinámica nativa · Fuente: tbl'+source,f['note'])
        headers=[row]+(colvalues+['Total general'] if col else [x[0] for x in measures]);ws.write_row(3,0,headers,f['head']);ws.set_row(3,32)
        for r,value in enumerate(values,4):
            ws.write(r,0,value,f['month'] if isinstance(value,datetime) else f['text']);sub=[x for x in rows if x[row]==value]
            for j,item in enumerate(colvalues if col else measures,1):
                subset=[x for x in sub if x[col]==item] if col else sub;measure=measures[0] if col else item;result=aggregate(subset,measure[1],measure[2]);ws.write(r,j,result,f['num'] if measure[2]=='average' else f['int'])
            if col:ws.write(r,len(colvalues)+1,len(sub),f['int'])
        r=len(values)+4;ws.write(r,0,'Total general',f['head'])
        for j,item in enumerate(colvalues if col else measures,1):
            subset=[x for x in rows if x[col]==item] if col else rows;measure=measures[0] if col else item;ws.write(r,j,aggregate(subset,measure[1],measure[2]),f['num'] if measure[2]=='average' else f['int'])
        if col:ws.write(r,len(colvalues)+1,len(rows),f['int'])
        return p
    count=[('Reclamos','ReclamoID','count')]
    cats=sorted(m['categories'],key=lambda k:(-m['categories'][k],k))
    pivot('TD_Categoria','Reclamos','Categoria',count,values=cats)
    pivot('TD_Estado','Reclamos','Estado',count)
    pivot('TD_MesReclamo','Reclamos','MesReclamo',count)
    pivot('TD_RegionPrioridad','Reclamos','Region',count,'Prioridad')
    pivot('TD_KPI_Reclamos','Reclamos','Universo',[('Total reclamos','ReclamoID','count'),('Dias promedio','DiasResolucion','average'),('Satisfaccion promedio','Satisfaccion_1a5','average'),('Con dias','DiasResolucion','count'),('Con satisfaccion','Satisfaccion_1a5','count')])
    sums=[('Planificadas','UnidadesPlanificadas','sum'),('Producidas','UnidadesProducidas','sum'),('Defectuosas','UnidadesDefectuosas','sum')]
    for name,field in [('TD_Planta','Planta'),('TD_Producto','Producto'),('TD_MesProduccion','MesProduccion'),('TD_Turno','Turno'),('TD_KPI_Produccion','Universo')]:pivot(name,'Produccion',field,sums+([('Lotes','LoteID','count')] if name=='TD_KPI_Produccion' else []))
    def gp(pivot_name,measure,field=None,value=None):
        extra=''
        if field:
            val=f'DATE({value.year},{value.month},1)' if isinstance(value,datetime) else '"'+str(value).replace('"','""')+'"'
            extra=f',"{field}",{val}'
        return f'GETPIVOTDATA("{measure}",\'{pivot_name}\'!$A$4{extra})'
    # Resumen con fórmulas de la consigna y contraste contra las TD.
    summary=sheet('Resumen_Reclamos','Resumen global · Reclamos');summary.write_row('A4',['Indicador','Fórmula de tabla','Referencia','TD (vista filtrada)'],f['head'])
    formulas=[('Total','=COUNTA(tblReclamos[ReclamoID])',450,'TD_KPI_Reclamos','Total reclamos'),('Resueltos','=COUNTIF(tblReclamos[Estado],"Resuelto")',318,'TD_Estado','Reclamos'),('Tasa resuelta','=B6/B5',318/450,None,None),('Días promedio','=AVERAGE(tblReclamos[DiasResolucion])',m['days'],'TD_KPI_Reclamos','Dias promedio'),('Satisfacción promedio','=AVERAGE(tblReclamos[Satisfaccion_1a5])',m['satisfaction'],'TD_KPI_Reclamos','Satisfaccion promedio'),('Días con dato','=COUNT(tblReclamos[DiasResolucion])',318,'TD_KPI_Reclamos','Con dias'),('Satisfacción con dato','=COUNT(tblReclamos[Satisfaccion_1a5])',318,'TD_KPI_Reclamos','Con satisfaccion'),('Días vacíos','=COUNTBLANK(tblReclamos[DiasResolucion])',132,None,None),('Satisfacción vacía','=COUNTBLANK(tblReclamos[Satisfaccion_1a5])',132,None,None)]
    for row,(label,formula,val,td,measure) in enumerate(formulas,4):
        fmt=f['pct'] if 'Tasa' in label else f['num'] if 'promedio' in label else f['int'];summary.write(row,0,label,f['text']);summary.write_formula(row,1,formula,fmt,val);summary.write(row,2,val,fmt)
        if td:summary.write_formula(row,3,'=IFERROR('+gp(td,measure,'Estado','Resuelto')+',0)' if label=='Resueltos' else '=IFERROR('+gp(td,measure)+',0)',fmt,val)
    summary.merge_range('A15:H16','Las fórmulas B son globales y no reaccionan a los segmentadores. Los dashboards usan exclusivamente TD compatibles y GETPIVOTDATA. Los promedios omiten vacíos y describen los 318 resueltos con registro.',f['note'])
    resprod=sheet('Resumen_Produccion','Resumen global · Producción');resprod.write_row('A4',['Indicador','Fórmula','Referencia'],f['head'])
    plan,produced,defects=m['totals']
    for row,(label,formula,val,fmt) in enumerate([('Planificadas','=SUM(tblProduccion[UnidadesPlanificadas])',plan,'int'),('Producidas','=SUM(tblProduccion[UnidadesProducidas])',produced,'int'),('Defectuosas','=SUM(tblProduccion[UnidadesDefectuosas])',defects,'int'),('Tasa de defectos','=B7/B6',defects/produced,'pct'),('Cumplimiento del plan','=B6/B5',produced/plan,'pct')],4):
        resprod.write(row,0,label,f['text']);resprod.write_formula(row,1,formula,f[fmt],val);resprod.write(row,2,val,f[fmt])
    resprod.merge_range('A12:H13',f'{m["overplan"]} lotes superan 100 % de cumplimiento; no se truncaron ni eliminaron. El total agregado es {produced/plan:.2%}. La tasa global usa razón de sumas.',f['note'])
    # Dashboard helper cells retain cached formula results and update from native pivots.
    def helper(ws,start,headers,rows):
        ws.write_row(start,0,headers,f['head'])
        for i,row in enumerate(rows,start+1):
            for j,v in enumerate(row):
                if isinstance(v,tuple):ws.write_formula(i,j,v[0],f[v[2]],v[1])
                else:ws.write(i,j,v,f['month'] if isinstance(v,datetime) else f['text'])
        return start+1,start+len(rows)
    def formula(expr,value,fmt='int'):return ('=IFERROR('+expr+',0)',value,fmt)
    def chart(ws,typ,title,block,cols,anchor,unit,stacked=False,percent=False):
        options={'type':typ};options.update({'subtype':'stacked'} if stacked else {})
        ch=book.add_chart(options);first,last=block
        for j,(col,label,color) in enumerate(cols):
            opts={'name':label,'categories':[ws.name,first,0,last,0],'values':[ws.name,first,col,last,col],'fill':{'color':color},'border':{'none':True}}
            if typ=='line':opts.update(line={'color':color,'width':2.5},marker={'type':'circle','size':4})
            ch.add_series(opts)
        ch.set_title({'name':title,'name_font':{'size':12,'color':BLUE}});ch.set_size({'width':720,'height':315});ch.set_chartarea({'border':{'none':True},'fill':{'color':'white'}});ch.set_plotarea({'border':{'none':True}})
        ch.set_legend({'position':'bottom'} if len(cols)>1 else {'none':True})
        axis={'name':unit,'min':0,'major_gridlines':{'visible':True,'line':{'color':'#E7EDF1'}}}
        if percent:axis['num_format']='0.0%'
        if typ=='bar':ch.set_x_axis(axis);ch.set_y_axis({'reverse':True,'num_font':{'size':10}})
        else:ch.set_y_axis(axis);ch.set_x_axis({'num_font':{'size':9}})
        ws.insert_chart(anchor,ch,{'x_offset':4,'y_offset':4})
    def card(ws,idx,label,expr,value,fmt='kint',groups=4):
        width=24//groups;c=idx*width;ws.merge_range(3,c,3,c+width-1,label,f['khead']);ws.merge_range(4,c,6,c+width-1,'',f[fmt]);fallback='"Sin datos"' if fmt in ['knum','kpct'] else '0';ws.write_formula(4,c,'=IFERROR('+expr+','+fallback+')',f[fmt],value)
    dr=sheet('Dashboard_Reclamos',dashboard=True);dr.merge_range('A1:X2','RECLAMOS · Seguimiento de atención',f['title']);dr.merge_range('A3:X3','Vista global inicial · enero 2025–enero 2026 · Filtrar con Region, Categoria y Estado',f['note'])
    card(dr,0,'TOTAL RECLAMOS',gp('TD_KPI_Reclamos','Total reclamos'),450)
    card(dr,1,'RESUELTOS',gp('TD_Estado','Reclamos','Estado','Resuelto'),318)
    card(dr,2,'DÍAS PROMEDIO',gp('TD_KPI_Reclamos','Dias promedio'),m['days'],'knum')
    card(dr,3,'SATISFACCIÓN / 5',gp('TD_KPI_Reclamos','Satisfaccion promedio'),m['satisfaction'],'knum')
    dr.merge_range('A8:X8','Segmentadores conectados a las cinco TD de reclamos. Borrar filtros restaura 450 casos.',f['note'])
    b=helper(dr,65,['Categoria','Reclamos'],[[c,formula(gp('TD_Categoria','Reclamos','Categoria',c),m['categories'][c])] for c in cats]);chart(dr,'bar','Reclamos por categoría · cantidad',b,[(1,'Reclamos',BLUE)],'A20','Cantidad de reclamos')
    states=sorted(m['states']);b=helper(dr,74,['Estado','Reclamos'],[[s,formula(gp('TD_Estado','Reclamos','Estado',s),m['states'][s])] for s in states]);chart(dr,'column','Reclamos por estado · cantidad',b,[(1,'Reclamos',TEAL)],'M20','Cantidad de reclamos')
    b=helper(dr,81,['MesReclamo','Reclamos'],[[d.strftime('%Y-%m'),formula(gp('TD_MesReclamo','Reclamos','MesReclamo',d),n)] for d,n in sorted(m['months'].items())]);chart(dr,'line','Evolución de reclamos · enero 2025–enero 2026',b,[(1,'Reclamos',BLUE)],'A36','Cantidad de reclamos')
    priorities=['Alta','Media','Baja'];regions=sorted({x['Region'] for x in data['Reclamos']});rows=[]
    for region in regions:
        row=[region]
        for priority in priorities:
            expr=gp('TD_RegionPrioridad','Reclamos','Region',region)[:-1]+f',"Prioridad","{priority}")' # append second dimension to GETPIVOTDATA
            row.append(formula(expr,sum(x['Region']==region and x['Prioridad']==priority for x in data['Reclamos'])))
        rows.append(row)
    b=helper(dr,98,['Region']+priorities,rows);chart(dr,'bar','Reclamos por región y prioridad',b,[(1,'Alta',GOLD),(2,'Media',BLUE),(3,'Baja',PURPLE)],'M36','Cantidad de reclamos',True)
    dr.merge_range('A53:X54','Días y satisfacción: solo registros disponibles. Los filtros modifican los gráficos y KPI. No constituyen tasas por ventas.',f['note']);dr.write_url('A56',URL,string='GitHub · Solución y datos originales');dr.merge_range('A58:X58','Fuente: CSV de la práctica UASDVirtual · Industrias Caribe S.A. · Vista académica',f['note'])
    dp=sheet('Dashboard_Produccion',dashboard=True);dp.merge_range('A1:X2','PRODUCCIÓN · Plan, volumen y calidad',f['title']);dp.merge_range('A3:X3','Vista global inicial · año 2025 · Filtrar con Planta, Turno y Producto',f['note'])
    for i,(label,measure,val) in enumerate(zip(['PLANIFICADAS','PRODUCIDAS','DEFECTUOSAS'],['Planificadas','Producidas','Defectuosas'],m['totals'])):card(dp,i,label,gp('TD_KPI_Produccion',measure),val,groups=6)
    card(dp,3,'TASA DEFECTOS',gp('TD_KPI_Produccion','Defectuosas')+'/'+gp('TD_KPI_Produccion','Producidas'),defects/produced,'kpct',groups=6)
    card(dp,4,'CUMPLIMIENTO',gp('TD_KPI_Produccion','Producidas')+'/'+gp('TD_KPI_Produccion','Planificadas'),produced/plan,'kpct',groups=6)
    card(dp,5,'LOTES',gp('TD_KPI_Produccion','Lotes'),1200,groups=6)
    dp.merge_range('A8:X8','Segmentadores conectados a las cinco TD de producción. Todos los KPI y gráficos responden a los filtros; tasas = razón de sumas.',f['note'])
    rows=[[plant]+[formula(gp('TD_Planta',label,'Planta',plant),v) for label,v in zip(['Planificadas','Producidas','Defectuosas'],vals)] for plant,vals in m['plants'].items()]
    b=helper(dp,65,['Planta','Planificadas','Producidas','Defectuosas'],rows);chart(dp,'column','Producción por planta · plan y real',b,[(1,'Planificadas',PURPLE),(2,'Producidas',BLUE)],'A20','Unidades')
    products=sorted(m['products'],key=lambda c:-m['products'][c][2]/m['products'][c][1]);rows=[]
    for product in products:
        vals=m['products'][product];rows.append([product,formula(gp('TD_Producto','Defectuosas','Producto',product)+'/'+gp('TD_Producto','Producidas','Producto',product),vals[2]/vals[1],'pct')])
    b=helper(dp,72,['Producto','Tasa de defectos'],rows);chart(dp,'bar','Tasa de defectos por producto · razón de sumas',b,[(1,'Tasa',GOLD)],'M20','Defectuosas / producidas',percent=True)
    rows=[[d.strftime('%Y-%m'),formula(gp('TD_MesProduccion','Producidas','MesProduccion',d),vals[1])] for d,vals in m['production_months'].items()];b=helper(dp,83,['Mes','Unidades producidas'],rows);chart(dp,'line','Evolución mensual de unidades producidas',b,[(1,'Producidas',BLUE)],'A36','Unidades')
    rows=[[turn]+[formula(gp('TD_Turno',label,'Turno',turn),v) for label,v in zip(['Planificadas','Producidas','Defectuosas'],vals)] for turn,vals in m['shifts'].items()];b=helper(dp,100,['Turno','Planificadas','Producidas','Defectuosas'],rows);chart(dp,'column','Cumplimiento por turno · plan y real',b,[(1,'Planificadas',PURPLE),(2,'Producidas',TEAL)],'M36','Unidades')
    dp.merge_range('A53:X54','Producción incluye unidades defectuosas. 419 lotes superan el plan; el cumplimiento global es 94.72 %. Los defectos se expresan en unidades, sin valoración de desperdicio monetario.',f['note']);dp.write_url('A56',URL,string='GitHub · Solución y datos originales');dp.merge_range('A58:X58','Fuente: CSV de la práctica UASDVirtual · Industrias Caribe S.A. · Vista académica',f['note'])
    validation=sheet('Validacion','Controles de calidad y conciliación');validation.write_row('A4',['Control','Observado','Esperado','Resultado'],f['head']);validation.set_column('A:A',49)
    for row,check in enumerate(checks,4):validation.write_row(row,0,check)
    validation.write(len(checks)+6,0,'Ventas copy.csv no se suma; es copia idéntica del original.',f['note'])
    # Static analytical findings with quantified evidence in a dedicated review sheet.
    findings=sheet('Hallazgos','Hallazgos y recomendaciones');findings.set_column('A:H',18)
    texts=[('Reclamos · hallazgo 1','Empaque lidera con 110/450 = 24.44 %; no es una tasa de fallas por producto.'),('Reclamos · hallazgo 2','318/450 = 70.67 % resueltos; quedan 132 sin resolver: 54 Abierto + 78 En proceso.'),('Reclamos · hallazgo 3',f'Promedio {m["days"]:.2f} días y satisfacción {m["satisfaction"]:.2f}/5, ambos con n=318; 27 casos son de enero 2026.'),('Reclamos · acciones','Revisar empaque con muestreo de recepción y despacho. Priorizar pendientes de alta prioridad y medir antigüedad antes de fijar capacidad.'),('Reclamos · limitación','Los promedios excluyen los casos aún sin resolución; no estiman el tiempo final de todos los reclamos. Sin denominador temporal compatible no se estiman tasas por producto.'),('Producción · hallazgo 1',f'{produced:,}/{plan:,} = {produced/plan:.2%} de cumplimiento; brecha de {plan-produced:,} unidades.'),('Producción · hallazgo 2',f'{defects:,}/{produced:,} = {defects/produced:.2%} defectuosas. Galletas Avena: 3.53 %; Jugo Mango: 3.32 %.'),('Producción · hallazgo 3','Santiago cumple 94.58 % y Santo Domingo 94.86 %; 419/1,200 lotes (34.92 %) superan el 100 %.'),('Producción · acciones','Investigar brechas plan-real por planta y mes. Revisar causas de defectos en Galletas Avena y Refresco Cola, validando mezcla de producto, lote y turno.'),('Producción · limitación','Se agregan unidades de productos diferentes sin ponderar tamaño ni costo. Las diferencias descriptivas no demuestran causas y no valoran desperdicio monetario.')]
    for i,(title,txt) in enumerate(texts,4):findings.merge_range(i*2-4,0,i*2-4,7,title,f['head']);findings.merge_range(i*2-3,0,i*2-3,7,txt,f['body']);findings.set_row(i*2-3,42)
    guide.activate();book.close()
    sheet_ids={name:i+1 for i,name in enumerate(sheets)}
    slicers=[{'source':source,'field':field,'name':prefix+'_'+field,'sheet':dashboard} for source,fields,prefix,dashboard in [('Reclamos',['Region','Categoria','Estado'],'R','Dashboard_Reclamos'),('Produccion',['Planta','Turno','Producto'],'P','Dashboard_Produccion')] for field in fields]
    inject(OUT,datasets,pivots,slicers,sheet_ids)
    print('Libro generado: 10 tablas dinámicas, 6 segmentadores conectados y 8 gráficos.')

if __name__=='__main__':build()
