# Guia de entrega APA/UASD - INF-8237 Unidad 2

## Alcance de la Fase I

El desarrollo y las evidencias deben demostrar:

1. Instalacion o disponibilidad de MySQL Community Edition y MySQL Workbench.
2. Importacion y uso de la base de datos Sakila.
3. Ejecucion de diez consultas SQL.
4. CRUD en Python para paises, ciudades, peliculas e inventario.
5. Funciones Create, Read, Update y Delete.
6. Importacion y exportacion de modelos en CSV.
7. Importacion y exportacion de modelos en JSON.
8. Calculo de media, rango, desviacion estandar, varianza y covarianza.

No basta con enumerar estos elementos. El informe debe explicar la implementacion y remitir a capturas, salidas o anexos que demuestren su ejecucion.

## Estructura obligatoria

Cada informe debe seguir esta organizacion:

1. Presentacion.
2. Resumen.
3. Abstract.
4. Tabla de contenido.
5. Desarrollo.
6. Referencias.
7. Anexos.

## Desarrollo recomendado

El cuerpo debe tener entre 5 y 10 paginas, sin contar presentacion, resumen, tabla de contenido, referencias ni anexos.

Secciones H2 recomendadas:

- Introduccion.
- Marco de referencia.
- Descripcion del caso practico.
- Metodologia.
- Implementacion y resultados.
- Conclusiones.

## Contenido tecnico recomendado

La seccion de implementacion y resultados debe identificar:

- El script `sql/01_fase_i_10_consultas.sql` y los resultados obtenidos en Workbench.
- Las entidades `country`, `city`, `film` e `inventory`.
- Las operaciones CRUD disponibles para cada entidad y sus limitaciones.
- Los modulos `models.py`, `repositories.py`, `services.py` y `main.py`.
- Las funciones de importacion y exportacion de `import_export.py`.
- Las metricas calculadas por `metrics.py` y `reports.py`.
- El procedimiento de ejecucion con `MAC_SH_QUICKSTART.sh`, `LINUX_SH_QUICKSTART.sh` o `WINDOWS_QUICKSTART.ps1`.

Cuando una funcion exista en el codigo, pero no este integrada en el menu, debe indicarse expresamente. En la version actual, CSV y JSON se ofrecen como funciones reutilizables de `import_export.py`.

## Citas requeridas

El informe debe incluir los tres tipos:

- Cita narrativa: Autor (anio) explica...
- Cita parentetica: ... al final de la idea (Autor, anio).
- Cita textual directa breve: menos de 40 palabras, con pagina, parrafo o seccion cuando aplique.

## Reglas de formato

- Tamano carta.
- Margenes de 2.54 cm.
- Times New Roman 12.
- Doble espacio.
- Alineacion izquierda.
- Sangria de primera linea de 1.27 cm.
- Referencias con sangria francesa.
- Numeracion superior derecha.

## Anexos

Los anexos deben estar despues de las referencias y ser citados en el cuerpo del informe.

Ejemplos:

- Anexo A. Capturas de ejecucion del CRUD.
- Anexo B. Scripts SQL y consultas de Sakila.
- Anexo C. Evidencias de CSV, JSON y metricas descriptivas.
- Anexo D. Evidencia del uso de agentes IA.

## Checklist final

- Todas las citas en el texto tienen referencia.
- Todas las referencias aparecen citadas.
- Las tablas y figuras tienen numero, titulo y nota.
- Los anexos estan nombrados y mencionados.
- El codigo se ejecuta o se documenta claramente la dependencia faltante.
- Las evidencias muestran resultados reales, no solo intencion.
