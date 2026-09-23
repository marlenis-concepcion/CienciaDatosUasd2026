#!/bin/bash

# ============================================================================
# GITHUB UPLOAD SCRIPT - Caso Práctico 2 OULAD
# ============================================================================
# Este script prepara y sube el proyecto a GitHub
# ============================================================================

set -e  # Exit on error

echo "════════════════════════════════════════════════════════════════════"
echo "  GITHUB UPLOAD - Caso Práctico 2: OULAD en Base de Datos"
echo "════════════════════════════════════════════════════════════════════"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ============================================================================
# STEP 1: Verificar que no hay rutas con vampy
# ============================================================================
echo "${YELLOW}[1/5]${NC} Verificando que NO hay rutas personales (vampy)..."
if grep -r "vampy" --include="*.py" --include="*.sh" --include="*.md" --include="*.txt" \
    --exclude-dir=".git" --exclude-dir=".venv" --exclude-dir="outputs" . 2>/dev/null; then
    echo "${RED}❌ ERROR: Aún hay referencias a 'vampy' en los archivos${NC}"
    echo "Por favor, revisa y reemplaza antes de subir a GitHub"
    exit 1
else
    echo "${GREEN}✅ Ninguna referencia a 'vampy' encontrada${NC}"
fi
echo ""

# ============================================================================
# STEP 2: Verificar Git
# ============================================================================
echo "${YELLOW}[2/5]${NC} Verificando Git..."
if ! command -v git &> /dev/null; then
    echo "${RED}❌ Git no está instalado${NC}"
    echo "Instala con: brew install git"
    exit 1
fi
echo "${GREEN}✅ Git disponible${NC}"
echo ""

# ============================================================================
# STEP 3: Inicializar repositorio (si no existe)
# ============================================================================
echo "${YELLOW}[3/5]${NC} Preparando repositorio Git..."
if [ ! -d ".git" ]; then
    echo "Inicializando nuevo repositorio..."
    git init
    git config user.name "Marlenis Judith Concepción Cuevas"
    git config user.email "marlenis.concepci@gmail.com"
fi
echo "${GREEN}✅ Repositorio listo${NC}"
echo ""

# ============================================================================
# STEP 4: Agregar archivos
# ============================================================================
echo "${YELLOW}[4/5]${NC} Agregando archivos (respetando .gitignore)..."
git add -A
git status --short
echo "${GREEN}✅ Archivos preparados${NC}"
echo ""

# ============================================================================
# STEP 5: Hacer commit
# ============================================================================
echo "${YELLOW}[5/5]${NC} Haciendo commit..."
COMMIT_MSG="Caso Práctico 2: OULAD en Base de Datos - Schema DDL, ETL, EDA extendido, Paper APA"
git commit -m "$COMMIT_MSG" || echo "Nada nuevo para commitear"
echo "${GREEN}✅ Commit listo${NC}"
echo ""

# ============================================================================
# INFORMACIÓN PARA GITHUB
# ============================================================================
echo "════════════════════════════════════════════════════════════════════"
echo "  ${GREEN}SIGUIENTE PASO: AGREGAR REMOTE Y HACER PUSH${NC}"
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "1. Ve a GitHub: https://github.com/new"
echo ""
echo "2. Crea repositorio con estos datos:"
echo "   • Nombre: CienciaDatosUasd2026"
echo "   • Descripción: Ciencia de Datos I - UASD Caso Práctico 2 OULAD"
echo "   • Visibilidad: Public"
echo "   • NO inicialices con README (ya tenemos uno)"
echo ""
echo "3. Luego ejecuta:"
echo ""
echo "   ${YELLOW}git remote add origin https://github.com/[TU-USUARIO]/CienciaDatosUasd2026.git${NC}"
echo "   ${YELLOW}git branch -M main${NC}"
echo "   ${YELLOW}git push -u origin main${NC}"
echo ""
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "${GREEN}✅ LISTO PARA SUBIR A GITHUB${NC}"
echo ""
echo "Directorio actual: $(pwd)"
echo "Commits pendientes para push: $(git rev-list --count origin/main..HEAD 2>/dev/null || echo '1')"
echo ""
