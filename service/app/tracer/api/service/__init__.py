from pprint import pprint
from typing import List

from web3 import AsyncHTTPProvider, Web3
from web3.eth import AsyncEth

from tracer import crud
from tracer.config import settings
from tracer.schemas.block import Block
from tracer.schemas.block_trace import BlockTrace


class EthereumBlockService(object):

    def __init__(self, db):
        self.db = db
        self.base_provider = AsyncHTTPProvider(settings.RPC_URL, request_kwargs={"timeout": 500})
        self.w3 = Web3(self.base_provider, modules={"eth": (AsyncEth,)}, middlewares=[])

    async def fetch_block(self, block_number: int):
        block = await self.w3.eth.get_block(block_number)
        return Block(block_number=block["number"], block_timestamp=block["timestamp"])

    async def get_block(self, block_number: int):
        block = crud.crud_block.get_by_block_number(db=self.db, block_number=block_number)
        if not block:
            fetched_block = await self.fetch_block(block_number=block_number)
            block = self.store_block(block_or_blocks=fetched_block)
        return block

    async def fetch_block_trace(self, block_number: int) -> List[BlockTrace]:
        traces_json = await self.base_provider.make_request("trace_block", [block_number])
        pprint(traces_json["result"])
        return [BlockTrace(**trace_json) for trace_json in traces_json["result"]]

    async def get_traces_for_blocks(self, blocks: List[int]) -> List[BlockTrace]:
        traces = []
        for block in blocks:
            block_traces = await self.get_trace_for_block(block_number=block)
            traces.append(block_traces)
        return traces

    async def get_trace_for_block(self, block_number: int):
        # store block first
        block = await self.get_block(block_number)
        has_traces = crud.crud_block_trace.get_block_has_traces(db=self.db, block_number=block.block_number)
        if has_traces:
            return crud.crud_block_trace.get_block_traces(db=self.db, block_number=block.block_number)
        else:
            block_traces = await self.fetch_block_trace(block_number=block.block_number)
            return self.store_block_traces(block_traces)

    def store_block_traces(self, traces: List[BlockTrace]):
        for trace in traces:
            crud.crud_block_trace.create(db=self.db, obj_in=trace)
        return traces

    def store_block(self, block_or_blocks: Block) -> Block:
        return crud.crud_block.create(db=self.db, obj_in=block_or_blocks)


def get_service(db):
    return EthereumBlockService(db)
