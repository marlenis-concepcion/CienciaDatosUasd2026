# Unidad II · Industrias Caribe S.A.

**Materia:** Visualización de Datos I · INF-8240-C2 · UASD
**Estudiante:** Marlenis Judith Concepción Cuevas

- [Excel de la solución](Marlenis_Concepcion_IndustriasCaribe.xlsx): datos, 10 tablas dinámicas nativas, 6 segmentadores, 2 dashboards, 8 gráficos y fórmulas revisables.
- [Informe PDF con portada UASD](Informe_Unidad_II_IndustriasCaribe.pdf): análisis, procedimiento, ocho gráficos, hallazgos, limitaciones y recomendaciones.
- [GitHub: solución completa](https://github.com/marlenis-concepcion/CienciaDatosUasd2026/tree/main/Visualizaci%C3%B3n%20de%20Datos%20I/INF-8240-C2/Unidad%20II/Practica%202).
- [Verificación y alcance de las pruebas](VERIFICACION.md).

## Usar el Excel

Abrir `Dashboard_Reclamos` o `Dashboard_Produccion` en Excel de escritorio compatible con segmentadores. Se entrega la vista global sin filtros restrictivos. Los segmentadores de cada dashboard se conectan a todas las tablas dinámicas de su conjunto; las tarjetas y series utilizan GETPIVOTDATA. Los resúmenes globales están identificados y no se anuncian como interactivos.

Reclamos permite filtrar Region, Categoria y Estado. Producción permite filtrar Planta, Turno y Producto. El icono de borrar filtro restablece los totales. Las medias sin observaciones y tasas sin denominador se muestran como «Sin datos» en los KPI, en lugar de inventar un cero. Para cambios en los datos, utilizar Datos > Actualizar todo.

Los controles docentes están conciliados: 450 reclamos, 318 resueltos, 318 días con dato y 318 respuestas. Se conservaron los 132 vacíos de cada campo. Los 1,200 lotes se utilizan sin eliminar sobrecumplimientos del plan. Las tasas de producción son razones de sumas.

Las conexiones y el contenido OOXML se verificaron estructuralmente y las fórmulas se conciliaron con los CSV. Los datos iniciales y gráficos se revisaron con LibreOffice; no se pudo ejecutar la interacción de los segmentadores en Excel de escritorio. Evitar guardar con visores o bibliotecas que eliminen extensiones de segmentadores.

## Datos originales

Se leen, con rutas relativas, los tres CSV ubicados en la carpeta de la materia, dos niveles por encima de esta práctica:

- `IndustriasCaribe_Reclamos.csv`: 450 filas.
- `IndustriasCaribe_Produccion.csv`: 1,200 filas.
- `IndustriasCaribe_Ventas.csv`: 3,000 filas, usadas para validar las relaciones de reclamos.

No se suma `IndustriasCaribe_Ventas copy.csv`, que es idéntico al original. Los CSV se conservan sin cambios. No se incluyen direcciones de sesión de Moodle, credenciales ni rutas del equipo.

## Reproducir

Desde esta carpeta, en un entorno Python 3.10 o posterior:

```sh
python -m pip install -r requirements.txt
python generar_excel.py
python generar_informe.py
python verificar_entrega.py
```

`datos.py` carga y valida los CSV. `generar_excel.py` construye datos, fórmulas y gráficos; `excel_nativo.py` añade las partes OOXML de tablas dinámicas y segmentadores. `generar_informe.py` compone el PDF, usando el escudo ya conservado en la Unidad I. `verificar_entrega.py` comprueba los datos, resultados, relaciones internas, conexiones y enlace de GitHub.

## Referencias técnicas del formato

La representación de los segmentadores sigue la documentación de Microsoft: [Slicer Cache](https://learn.microsoft.com/en-us/openspecs/office_standards/ms-xlsx/7dbb4481-b021-45cc-8bd4-6094b566a5ff), [CT_Slicer](https://learn.microsoft.com/en-us/openspecs/office_standards/ms-xlsx/03ec9cc4-ffa9-4646-b4a8-8343bbe076d0) y [Pivot Cache Definition](https://learn.microsoft.com/en-us/openspecs/office_standards/ms-xlsx/2924f3f8-a9cb-4b09-8557-fda87770d5bd).

Fuente académica: consigna y CSV de UASDVirtual facilitados por la estudiante. Escudo UASD: recurso del repositorio, Wikimedia Commons, CC BY-SA 4.0. Trabajo preparado con apoyo de programación e IA y sujeto a revisión de la estudiante antes de entregar.
