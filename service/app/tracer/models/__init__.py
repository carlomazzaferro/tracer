from functools import wraps

from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from tracer.exceptions import UniqueValueQueryException


def raises_for_one(fn):
    @wraps(fn)
    def wrap(self, *args, **kwargs):
        try:
            output = fn(self, *args, **kwargs)
        except NoResultFound:
            raise UniqueValueQueryException("No value found for query `one()`")
        except MultipleResultsFound:
            raise UniqueValueQueryException("More than one result found for query `one()`")

        return output

    return wrap
