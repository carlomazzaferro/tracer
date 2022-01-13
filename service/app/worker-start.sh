#! /usr/bin/env bash
set -e

python /app/tracer/celeryworker_pre_start.py


if [ "$ENV" == "local" ]
then
    watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery -A tracer.worker worker -l info --concurrency=2 -E
else
    celery -A tracer.worker worker -l info --concurrency=2 -Q main-queue
fi
