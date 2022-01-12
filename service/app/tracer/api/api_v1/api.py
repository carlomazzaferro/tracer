from fastapi import APIRouter

from tracer.api.api_v1.endpoints import (
    backfill,
    trace,
)

api_router = APIRouter()
api_router.include_router(backfill.router, prefix="/backfill", tags=["analysis"])
api_router.include_router(trace.router, prefix="/trace", tags=["models"])
