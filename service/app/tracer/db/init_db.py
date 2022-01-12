import logging

# NOTES:
# [1] make sure all SQL Alchemy models are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

logger = logging.getLogger(__name__)


def init_db(db):
    pass
