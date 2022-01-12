import re
import uuid
from typing import cast

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr


def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


UUIDColumn = cast("TypeEngine[UUID4]", UUID(as_uuid=True))


@as_declarative()
class Base:
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls):
        return camel_to_snake(cls.__name__)  # type: ignore

    # @property
    # def id(self):
    #     return str(self.id)


class IdMixin(object):
    id = Column(UUIDColumn, primary_key=True, default=uuid.uuid4, unique=True, nullable=False, )
