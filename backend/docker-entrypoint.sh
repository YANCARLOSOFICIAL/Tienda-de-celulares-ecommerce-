#!/bin/sh
# Entrypoint del contenedor de la API.
# Espera la base de datos, aplica migraciones y (opcionalmente) el seed,
# y luego arranca uvicorn. Todo es idempotente: se puede reiniciar el
# contenedor las veces que haga falta sin "batallar".
set -e

: "${RUN_MIGRATIONS:=true}"
: "${RUN_SEED:=true}"
: "${UVICORN_RELOAD:=false}"
: "${APP_MODULE:=app.main:app}"
: "${PORT:=8000}"

if [ "$RUN_MIGRATIONS" = "true" ]; then
  echo "[entrypoint] Aplicando migraciones (alembic upgrade head)..."
  alembic upgrade head
fi

if [ "$RUN_SEED" = "true" ]; then
  echo "[entrypoint] Ejecutando seed de desarrollo (idempotente)..."
  python -m scripts.seed || echo "[entrypoint] AVISO: el seed fallo, se continua igualmente."
fi

RELOAD_FLAG=""
if [ "$UVICORN_RELOAD" = "true" ]; then
  RELOAD_FLAG="--reload"
fi

echo "[entrypoint] Iniciando API en 0.0.0.0:${PORT} (reload=${UVICORN_RELOAD})..."
exec uvicorn "$APP_MODULE" --host 0.0.0.0 --port "$PORT" $RELOAD_FLAG
