class TracerException(Exception):
    ...


class CRUDException(TracerException):
    ...


class UniqueValueQueryException(CRUDException):
    ...
