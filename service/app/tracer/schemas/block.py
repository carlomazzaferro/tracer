from typing import Optional

from pydantic import BaseModel


class Block(BaseModel):
    block_number: int
    block_timestamp: int


class BlockCreate(BaseModel):
    block_number: int
    block_timestamp: int


class BlockUpdate(BaseModel):
    block_number: Optional[int]
    block_timestamp: Optional[int]
