from fastapi import APIRouter
from fastapi.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

router = APIRouter()


@router.get("/healthz", response_model=None, status_code=204)
def healthz():
    """
    Healthz
    """
    return Response(status_code=HTTP_204_NO_CONTENT)
