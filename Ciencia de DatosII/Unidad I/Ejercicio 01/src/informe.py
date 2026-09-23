"""Genera el informe a partir de las evidencias ejecutadas."""
from laboratorio_e01 import ROOT, crear_pdf
import pandas as pd
import json


def generar():
    r=ROOT/'reports';df=pd.read_csv(r/'resultados.csv')
    best=df[(df.modelo=='SVM')&(df.particion=='prueba')].iloc[0]
    base=df[(df.modelo=='Baseline')&(df.particion=='prueba')].iloc[0]
    val=df[(df.modelo=='SVM')&(df.particion=='validacion')].iloc[0]
    train=df[(df.modelo=='SVM')&(df.particion=='entrenamiento')].iloc[0]
    errors=pd.read_csv(r/'predicciones_prueba.csv');n=int(errors.error.sum())
    params=json.loads((r/'parametros.json').read_text())
    conclusion=f'''El experimento examinó si un pipeline SVM podía clasificar retornos de radar y superar una regla constante. Se utilizó Ionosphere, procedente de UCI y distribuido con licencia CC BY 4.0. La comparación previa con Banknote Authentication favoreció provisionalmente Ionosphere porque sus 34 atributos permiten estudiar posteriormente reducción dimensional. Esta selección sigue pendiente de aprobación docente; la ejecución técnica no sustituye ese requisito académico.

La auditoría identificó 351 registros originales, ningún valor faltante y un duplicado exacto. Se retiró ese duplicado antes de particionar para impedir que una observación idéntica apareciera en conjuntos diferentes. Quedaron 350 registros: 210 para entrenamiento, 70 para validación y 70 para prueba. Se mantuvo una columna constante, cuyo escalamiento es manejado por el pipeline, para conservar el esquema original. La clase objetivo se separó de los predictores y los índices de las particiones quedaron registrados.

La búsqueda comparó kernels lineal y RBF con validación cruzada estratificada de cinco pliegues exclusivamente sobre entrenamiento. La imputación y el escalamiento se ajustaron dentro de cada pliegue. La configuración seleccionada fue {params['mejores_parametros']['svm__kernel']}, con C={params['mejores_parametros']['svm__C']} y gamma={params['mejores_parametros'].get('svm__gamma','scale')}. El baseline predijo siempre la clase mayoritaria. En prueba, su F1 macro fue {base.f1_macro:.3f}, mientras que el SVM alcanzó {best.f1_macro:.3f}, una diferencia de {best.f1_macro-base.f1_macro:.3f}. La exactitud del SVM fue {best.accuracy:.3f}; se priorizó F1 macro para representar ambas clases.

El F1 macro descendió de {train.f1_macro:.3f} en entrenamiento a {val.f1_macro:.3f} en validación y {best.f1_macro:.3f} en prueba. Esta diferencia exige cautela frente al sobreajuste, aunque no elimina la mejora respecto a la referencia. Hubo {n} errores entre las 70 observaciones de prueba. El recall fue {best.recall_b:.3f} para retornos malos y {best.recall_g:.3f} para buenos; la matriz de confusión permite distinguir los errores en ambas direcciones. Sin información adicional de adquisición no se puede atribuir causalmente cada fallo a una característica concreta.

Los resultados respaldan continuar con la comparación de ensambles, pero no garantizan desempeño fuera de este radar histórico. El pequeño tamaño de prueba limita la precisión de las estimaciones y no se calculó un intervalo de confianza. La descarga verificada, las semillas, las pruebas y el código reutilizable facilitan reproducir el procedimiento.'''
    assert 300<=len(conclusion.split())<=500, len(conclusion.split())
    (r/'conclusion.md').write_text('# Conclusión\n\n'+conclusion+'\n')
    table=[['Modelo','Conjunto','F1 macro','Accuracy','Recall b','Recall g']]+[[row.modelo,row.particion,f'{row.f1_macro:.3f}',f'{row.accuracy:.3f}',f'{row.recall_b:.3f}',f'{row.recall_g:.3f}'] for _,row in df.iterrows()]
    audit=json.loads((r/'auditoria.json').read_text())
    sections=[('Dataset y selección','Ionosphere (UCI): 351 registros, 34 atributos numéricos, clasificación g/b, CC BY 4.0. Alternativa: Banknote Authentication, 1372 registros y 4 atributos. Se propone Ionosphere por su dimensionalidad; aprobación pendiente. La ficha completa y las fuentes están en reports/seleccion_dataset.md.'),
              ('Auditoría y protocolo',f'Un duplicado eliminado; {audit["faltantes"]} faltantes; atributo_02 constante. División estratificada 210/70/70, semilla 42. El identificador de fila solo documenta la partición y no entra en el modelo. Búsqueda de 12 combinaciones y cinco pliegues sobre entrenamiento. Validación y prueba no ajustan transformaciones. SHA256 y diccionario en reports. Prueba reservada para evaluación posterior a la selección.'),
              ('Conclusión',conclusion),
              ('Fuentes','Sigillito, Wing, Hutton y Baker (1989), Ionosphere: https://doi.org/10.24432/C5W01B. Lohweg (2012), Banknote Authentication: https://doi.org/10.24432/C55P57. Documentación de scikit-learn sobre pipelines y prevención de fuga: https://scikit-learn.org/stable/common_pitfalls.html.')]
    crear_pdf(r/'Ejercicio_01.pdf','Ejercicio 01 · Dataset público y SVM',sections,table,[(r/'matriz_confusion.png','Matriz de confusión del SVM en prueba')],tests=pd.read_csv(ROOT/'docs/pruebas.csv'))
    print('PDF 01 y conclusión generados:',len(conclusion.split()),'palabras')

if __name__=='__main__':generar()
