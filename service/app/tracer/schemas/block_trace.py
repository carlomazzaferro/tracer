from typing import List, Optional

from hexbytes import HexBytes
from pydantic import BaseModel, UUID4
from web3.datastructures import AttributeDict

from tracer.t import TraceType


# shamelessly gotten from mev-inspect py
def to_camel(string: str) -> str:
    return "".join(
        word.capitalize() if i > 0 else word for i, word in enumerate(string.split("_"))
    )


class Web3Model(BaseModel):
    """BaseModel that handles web3's unserializable objects"""

    class Config:
        json_encoders = {
            AttributeDict: dict,
            HexBytes: lambda h: h.hex(),
        }


class CamelModel(BaseModel):
    """BaseModel that translates from snake_case to camelCase"""

    class Config(Web3Model.Config):
        alias_generator = to_camel
        allow_population_by_field_name = True


class BlockTraceCreate(CamelModel):
    action: dict
    block_hash: str
    block_number: int
    result: Optional[dict]
    subtraces: int
    trace_address: List[int]
    transaction_hash: Optional[str]
    transaction_position: Optional[int]
    type: TraceType
    error: Optional[str]


class BlockTraceUpdate(CamelModel):
    result: Optional[dict]
    subtraces: Optional[int]
    trace_address: List[int]
    transaction_hash: Optional[str]
    transaction_position: Optional[int]
    type: Optional[TraceType]
    error: Optional[str]


class BlockTrace(CamelModel):
    id: Optional[UUID4]
    action: dict
    block_hash: str
    block_number: int
    result: Optional[dict]
    subtraces: int
    trace_address: List[int]
    transaction_hash: Optional[str]
    transaction_position: Optional[int]
    type: TraceType
    error: Optional[str]

    class Config:
        orm_mode = True
