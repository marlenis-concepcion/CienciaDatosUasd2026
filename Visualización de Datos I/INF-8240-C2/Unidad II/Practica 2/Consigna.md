# Práctica Unidad II · Creación y análisis de gráficas Industrias Caribe S.A.

Transcripción estructurada de los requisitos facilitados por la estudiante, sin enlaces de sesión ni navegación de Moodle.

## Parte A · Reclamos

1. Guardar copia del libro como nombre_alumnoXX_IndustriasCaribe.xlsx.
2. Crear tabla `tblReclamos` con encabezados.
3. Revisar ReclamoID, VentaID, FechaReclamo, ProductoID, Region, Categoria, Prioridad, Estado, DiasResolucion y Satisfaccion_1a5.
4. Convertir FechaReclamo ISO a fecha real y crear MesReclamo con FECHA(AÑO([@FechaReclamo]); MES([@FechaReclamo]); 1).
5. Comprobar ReclamoID único e investigar vacíos. No sustituir los 132 vacíos de días y satisfacción automáticamente por cero.
6. Crear Resumen_Reclamos con total, resueltos y tasa resuelta.
7. Calcular PROMEDIO de días; Excel omite vacíos y solo representa casos con registro.
8. Calcular satisfacción promedio; solo respuestas disponibles.
9. Crear TD_Categoria: filas Categoria, recuento ReclamoID y barras ordenadas.
10. Crear TD_Estado: filas Estado, recuento ReclamoID y barras o columnas.
11. Crear TD_MesReclamo: filas MesReclamo, recuento ReclamoID y líneas; conservar reclamos de 2026 aunque las ventas sean de 2025.
12. Crear TD_RegionPrioridad: filas Region, columnas Prioridad, recuento ReclamoID y barras apiladas.
13. Crear Dashboard_Reclamos con cuatro KPI: total, resueltos, días promedio y satisfacción, y al menos tres gráficos.
14. Agregar segmentadores Region, Categoria y Estado conectados a las TD compatibles. Si se anuncian interactivas, las tarjetas deben actualizarse desde resúmenes de TD.
15. Verificar totales y filtros y redactar tres hallazgos, una limitación y dos recomendaciones.

**Control docente:** 450 reclamos; 318 resueltos; días con dato 318; satisfacción con dato 318. No comparar reclamos como tasa por producto sin denominador de ventas compatible.

**Preguntas:** categoría dominante; cuántos siguen abiertos; por qué se excluyen vacíos del promedio; acción prioritaria.

## Parte B · Producción

- Preparar y validar 1,200 registros; crear `tblProduccion`.
- Al menos cuatro indicadores: unidades planificadas, producidas, defectuosas y tasa de defectos = SUMA(defectuosas) / SUMA(producidas).
- Cumplimiento del plan = SUMA(producidas) / SUMA(planificadas); documentar valores superiores a 100 %.
- Al menos tres gráficos: plan vs. real por planta; tasa de defectos por producto; evolución mensual de producción o comparación por turno.
- Dashboard_Produccion con segmentadores Planta, Turno y Producto, títulos y formatos claros.
- Tres hallazgos cuantificados, dos recomendaciones y una limitación metodológica.

**Advertencias:** no promediar porcentajes de lotes para obtener la tasa global; usar razón de sumas. No interpretar UnidadesDefectuosas como desperdicio monetario sin regla de valoración.

**Fecha de entrega indicada:** 8 de noviembre de 2026, 00:00. El envío a UASDVirtual lo realiza la estudiante.
