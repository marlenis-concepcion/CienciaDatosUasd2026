# Runbook de ejecucion - Fase I del Caso practico 2

Este runbook resume los pasos operativos para correr el CRUD/ORM nativo con MySQL Sakila y generar evidencias.

## Requisitos de la Fase I

- MySQL Community Edition y MySQL Workbench, o Docker Desktop como entorno reproducible.
- Base de datos Sakila.
- Python 3.
- Diez consultas SQL.
- CRUD de paises, ciudades, peliculas e inventario.
- Importacion/exportacion CSV y JSON.
- Metricas descriptivas y covarianza.

## Vista general

Abrir la pagina visual del Caso 2:

```bash
cd CienciaDatosUasd2026/Unidad_2/Practica_02_Sakila_CRUD_ORM
open index.html
```

## Preparacion general

```bash
cd CienciaDatosUasd2026/Unidad_2/Practica_02_Sakila_CRUD_ORM
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
```

## Sakila CRUD/ORM

Desde la carpeta del caso:

Mac:

```bash
cd CienciaDatosUasd2026/Unidad_2/Practica_02_Sakila_CRUD_ORM/caso_practico_2_sakila_crud_orm
chmod +x MAC_SH_QUICKSTART.sh
./MAC_SH_QUICKSTART.sh
```

Linux:

```bash
cd CienciaDatosUasd2026/Unidad_2/Practica_02_Sakila_CRUD_ORM/caso_practico_2_sakila_crud_orm
chmod +x LINUX_SH_QUICKSTART.sh
./LINUX_SH_QUICKSTART.sh
```

Windows PowerShell:

```powershell
cd CienciaDatosUasd2026/Unidad_2/Practica_02_Sakila_CRUD_ORM\caso_practico_2_sakila_crud_orm
.\WINDOWS_QUICKSTART.ps1
```

Script base:

```bash
cd CienciaDatosUasd2026/Unidad_2/Practica_02_Sakila_CRUD_ORM/caso_practico_2_sakila_crud_orm
python3 -m pip install -r requirements.txt
chmod +x setup_run_sakila_docker.sh
./setup_run_sakila_docker.sh
```

El script realiza:

- Verificacion de Docker.
- Creacion o inicio del contenedor `sakila-mysql`.
- Importacion de Sakila cuando la base no tiene tablas.
- Exportacion de variables `SAKILA_DB_*`.
- Prueba de conexion.
- Apertura del menu CRUD/ORM.
- Registro local de la salida con un nombre aleatorio.

En el menu:

- Las opciones `1` a `4` permiten demostrar el CRUD.
- La opcion `5` permite buscar y listar tiendas.
- La opcion `6` calcula las metricas descriptivas.
- La opcion `7` muestra el historial de operaciones.

## Diez consultas SQL

Abrir MySQL Workbench, conectarse a Sakila y ejecutar:

```text
caso_practico_2_sakila_crud_orm/sql/01_fase_i_10_consultas.sql
```

Guardar una captura de los resultados. El archivo contiene consultas de paises, ciudades, peliculas, inventario, categorias, tiendas, clientes, rentas y metricas SQL.

## CSV y JSON

Las funciones se encuentran en:

```text
caso_practico_2_sakila_crud_orm/src/import_export.py
```

La version actual las ofrece como API de Python mediante `export_to_csv`, `import_from_csv`, `export_to_json` e `import_from_json`. Todavia no estan integradas como opcion del menu; su ejecucion puede registrarse con el recolector local.

Credenciales por defecto:

```text
Host: 127.0.0.1
Puerto: 3307
Usuario: root
Password: sakila123
Base: sakila
```

Comprobacion manual:

```bash
export SAKILA_DB_HOST=127.0.0.1
export SAKILA_DB_PORT=3307
export SAKILA_DB_USER=root
export SAKILA_DB_PASSWORD=sakila123
export SAKILA_DB_NAME=sakila
python3 -m src.check_connection
python3 -m src.main
```

## Registros locales

Para guardar la salida de cualquier comando:

```bash
python3 scripts/ejecutar_con_evidencia.py -- COMANDO
```

Cada registro se guarda con fecha y un identificador aleatorio en `evidencias_locales/`. El recolector elimina secuencias de color y redacta contrasenas, tokens y secretos conocidos antes de escribir el archivo.

`evidencias_locales/` esta excluido por `.gitignore`; no debe forzarse su inclusion ni publicarse en GitHub.

Pruebas:

```bash
cd CienciaDatosUasd2026/Unidad_2/Practica_02_Sakila_CRUD_ORM
python3 scripts/ejecutar_con_evidencia.py -- python3 -m pytest caso_practico_2_sakila_crud_orm/tests
```
