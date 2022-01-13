from starlette.requests import Request

from tracer.db.session import db


def get_db(request: Request):
    return request.state.db


def get_session():
    return db
