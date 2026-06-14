# Caso practico 2: CRUD/ORM nativo con Sakila

Equipo: Mccarthy Team

Asignatura: INF-8237-C2 Ciencia de Datos I

## Objetivo

Crear un CRUD/ORM nativo en Python, basado en programacion orientada a objetos y estructuras de datos, para operar sobre la base de datos MySQL Sakila.

## Fase I cubierta

- MySQL Community Edition y MySQL Workbench, con alternativa reproducible en Docker.
- Importacion de la base de datos Sakila.
- Diez consultas en `sql/01_fase_i_10_consultas.sql`.
- CRUD para `country`, `city`, `film` e `inventory`.
- Funciones Create, Read, Update y Delete.
- Importacion y exportacion CSV/JSON en `src/import_export.py`.
- Media, rango, desviacion estandar, varianza y covarianza en `src/metrics.py` y `src/reports.py`.

Las funciones CSV/JSON estan disponibles para uso programatico, pero todavia no forman parte del menu de consola.

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

La version actual implementa un CRUD/ORM nativo sobre las entidades `country`, `city`, `film` e `inventory`, que coinciden con el enunciado de la practica: ciudades, paises, peliculas e inventario. Tambien permite consultar `store` para seleccionar tiendas validas al crear inventario. La arquitectura separa conexion, entidades, repositorios, controladores, servicios, estructuras de datos y menu de consola.

## Tablas implementadas

- `country`
- `city`
- `film`
- `inventory`
- `store` (consulta)

Tambien se incluyen consultas SQL sobre tablas complementarias de Sakila como `category`, `rental`, `customer`, `store` y `language` para cubrir analisis y evidencias.

## Arquitectura aplicada

- `dbcontext.py`: punto central de acceso a repositorios y estructuras compartidas.
- `models.py`: entidades tipo dataclass y `ModelCollection` como lista de entidades.
- `repositories.py`: operaciones CRUD genericas y repositorios concretos.
- `controllers.py`: capa de controladores para el flujo tipo MVC.
- `services.py`: servicio de aplicacion que conecta contexto y controladores.
- `structures.py`: cache por entidad e historial de operaciones.
- `metrics.py` y `reports.py`: metricas descriptivas y covarianza sobre peliculas.
- `import_export.py`: importacion y exportacion CSV/JSON.
- `main.py`: menu de consola para ejecutar la demostracion.

## Estructura sugerida

```text
caso_practico_2_sakila_crud_orm/
  README.md
  src/
    config.py
    db.py
    dbcontext.py
    models.py
    repositories.py
    controllers.py
    services.py
    structures.py
    metrics.py
    reports.py
    import_export.py
    main.py
  sql/
  tests/
  docs/
    informe/
```

## Ejecucion recomendada con Docker

Usar el archivo correspondiente al sistema operativo:

Mac:

```bash
chmod +x MAC_SH_QUICKSTART.sh
./MAC_SH_QUICKSTART.sh
```

Linux:

```bash
chmod +x LINUX_SH_QUICKSTART.sh
./LINUX_SH_QUICKSTART.sh
```

Windows PowerShell:

```powershell
.\WINDOWS_QUICKSTART.ps1
```

Todos estos archivos preparan MySQL/Sakila con Docker, prueban la conexion y abren el menu CRUD/ORM.

Archivo base compartido por Mac y Linux:

```bash
cd caso_practico_2_sakila_crud_orm
python3 -m pip install -r requirements.txt
chmod +x setup_run_sakila_docker.sh
./setup_run_sakila_docker.sh
```

El script crea o inicia un contenedor `sakila-mysql`, importa Sakila si hace falta, configura variables de entorno y abre el menu CRUD/ORM.

Credenciales por defecto del entorno Docker:

```text
Host: 127.0.0.1
Puerto: 3307
Usuario: root
Password: sakila123
Base de datos: sakila
```

## Ejecucion manual

Si el contenedor ya existe o se usa otro MySQL compatible:

```bash
export SAKILA_DB_HOST=127.0.0.1
export SAKILA_DB_PORT=3307
export SAKILA_DB_USER=root
export SAKILA_DB_PASSWORD=sakila123
export SAKILA_DB_NAME=sakila

python3 -m src.check_connection
python3 -m src.main
```

## Quick start clasico

Para ejecutar instalacion, compilacion, pruebas, verificacion de conexion y menu CRUD en un solo flujo con credenciales ya configuradas:

```bash
cd caso_practico_2_sakila_crud_orm
chmod +x quick_start.sh
./quick_start.sh
```

El script usa rutas relativas y no contiene rutas internas de ninguna computadora.

## Verificacion de conexion

Antes de correr el menu CRUD, verificar que MySQL este activo y que Sakila exista:

```bash
python3 -m src.check_connection
```

Si aparece `Can't connect to MySQL server on 'localhost:3306'`, el problema no es el codigo Python. Significa que MySQL no esta encendido, no esta usando el puerto 3306, o Sakila/credenciales no estan configuradas.

Checklist:

- MySQL Community Server instalado.
- MySQL Workbench instalado.
- Servicio MySQL iniciado.
- Base de datos `sakila` importada.
- Variables de entorno `SAKILA_DB_USER` y `SAKILA_DB_PASSWORD` configuradas.
- Usuario con permisos sobre `sakila`.

## Pruebas

Desde `CienciaDatosUasd2026/Unidad_2/Practica_02_Sakila_CRUD_ORM/`:

```bash
python3 -m pytest caso_practico_2_sakila_crud_orm/tests
```

Las pruebas actuales cubren estructuras de datos. Las pruebas de integracion con MySQL deben ejecutarse cuando Sakila este disponible.

## Registro local de ejecuciones

Los quickstarts de Mac y Linux guardan automaticamente la salida de cada ejecucion en `../evidencias_locales/`, usando fecha y un identificador aleatorio. Los registros se sanitizan para ocultar contrasenas, tokens y secretos conocidos.

Para registrar manualmente otro comando desde la raiz del proyecto:

```bash
python3 scripts/ejecutar_con_evidencia.py -- python3 -m pytest caso_practico_2_sakila_crud_orm/tests
```

La carpeta `evidencias_locales/` esta incluida en `.gitignore`. Su contenido es privado y no se sube a GitHub.

## Checklist APA/UASD

- Presentacion.
- Resumen.
- Abstract.
- Tabla de contenido.
- Desarrollo de 5 a 10 paginas.
- Citas narrativa, parentetica y textual directa.
- Referencias solo con fuentes citadas.
- Anexos con evidencias, si aplica.
