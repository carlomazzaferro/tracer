from typing import Dict

from fastapi import status
from fastapi.responses import JSONResponse


class SuccessResponse(JSONResponse):
    def __init__(self, detail: str, headers: Dict[str, str] = None):
        super().__init__(
            content={"detail": detail}, status_code=status.HTTP_200_OK, headers=headers,
        )
