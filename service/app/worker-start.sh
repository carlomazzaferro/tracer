#! /usr/bin/env bash
set -e

python /app/tracer/celeryworker_pre_start.py


if [ "$ENV" == "local" ]
then
    watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery -A tracer.worker worker -l info --concurrency=1
else
    celery -A tracer.worker worker -l info --concurrency=2
fi
