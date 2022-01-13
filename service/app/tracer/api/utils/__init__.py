from typing import List

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


def get_block_ranges(from_block: int, to_block: int) -> List[int]:
    if to_block < from_block:
        raise HTTPException(detail="from_block must be bigger than to_block", status_code=HTTP_400_BAD_REQUEST)
    return list(range(from_block, to_block))
