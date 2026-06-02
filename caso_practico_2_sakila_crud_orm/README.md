# Caso practico 2: CRUD/ORM nativo con Sakila

Equipo: UASDVirtual

Asignatura: INF-8237-C2 Ciencia de Datos I

## Objetivo

Crear un CRUD/ORM nativo en Python, basado en programacion orientada a objetos y estructuras de datos, para operar sobre la base de datos MySQL Sakila.

## Entregables

- Codigo fuente del CRUD/ORM nativo.
- Script o notebook de demostracion con operaciones CRUD.
- Evidencias de ejecucion: capturas, logs o salida documentada.
- Informe academico en formato APA 7/UASD.

## Alcance tecnico propuesto

- Conexion a MySQL usando un conector Python.
- Clases de dominio para tablas seleccionadas de Sakila.
- Repositorios o managers para operaciones CRUD.
- Uso explicito de estructuras de datos en Python: listas, colas, pilas o diccionarios segun aplique.
- Validaciones basicas antes de insertar o actualizar registros.
- Manejo de errores de conexion, consultas y datos invalidos.

## Decision de implementacion inicial

La primera version incluida en `src/` implementa el CRUD de `actor`, porque es una tabla adecuada para demostrar insercion, consulta, actualizacion y eliminacion sin depender de relaciones complejas. La clase `Customer` queda preparada como segunda entidad para extender la entrega.

## Tablas sugeridas

- `actor`
- `film`
- `category`
- `customer`
- `rental`

La seleccion final puede ajustarse segun tiempo, acceso a MySQL y requisitos del profesor.

## Estructura sugerida

```text
caso_practico_2_sakila_crud_orm/
  README.md
  src/
    config.py
    db.py
    models.py
    repositories.py
    structures.py
    main.py
  tests/
  docs/
    informe/
    evidencias/
```

## Ejecucion sugerida

```bash
cd caso_practico_2_sakila_crud_orm
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SAKILA_DB_USER=sakila_app
export SAKILA_DB_PASSWORD=tu_password
python -m src.main
```

Tambien puede copiarse `../.env.example` a `../.env` y completar credenciales. No subir archivos `.env`.

## Pruebas

Desde `Unidad_2_UASDVirtual/`:

```bash
python -m pytest caso_practico_2_sakila_crud_orm/tests
```

Las pruebas actuales cubren estructuras de datos. Las pruebas de integracion con MySQL deben ejecutarse cuando Sakila este disponible.

## Checklist APA/UASD

- Presentacion.
- Resumen.
- Abstract.
- Tabla de contenido.
- Desarrollo de 5 a 10 paginas.
- Citas narrativa, parentetica y textual directa.
- Referencias solo con fuentes citadas.
- Anexos con evidencias, si aplica.
