from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from tracer.api.utils.db import get_db
from tracer.worker import backfill_blocks

router = APIRouter()


@router.post("/")
def backfill(
        from_block: int, to_block: str, db: Session = Depends(get_db),
):
    """
    backfill block
    """
    task = backfill_blocks.delay(from_block=from_block, to_block=to_block)
    return task.task_id


@router.get("/{job_id}")
def backfill_job_status(job_id: str):
    """
    Retrieve job status
    """
    result = backfill_blocks.AsyncResult(job_id)
    return {
        "status": result.status,
        "completed": result.ready()
    }
