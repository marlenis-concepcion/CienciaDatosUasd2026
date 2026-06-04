# Caso practico 2: CRUD/ORM nativo con Sakila

## Presentacion

Universidad Autonoma de Santo Domingo  
Facultad: [Completar]  
Asignatura: INF-8237 Ciencia de Datos I  
Unidad 2: Manipulacion y Procesamiento de Datos  
Tema: CRUD/ORM nativo basado en POO y estructuras de datos en MySQL Sakila  
Equipo: Mccarthy Team  
Integrantes: [Completar]  
Facilitador: [Completar]  
Fecha: [Completar]  

## Resumen

[Redactar 250 palabras sobre objetivo, tecnologia usada, alcance del CRUD/ORM, resultados, evidencias y aprendizaje.]

## Abstract

[English version of the summary.]

## Tabla de contenido

[Generar en Word o completar segun el documento final.]

## Introduccion

Presentar el contexto de las bases de datos relacionales, Sakila, POO y el objetivo del caso practico.

## Marco de referencia

Incluir conceptos de CRUD, ORM, POO, estructuras de datos y MySQL.

Ejemplos de citas a completar:

- Cita narrativa: Oracle (s.f.) describe Sakila como...
- Cita parentetica: El patron ORM facilita mapear entidades de negocio a tablas relacionales (Autor, anio).
- Cita textual directa breve: "[Completar cita textual corta]" (Autor, anio, p. xx).

## Descripcion del caso practico

Explicar el alcance: entidades `country`, `city`, `film` e `inventory`, conexion a MySQL Sakila mediante Docker o variables de entorno, operaciones CRUD, importacion/exportacion y metricas descriptivas.

## Arquitectura del sistema

Describir:

- `db.py`: conexion.
- `dbcontext.py`: contexto central de acceso a repositorios.
- `models.py`: entidades.
- `repositories.py`: CRUD generico.
- `controllers.py`: flujo tipo MVC.
- `services.py`: reglas de negocio.
- `structures.py`: cache e historial.
- `metrics.py` y `reports.py`: metricas descriptivas.
- `import_export.py`: CSV y JSON.
- `main.py`: menu de consola.

## Implementacion del CRUD

Documentar crear, leer, listar, actualizar y eliminar.

## Pruebas y resultados

Agregar capturas o salidas de:

- Conexion exitosa.
- Creacion de pais, ciudad, pelicula o inventario.
- Consulta por ID.
- Actualizacion.
- Eliminacion.
- Metricas descriptivas.
- Consultas SQL y unique constraints.

## Conclusiones

Resumir logros, limitaciones y aprendizajes.

## Referencias

[Completar en APA 7 solo con fuentes citadas.]

## Anexos

- Anexo A. Codigo fuente relevante.
- Anexo B. Evidencias de ejecucion.
- Anexo C. Uso de agentes IA.
