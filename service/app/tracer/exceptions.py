import http


class TracerException(Exception):
    ...


class CRUDException(TracerException):
    ...


class UniqueValueQueryException(CRUDException):
    ...


class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str = None) -> None:
        if detail is None:
            detail = http.HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.detail = detail

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"


class APIClientException(HTTPException):
    ...
