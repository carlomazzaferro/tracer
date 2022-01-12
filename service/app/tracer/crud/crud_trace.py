from typing import List

from sqlalchemy.orm import Session

from schemas.block_trace import BlockTraceCreate, BlockTraceUpdate
from tracer.crud.base import CRUDBase
from tracer.models.block_trace import BlockTrace


class CRUDBlockTrace(CRUDBase[BlockTrace, BlockTraceCreate, BlockTraceUpdate]):
    def get_by_block_number(self, db: Session, *, block_number: int) -> List[BlockTrace]:
        return db.query(BlockTrace).filter(BlockTrace.block_number == block_number).all()


crud_block_trace = CRUDBlockTrace(BlockTrace)
