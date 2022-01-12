#!/bin/bash

set -e

cd /src/app

python tracer/tests_pre_start.py

alembic upgrade head

python tracer/unit_test_pre_start.py

pytest --ignore=tests/integration tests -vv
