from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from tracer.api.api_v1.api import api_router
from tracer.api.utils.healthz import router as healthz_router
from tracer.config import settings
from tracer.db.session import Session
from tracer.log import setup_logging

setup_logging()

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json", )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] + [str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(healthz_router, prefix="")


@app.middleware("http")
async def db_middleware(request: Request, call_next):
    request.state.db = Session()
    try:
        return await call_next(request)
    finally:
        request.state.db.close()
