from loguru import logger

from tracer.api.service import get_service
from tracer.api.utils import get_block_ranges
from tracer.api.utils.db import get_session
from tracer.celery_app import celery_app
from tracer.log import setup_logging

setup_logging()


@celery_app.task(acks_late=True)
def test_celery(word: str):
    logger.info(f"Celery test {word}")
    return f"test task return {word}"


@celery_app.task(acks_late=False)
def backfill_blocks(from_block: int, to_block: int):
    """
    Parameters
    ----------
    from_block : str
        starting block
    to_block : str
        ending block
    """
    block_ranges = get_block_ranges(from_block, to_block)
    service = get_service(db=get_session())
    block_traces = service.get_traces_for_blocks(blocks=block_ranges)
    return [b.id for b in block_traces]
