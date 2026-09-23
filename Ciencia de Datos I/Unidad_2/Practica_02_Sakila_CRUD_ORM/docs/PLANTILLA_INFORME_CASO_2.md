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

## Requisitos de la Fase I

Describir y demostrar:

1. Preparacion de MySQL Community Edition y MySQL Workbench.
2. Importacion de la base de datos Sakila.
3. Ejecucion de las diez consultas de `sql/01_fase_i_10_consultas.sql`.
4. CRUD en Python para paises, ciudades, peliculas e inventario.
5. Funciones Create, Read, Update y Delete.
6. Importacion y exportacion de modelos en CSV y JSON.
7. Calculo de media, rango, desviacion estandar, varianza y covarianza.

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

Documentar crear, leer, listar, actualizar y eliminar. Identificar cuales operaciones estan disponibles para cada entidad y explicar cualquier limitacion observada.

## Consultas SQL

Presentar el objetivo y el resultado de las diez consultas incluidas en `sql/01_fase_i_10_consultas.sql`. Incluir al menos una figura de MySQL Workbench y remitir al anexo que contiene el script completo.

## Importacion y exportacion CSV/JSON

Explicar las funciones de `import_export.py`, los modelos utilizados, los archivos generados y el numero de registros procesados. Indicar que estas funciones son una API del codigo y que, en la version actual, no forman parte del menu interactivo.

## Metricas descriptivas

Presentar la media, el rango, la desviacion estandar y la varianza de las variables analizadas. Explicar tambien la covarianza calculada entre longitud, tarifa de alquiler y costo de reemplazo de las peliculas.

## Pruebas y resultados

Agregar capturas o salidas de:

- Conexion exitosa.
- Creacion de pais, ciudad, pelicula o inventario.
- Consulta por ID.
- Actualizacion.
- Eliminacion.
- Metricas descriptivas.
- Diez consultas SQL en MySQL Workbench.
- Exportacion e importacion CSV.
- Exportacion e importacion JSON.
- Unique constraints.

## Conclusiones

Resumir logros, limitaciones y aprendizajes.

## Referencias

[Completar en APA 7 solo con fuentes citadas.]

## Anexos

- Anexo A. Codigo fuente relevante.
- Anexo B. Evidencias de ejecucion.
- Anexo C. Diez consultas SQL.
- Anexo D. Archivos o salidas CSV y JSON.
- Anexo E. Uso de agentes IA.
