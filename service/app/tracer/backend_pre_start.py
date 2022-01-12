import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from tracer.config import settings
from tracer.db.session import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 3


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init():
    try:
        # Try to create session to check if DB is awake
        db.execute("SELECT 1")
        if settings.REINITIALIZE_DB:
            db.execute(
                """
            DROP SCHEMA public CASCADE;
            CREATE SCHEMA public;
            GRANT ALL ON SCHEMA public TO tracer;
            GRANT ALL ON SCHEMA public TO public;
            COMMENT ON SCHEMA public IS 'standard public schema';
            """
            )
            logger.info("Dropped everything")
            db.commit()
            logger.info("Committed changes")

    except Exception as e:
        logger.error(e)
        raise e


def main():
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
