"""Versión Word editable a partir del mismo contenido del informe PDF."""
from pathlib import Path
from html.parser import HTMLParser
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
import datos
from datos import ROOT,load,audit,metrics
from generar_excel import URL,BLUE

OUT=ROOT/'Informe_Unidad_II_IndustriasCaribe.docx'

class Inline(HTMLParser):
    def __init__(self,paragraph):
        super().__init__();self.p=paragraph;self.bold=False;self.italic=False;self.underline=False;self.href=None
    def handle_starttag(self,tag,attrs):
        if tag=='b':self.bold=True
        if tag=='i':self.italic=True
        if tag=='u':self.underline=True
        if tag=='br':self.p.add_run().add_break()
        if tag=='link':self.href=dict(attrs).get('href')
    def handle_endtag(self,tag):
        if tag=='b':self.bold=False
        if tag=='i':self.italic=False
        if tag=='u':self.underline=False
        if tag=='link':self.href=None
    def handle_data(self,text):
        if self.href:
            element=OxmlElement('w:hyperlink');element.set(qn('r:id'),self.p.part.relate_to(self.href,RT.HYPERLINK,is_external=True))
            run=OxmlElement('w:r');pr=OxmlElement('w:rPr');color=OxmlElement('w:color');color.set(qn('w:val'),'126782');pr.append(color);u=OxmlElement('w:u');u.set(qn('w:val'),'single');pr.append(u);run.append(pr);t=OxmlElement('w:t');t.text=text;run.append(t);element.append(run);self.p._p.append(element)
        else:
            r=self.p.add_run(text);r.bold=self.bold;r.italic=self.italic;r.underline=self.underline

def inline(paragraph,text):Inline(paragraph).feed(text)
def xmlprop(parent,name,**attrs):
    e=OxmlElement(name)
    for k,v in attrs.items():e.set(qn(k),str(v))
    parent.append(e);return e

def build():
    # Accept both the original shared-data location and the student's Unit II folder.
    if not (datos.SUBJECT/'IndustriasCaribe_Reclamos.csv').exists():datos.SUBJECT=datos.SUBJECT/'Unidad II'
    data=load();audit(data);m=metrics(data);plan,produced,defects=m['totals']
    story=[]
    def p(text):story.append(('p',text))
    def h(text):story.append(('h',text))
    def image(name):story.append(('image',name))
    def table(rows,widths):story.append(('table',rows,widths))
    def keep(start):
        items=story[start:];del story[start:];story.append(('group',items))
    source=(ROOT/'generar_informe.py').read_text();begin=source.index("    h('Informe gerencial");end=source.index('    def footer(',begin)
    import textwrap
    exec(compile(textwrap.dedent(source[begin:end]),'contenido_del_informe','exec'),{'ROOT':ROOT,'URL':URL,'BLUE':BLUE,'data':data,'m':m,'plan':plan,'produced':produced,'defects':defects,'story':story,'p':p,'h':h,'image':image,'table':table,'keep':keep})
    doc=Document();doc.core_properties.author='Marlenis Judith Concepción Cuevas';doc.core_properties.last_modified_by='';doc.core_properties.title='Práctica Unidad II · Industrias Caribe S.A.';doc.core_properties.subject='Visualización de Datos I · INF-8240-C2'
    normal=doc.styles['Normal'];normal.font.name='DejaVu Sans';normal.font.size=Pt(10);normal.paragraph_format.line_spacing=Pt(14);normal.paragraph_format.space_after=Pt(7);normal.paragraph_format.widow_control=True;normal.paragraph_format.keep_together=True
    heading=doc.styles['Heading 1'];heading.font.name='DejaVu Sans';heading.font.size=Pt(13);heading.font.color.rgb=RGBColor.from_string('126782');heading.paragraph_format.space_before=Pt(12);heading.paragraph_format.space_after=Pt(8);heading.paragraph_format.keep_with_next=True
    def section_setup(sec):
        sec.page_width=Pt(595.28);sec.page_height=Pt(841.89);sec.left_margin=sec.right_margin=Pt(45);sec.top_margin=Pt(35);sec.bottom_margin=Pt(42);sec.footer_distance=Pt(19)
    section_setup(doc.sections[0])
    def cover(text,after=14,size=13):
        pp=doc.add_paragraph();pp.alignment=WD_ALIGN_PARAGRAPH.CENTER;pp.paragraph_format.space_after=Pt(after);pp.paragraph_format.line_spacing=Pt(21);inline(pp,text)
        for r in pp.runs:r.font.size=Pt(size)
    logo=ROOT.parents[1]/'Unidad I/Practica 1/recursos/uasd_logo.png'
    pp=doc.add_paragraph();pp.alignment=WD_ALIGN_PARAGRAPH.CENTER;pp.paragraph_format.space_before=Pt(15);pp.paragraph_format.space_after=Pt(16);pp.paragraph_format.line_spacing=1;pp.add_run().add_picture(str(logo),width=Pt(100),height=Pt(120))
    cover('<b>UNIVERSIDAD AUTÓNOMA DE SANTO DOMINGO</b>');cover('UASD · Primada de América',after=34)
    cover('<b>Visualización de Datos I</b><br/>INF-8240-C2');cover('<b>Práctica Unidad II</b><br/>Creación y análisis de gráficas<br/>Industrias Caribe S.A.',after=34)
    cover('<b>Presentado por</b><br/>Marlenis Judith Concepción Cuevas',after=39);cover('Santo Domingo, República Dominicana<br/>2 de noviembre de 2026')
    sec=doc.add_section(WD_SECTION.NEW_PAGE);section_setup(sec);sec.footer.is_linked_to_previous=False
    xmlprop(sec._sectPr,'w:pgNumType',**{'w:start':'1'})
    footer=sec.footer.paragraphs[0];footer.paragraph_format.space_after=Pt(0);footer.add_run('INF-8240-C2 · Unidad II · Marlenis Judith Concepción Cuevas\t');footer.paragraph_format.tab_stops.add_tab_stop(Pt(505),WD_ALIGN_PARAGRAPH.RIGHT)
    fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
    for r in footer.runs:r.font.size=Pt(7)
    def append(item):
        kind=item[0]
        if kind=='p':inline(doc.add_paragraph(),item[1])
        elif kind=='h':doc.add_paragraph(item[1],style='Heading 1')
        elif kind=='image':
            pp=doc.add_paragraph();pp.alignment=WD_ALIGN_PARAGRAPH.CENTER;pp.paragraph_format.space_after=Pt(0);pp.paragraph_format.line_spacing=1;pp.add_run().add_picture(str(ROOT/'graficos'/f'{item[1]}.png'),width=Pt(455))
        elif kind=='table':
            rows,widths=item[1:];t=doc.add_table(rows=0,cols=len(widths));t.autofit=False;t.alignment=0
            for c,w in zip(t.columns,widths):c.width=Pt(w)
            for i,row in enumerate(rows):
                cells=t.add_row().cells
                for j,(c,value) in enumerate(zip(cells,row)):
                    c.width=Pt(widths[j]);tcpr=c._tc.get_or_add_tcPr();borders=xmlprop(tcpr,'w:tcBorders')
                    for side in ['top','left','bottom','right']:xmlprop(borders,'w:'+side,**{'w:val':'single','w:sz':'3','w:color':'D1DDE3'})
                    margins=xmlprop(tcpr,'w:tcMar');xmlprop(margins,'w:top',**{'w:w':'100','w:type':'dxa'});xmlprop(margins,'w:bottom',**{'w:w':'100','w:type':'dxa'})
                    if i==0:xmlprop(tcpr,'w:shd',**{'w:fill':'E6F1F5'})
                    pp=c.paragraphs[0];pp.paragraph_format.space_after=Pt(2);pp.paragraph_format.line_spacing=Pt(12);pp.paragraph_format.keep_with_next=i<len(rows)-1;inline(pp,str(value))
                    for run in pp.runs:run.font.size=Pt(9)
                trpr=t.rows[-1]._tr.get_or_add_trPr();xmlprop(trpr,'w:cantSplit')
                if i==0:xmlprop(trpr,'w:tblHeader')
            pp=doc.add_paragraph();pp.paragraph_format.space_after=Pt(0);pp.paragraph_format.line_spacing=Pt(5);pp.add_run().font.size=Pt(1)
        elif kind=='group':
            offset=len(doc._element.body)
            for child in item[1]:append(child)
            new=list(doc._element.body)[max(0,offset-1):-1];paragraphs=[pp for e in new for pp in e.iter(qn('w:p'))]
            for pp in paragraphs[:-1]:
                pr=pp.find(qn('w:pPr'))
                if pr is None:pr=OxmlElement('w:pPr');pp.insert(0,pr)
                xmlprop(pr,'w:keepNext')
    for item in story:append(item)
    doc.save(OUT);print('Word editable creado con portada, tablas, ocho gráficos y enlace GitHub.')

if __name__=='__main__':build()
