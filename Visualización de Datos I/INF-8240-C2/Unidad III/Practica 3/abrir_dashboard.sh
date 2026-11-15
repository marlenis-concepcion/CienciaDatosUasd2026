#!/bin/sh
# Inicia el dashboard web en Docker y lo abre en el navegador.
cd "$(dirname "$0")" || exit 1
docker info >/dev/null 2>&1 || { open -a Docker; echo "Iniciando Docker..."; until docker info >/dev/null 2>&1; do sleep 2; done; }
docker compose up --build -d || exit 1
echo "Esperando a que el dashboard responda..."
until curl -fs http://localhost:8501/_stcore/health >/dev/null; do sleep 1; done
open http://localhost:8501
echo "Dashboard abierto en http://localhost:8501  (para cerrarlo: ./cerrar_dashboard.sh)"
