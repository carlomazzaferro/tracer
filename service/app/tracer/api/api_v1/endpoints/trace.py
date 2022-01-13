from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from tracer.api.service import get_service
from tracer.api.utils import get_block_ranges
from tracer.api.utils.db import get_db
from tracer.schemas.block_trace import BlockTrace

router = APIRouter()


@router.get("/", response_model=List[BlockTrace])
def trace_block(
        db: Session = Depends(get_db),
        block_number: int = None,
        from_block: int = None,
        to_block: int = None,
):
    """
    trace blocks
    """
    service = get_service(db)
    if block_number:
        return service.get_trace_for_block(block_number=block_number)
    if (from_block and not to_block) or (to_block and not from_block):
        raise HTTPException(detail="If passing from_block or to block, must provide the other parameter",
                            status_code=HTTP_400_BAD_REQUEST)
    block_ranges = get_block_ranges(from_block=from_block, to_block=to_block)
    return service.get_traces_for_blocks(blocks=block_ranges)
