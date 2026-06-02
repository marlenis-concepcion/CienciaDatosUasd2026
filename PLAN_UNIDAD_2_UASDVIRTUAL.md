# Plan de trabajo Unidad 2 - UASDVirtual

Asignatura: INF-8237-C2 Ciencia de Datos I

Equipo: UASDVirtual

## Tareas

1. Caso practico 2: CRUD/ORM nativo con MySQL Sakila.
2. Caso practico 3: OULAD a base de datos relacional, limpieza, PK, FK, dominios, ETL y EDA extendido.

## Division inicial del trabajo

- Agente Sagan: plan tecnico para Sakila CRUD/ORM.
- Agente Sartre: plan tecnico para OULAD ETL/EDA.
- Codex principal: estructura del proyecto, integracion de planes, formato APA/UASD y coordinacion.

## Decisiones tecnicas

- Caso 2 usara MySQL con la base Sakila.
- Caso 2 tendra un ORM nativo simple: modelos, repositorios, servicios, cache y menu de consola.
- Caso 3 usara PostgreSQL como recomendacion principal por su soporte para `CHECK`, PK, FK, vistas e indices.
- Caso 3 conservara las fechas negativas validas de OULAD, porque representan dias antes del inicio del curso.
- Ambos informes seguiran la estructura APA/UASD: presentacion, resumen, abstract, tabla de contenido, desarrollo, referencias y anexos.

## Archivos creados

- `caso_practico_2_sakila_crud_orm/src/`: base del CRUD/ORM nativo para Sakila.
- `caso_practico_2_sakila_crud_orm/tests/`: pruebas iniciales de estructuras de datos.
- `caso_practico_3_oulad_etl_eda/sql/`: esquema, indices, vistas y consultas de calidad para OULAD.
- `caso_practico_3_oulad_etl_eda/src/`: extraccion, limpieza, calidad, transformacion y carga.

## Flujo recomendado

1. Confirmar herramientas disponibles: Python, MySQL/PostgreSQL, acceso a Sakila y dataset OULAD.
2. Construir primero una version pequena y demostrable de cada caso.
3. Agregar evidencias tecnicas: capturas, logs, consultas y graficas.
4. Redactar informes APA con citas, referencias y anexos.
5. Revisar checklist final antes de subir a UASD Virtual.

## Insumos pendientes

- Dataset OULAD en formato CSV o ZIP.
- Acceso o dump de la base de datos Sakila.
- Preferencia de motor para OULAD: PostgreSQL, MySQL o MS SQL Server.
- Nombres y matriculas de los integrantes, si deben aparecer en la portada.
- Nombre del facilitador y fecha exacta de entrega.
