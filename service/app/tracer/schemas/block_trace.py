from typing import List, Optional

from pydantic.main import BaseModel

from tracer.t import ExtendedEnum


class BlockTraceCreate(BaseModel):
    action: dict
    block_hash: str
    block_number: int
    result: Optional[dict]
    subtraces: int
    trace_address: List[int]
    transaction_hash: Optional[str]
    transaction_position: Optional[int]
    type: ExtendedEnum
    error: Optional[str]


class BlockTraceUpdate(BaseModel):
    result: Optional[dict]
    subtraces: Optional[int]
    trace_address: List[int]
    transaction_hash: Optional[str]
    transaction_position: Optional[int]
    type: Optional[ExtendedEnum]
    error: Optional[str]


class BlockTrace(BaseModel):
    action: dict
    block_hash: str
    block_number: int
    result: Optional[dict]
    subtraces: int
    trace_address: List[int]
    transaction_hash: Optional[str]
    transaction_position: Optional[int]
    type: ExtendedEnum
    error: Optional[str]

    class Config:
        orm_mode = True
