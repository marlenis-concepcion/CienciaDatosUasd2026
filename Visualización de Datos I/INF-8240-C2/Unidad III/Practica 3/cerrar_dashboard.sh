#!/bin/sh
# Detiene el dashboard web.
cd "$(dirname "$0")" || exit 1
docker compose down
