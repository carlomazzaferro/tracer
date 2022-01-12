#! /usr/bin/env bash

# Let the DB start
python /app/tracer/backend_pre_start.py

# Run migrations
cd /app && alembic upgrade head
cd /app && alembic stamp head

# Create initial data in DB
python /app/tracer/initial_data.py
