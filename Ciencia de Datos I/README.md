# Ciencia de Datos UASD 2026

Repositorio académico de Marlenis Judith Concepción Cuevas para la asignatura
INF-8237-C2 Ciencia de Datos I.

## Organización

```text
CienciaDatosUasd2026/
  General/
  Unidad_2/
    Practica_02_Sakila_CRUD_ORM/
  Unidad_3/
    Practica_03_Caso_Practico_2_OULAD_DBMS/
  Unidad_4/
    Ensayo_02_Revision_Literatura_ML/
    Practica_Recuperacion_Metricas_Inferenciales_ML/
    Practica_04_Proyecto_Final_OULAD/
```

## General

Materiales transversales que no pertenecen directamente a una práctica: versiones históricas
de documentos, normas APA, plantillas, recursos visuales, scripts generadores y herramientas.

- [Índice general](General/README.md)

## Unidad 2

### Práctica 02: Sakila CRUD/ORM

Proyecto Python con MySQL Sakila, programación orientada a objetos, estructuras de datos,
operaciones CRUD, importación/exportación y métricas descriptivas.

- [Documentación](Unidad_2/Practica_02_Sakila_CRUD_ORM/README.md)
- [Portal HTML](Unidad_2/Practica_02_Sakila_CRUD_ORM/index.html)
- [Código principal](Unidad_2/Practica_02_Sakila_CRUD_ORM/caso_practico_2_sakila_crud_orm)

## Unidad 3

### Práctica 03: caso práctico OULAD DBMS

Proyecto POO/OSEMN con OULAD, base de datos, EDA, métricas, modelos supervisados,
documentación colaborativa y artículo APA 7.

- [Documentación](Unidad_3/Practica_03_Caso_Practico_2_OULAD_DBMS/README.md)
- [Caso práctico](Unidad_3/Practica_03_Caso_Practico_2_OULAD_DBMS/CASO_PRACTICO_2.md)
- [Cuaderno Colab](Unidad_3/Practica_03_Caso_Practico_2_OULAD_DBMS/notebooks/Proyecto_Final_OULAD_Colab.ipynb)

## Unidad 4

### Ensayo 02: revisión de literatura ML

Ensayo académico en formato APA 7 sobre revisión de literatura aplicada a Machine Learning.

- [Documentación](Unidad_4/Ensayo_02_Revision_Literatura_ML/README.md)
- [Documento final](Unidad_4/Ensayo_02_Revision_Literatura_ML/docs/Ensayo_2_Revision_Literatura_ML_Marlenis_APA7.docx)

### Recuperación: métricas inferenciales y ML

Cuaderno experimental con EDA, Pearson, Spearman, t-test, ANOVA, chi-cuadrado, regresión,
SVM y una red neuronal básica.

- [Documentación](Unidad_4/Practica_Recuperacion_Metricas_Inferenciales_ML/README.md)
- [Cuaderno Colab](Unidad_4/Practica_Recuperacion_Metricas_Inferenciales_ML/Practica_Unidad_4_Metricas_Inferenciales_ML.ipynb)

### Práctica 04: proyecto final OULAD

Proyecto colaborativo POO/OSEMN con OULAD, Experimento X sintético, EDA extendido, tres tipos
de objetivo, nueve modelos supervisados, métricas, predicciones caso a caso e importancias.

- [Documentación](Unidad_4/Practica_04_Proyecto_Final_OULAD/README.md)
- [Portal HTML](Unidad_4/Practica_04_Proyecto_Final_OULAD/index.html)
- [Artículo APA 7](Unidad_4/Practica_04_Proyecto_Final_OULAD/docs/Articulo_Cientifico_OULAD_APA7.docx)
- [Cuaderno Colab](Unidad_4/Practica_04_Proyecto_Final_OULAD/notebooks/Proyecto_Final_OULAD_Colab.ipynb)

## Validación

Cada práctica conserva su propio entorno y configuración para evitar conflictos entre paquetes
llamados `src`.

```bash
python3 scripts/validar_repositorio.py
```

## Privacidad y reproducibilidad

- No se versionan credenciales, entornos virtuales ni cachés.
- `data/oulad.zip` se descarga desde UCI y no se publica en GitHub.
- Las rutas del código son relativas al proyecto.
- El Experimento X de Unidad 4 es sintético y no representa estudiantes reales.
- Los criterios completos están en
  [General/ARCHIVOS_GITIGNORE.md](General/ARCHIVOS_GITIGNORE.md).
