import logging

from tracer.db.init_db import init_db
from tracer.db.session import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init():
    try:
        init_db(db)
    except Exception as e:
        logger.error(f"Could not init db: {e}")


def main():
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
