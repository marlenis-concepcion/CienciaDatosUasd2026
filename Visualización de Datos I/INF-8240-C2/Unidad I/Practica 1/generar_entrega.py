from pathlib import Path
import os
import tempfile
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'visualizacion-matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import LineChart, BarChart, PieChart, Reference
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# Use Matplotlib's bundled fonts so generation works across operating systems.
FONT_DIR = Path(matplotlib.get_data_path()) / 'fonts' / 'ttf'
for name, filename in [('Helvetica', 'DejaVuSans.ttf'), ('Helvetica-Bold', 'DejaVuSans-Bold.ttf'), ('Helvetica-Oblique', 'DejaVuSans-Oblique.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))
from pptx import Presentation
from pptx.util import Inches, Pt

ROOT=Path(__file__).resolve().parent
G=ROOT/'graficos'; G.mkdir(exist_ok=True)
MONTHS=['Enero','Febrero','Marzo','Abril','Mayo','Junio']
SALES=[100,120,120,140,160,260]; CLAIMS=[8,9,9,12,15,25]
CHANNELS=['Página web','Aplicación móvil','Redes sociales','Ventas telefónicas']; VALUES=[100,80,50,30]
SOURCE='Fuente: consigna de Práctica 1, Unidad I, INF-8240-C2. ComercioDigital RD (caso ficticio).'
PALETTE=['#126782','#219EBC','#E9A23B','#7B6BA8']
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.titlesize':15})
def save(name):
    plt.figtext(.03,.015,'Fuente: consigna de la Práctica 1 · ComercioDigital RD (datos ficticios).',fontsize=8,color='#444444')
    plt.tight_layout(rect=(0,.06,1,1)); plt.savefig(G/f'{name}.png',dpi=180); plt.close()
plt.figure(figsize=(9,4.3)); plt.plot(MONTHS,SALES,marker='o',lw=2.5,color=PALETTE[0]); plt.ylim(0,300); plt.ylabel('Ventas (miles de RD$)'); plt.xlabel('Mes (año no especificado)'); plt.title('Junio alcanza 260 mil RD$: +62.5 % frente a mayo'); plt.grid(axis='y',alpha=.2)
for i,v in enumerate(SALES): plt.annotate(str(v),(i,v),xytext=(0,9),textcoords='offset points',ha='center')
save('01_ventas')
plt.figure(figsize=(9,4.3)); plt.barh(CHANNELS,VALUES,color=PALETTE); plt.gca().invert_yaxis(); plt.xlim(0,120); plt.xlabel('Ventas de junio (miles de RD$)'); plt.title('La página web lidera las ventas de junio')
for i,v in enumerate(VALUES): plt.text(v+1,i,f'{v}  ({v/260:.1%})',va='center')
save('02_canales')
plt.figure(figsize=(9,4.8)); plt.pie(VALUES,labels=CHANNELS,autopct='%1.1f%%',colors=PALETTE,startangle=90,wedgeprops={'edgecolor':'white'},textprops={'fontsize':10}); plt.title('Web y aplicación concentran el 69.2 % de junio\nTotal: 260 mil RD$'); save('03_participacion')
plt.figure(figsize=(9,4.3)); plt.scatter(SALES,CLAIMS,s=70,color=PALETTE[0]); plt.xlim(0,300); plt.ylim(0,30); plt.xlabel('Ventas (miles de RD$)'); plt.ylabel('Reclamaciones (cantidad)'); plt.title('Ventas y reclamaciones presentan asociación positiva')
for x,y,label in zip(SALES,CLAIMS,['Enero','Febrero / Marzo','','Abril','Mayo','Junio']):
    if label: plt.annotate(label,(x,y),xytext=(6,6),textcoords='offset points',fontsize=9)
save('04_relacion')

wb=Workbook(); ws=wb.active; ws.title='Datos mensuales'
ws.append(['Mes','Ventas (miles RD$)','Reclamaciones','Variación ventas','Reclamaciones por mil RD$'])
for r,(m,v,c) in enumerate(zip(MONTHS,SALES,CLAIMS),2):
    ws.append([m,v,c,None if r==2 else f'=B{r}/B{r-1}-1',f'=C{r}/B{r}']); ws.cell(r,4).number_format='0.00%'; ws.cell(r,5).number_format='0.0000'
ws.append(['Total','=SUM(B2:B7)','=SUM(C2:C7)'])
ws.append([SOURCE]); ws.append(['La razón reclamaciones/ventas NO es una tasa por pedido: no se dispone del número de pedidos.'])
can=wb.create_sheet('Canales junio'); can.append(['Canal','Ventas (miles RD$)','Participación'])
for r,(c,v) in enumerate(zip(CHANNELS,VALUES),2): can.append([c,v,f'=B{r}/SUM($B$2:$B$5)']); can.cell(r,3).number_format='0.00%'
can.append(['Total','=SUM(B2:B5)','=SUM(C2:C5)']); can.append([SOURCE])
calc=wb.create_sheet('Cálculos'); calc.append(['Indicador','Fórmula Excel','Resultado de referencia','Procedimiento'])
rows=[('Media','=AVERAGE(\'Datos mensuales\'!B2:B7)',150,'900 / 6'),('Mediana','=MEDIAN(\'Datos mensuales\'!B2:B7)',130,'(120 + 140) / 2'),('Moda','=MODE(\'Datos mensuales\'!B2:B7)',120,'120 aparece dos veces'),('Mínimo','=MIN(\'Datos mensuales\'!B2:B7)',100,'Menor valor'),('Máximo','=MAX(\'Datos mensuales\'!B2:B7)',260,'Mayor valor'),('Rango','=MAX(\'Datos mensuales\'!B2:B7)-MIN(\'Datos mensuales\'!B2:B7)',160,'260 - 100'),('Media enero-mayo','=AVERAGE(\'Datos mensuales\'!B2:B6)',128,'640 / 5'),('Crecimiento mayo-junio',"='Datos mensuales'!B7/'Datos mensuales'!B6-1",.625,'(260 - 160) / 160'),('Aumento de media al incluir junio','=B2-B8',22,'150 - 128'),('Crecimiento reclamaciones mayo-junio',"='Datos mensuales'!C7/'Datos mensuales'!C6-1",2/3,'(25 - 15) / 15')]
for row in rows: calc.append(row)
calc.append(['Nota','Los resultados de referencia permiten revisar los valores sin depender del recálculo del visor.'])
for sheet,kind,maxrow in [(ws,LineChart,7),(can,BarChart,5),(can,PieChart,5)]:
    chart=kind(); chart.title='Ventas mensuales (miles RD$)' if sheet==ws else 'Ventas por canal en junio (miles RD$)'; chart.add_data(Reference(sheet,min_col=2,min_row=1,max_row=maxrow),titles_from_data=True); chart.set_categories(Reference(sheet,min_col=1,min_row=2,max_row=maxrow)); sheet.add_chart(chart,'G2' if kind!=PieChart else 'G18')
for sheet in wb:
    sheet.freeze_panes='A2'
    for cell in sheet[1]: cell.fill=PatternFill('solid',fgColor='126782'); cell.font=Font(color='FFFFFF',bold=True)
    for col in sheet.columns:
        sheet.column_dimensions[col[0].column_letter].width= min(65,max(23,max(len(str(c.value or '')) for c in col)+2))
    for row in sheet:
        for cell in row: cell.alignment=Alignment(vertical='top',wrap_text=True)
wb.save(ROOT/'Calculos_Visualizacion_Datos_I.xlsx')

styles=getSampleStyleSheet(); styles.add(ParagraphStyle(name='BodyES',fontName='Helvetica',fontSize=10.5,leading=14,spaceAfter=7)); styles['Title'].textColor=colors.HexColor('#126782')
story=[]
class WholeParagraph(Paragraph):
    def split(self, availWidth, availHeight):
        return []
def p(t): story.append(WholeParagraph(t,styles['BodyES']))
def h(t): story.append(Paragraph(t,styles['Heading2']))
def keep_block(start):
    block=story[start:]
    del story[start:]
    story.append(KeepTogether(block))
def table(rows,widths=None):
    data=[[Paragraph(str(c),styles['BodyES']) for c in row] for row in rows]; t=Table(data,colWidths=widths,repeatRows=1); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E6F1F5')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.3,colors.lightgrey),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7)])); story.append(t); story.append(Spacer(1,10))
def img(name):
    from PIL import Image as PILImage
    with PILImage.open(G/f'{name}.png') as graphic:
        ratio = graphic.height / graphic.width
    story.append(Image(str(G/f'{name}.png'), width=430, height=430*ratio))
def page(): story.append(PageBreak())
# Portada institucional independiente del análisis.
styles.add(ParagraphStyle(name='CoverES',fontName='Helvetica',fontSize=13,leading=21,alignment=1,spaceAfter=13))
def coverline(text): story.append(Paragraph(text,styles['CoverES']))
story.append(Spacer(1,15))
story.append(Image(str(ROOT/'recursos/uasd_logo.png'),width=105,height=125,kind='proportional'))
story.append(Spacer(1,15))
coverline('<b>UNIVERSIDAD AUTÓNOMA DE SANTO DOMINGO</b>')
coverline('UASD · Primada de América')
story.append(Spacer(1,25))
coverline('<b>Visualización de Datos I</b><br/>INF-8240-C2')
story.append(Spacer(1,18))
coverline('<b>Práctica 1</b><br/>Evaluación integral de la Unidad I<br/>Fundamentos de visualización de datos')
coverline('ComercioDigital RD:<br/>análisis de desempeño y recomendaciones para la gerencia')
story.append(Spacer(1,22))
coverline('<b>Presentado por</b><br/>Marlenis Judith Concepción Cuevas')
story.append(Spacer(1,28))
coverline('Santo Domingo, República Dominicana<br/>2 de noviembre de 2026')
page()
story.append(Paragraph('Visualización de Datos I',styles['Title'])); p('Práctica 1. Evaluación integral de la Unidad I'); p('<b>ComercioDigital RD: análisis de desempeño y recomendaciones para la gerencia</b>'); h('Resumen ejecutivo'); p('Las ventas suman 900 mil RD$ durante los seis meses y alcanzan 260 mil RD$ en junio, un 62.5 % más que en mayo. La página web aporta 38.46 % de junio; junto con la aplicación móvil representa 69.23 %. Las reclamaciones suben de 15 a 25 entre mayo y junio. Se recomienda proteger la capacidad de atención en los canales principales e investigar los motivos de las reclamaciones. Los datos son descriptivos: no permiten establecer causas ni garantizar ventas futuras.'); p(SOURCE); h('Datos utilizados'); table([['Mes','Ventas (miles RD$)','Reclamaciones']]+list(zip(MONTHS,SALES,CLAIMS)),[150,170,150]); p('El caso no especifica el año, los pedidos, los clientes ni el tipo de reclamación. No se añaden observaciones externas. Los importes se mantienen en miles de pesos dominicanos.')
h('Parte I · Comprensión y análisis de datos'); h('Actividad 1. Variables y dimensión temporal'); table([['Variable','Clasificación','Dimensión temporal'],['Mes (A)','Categórica ordinal: meses ordenados','Índice temporal mensual; año desconocido'],['Ventas (A y B)','Cuantitativa, medida monetaria de razón','En A cambia por mes; en B corresponde a junio'],['Reclamaciones (A)','Cuantitativa discreta, conteo','Conteo agregado por mes'],['Canal (B)','Categórica nominal','No es temporal; se compara en junio']],[110,205,155]); p('El total de 260 en B es una suma de canales, no un canal adicional. Ambos conjuntos se vinculan por junio y su total de ventas.'); activity_start=len(story); h('Actividad 2. Del dato a la decisión'); p('<b>Dato:</b> en junio se registran 25 reclamaciones.<br/><b>Información:</b> son 10 más que en mayo (15), un aumento de 66.67 %, mientras las ventas crecen 62.5 %.<br/><b>Conocimiento o interpretación contextualizada:</b> el crecimiento de actividad coincide con más reclamaciones. La razón pasa de 0.09375 a 0.09615 reclamaciones por mil RD$; esto sugiere revisar la atención, pero no demuestra deterioro de la calidad porque faltan pedidos, clientes y severidad.<br/><b>Decisión propuesta:</b> clasificar las reclamaciones por motivo y canal y monitorear semanalmente reclamaciones por cada 100 pedidos cuando se disponga de ese denominador.'); keep_block(activity_start); h('Actividad 3. Beneficios y tipos de visualización'); p('1. Facilita la exploración: una línea temporal permite detectar la estabilidad de febrero-marzo y el salto de junio, orientando preguntas para investigar.<br/>2. Mejora la comunicación: una comparación de canales hace visible dónde se concentra el ingreso y ayuda a priorizar recursos con evidencia.<br/>Una visualización estática conserva una vista fija, como los gráficos de este PDF. Una interactiva permite filtrar canales, consultar detalles o cambiar periodos; requiere diseño cuidadoso para evitar comparaciones engañosas.')
h('Parte II · Estadística descriptiva'); h('Actividad 4. Fórmulas y cálculos'); p('Ventas ordenadas: 100, 120, 120, 140, 160 y 260. Número de meses: n = 6. Suma: 100 + 120 + 120 + 140 + 160 + 260 = 900 mil RD$.'); table([['Medida','Fórmula y sustitución','Resultado (miles RD$)'],['Media','Media = suma(x) / n = 900 / 6','150'],['Mediana','Para n par: (x(3) + x(4)) / 2 = (120 + 140) / 2','130'],['Moda','Valor con mayor frecuencia: 120 aparece 2 veces','120'],['Mínimo','min(x) = 100','100'],['Máximo','max(x) = 260','260'],['Rango','max(x) − min(x) = 260 − 100','160']],[80,295,95]); h('Actividad 5. Representatividad de la media'); p('La media de 150 mil RD$ resume correctamente el promedio del semestre, pero describe con limitaciones un mes habitual: cuatro de los seis meses están por debajo de ella y los primeros cinco meses se sitúan entre 100 y 160. La mediana (130) y la moda (120) complementan la descripción del centro.'); p('Sin junio, la media sería (100 + 120 + 120 + 140 + 160) / 5 = 128 mil RD$. Al incluir junio aumenta 22 mil RD$, equivalentes a 22 / 128 × 100 = 17.19 %. Junio ejerce influencia sobre el promedio por su magnitud. Esto no justifica eliminarlo ni declararlo erróneo: es parte de los datos y debe explicarse.')
block_start=len(story); h('Parte III · Construcción e interpretación de gráficos'); h('Actividades 6 y 7. Gráfico de líneas'); img('01_ventas'); p('<b>Pregunta:</b> ¿cómo evolucionaron las ventas entre enero y junio?<br/><b>Elección:</b> las líneas conectan periodos consecutivos y facilitan observar cambios temporales. La escala comienza en cero y los meses tienen separación uniforme.<br/><b>Hallazgo:</b> junio alcanza 260 mil RD$, frente a 160 en mayo: +100 mil RD$ (+62.5 %). Febrero y marzo mantienen 120.<br/><b>Limitación:</b> solo hay seis agregados mensuales; no muestra variación diaria, estacionalidad anual ni causas del crecimiento.'); keep_block(block_start); block_start=len(story); h('Gráfico de barras'); img('02_canales'); p('<b>Pregunta:</b> ¿qué canal vendió más en junio y cuánto difieren los canales?<br/><b>Elección:</b> las longitudes desde cero permiten comparar categorías con precisión; las barras horizontales facilitan leer los nombres.<br/><b>Hallazgo:</b> la página web lidera con 100 mil RD$, 20 mil más que la aplicación móvil.<br/><b>Limitación:</b> muestra un solo mes y ventas brutas; no informa sobre rentabilidad, costos o evolución por canal.'); keep_block(block_start);
block_start=len(story); h('Gráfico circular'); img('03_participacion'); table([['Canal','Ventas (miles RD$)','Participación'], *[[c,v,f'{v}/260 × 100 = {v/260*100:.2f} %'] for c,v in zip(CHANNELS,VALUES)],['Total',260,'100 %']],[165,125,180]); p('<b>Pregunta:</b> ¿qué proporción de las ventas de junio representa cada canal?<br/><b>Elección:</b> hay cuatro categorías que componen un total conocido; el circular comunica la relación parte-todo.<br/><b>Hallazgo:</b> web y aplicación suman 180 / 260 × 100 = 69.23 %.<br/><b>Limitación:</b> los ángulos se comparan con menor precisión que las barras. El gráfico no muestra cambios temporales; los porcentajes redondeados de las etiquetas pueden sumar 99.9 %.'); keep_block(block_start); block_start=len(story); h('Actividad 8. Relación entre ventas y reclamaciones'); p('Usaría un diagrama de dispersión, con ventas en el eje X y reclamaciones en el eje Y, identificando cada mes. Permite explorar dirección, concentración y posibles observaciones influyentes. Febrero y marzo comparten coordenadas (120, 9), por lo que deben identificarse juntos.'); img('04_relacion'); p('Se observa asociación positiva: los meses con más ventas también presentan más reclamaciones. Solo hay seis observaciones y junio tiene gran influencia. La coincidencia no demuestra que una variable provoque la otra: podrían intervenir el volumen de pedidos, campañas, cambios de canal, demoras u otros factores no medidos. La tendencia temporal compartida también puede producir asociación. Para estudiar causas harían falta datos adicionales y un diseño de investigación adecuado.'); keep_block(block_start); h('Parte IV · Interpretación crítica y comunicación'); h('Actividad 9. Evaluación de afirmaciones'); table([['Afirmación','Clasificación y justificación'],['A. Junio superó a enero','Sustentada. 260 > 100 mil RD$; diferencia de 160 mil RD$ y aumento de 160 %.'],['B. La aplicación móvil fue el mayor canal','No sustentada. La web registró 100 y la aplicación 80 mil RD$.'],['C. Las reclamaciones provocaron el aumento de ventas','No sustentada. Hay asociación descriptiva, sin evidencia de causalidad ni control de otras variables.'],['D. Las ventas aumentaron o se mantuvieron entre meses','Sustentada. Diferencias consecutivas: +20, 0, +20, +20 y +100 mil RD$.'],['E. Junio garantiza aumentos en julio','No sustentada. Julio no está observado y seis meses no garantizan una tendencia futura.']],[180,290])
h('Parte V · Storytelling con datos'); p('Actividad 10. Presentación de cuatro diapositivas. A continuación se presentan las cuatro diapositivas; también se incluye su versión PowerPoint editable.');
slides=[('1 · Contexto','Las ventas crecen; la gerencia necesita decidir cómo sostener la operación',None,'ComercioDigital RD · Caso ficticio de comercio electrónico.\nPregunta principal: ¿cómo evolucionaron las ventas, qué canales contribuyen en junio y qué señales requieren atención?\nAlcance: enero-junio; ventas, reclamaciones y canales de junio. Total semestral: 900 mil RD$.'),('2 · Evidencia','Junio crece 62.5 % respecto a mayo','01_ventas','Junio: 260 mil RD$; mayo: 160 mil RD$. Diferencia: 100 mil RD$.\nFebrero y marzo se mantienen en 120 mil RD$. El salto de junio requiere contexto; no permite predecir julio.'),('3 · Análisis','Web y aplicación aportan 69.2 %; las reclamaciones llegan a 25','02_canales','Web: 38.46 % · Aplicación: 30.77 % · Redes: 19.23 % · Teléfono: 11.54 %.\nReclamaciones: 8 → 9 → 9 → 12 → 15 → 25 (enero-junio).\nMayo-junio: +66.67 %. La razón por mil RD$ pasa de 0.09375 a 0.09615; no equivale a reclamaciones por pedido.'),('4 · Recomendación','Priorizar capacidad y medir la calidad antes de ampliar recursos',None,'1. Revisar capacidad de atención y disponibilidad en web y aplicación: concentran 180 de los 260 mil RD$ de junio. Usar esa evidencia para planificar cobertura; validar costos antes de elevar inversión.\n2. Clasificar reclamaciones por motivo y canal y registrar pedidos; revisar semanalmente reclamaciones por 100 pedidos y tiempo de resolución. Fundamento: suben de 15 a 25 en mayo-junio.\nLimitación: seis meses, sin pedidos, costos ni campañas; no se atribuyen causas ni se garantiza crecimiento.')]
prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
for tag,title,graph,body in slides:
    slide_start=len(story)
    p(tag); story.append(Paragraph(title,styles['Title']))
    if graph: img(graph)
    for text in body.split('\n'): p(text)
    p(SOURCE)
    keep_block(slide_start)
    slide=prs.slides.add_slide(prs.slide_layouts[6])
    def textbox(x,y,w,hh,text,size,color='#183B4E'):
        box=slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(hh)); tf=box.text_frame; tf.word_wrap=True
        for i,line in enumerate(text.split('\n')):
            para=tf.paragraphs[0] if i==0 else tf.add_paragraph(); para.text=line; para.font.size=Pt(size); para.font.color.rgb=__import__('pptx').dml.color.RGBColor.from_string(color.lstrip('#')); para.space_after=Pt(14)
    textbox(.5,.15,12.3,.4,tag,15); textbox(.5,.65,12.3,1.05,title,28)
    if graph:
        slide.shapes.add_picture(str(G/f'{graph}.png'), Inches(.4), Inches(1.85),width=Inches(7.7)); textbox(8.3,1.9,4.5,4.7,body,20)
    else: textbox(.7,2,11.8,4.5,body,23)
    textbox(.5,7,12.3,.4,SOURCE,10)
prs.save(ROOT/'Presentacion_Visualizacion_Datos_I.pptx')
reflection_start=len(story); h('Parte VI · Reflexión final'); h('Actividad 11. Reflexión (menos de 200 palabras)'); p('Un profesional de Ciencia de Datos debe comprender la visualización y la comunicación porque un gráfico automático no garantiza una interpretación correcta. La herramienta puede dibujar barras o líneas, pero no decide por sí sola si las variables, la escala y el contexto responden a la pregunta empresarial. Una escala recortada puede exagerar diferencias; un promedio puede ocultar un mes excepcional; y dos variables que crecen juntas no necesariamente mantienen una relación causal.'); p('Comprender estos principios permite revisar unidades, identificar limitaciones y escoger representaciones adecuadas para la audiencia. También ayuda a distinguir entre describir lo observado y anticipar lo que podría ocurrir. En ComercioDigital RD, el aumento de ventas y reclamaciones exige investigar, pero no demuestra que uno cause el otro.'); p('Comunicar bien implica explicar qué sabemos, qué falta y qué decisión puede apoyarse en la evidencia disponible. Las herramientas automáticas agilizan el trabajo; el criterio profesional sigue siendo necesario para convertir sus resultados en mensajes claros, responsables y útiles.'); keep_block(reflection_start); h('Fuente y trazabilidad'); p('UASDVirtual. (s. f.). <i>Práctica 1. Evaluación integral de la Unidad I: Fundamentos de visualización de datos</i> [Consigna de actividad, INF-8240-C2]. Texto facilitado por la estudiante. Todos los datos y cálculos proceden de esta consigna.'); p('El Excel adjunto contiene datos originales, fórmulas editables, resultados de referencia y gráficos. El script generar_entrega.py reproduce los archivos. Trabajo preparado con apoyo de IA; corresponde a la estudiante revisar los resultados y su interpretación antes de entregar.');
def footer(canvas,doc):
    if doc.page == 1:
        return
    canvas.setFont('Helvetica',8); canvas.drawString(48,25,'INF-8240-C2 · Práctica 1 · Marlenis Judith Concepción Cuevas'); canvas.drawRightString(560,25,str(doc.page - 1))
SimpleDocTemplate(str(ROOT/'Entrega_Visualizacion_Datos_I.pdf'),rightMargin=48,leftMargin=48,topMargin=40,bottomMargin=45).build(story,onFirstPage=footer,onLaterPages=footer)
print('PDF, Excel, PowerPoint y cuatro gráficos generados correctamente.')
