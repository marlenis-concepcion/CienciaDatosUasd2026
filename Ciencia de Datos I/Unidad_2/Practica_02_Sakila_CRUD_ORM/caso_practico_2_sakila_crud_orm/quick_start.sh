#!/usr/bin/env bash
set -euo pipefail

echo "Quick start - Caso practico 2 Sakila CRUD/ORM"
echo

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 no esta instalado o no esta en PATH."
  exit 1
fi

echo "1. Instalando dependencias..."
python3 -m pip install -r requirements.txt

echo
echo "2. Verificando sintaxis Python..."
python3 -m compileall src

echo
echo "3. Ejecutando pruebas unitarias disponibles..."
python3 -m pytest tests

echo
echo "4. Verificando conexion a MySQL Sakila..."
echo "   Si este paso falla, revise que MySQL este encendido, Sakila importada y credenciales configuradas."
python3 -m src.check_connection

echo
echo "5. Iniciando menu CRUD/ORM..."
python3 -m src.main

