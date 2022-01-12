from loguru import logger

from tracer.api.service.events.dispatcher import dispatch  # noqa: F401
from tracer.celery_app import celery_app
from tracer.celery_workers.slack import deploy_message, unsuccessful_deployment  # noqa: F401
from tracer.log import setup_logging

setup_logging()


@celery_app.task(acks_late=True)
def test_celery(word: str):
    logger.info(f"Celery test {word}")
    return f"test task return {word}"
