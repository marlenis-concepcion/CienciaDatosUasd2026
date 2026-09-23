"""Comparación homogénea; selección en validación y prueba solo del elegido."""
from pathlib import Path
import sys
import time
import json
import io
import platform
import os
ROOT=Path(__file__).resolve().parents[1]
E1=ROOT.parent/'Ejercicio 01'
sys.path.append(str(E1/'src'))
from laboratorio_e01 import cargar_datos, particionar, pipeline_svm, medir, guardar_json, SEED
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.base import clone
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE, trustworthiness
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import ConfusionMatrixDisplay
from threadpoolctl import threadpool_limits


def configuraciones(params):
    svm=pipeline_svm();svm.set_params(**params)
    reduced=Pipeline([('imputar',SimpleImputer(strategy='median')),('escalar',StandardScaler()),
                      ('pca',PCA(n_components=0.95,svd_solver='full')),('svm',clone(svm.named_steps['svm']))])
    return {'SVM':svm,'SVM_PCA95':reduced,
            'RF_50':Pipeline([('imputar',SimpleImputer(strategy='median')),('modelo',RandomForestClassifier(n_estimators=50,max_depth=6,random_state=SEED,n_jobs=1))]),
            'RF_150':Pipeline([('imputar',SimpleImputer(strategy='median')),('modelo',RandomForestClassifier(n_estimators=150,max_depth=None,random_state=SEED,n_jobs=1))]),
            'GB_50':Pipeline([('imputar',SimpleImputer(strategy='median')),('modelo',GradientBoostingClassifier(n_estimators=50,max_depth=2,learning_rate=0.1,random_state=SEED))]),
            'GB_100':Pipeline([('imputar',SimpleImputer(strategy='median')),('modelo',GradientBoostingClassifier(n_estimators=100,max_depth=2,learning_rate=0.1,random_state=SEED))])}


def frontera(tabla):
    # Maximizar F1; minimizar ajuste, latencia y tamaño. Igualdad no domina.
    values=tabla[['f1_macro','ajuste_s','inferencia_ms_fila','tamano_kib']].to_numpy().copy()
    values[:,0]*=-1
    return np.array([not np.any(np.all(values<=row,axis=1)&np.any(values<row,axis=1)) for row in values])


def elegir(tabla):
    feasible=tabla[tabla.pareto & (tabla.f1_macro >= tabla.f1_macro.max()-0.02)]
    return feasible.sort_values(['inferencia_ms_fila','tamano_kib','modelo']).iloc[0]


def ejecutar():
    report=ROOT/'reports';(report/'modelos').mkdir(parents=True,exist_ok=True)
    if not (E1/'reports/parametros.json').exists():
        raise RuntimeError('Ejecutar primero el Ejercicio 01.')
    _,X,y=cargar_datos(); parts=particionar(X,y)
    saved=pd.read_csv(E1/'reports/particiones.csv')
    for name,ids in parts.items():
        if not np.array_equal(saved.loc[saved.particion==name,'fila_original'].to_numpy(),ids):
            raise ValueError('La partición difiere del Ejercicio 01.')
    saved.to_csv(report/'particiones.csv',index=False)
    params=json.loads((E1/'reports/parametros.json').read_text())['mejores_parametros']
    configs=configuraciones(params);train=parts['entrenamiento'];val=parts['validacion'];test=parts['prueba']
    raw=[];models={}
    with threadpool_limits(limits=1):
        # Calentamiento común excluido de las mediciones.
        for template in configs.values(): clone(template).fit(X.loc[train],y.loc[train]).predict(X.loc[val])
        for repeat in range(3):
            order=list(configs);np.random.default_rng(SEED+repeat).shuffle(order)
            for name in order:
                model=clone(configs[name]);start=time.perf_counter();model.fit(X.loc[train],y.loc[train]);fit=time.perf_counter()-start
                model.predict(X.loc[val])
                timings=[]
                for _ in range(30):
                    start=time.perf_counter();model.predict(X.loc[val]);timings.append(time.perf_counter()-start)
                blob=io.BytesIO();joblib.dump(model,blob,compress=0)
                raw.append({'modelo':name,'repeticion':repeat+1,'ajuste_s':fit,
                            'inferencia_ms_fila':np.median(timings)*1000/len(val),'tamano_kib':blob.tell()/1024,
                            **medir(model,X.loc[val],y.loc[val])})
                models[name]=model
    repetitions=pd.DataFrame(raw);repetitions.to_csv(report/'repeticiones.csv',index=False)
    result=repetitions.groupby('modelo',sort=False).median(numeric_only=True).drop(columns='repeticion').reset_index()
    result['pareto']=frontera(result);result.to_csv(report/'comparacion.csv',index=False)
    selected=elegir(result);name=selected['modelo'];model=models[name]
    # Decisión fijada antes de calcular las métricas finales.
    decision={'modelo':name,'regla':'Frontera Pareto de cuatro objetivos; F1 macro >= mejor F1 - 0.02; menor latencia amortizada por fila; desempate por tamaño.',
              'f1_validacion':selected.f1_macro,'tolerancia_f1':0.02,'criterio':'validacion', 'semilla':SEED}
    guardar_json(report/'decision.json',decision)
    for label,fitted in models.items():joblib.dump(fitted,report/'modelos'/f'{label}.joblib',compress=0)
    final=pd.DataFrame([{'modelo':name,'particion':'prueba',**medir(model,X.loc[test],y.loc[test])}]);final.to_csv(report/'prueba_final.csv',index=False)
    ConfusionMatrixDisplay.from_estimator(model,X.loc[test],y.loc[test],display_labels=['b','g'],cmap='Blues')
    plt.title(f'{name} · prueba reservada');plt.tight_layout();plt.savefig(report/'matriz_confusion.png',dpi=150);plt.close()
    fig,ax=plt.subplots(figsize=(7,4))
    for _,row in result.iterrows():
        ax.scatter(row.inferencia_ms_fila,row.f1_macro,c='tab:green' if row.pareto else 'tab:gray',s=80)
        offset={'GB_50':(-12,-28),'GB_100':(5,25),'SVM_PCA95':(28,-13)}.get(row.modelo,(4,5))
        ax.annotate(row.modelo,(row.inferencia_ms_fila,row.f1_macro),fontsize=8,xytext=offset,textcoords='offset points',arrowprops={'arrowstyle':'-','lw':0.5} if row.modelo in {'GB_50','GB_100','SVM_PCA95'} else None)
    ax.set(xlabel='Inferencia amortizada (ms/fila, lote de validación)',ylabel='F1 macro de validación',title='Pareto: proyección 2D de cuatro objetivos (verde=no dominado)')
    ax.margins(0.2);fig.tight_layout();fig.savefig(report/'pareto.png',dpi=150);plt.close(fig)
    with threadpool_limits(limits=1):
        scaler=StandardScaler();scaled=scaler.fit_transform(X.loc[train])
        pca=PCA().fit(scaled);cum=np.cumsum(pca.explained_variance_ratio_)
        pd.DataFrame({'componente':np.arange(1,len(cum)+1),'varianza_acumulada':cum}).to_csv(report/'pca_varianza.csv',index=False)
        fig,ax=plt.subplots(figsize=(7,4));ax.plot(np.arange(1,len(cum)+1),cum,marker='.');ax.axhline(0.95,c='red',ls='--')
        ax.set(xlabel='Componentes',ylabel='Varianza acumulada',title='PCA ajustado solo en entrenamiento');fig.tight_layout();fig.savefig(report/'pca.png',dpi=150);plt.close(fig)
        projections=[]
        for seed in [42,73]:
            tsne=TSNE(n_components=2,perplexity=30,init='random',learning_rate='auto',max_iter=1000,random_state=seed,n_jobs=1)
            coords=tsne.fit_transform(scaled)
            score=trustworthiness(scaled,coords,n_neighbors=5)
            projections.append({'semilla':seed,'perplexity':30,'trustworthiness_k5':score,'kl_divergence':tsne.kl_divergence_})
            fig,ax=plt.subplots(figsize=(7,4))
            for label,title in [(0,'b: malo'),(1,'g: bueno')]:
                mask=y.loc[train].to_numpy()==label;ax.scatter(coords[mask,0],coords[mask,1],s=16,label=title,alpha=0.7)
            ax.legend();ax.set(title=f't-SNE entrenamiento · semilla {seed}',xlabel='Dimensión 1',ylabel='Dimensión 2');fig.tight_layout();fig.savefig(report/f'tsne_{seed}.png',dpi=150);plt.close(fig)
        pd.DataFrame(projections).to_csv(report/'tsne_calidad.csv',index=False)
    guardar_json(report/'entorno.json',{'python':platform.python_version(),'sistema':platform.platform(),'maquina':platform.machine(),
                  'hilos':1,'repeticiones':3,'predicciones_por_repeticion':30,'tamano_lote':len(val),
                  'inferencia':'mediana de 30 predicciones de lote por repetición, dividida por filas; luego mediana de tres repeticiones',
                  'energia':'No medida; tiempo y tamaño son indicadores indirectos, no kWh ni CO2.',
                  'advertencia':'Las tres repeticiones mantienen semilla y partición; miden variabilidad temporal, no incertidumbre estadística.'})
    print(result.round(5).to_string(index=False));print('Modelo elegido:',name);print(final.round(4).to_string(index=False))
    return result

if __name__=='__main__':ejecutar()
