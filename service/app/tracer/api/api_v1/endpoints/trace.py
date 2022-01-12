from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.block_trace import BlockTrace
from tracer.api.utils.db import get_db

router = APIRouter()


@router.get("/", response_model=List[BlockTrace])
def trace_block(
        db: Session = Depends(get_db),
        block_number: int = 1,
        from_block: int = None,
        to_block: int = None,
):
    """
    trace blocks
    """
