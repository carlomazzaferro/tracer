from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from tracer.api.utils.db import get_db
from tracer.celery_app import celery_app

router = APIRouter()


@router.post("/")
def backfill(
        from_block: int, to_block: str, db: Session = Depends(get_db),
):
    """
    backfill block
    """
    celery_app.send_task("app.worker.test_celery", args=[from_block, to_block])


@router.get("/{job_id}")
def backfill_job_status(
        job_id: int,
        db: Session = Depends(get_db),
):
    """
    Retrieve job status
    """
