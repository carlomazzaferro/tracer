from typing import List

from sqlalchemy.orm import Session

from tracer.crud.base import CRUDBase
from tracer.models.block import Block
from tracer.schemas.block import BlockCreate, BlockUpdate


class CRUDBlock(CRUDBase[Block, BlockCreate, BlockUpdate]):
    def get_by_block_number(self, db: Session, *, block_number: int) -> List[Block]:
        return db.query(Block).filter(Block.block_number == block_number).one_or_none()


crud_block = CRUDBlock(Block)
