#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Quickstart Linux - Sakila CRUD/ORM"
echo "Requisitos: Docker activo, permisos para usar docker y Python 3 instalado."
echo

chmod +x setup_run_sakila_docker.sh
python3 ../scripts/ejecutar_con_evidencia.py -- ./setup_run_sakila_docker.sh
