#! /usr/bin/env sh
set -e


DEFAULT_MODULE_NAME=tracer.main
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

DEFAULT_GUNICORN_CONF=/gunicorn_conf.py
export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}

# If there's a prestart.sh script in the /app directory or other path specified, run it before starting

PRE_START_PATH=${PRE_START_PATH:-/app/prestart.sh}
echo "Running script $PRE_START_PATH"
. "$PRE_START_PATH"


# Start Uvicorn with live reload
exec uvicorn --reload --host "0.0.0.0" --port 8080 --log-level debug "$APP_MODULE"