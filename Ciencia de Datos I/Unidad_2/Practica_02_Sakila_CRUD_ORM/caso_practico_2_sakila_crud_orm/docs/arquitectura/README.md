# Arquitectura - Caso practico 2

## Componentes

- `src/config.py`: lee configuracion desde variables de entorno.
- `src/db.py`: administra conexion, cursores, commit y rollback.
- `src/models.py`: define entidades Python para tablas Sakila.
- `src/repositories.py`: implementa CRUD generico.
- `src/services.py`: valida reglas de negocio antes del repositorio.
- `src/structures.py`: evidencia estructuras de datos como cache e historial.
- `src/main.py`: interfaz de consola para demostracion.

## Decision tecnica

El ORM es nativo y limitado a operaciones CRUD basicas. No usa SQLAlchemy, Django ORM ni Peewee. Esto mantiene el proyecto alineado con la solicitud de construir la capa objeto-relacional de forma manual.

