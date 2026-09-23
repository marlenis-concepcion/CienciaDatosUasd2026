#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${CONTAINER_NAME:-sakila-mysql}"
MYSQL_IMAGE="${MYSQL_IMAGE:-mysql:8.0}"
MYSQL_ROOT_PASSWORD="${MYSQL_ROOT_PASSWORD:-sakila123}"
MYSQL_DATABASE="${MYSQL_DATABASE:-sakila}"
MYSQL_PORT="${MYSQL_PORT:-3307}"
SAKILA_ZIP_URL="${SAKILA_ZIP_URL:-https://downloads.mysql.com/docs/sakila-db.zip}"
SAKILA_DIR="${SAKILA_DIR:-/tmp/sakila-db}"
SAKILA_ZIP="${SAKILA_ZIP:-/tmp/sakila-db.zip}"

info() {
  printf "\n==> %s\n" "$1"
}

if ! command -v docker >/dev/null 2>&1; then
  echo "Error: Docker no esta instalado o no esta en PATH."
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 no esta instalado o no esta en PATH."
  exit 1
fi

info "Verificando Docker"
docker info >/dev/null

if docker ps -a --format '{{.Names}}' | grep -qx "$CONTAINER_NAME"; then
  if ! docker ps --format '{{.Names}}' | grep -qx "$CONTAINER_NAME"; then
    info "Iniciando contenedor $CONTAINER_NAME"
    docker start "$CONTAINER_NAME" >/dev/null
  else
    info "El contenedor $CONTAINER_NAME ya esta corriendo"
  fi
else
  info "Creando contenedor MySQL $CONTAINER_NAME en puerto $MYSQL_PORT"
  docker run \
    --name "$CONTAINER_NAME" \
    -e MYSQL_ROOT_PASSWORD="$MYSQL_ROOT_PASSWORD" \
    -e MYSQL_DATABASE="$MYSQL_DATABASE" \
    -p "$MYSQL_PORT:3306" \
    -d "$MYSQL_IMAGE" >/dev/null
fi

info "Esperando a que MySQL este listo"
until docker exec "$CONTAINER_NAME" mysqladmin ping -uroot -p"$MYSQL_ROOT_PASSWORD" >/dev/null 2>&1; do
  sleep 2
done

TABLE_COUNT="$(
  docker exec "$CONTAINER_NAME" mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -Nse \
    "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '$MYSQL_DATABASE';" 2>/dev/null
)"

if [ "$TABLE_COUNT" -lt 10 ]; then
  info "Importando base de datos Sakila"
  if [ ! -f "$SAKILA_DIR/sakila-schema.sql" ] || [ ! -f "$SAKILA_DIR/sakila-data.sql" ]; then
    info "Descargando Sakila oficial"
    curl -L "$SAKILA_ZIP_URL" -o "$SAKILA_ZIP"
    unzip -o "$SAKILA_ZIP" -d /tmp
  fi

  docker cp "$SAKILA_DIR/sakila-schema.sql" "$CONTAINER_NAME:/tmp/sakila-schema.sql"
  docker cp "$SAKILA_DIR/sakila-data.sql" "$CONTAINER_NAME:/tmp/sakila-data.sql"
  docker exec "$CONTAINER_NAME" mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -e \
    "SOURCE /tmp/sakila-schema.sql; SOURCE /tmp/sakila-data.sql;"
else
  info "Sakila ya parece estar importada ($TABLE_COUNT tablas)"
fi

export SAKILA_DB_HOST="${SAKILA_DB_HOST:-127.0.0.1}"
export SAKILA_DB_PORT="${SAKILA_DB_PORT:-$MYSQL_PORT}"
export SAKILA_DB_USER="${SAKILA_DB_USER:-root}"
export SAKILA_DB_PASSWORD="${SAKILA_DB_PASSWORD:-$MYSQL_ROOT_PASSWORD}"
export SAKILA_DB_NAME="${SAKILA_DB_NAME:-$MYSQL_DATABASE}"

info "Probando conexion desde Python"
python3 -m src.check_connection

info "Abriendo menu CRUD/ORM"
python3 -m src.main
