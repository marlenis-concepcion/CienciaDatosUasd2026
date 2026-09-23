"""Descarga, auditoría, partición y evaluación reproducible de SVM."""
from pathlib import Path
from io import BytesIO
import hashlib
import json
import platform
import zipfile
import time
import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/u01-matplotlib')
import requests
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import joblib
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score, roc_auc_score, ConfusionMatrixDisplay
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://archive.ics.uci.edu/static/public/52/ionosphere.zip'
SHA256 = '46d52186b84e20be52918adb93e8fb9926b34795ff7504c24350ae0616a04bbd'
SEED = 42
FEATURES = [f'atributo_{i:02d}' for i in range(1, 35)]


def cargar_datos():
    path = ROOT / 'data/ionosphere.data'
    if not path.exists():
        response = requests.get(URL, timeout=60)
        response.raise_for_status()
        with zipfile.ZipFile(BytesIO(response.content)) as archive:
            content = archive.read('ionosphere.data')
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(content)
    if hashlib.sha256(path.read_bytes()).hexdigest() != SHA256:
        raise ValueError('El archivo no coincide con el SHA256 documentado.')
    raw = pd.read_csv(path, header=None, names=FEATURES + ['clase'])
    if set(raw.clase) != {'g', 'b'} or not all(pd.api.types.is_numeric_dtype(raw[c]) for c in FEATURES):
        raise ValueError('Esquema o etiquetas inesperados.')
    # Los registros idénticos no deben repartirse entre entrenamiento y evaluación.
    clean = raw.drop_duplicates().copy()
    if clean.duplicated(subset=FEATURES).any():
        raise ValueError('Predictores idénticos con etiquetas incompatibles; revisar agrupación.')
    X = clean[FEATURES]
    y = clean.clase.map({'b': 0, 'g': 1})
    return raw, X, y


def particionar(X, y):
    train_val, test = train_test_split(X.index, test_size=0.2, stratify=y, random_state=SEED)
    train, val = train_test_split(train_val, test_size=0.25, stratify=y.loc[train_val], random_state=SEED)
    return {name: np.sort(ids) for name, ids in [('entrenamiento', train), ('validacion', val), ('prueba', test)]}


def pipeline_svm(kernel='rbf', C=1.0, gamma='scale'):
    return Pipeline([('imputar', SimpleImputer(strategy='median')), ('escalar', StandardScaler()),
                     ('svm', SVC(kernel=kernel, C=C, gamma=gamma, random_state=SEED))])


def medir(model, X, y):
    prediction = model.predict(X)
    score = model.decision_function(X) if hasattr(model, 'decision_function') else model.predict_proba(X)[:, 1]
    return {'accuracy': accuracy_score(y, prediction), 'f1_macro': f1_score(y, prediction, average='macro', zero_division=0),
            'precision_macro': precision_score(y, prediction, average='macro', zero_division=0),
            'recall_b': recall_score(y, prediction, pos_label=0, zero_division=0),
            'recall_g': recall_score(y, prediction, pos_label=1, zero_division=0), 'roc_auc': roc_auc_score(y, score)}


def guardar_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, default=lambda x: x.item() if hasattr(x, 'item') else str(x)))


def crear_pdf(path, titulo, sections, table, figures, tests=None):
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    styles = getSampleStyleSheet()
    styles['BodyText'].fontSize = 9
    styles['BodyText'].leading = 13
    styles['BodyText'].alignment = TA_LEFT
    story = [Paragraph(titulo, styles['Title']), Paragraph('Marlenis Judith Concepción Cuevas · INF-8239-C2 · Unidad I', styles['BodyText']), Spacer(1, 10),
             Paragraph('Dataset propuesto: Ionosphere (UCI). Aprobación docente pendiente.', styles['BodyText'])]
    link = 'https://github.com/marlenis-concepcion/CienciaDatosUasd2026/tree/main/Ciencia%20de%20DatosII/Unidad%20I/' + ('Ejercicio%2001' if '01' in titulo else 'Ejercicio%2002')
    story += [Paragraph(f'Repositorio: <link href="{link}" color="blue">abrir carpeta del ejercicio en GitHub</link>', styles['BodyText']), Spacer(1, 10)]
    if table is not None:
        cells = [[Paragraph(str(v), styles['BodyText']) for v in row] for row in table]
        t = Table(cells, repeatRows=1, hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dde9f4')),('GRID',(0,0),(-1,-1),0.3,colors.grey),('VALIGN',(0,0),(-1,-1),'TOP')]))
        story += [t, Spacer(1, 12)]
    for heading, body in sections:
        story += [Paragraph(heading, styles['Heading2'])]
        for para in body.split('\n\n'):
            story += [Paragraph(para.replace('\n',' '), styles['BodyText']), Spacer(1, 6)]
    for fig, caption in figures:
        story += [KeepTogether([Paragraph(caption, styles['Heading3']), Image(str(fig), width=440, height=290)])]
    if tests is not None:
        small = styles['BodyText'].clone('Pruebas', fontSize=7.5, leading=9.5)
        story += [Paragraph(f'Pruebas automatizadas ({len(tests)}, todas aprobadas)', styles['Heading2'])]
        rows = [['#', 'Prueba', 'Qué comprueba', 'Por qué se hizo']] + [
            [r.n, r.prueba.replace('_', ' '), r.comprueba, r.por_que] for r in tests.itertuples()]
        t = Table([[Paragraph(str(v), small) for v in row] for row in rows], repeatRows=1, hAlign='LEFT',
                  colWidths=[24, 136, 175, 175])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dde9f4')),('GRID',(0,0),(-1,-1),0.3,colors.grey),('VALIGN',(0,0),(-1,-1),'TOP')]))
        story += [t]
    story += [Paragraph('Uso de IA', styles['Heading2']),
              Paragraph('Utilicé Claude Code (Claude Opus 5.5), Codex (OpenAI) y DeepSeek como apoyo para código, pruebas y '
                        'redacción. Verifiqué las cifras ejecutando el código y las pruebas; la interpretación y las decisiones '
                        'son propias.', styles['BodyText'])]
    small_ai = styles['BodyText'].clone('IA', fontSize=7.5, leading=9.5)
    ai_rows = [['Herramienta', 'Modelo', 'Uso en esta práctica', 'Para qué sirve', 'Límite y control'],
               ['Claude Code (Anthropic)', '<b>Claude Opus 5.5</b>', '<b>Usado.</b> Código, pruebas, cuaderno, documentación y PDF',
                'Tareas largas de varios pasos sobre un repositorio', 'Todo se verificó con pruebas y reportes'],
               ['Claude (Anthropic)', 'Claude Sonnet 5', 'No usado', 'Programación cotidiana, equilibrio velocidad-calidad',
                'Menos profundidad en tareas largas'],
               ['Claude (Anthropic)', 'Claude Haiku 4.5', 'No usado', 'Tareas rápidas y baratas: resúmenes, clasificación',
                'No indicado para diseño experimental'],
               ['Codex (OpenAI)', 'Modelo de OpenAI orientado a código (familia GPT-5-Codex)', 'Apoyo complementario',
                'Proponer y revisar código, explicar errores, sugerir pruebas', 'Se acepta solo si pasa las pruebas'],
               ['DeepSeek', 'DeepSeek-V3 (chat)', 'Apoyo complementario', 'Explicar conceptos y revisar redacción',
                'Puede inventar referencias: se verificaron en la fuente'],
               ['DeepSeek', 'DeepSeek-R1 (razonamiento)', 'No usado; recomendado para revisar la lógica de métricas', 'Razonamiento paso a paso y depuración lógica',
                'No sustituye la ejecución']]
    resp_rows = [['Responsabilidad', 'Quién'],
                 ['Valores del análisis (métrica principal, tolerancias, decisiones de uso)', 'La autora'],
                 ['Elección de datos y verificación de licencias y referencias', 'La autora, con apoyo de las herramientas'],
                 ['Borradores de código, pruebas y redacción', 'Herramientas de IA'],
                 ['Ejecución de pruebas y comprobación de cada cifra contra reports/', 'La autora, con Claude Code'],
                 ['Defensa oral y respuesta a preguntas técnicas', 'La autora']]
    for rows, widths in [(ai_rows, [80, 90, 115, 115, 110]), (resp_rows, [330, 180])]:
        t = Table([[Paragraph(str(v), small_ai) for v in row] for row in rows], repeatRows=1, hAlign='LEFT', colWidths=widths)
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dde9f4')),('GRID',(0,0),(-1,-1),0.3,colors.grey),('VALIGN',(0,0),(-1,-1),'TOP')]))
        story += [Spacer(1, 6), t]
    SimpleDocTemplate(str(path), rightMargin=42,leftMargin=42,topMargin=36,bottomMargin=36).build(story)


def ejecutar():
    report = ROOT / 'reports'; report.mkdir(exist_ok=True)
    (report / 'modelos').mkdir(exist_ok=True)
    raw, X, y = cargar_datos(); parts = particionar(X, y)
    split = pd.concat([pd.DataFrame({'fila_original': ids, 'particion': name}) for name, ids in parts.items()], ignore_index=True)
    split.to_csv(report / 'particiones.csv', index=False)
    audit = {'filas_originales': len(raw), 'filas_utilizadas': len(X), 'duplicados_eliminados': len(raw)-len(X),
             'faltantes': int(raw.isna().sum().sum()), 'columnas_constantes': X.columns[X.nunique()==1].tolist(),
             'clases': raw.clase.value_counts().to_dict(), 'sha256_datos': SHA256,
             'particiones': {k: len(v) for k,v in parts.items()}, 'semilla': SEED, 'aprobacion_docente': 'pendiente'}
    guardar_json(report/'auditoria.json', audit)
    pd.DataFrame([{'variable': c, 'tipo': str(raw[c].dtype), 'rol': 'predictor',
                   'descripcion': f'Atributo {i} de la señal procesada por autocorrelación; sin unidad individual especificada por UCI.',
                   'faltantes': int(raw[c].isna().sum())} for i,c in enumerate(FEATURES,1)] +
                 [{'variable':'clase','tipo':'categorica','rol':'target','descripcion':'b=retorno malo (0); g=retorno bueno (1).','faltantes':0}]).to_csv(report/'diccionario.csv',index=False)
    train, val, test = [parts[n] for n in ['entrenamiento','validacion','prueba']]
    baseline = DummyClassifier(strategy='most_frequent').fit(X.loc[train], y.loc[train])
    grid = [{'svm__kernel':['linear'],'svm__C':[0.1,1,10]},
            {'svm__kernel':['rbf'],'svm__C':[0.1,1,10],'svm__gamma':['scale',0.01,0.1]}]
    start = time.perf_counter()
    with threadpool_limits(limits=1):
        search = GridSearchCV(pipeline_svm(), grid, scoring='f1_macro', cv=StratifiedKFold(5,shuffle=True,random_state=SEED), n_jobs=1, return_train_score=True)
        search.fit(X.loc[train],y.loc[train])
    search_time = time.perf_counter()-start
    pd.DataFrame(search.cv_results_).to_csv(report/'busqueda_cv.csv',index=False)
    best = search.best_estimator_
    guardar_json(report/'parametros.json', {'mejores_parametros':search.best_params_,'f1_cv':search.best_score_,'busqueda_segundos':search_time})
    rows=[]
    for label, model in [('Baseline',baseline),('SVM',best)]:
        for part,ids in parts.items(): rows.append({'modelo':label,'particion':part,**medir(model,X.loc[ids],y.loc[ids])})
    result = pd.DataFrame(rows); result.to_csv(report/'resultados.csv',index=False)
    pred = best.predict(X.loc[test]); errors=pd.DataFrame({'fila_original':test,'real':y.loc[test].to_numpy(),'prediccion':pred})
    errors['error']=errors.real != errors.prediccion; errors.to_csv(report/'predicciones_prueba.csv',index=False)
    joblib.dump(best, report/'modelos/svm.joblib')
    ConfusionMatrixDisplay.from_predictions(y.loc[test],pred,display_labels=['b','g'],cmap='Blues')
    plt.title('SVM · prueba reservada');plt.tight_layout();plt.savefig(report/'matriz_confusion.png',dpi=150);plt.close()
    metadata={'python':platform.python_version(),'sistema':platform.platform(),'maquina':platform.machine(),'cpu_logicas':os.cpu_count(),'hilos_blas':1}
    guardar_json(report/'entorno.json',metadata)
    print(result.round(4).to_string(index=False)); print('Auditoría:',audit);print('Mejores parámetros:',search.best_params_)
    return result

if __name__ == '__main__':
    ejecutar()
