from loguru import logger

from tracer.celery_app import celery_app
from tracer.log import setup_logging

setup_logging()


@celery_app.task(acks_late=True)
def test_celery(word: str):
    logger.info(f"Celery test {word}")
    return f"test task return {word}"
