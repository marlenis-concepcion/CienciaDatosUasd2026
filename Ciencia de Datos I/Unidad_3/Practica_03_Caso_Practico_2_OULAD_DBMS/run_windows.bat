@echo off
REM ============================================================================
REM OULAD ETL Pipeline - Windows Batch Setup & Execution Script
REM Caso Práctico 2 - Ciencia de Datos I (UASD)
REM
REM Uso:
REM   run_windows.bat                    # Ejecutar completo
REM   run_windows.bat --skip-postgres    # Sin BD
REM   run_windows.bat --help             # Ver ayuda
REM ============================================================================

setlocal enabledelayedexpansion

REM Colors and formatting
set "BLUE=[94m"
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "RESET=[0m"

REM Get script directory
set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%.venv"

REM ============================================================================
REM Functions
REM ============================================================================

:print_header
cls
echo.
echo ============================================================================
echo %~1
echo ============================================================================
echo.
goto :eof

:print_success
echo [+] %~1
goto :eof

:print_error
echo [-] %~1
goto :eof

:print_info
echo [*] %~1
goto :eof

:show_help
cls
echo.
echo ============================================================================
echo           OULAD ETL Pipeline - Windows
echo ============================================================================
echo.
echo USO:
echo   run_windows.bat [OPCION]
echo.
echo OPCIONES:
echo   (sin opciones)     Ejecutar pipeline completo (requiere PostgreSQL)
echo   --skip-postgres    Ejecutar EDA sin BD (MAS RAPIDO - RECOMENDADO)
echo   --venv-only        Solo crear ambiente virtual
echo   --help             Mostrar esta ayuda
echo.
echo EJEMPLOS:
echo   run_windows.bat                    # Ejecucion completa
echo   run_windows.bat --skip-postgres    # Sin BD (recomendado)
echo   run_windows.bat --venv-only        # Solo venv
echo.
echo REQUISITOS:
echo   - Python 3.8+ instalado
echo   - PostgreSQL 12+ (solo si no usas --skip-postgres)
echo.
echo DOCUMENTACION:
echo   - QUICKSTART.md         - Inicio rapido
echo   - CASO_PRACTICO_2.md    - Guia completa
echo   - GUIA_COLABORACION.md  - Trabajo en equipo
echo.
goto :eof

:check_python
call :print_info "Verificando Python..."
python --version >nul 2>&1
if errorlevel 1 (
    call :print_error "Python no encontrado. Instala Python 3.8+ desde python.org"
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
call :print_success "Python %PYTHON_VERSION% encontrado"
goto :eof

:create_venv
call :print_header "Paso 1: Crear Ambiente Virtual"
if exist "%VENV_DIR%" (
    call :print_info "Ambiente virtual ya existe. Actualizando..."
) else (
    call :print_info "Creando ambiente virtual..."
    python -m venv "%VENV_DIR%"
    call :print_success "Ambiente virtual creado"
)
goto :eof

:activate_venv
call :print_info "Activando ambiente virtual..."
call "%VENV_DIR%\Scripts\activate.bat"
call :print_success "Ambiente virtual activado"
goto :eof

:install_dependencies
call :print_header "Paso 2: Instalar Dependencias"
call :print_info "Actualizando pip..."
python -m pip install --upgrade pip setuptools wheel >nul 2>&1

call :print_info "Instalando dependencias..."
if not exist "%SCRIPT_DIR%requirements.txt" (
    call :print_error "Archivo requirements.txt no encontrado"
    exit /b 1
)
pip install -r "%SCRIPT_DIR%requirements.txt"
call :print_success "Dependencias instaladas"
goto :eof

:run_etl_skip_postgres
call :print_header "Paso 3: Ejecutar Pipeline (sin PostgreSQL)"
call :print_info "Iniciando ETL (saltando carga a BD)..."
cd /d "%SCRIPT_DIR%"
python etl_orchestrator.py --skip-postgres
if errorlevel 1 (
    call :print_error "Error durante la ejecucion"
    exit /b 1
)
goto :eof

:run_etl_full
call :print_header "Paso 3: Ejecutar Pipeline Completo (con PostgreSQL)"
call :print_info "Verificando PostgreSQL..."
where psql >nul 2>&1
if errorlevel 1 (
    call :print_error "PostgreSQL no esta instalado o no esta en PATH"
    call :print_info "Usa: run_windows.bat --skip-postgres"
    exit /b 1
)
call :print_success "PostgreSQL encontrado"

call :print_info "Iniciando pipeline ETL..."
cd /d "%SCRIPT_DIR%"
python etl_orchestrator.py
if errorlevel 1 (
    call :print_error "Error durante la ejecucion"
    exit /b 1
)
goto :eof

:verify_outputs
call :print_header "Verificacion de Salidas"
set "OUTPUTS_DIR=%SCRIPT_DIR%outputs"

if not exist "%OUTPUTS_DIR%" (
    call :print_error "Directorio outputs/ no encontrado"
    goto :eof
)

call :print_info "Verificando archivos generados..."
for /r "%OUTPUTS_DIR%" %%f in (*.png) do (
    call :print_success "PNG encontrado: %%~nxf"
)
for /r "%OUTPUTS_DIR%" %%f in (*.csv) do (
    call :print_success "CSV encontrado: %%~nxf"
)

set "DOC=%SCRIPT_DIR%docs\Articulo_Cientifico_OULAD_APA7.docx"
if exist "%DOC%" (
    call :print_success "Articulo APA generado"
) else (
    call :print_info "Articulo APA sera generado"
)
goto :eof

:print_summary
call :print_header "Resumen de Ejecucion"
echo.
echo COMPONENTES GENERADOS:
echo   [+] Datos OULAD descargados
echo   [+] Analisis exploratorio ^(EDA^)
echo   [+] Visualizaciones ^(PNG^)
echo   [+] Analisis estadisticos ^(CSV^)
echo   [+] Articulo cientifico APA
echo.
echo PROXIMOS PASOS:
echo   1. Revisar outputs en: %SCRIPT_DIR%outputs\
echo   2. Abrir: %SCRIPT_DIR%docs\Articulo_Cientifico_OULAD_APA7.docx
echo   3. Grabar video colaborativo ^(2-5 min^)
echo   4. Insertar enlace video en documento
echo   5. Empaquetar y enviar antes del 20 junio 23:59
echo.
echo DOCUMENTACION:
echo   - QUICKSTART.md         - Inicio rapido
echo   - CASO_PRACTICO_2.md    - Guia completa
echo   - GUIA_COLABORACION.md  - Trabajo en equipo
echo.
goto :eof

REM ============================================================================
REM Main
REM ============================================================================

:main
setlocal enabledelayedexpansion

set SKIP_POSTGRES=false
set VENV_ONLY=false

REM Parse arguments
:parse_args
if "%~1"=="" goto start_execution
if "%~1"=="--skip-postgres" (
    set SKIP_POSTGRES=true
    goto next_arg
)
if "%~1"=="--venv-only" (
    set VENV_ONLY=true
    goto next_arg
)
if "%~1"=="--help" (
    call :show_help
    exit /b 0
)

call :print_error "Opcion desconocida: %~1"
call :show_help
exit /b 1

:next_arg
shift
goto parse_args

:start_execution
cls
echo.
echo ============================================================================
echo.
echo                   OULAD ETL Pipeline - Windows
echo                   Caso Practico 2 - Ciencia de Datos I
echo.
echo              Data Loading ^-^> Database ^-^> EDA ^-^> Scientific Paper
echo.
echo ============================================================================
echo.

call :check_python
if errorlevel 1 exit /b 1

call :create_venv
call :activate_venv
call :install_dependencies

if "%VENV_ONLY%"=="true" (
    call :print_success "Ambiente virtual listo"
    call :print_info "Proximo paso: python etl_orchestrator.py"
    exit /b 0
)

if "%SKIP_POSTGRES%"=="true" (
    call :run_etl_skip_postgres
) else (
    call :run_etl_full
)

if errorlevel 1 (
    call :print_error "Error en la ejecucion del pipeline"
    exit /b 1
)

call :verify_outputs
call :print_summary

call :print_success "Pipeline completado exitosamente!"
echo.
pause

endlocal
goto :eof
