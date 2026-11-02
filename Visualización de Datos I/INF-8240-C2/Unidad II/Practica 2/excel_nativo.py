"""Partes OOXML de tablas dinámicas y segmentadores (MS-XLSX, Office 2010+).
Se ejecuta al final: no volver a guardar el resultado con openpyxl, que no conserva slicers.
"""
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from openpyxl.utils import get_column_letter

NS='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
REL='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKG='http://schemas.openxmlformats.org/package/2006/relationships'
X14='http://schemas.microsoft.com/office/spreadsheetml/2009/9/main'
DRAW='http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
SLE='http://schemas.microsoft.com/office/drawing/2010/slicer'
MC='http://schemas.openxmlformats.org/markup-compatibility/2006'
CT='http://schemas.openxmlformats.org/package/2006/content-types'

def node(parent,tag,ns=NS,**attrs):
    return E.SubElement(parent,f'{{{ns}}}{tag}',{k:str(v) for k,v in attrs.items()})
def xml(root): return E.tostring(root,encoding='UTF-8',xml_declaration=True,standalone=True)
def unique(rows,col):
    return sorted(set(x[col] for x in rows),key=lambda v:(v is None,str(v)))
def relation(root,target,kind):
    rid='rId'+str(max([int(x.get('Id')[3:]) for x in root]+[0])+1)
    node(root,'Relationship',PKG,Id=rid,Type=kind,Target=target);return rid

def inject(path,datasets,pivots,slicers,sheet_ids):
    with ZipFile(path) as z: parts={n:z.read(n) for n in z.namelist()}
    types=E.fromstring(parts['[Content_Types].xml'])
    def content(name,typ):node(types,'Override',CT,PartName='/'+name,ContentType=typ)
    def relationships(name):
        return E.fromstring(parts[name]) if name in parts else E.Element(f'{{{PKG}}}Relationships',nsmap={None:PKG})
    workbook=E.fromstring(parts['xl/workbook.xml']);wr=relationships('xl/_rels/workbook.xml.rels')
    caches=E.Element(f'{{{NS}}}pivotCaches')
    # pivotCaches appears before calcPr in the base schema.
    idx=next((i for i,c in enumerate(workbook) if E.QName(c).localname in ['calcPr','extLst']),len(workbook));workbook.insert(idx,caches)
    shared={}
    for cache_id,(key,info) in enumerate(datasets.items(),1):
        rows,table=info['rows'],info['table'];cols=list(rows[0]);shared[key]={c:unique(rows,c) for c in cols};info['id']=cache_id
        cache=E.Element(f'{{{NS}}}pivotCacheDefinition',nsmap={None:NS,'r':REL},attrib={f'{{{REL}}}id':'rId1','recordCount':str(len(rows)),'saveData':'1','refreshOnLoad':'0','enableRefresh':'1','createdVersion':'6','refreshedVersion':'6','minRefreshableVersion':'3'})
        source=node(cache,'cacheSource',type='worksheet');node(source,'worksheetSource',name=table,sheet=key)
        fields=node(cache,'cacheFields',count=len(cols))
        for c in cols:
            field=node(fields,'cacheField',name=c,numFmtId='0',serverField='0');vals=shared[key][c];available=[v for v in vals if v is not None]
            is_date=available and isinstance(available[0],datetime);is_num=available and isinstance(available[0],(int,float))
            attrs=dict(count=len(vals),containsBlank=int(None in vals),containsString=int(not is_date and not is_num),containsNumber=int(bool(is_num)),containsDate=int(bool(is_date)),containsNonDate=int(not is_date),containsMixedTypes='0',containsSemiMixedTypes=int(None in vals))
            if is_date:field.set('numFmtId','14')
            if is_num:attrs.update(minValue=min(available),maxValue=max(available),containsInteger=int(all(float(v).is_integer() for v in available)))
            items=node(field,'sharedItems',**attrs)
            for val in vals:
                if val is None:node(items,'m')
                elif isinstance(val,datetime):node(items,'d',v=val.isoformat(timespec='seconds'))
                elif isinstance(val,(int,float)):node(items,'n',v=val)
                else:node(items,'s',v=val)
        extlist=node(cache,'extLst');ext=node(extlist,'ext',uri='{725AE2AE-9491-48BE-B2B4-4EB974FC3084}');node(ext,'pivotCacheDefinition',X14,pivotCacheId=cache_id)
        rec=E.Element(f'{{{NS}}}pivotCacheRecords',nsmap={None:NS},count=str(len(rows)))
        maps={c:{v:i for i,v in enumerate(shared[key][c])} for c in cols}
        for row in rows:
            record=node(rec,'r')
            for c in cols:node(record,'x',v=maps[c][row[c]])
        name=f'xl/pivotCache/pivotCacheDefinition{cache_id}.xml';parts[name]=xml(cache);content(name,'application/vnd.openxmlformats-officedocument.spreadsheetml.pivotCacheDefinition+xml')
        name=f'xl/pivotCache/pivotCacheRecords{cache_id}.xml';parts[name]=xml(rec);content(name,'application/vnd.openxmlformats-officedocument.spreadsheetml.pivotCacheRecords+xml')
        cr=E.Element(f'{{{PKG}}}Relationships',nsmap={None:PKG});relation(cr,f'pivotCacheRecords{cache_id}.xml',REL+'/pivotCacheRecords');parts[f'xl/pivotCache/_rels/pivotCacheDefinition{cache_id}.xml.rels']=xml(cr)
        rid=relation(wr,f'pivotCache/pivotCacheDefinition{cache_id}.xml',REL+'/pivotCacheDefinition');node(caches,'pivotCache',cacheId=cache_id,**{f'{{{REL}}}id':rid})
    for i,p in enumerate(pivots,1):
        key=p['source'];cols=list(datasets[key]['rows'][0]);ridf=p['row'];colf=p.get('col');measures=p['metrics'];rvalues=p['values'];cvalues=p.get('colvalues',[])
        pivot=E.Element(f'{{{NS}}}pivotTableDefinition',nsmap={None:NS,'r':REL},name=p['name'],cacheId=str(datasets[key]['id']),dataCaption='Valores',grandTotalCaption='Total general',rowHeaderCaption=ridf,createdVersion='6',updatedVersion='6',minRefreshableVersion='3',compact='0',compactData='0',outline='0',gridDropZones='0',rowGrandTotals='1',colGrandTotals='1',showCalcMbrs='1',useAutoFormatting='1',applyNumberFormats='1',errorCaption='0',showError='1')
        ncols=1+(len(cvalues) if colf else len(measures));height=2+len(rvalues)
        node(pivot,'location',ref=f'A4:{get_column_letter(ncols)}{3+height}',firstHeaderRow='0',firstDataRow='1',firstDataCol='1')
        pf=node(pivot,'pivotFields',count=len(cols))
        for c in cols:
            attrs={'showAll':'1','defaultSubtotal':'0','sortType':'manual'}
            if c==ridf:
                attrs['axis']='axisRow'
                if isinstance(rvalues[0],datetime):attrs['numFmtId']='14'
            if c==colf:attrs['axis']='axisCol'
            if c in [m[1] for m in measures]:attrs['dataField']='1'
            field=node(pf,'pivotField',**attrs)
            # Items are cache indices; use the materialized row order for manual sorting.
            vals=(rvalues if c==ridf else cvalues if c==colf else shared[key][c])
            if c not in [m[1] for m in measures] or c in [ridf,colf]:
                it=node(field,'items',count=len(vals)+(1 if c in [ridf,colf] else 0))
                for value in vals:node(it,'item',x=shared[key][c].index(value))
                if c in [ridf,colf]:node(it,'item',t='default')
        rf=node(pivot,'rowFields',count='1');node(rf,'field',x=cols.index(ridf))
        ri=node(pivot,'rowItems',count=len(rvalues)+1)
        for j in range(len(rvalues)):
            it=node(ri,'i');node(it,'x',v=j)
        it=node(ri,'i',t='grand');node(it,'x')
        cf=node(pivot,'colFields',count='1');node(cf,'field',x=cols.index(colf) if colf else '-2')
        ci=node(pivot,'colItems',count=len(cvalues)+1 if colf else len(measures))
        if colf:
            for j in range(len(cvalues)):
                it=node(ci,'i');node(it,'x',v=j)
            it=node(ci,'i',t='grand');node(it,'x')
            # Add total column to the native range.
            pivot.find(f'{{{NS}}}location').set('ref',f'A4:{get_column_letter(ncols+1)}{3+height}')
        else:
            for j in range(len(measures)):
                it=node(ci,'i',i=j);node(it,'x',v=j)
        df=node(pivot,'dataFields',count=len(measures))
        for caption,c,fn in measures:node(df,'dataField',name=caption,fld=cols.index(c),subtotal=fn,baseField='0',baseItem='0',numFmtId='2' if fn=='average' else '3')
        node(pivot,'pivotTableStyleInfo',name='PivotStyleMedium9',showRowHeaders='1',showColHeaders='1',showRowStripes='1',showColStripes='0',showLastColumn='1')
        pr=E.Element(f'{{{PKG}}}Relationships',nsmap={None:PKG});relation(pr,f'../pivotCache/pivotCacheDefinition{datasets[key]["id"]}.xml',REL+'/pivotCacheDefinition');parts[f'xl/pivotTables/_rels/pivotTable{i}.xml.rels']=xml(pr)
        name=f'xl/pivotTables/pivotTable{i}.xml';parts[name]=xml(pivot);content(name,'application/vnd.openxmlformats-officedocument.spreadsheetml.pivotTable+xml')
        sheet_id=sheet_ids[p['name']];sheetname=f'xl/worksheets/sheet{sheet_id}.xml';srname=f'xl/worksheets/_rels/sheet{sheet_id}.xml.rels';sr=relationships(srname);sheet=E.fromstring(parts[sheetname]);pt=sheet.find(f'{{{NS}}}pivotParts')
        if pt is None:pt=node(sheet,'pivotParts',count='1')
        rid=relation(sr,f'../pivotTables/pivotTable{i}.xml',REL+'/pivotTable');node(pt,'pivotPart',**{f'{{{REL}}}id':rid});parts[sheetname]=xml(sheet);parts[srname]=xml(sr)
    # Native slicer caches are connected to every compatible PivotTable.
    extlist=workbook.find(f'{{{NS}}}extLst')
    if extlist is None:extlist=node(workbook,'extLst')
    ext=node(extlist,'ext',uri='{BBE1A952-AA13-448E-AADC-164F8A28A991}')
    scl=node(ext,'slicerCaches',X14)
    bysheet={}
    for i,sl in enumerate(slicers,1):
        key=sl['source'];field=sl['field'];name=sl['name'];cache_name='SlicerCache_'+name
        sc=E.Element(f'{{{X14}}}slicerCacheDefinition',nsmap={None:X14},name=cache_name,sourceName=field)
        pts=node(sc,'pivotTables',X14)
        for p in pivots:
            if p['source']==key:node(pts,'pivotTable',X14,tabId=sheet_ids[p['name']],name=p['name'])
        data=node(sc,'data',X14);tab=node(data,'tabular',X14,pivotCacheId=datasets[key]['id'],sortOrder='ascending',customListSort='0',showMissing='1',crossFilter='showItemsWithDataAtTop');items=node(tab,'items',X14,count=len(shared[key][field]))
        for j in range(len(shared[key][field])):node(items,'i',X14,x=j,s='1',nd='0')
        fname=f'xl/slicerCaches/slicerCache{i}.xml';parts[fname]=xml(sc);content(fname,'application/vnd.ms-excel.slicerCache+xml')
        rid=relation(wr,f'slicerCaches/slicerCache{i}.xml','http://schemas.microsoft.com/office/2007/relationships/slicerCache');node(scl,'slicerCache',X14,**{f'{{{REL}}}id':rid})
        bysheet.setdefault(sl['sheet'],[]).append((sl,cache_name))
    for num,(sheet_name,entries) in enumerate(bysheet.items(),1):
        sid=sheet_ids[sheet_name];sheetname=f'xl/worksheets/sheet{sid}.xml';srname=f'xl/worksheets/_rels/sheet{sid}.xml.rels';sheet=E.fromstring(parts[sheetname]);sr=relationships(srname)
        sls=E.Element(f'{{{X14}}}slicers',nsmap={None:X14})
        for sl,cachename in entries:node(sls,'slicer',X14,name=sl['name'],cache=cachename,caption=sl['field'],rowHeight='228600',style='SlicerStyleLight2',columnCount='1',showCaption='1')
        fname=f'xl/slicers/slicer{num}.xml';parts[fname]=xml(sls);content(fname,'application/vnd.ms-excel.slicer+xml')
        rid=relation(sr,f'../slicers/slicer{num}.xml','http://schemas.microsoft.com/office/2007/relationships/slicer')
        exts=sheet.find(f'{{{NS}}}extLst')
        if exts is None:exts=node(sheet,'extLst')
        ext=node(exts,'ext',uri='{A8765BA9-456A-4DAB-B4F3-ACF838C121DE}');refs=node(ext,'slicerList',X14);node(refs,'slicer',X14,**{f'{{{REL}}}id':rid})
        draw_id=sheet.find(f'{{{NS}}}drawing').get(f'{{{REL}}}id');target=next(x.get('Target') for x in sr if x.get('Id')==draw_id);drawname='xl/'+target.replace('../','');drawing=E.fromstring(parts[drawname])
        for j,(sl,cachename) in enumerate(entries):
            anc=node(drawing,'twoCellAnchor',DRAW)
            for label,col,row in [('from',j*8,8),('to',(j+1)*8,18)]:
                marker=node(anc,label,DRAW)
                for k,v in [('col',col),('colOff',0),('row',row),('rowOff',0)]:node(marker,k,DRAW).text=str(v)
            alt=node(anc,'AlternateContent',MC);choice=E.SubElement(alt,f'{{{MC}}}Choice',Requires='sle',nsmap={'sle':SLE})
            gf=node(choice,'graphicFrame',DRAW,macro='');nv=node(gf,'nvGraphicFramePr',DRAW);node(nv,'cNvPr',DRAW,id=100+j,name=sl['name']);node(nv,'cNvGraphicFramePr',DRAW)
            transform=node(gf,'xfrm',DRAW);node(transform,'off',A,x='0',y='0');node(transform,'ext',A,cx='0',cy='0')
            graphic=node(gf,'graphic',A);gd=node(graphic,'graphicData',A,uri=SLE);node(gd,'slicer',SLE,name=sl['name'])
            # Fallback for viewers without Excel slicer support.
            fallback=node(alt,'Fallback',MC);shape=node(fallback,'sp',DRAW);nv=node(shape,'nvSpPr',DRAW);node(nv,'cNvPr',DRAW,id=200+j,name='Compatibilidad '+sl['name']);node(nv,'cNvSpPr',DRAW);sp=node(shape,'spPr',DRAW);geom=node(sp,'prstGeom',A,prst='rect');node(geom,'avLst',A)
            tx=node(shape,'txBody',DRAW);node(tx,'bodyPr',A);node(tx,'lstStyle',A);pp=node(tx,'p',A);rr=node(pp,'r',A);node(rr,'t',A).text=sl['field']+' · Abrir en Excel para usar este segmentador.'
            node(anc,'clientData',DRAW)
        parts[drawname]=xml(drawing);parts[sheetname]=xml(sheet);parts[srname]=xml(sr)
    parts['xl/workbook.xml']=xml(workbook);parts['xl/_rels/workbook.xml.rels']=xml(wr);parts['[Content_Types].xml']=xml(types)
    with ZipFile(path,'w',ZIP_DEFLATED) as z:
        for name,data in parts.items():z.writestr(name,data)
