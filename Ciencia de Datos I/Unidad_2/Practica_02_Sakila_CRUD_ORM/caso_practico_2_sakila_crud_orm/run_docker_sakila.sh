#!/usr/bin/env bash
set -euo pipefail

export SAKILA_DB_HOST="${SAKILA_DB_HOST:-127.0.0.1}"
export SAKILA_DB_PORT="${SAKILA_DB_PORT:-3307}"
export SAKILA_DB_USER="${SAKILA_DB_USER:-root}"
export SAKILA_DB_PASSWORD="${SAKILA_DB_PASSWORD:-sakila123}"
export SAKILA_DB_NAME="${SAKILA_DB_NAME:-sakila}"

python3 -m src.check_connection
python3 -m src.main
