"""Informe de comparación, con interpretación y decisión cuantificada."""
from laboratorio_e02 import ROOT
from laboratorio_e01 import crear_pdf
import pandas as pd
import json


def generar():
    r=ROOT/'reports';df=pd.read_csv(r/'comparacion.csv');decision=json.loads((r/'decision.json').read_text())
    chosen=df[df.modelo==decision['modelo']].iloc[0];maxf=df.f1_macro.max();final=pd.read_csv(r/'prueba_final.csv').iloc[0]
    svm=df[df.modelo=='SVM'].iloc[0];pca=df[df.modelo=='SVM_PCA95'].iloc[0]
    variance=pd.read_csv(r/'pca_varianza.csv');count=int(variance[variance.varianza_acumulada>=0.95].iloc[0].componente)
    tsne=pd.read_csv(r/'tsne_calidad.csv')
    conclusion=f'''Se compararon seis configuraciones sobre las mismas 350 observaciones, target y partición del Ejercicio 01: SVM, SVM con PCA al 95%, dos Random Forest y dos Gradient Boosting. Los parámetros del SVM proceden de la búsqueda previa sobre entrenamiento; las alternativas de ensambles se fijaron antes de evaluar validación. El conjunto de prueba se utilizó únicamente después de registrar la decisión de este ejercicio. La aprobación docente del dataset continúa pendiente.

La comparación priorizó F1 macro de validación. El mayor valor fue {maxf:.3f}. La regla previamente definida admitió una pérdida máxima de 0.02 frente a ese valor y seleccionó la menor latencia entre las configuraciones no dominadas. La frontera consideró simultáneamente F1, tiempo de entrenamiento, inferencia amortizada y tamaño serializado. Resultó seleccionado {chosen.modelo}, con F1 de validación {chosen.f1_macro:.3f}, ajuste de {chosen.ajuste_s:.4f} segundos, inferencia de {chosen.inferencia_ms_fila:.4f} milisegundos por fila y tamaño de {chosen.tamano_kib:.1f} KiB. La diferencia frente al máximo fue {maxf-chosen.f1_macro:.3f}. Su F1 macro final en prueba fue {final.f1_macro:.3f}.

Cada configuración se entrenó tres veces con la misma semilla, usando un hilo y alternando el orden. Se excluyó el calentamiento y se midieron treinta predicciones del lote de validación por repetición. Los valores publicados son medianas. La latencia por fila se obtiene dividiendo el tiempo del lote entre sus observaciones; no representa una solicitud individual en producción. Estas repeticiones caracterizan el tiempo local, no la incertidumbre de generalización. El tamaño corresponde al archivo del pipeline completo sin compresión y no mide memoria RAM máxima.

PCA necesitó {count} componentes para retener al menos el 95% de la varianza de entrenamiento. El SVM sin reducción obtuvo F1 de validación {svm.f1_macro:.3f}, frente a {pca.f1_macro:.3f} con PCA; conservar varianza no garantiza conservar toda la información discriminativa. Las dos proyecciones t-SNE usan semillas 42 y 73, con perplexity 30. Su preservación de vecindades, medida mediante trustworthiness con cinco vecinos, fue {tsne.iloc[0].trustworthiness_k5:.3f} y {tsne.iloc[1].trustworthiness_k5:.3f}. En la semilla 42 se observa una zona de retornos buenos en la parte superior izquierda y otra hacia la inferior derecha, con retornos malos más presentes en el centro derecho. En la semilla 73 cambia la disposición: aparece una banda de buenos en la parte superior y se mantiene mezcla de clases en zonas centrales. Ningún mapa separa por completo ambas clases. Las figuras deben interpretarse como exploración local: cambios de orientación, distancias entre grupos o separación aparente no demuestran capacidad predictiva.

La decisión expresa un compromiso medido en este equipo y podría cambiar con hardware, carga o tamaño de lote. No se midieron energía ni emisiones, por lo que no se atribuyen ahorros de kWh o CO2. Se conservaron modelos, resultados individuales y evidencia de la partición para revisión. Antes de entregar, corresponde confirmar la selección con el profesor y revisar personalmente la interpretación y los límites del experimento.'''
    (r/'conclusion.md').write_text('# Conclusión · borrador para revisión personal\n\n'+conclusion+'\n')
    table=[['Modelo','F1 val.','Ajuste s','ms/fila','KiB','Pareto']]+[[x.modelo,f'{x.f1_macro:.3f}',f'{x.ajuste_s:.4f}',f'{x.inferencia_ms_fila:.4f}',f'{x.tamano_kib:.1f}','Sí' if x.pareto else 'No'] for _,x in df.iterrows()]
    sections=[('Protocolo','Mismo dataset, target e índices del Ejercicio 01. Seis configuraciones, tres repeticiones temporales y mediana; n_jobs=1 y BLAS limitado a un hilo. Regla: pérdida de F1 macro de validación no mayor de 0.02 y mínima latencia entre modelos no dominados. La gráfica Pareto muestra una proyección 2D de cuatro objetivos; por eso un punto puede parecer dominado en el plano y pertenecer a la frontera de cuatro dimensiones.'),
              ('Resultados, interpretación y defensa de la decisión',conclusion),
              ('Fuentes','Dataset: Sigillito et al. (1989), https://doi.org/10.24432/C5W01B, CC BY 4.0. PCA y t-SNE: documentación oficial de scikit-learn, https://scikit-learn.org/stable/modules/decomposition.html y https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html.')]
    figures=[(r/name,caption) for name,caption in [('pca.png','Varianza acumulada de PCA'),('tsne_42.png','t-SNE: semilla 42'),('tsne_73.png','t-SNE: semilla 73'),('pareto.png','Desempeño y costo de inferencia')]]
    crear_pdf(r/'Ejercicio_02.pdf','Ejercicio 02 · Ensambles, reducción y Green AI',sections,table,figures)
    print('PDF 02 y conclusión generados')

if __name__=='__main__':generar()
