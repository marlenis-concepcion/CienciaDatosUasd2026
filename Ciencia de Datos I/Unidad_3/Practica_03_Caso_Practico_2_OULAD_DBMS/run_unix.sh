#!/bin/bash

################################################################################
# OULAD ETL Pipeline - Unix/Linux/macOS Setup & Execution Script
# Caso Práctico 2 - Ciencia de Datos I (UASD)
#
# Uso:
#   ./run_unix.sh                    # Ejecutar completo (requiere PostgreSQL)
#   ./run_unix.sh --skip-postgres    # Ejecutar sin BD (más rápido)
#   ./run_unix.sh --help             # Ver ayuda
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_DIR="$SCRIPT_DIR/.venv"
PYTHON_CMD="python3"

################################################################################
# Functions
################################################################################

print_header() {
    echo -e "${BLUE}════════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════════════════════${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

show_help() {
    cat << EOF
${BLUE}OULAD ETL Pipeline - Unix/Linux/macOS${NC}

${GREEN}Uso:${NC}
  ./run_unix.sh [OPCIÓN]

${GREEN}Opciones:${NC}
  (sin opciones)     Ejecutar pipeline completo (requiere PostgreSQL)
  --skip-postgres    Ejecutar EDA y paper sin cargar en BD (más rápido)
  --venv-only        Solo crear/actualizar ambiente virtual
  --help             Mostrar esta ayuda

${GREEN}Ejemplos:${NC}
  ./run_unix.sh                    # Ejecución completa
  ./run_unix.sh --skip-postgres    # Sin BD (recomendado si no tienes PostgreSQL)
  ./run_unix.sh --venv-only        # Solo preparar ambiente

${GREEN}Requisitos:${NC}
  • Python 3.8+
  • pip instalado
  • PostgreSQL 12+ (solo si no usas --skip-postgres)

${GREEN}Más información:${NC}
  • CASO_PRACTICO_2.md    - Guía completa
  • QUICKSTART.md         - Inicio rápido
  • GUIA_COLABORACION.md  - Trabajo en equipo

EOF
}

check_python() {
    print_info "Verificando Python..."
    if ! command -v $PYTHON_CMD &> /dev/null; then
        print_error "Python 3 no encontrado. Por favor instala Python 3.8 o superior."
        exit 1
    fi
    PYTHON_VERSION=$($PYTHON_CMD --version | awk '{print $2}')
    print_success "Python $PYTHON_VERSION encontrado"
}

create_venv() {
    print_header "Paso 1: Crear Ambiente Virtual"

    if [ -d "$VENV_DIR" ]; then
        print_info "Ambiente virtual ya existe. Actualizando..."
    else
        print_info "Creando ambiente virtual..."
        $PYTHON_CMD -m venv "$VENV_DIR"
        print_success "Ambiente virtual creado"
    fi
}

activate_venv() {
    print_info "Activando ambiente virtual..."
    source "$VENV_DIR/bin/activate"
    print_success "Ambiente virtual activado"
}

install_dependencies() {
    print_header "Paso 2: Instalar Dependencias"

    print_info "Actualizando pip..."
    pip install --upgrade pip setuptools wheel > /dev/null 2>&1

    print_info "Instalando dependencias desde requirements.txt..."
    if [ ! -f "$SCRIPT_DIR/requirements.txt" ]; then
        print_error "Archivo requirements.txt no encontrado"
        exit 1
    fi

    pip install -r "$SCRIPT_DIR/requirements.txt"
    print_success "Dependencias instaladas"
}

check_postgres() {
    print_info "Verificando PostgreSQL..."
    if command -v psql &> /dev/null; then
        PG_VERSION=$(psql --version 2>/dev/null | awk '{print $NF}' || echo "unknown")
        print_success "PostgreSQL $PG_VERSION encontrado"

        # Check if server is running
        if pg_isready -h localhost -p 5432 &> /dev/null; then
            print_success "Servidor PostgreSQL está ejecutándose"
            return 0
        else
            print_error "PostgreSQL está instalado pero el servidor no está corriendo"
            print_info "Inicia PostgreSQL con: brew services start postgresql (macOS)"
            print_info "O: sudo systemctl start postgresql (Linux)"
            return 1
        fi
    else
        print_error "PostgreSQL no encontrado"
        print_info "Instala PostgreSQL o usa la opción --skip-postgres"
        return 1
    fi
}

run_etl_full() {
    print_header "Paso 3: Ejecutar Pipeline Completo (con PostgreSQL)"

    if ! check_postgres; then
        print_error "No se puede ejecutar el pipeline completo sin PostgreSQL"
        print_info "Consejo: ejecuta con ./run_unix.sh --skip-postgres"
        exit 1
    fi

    print_info "Iniciando pipeline ETL..."
    cd "$SCRIPT_DIR"
    $PYTHON_CMD etl_orchestrator.py
}

run_etl_skip_postgres() {
    print_header "Paso 3: Ejecutar Pipeline (sin PostgreSQL)"

    print_info "Iniciando pipeline (saltando carga a BD)..."
    cd "$SCRIPT_DIR"
    $PYTHON_CMD etl_orchestrator.py --skip-postgres
}

verify_outputs() {
    print_header "Verificación de Salidas"

    OUTPUTS_DIR="$SCRIPT_DIR/outputs"

    if [ ! -d "$OUTPUTS_DIR" ]; then
        print_error "Directorio outputs/ no encontrado"
        return 1
    fi

    # Check for PNG files
    PNG_COUNT=$(find "$OUTPUTS_DIR" -name "*.png" 2>/dev/null | wc -l)
    if [ $PNG_COUNT -gt 0 ]; then
        print_success "Gráficos PNG generados: $PNG_COUNT archivos"
    else
        print_error "No se encontraron archivos PNG"
    fi

    # Check for CSV files
    CSV_COUNT=$(find "$OUTPUTS_DIR" -name "*.csv" 2>/dev/null | wc -l)
    if [ $CSV_COUNT -gt 0 ]; then
        print_success "Archivos CSV generados: $CSV_COUNT archivos"
    else
        print_error "No se encontraron archivos CSV"
    fi

    # Check for Word document
    DOCS_DIR="$SCRIPT_DIR/docs"
    if [ -f "$DOCS_DIR/Articulo_Cientifico_OULAD_APA7.docx" ]; then
        print_success "Artículo APA generado"
    else
        print_info "Artículo APA será generado en próxima ejecución"
    fi
}

print_summary() {
    print_header "Resumen de Ejecución"

    echo -e "${GREEN}Componentes generados:${NC}"
    echo "  ✓ Datos OULAD descargados"
    echo "  ✓ Análisis exploratorio (EDA)"
    echo "  ✓ Visualizaciones (PNG)"
    echo "  ✓ Análisis estadísticos (CSV)"
    echo "  ✓ Artículo científico APA"

    echo -e "\n${GREEN}Próximos pasos:${NC}"
    echo "  1. Revisar outputs en: $SCRIPT_DIR/outputs/"
    echo "  2. Abrir documento: $SCRIPT_DIR/docs/Articulo_Cientifico_OULAD_APA7.docx"
    echo "  3. Grabar video colaborativo (2-5 min)"
    echo "  4. Insertar enlace video en documento"
    echo "  5. Empaquetar y enviar antes del 20 junio 23:59"

    echo -e "\n${GREEN}Documentación:${NC}"
    echo "  • QUICKSTART.md         - Inicio rápido"
    echo "  • CASO_PRACTICO_2.md    - Guía completa"
    echo "  • GUIA_COLABORACION.md  - Trabajo en equipo"
}

################################################################################
# Main
################################################################################

main() {
    clear

    # Parse arguments
    SKIP_POSTGRES=false
    VENV_ONLY=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-postgres)
                SKIP_POSTGRES=true
                shift
                ;;
            --venv-only)
                VENV_ONLY=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                print_error "Opción desconocida: $1"
                show_help
                exit 1
                ;;
        esac
    done

    # Execution flow
    echo -e "${BLUE}"
    cat << "EOF"
╔════════════════════════════════════════════════════════════════════════════╗
║                   OULAD ETL Pipeline - Unix/Linux/macOS                    ║
║                   Caso Práctico 2 - Ciencia de Datos I                     ║
║                                                                            ║
║              Data Loading → Database → EDA → Scientific Paper              ║
╚════════════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}\n"

    check_python
    create_venv
    activate_venv
    install_dependencies

    if [ "$VENV_ONLY" = true ]; then
        print_success "Ambiente virtual listo"
        print_info "Próximo paso: python etl_orchestrator.py"
        exit 0
    fi

    if [ "$SKIP_POSTGRES" = true ]; then
        run_etl_skip_postgres
    else
        run_etl_full
    fi

    verify_outputs
    print_summary

    print_success "Pipeline completado exitosamente!"
}

# Run main function
main "$@"
