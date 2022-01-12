from sqlalchemy import Column, Integer

from tracer.db.base_class import Base, IdMixin


class BlockTrace(IdMixin, Base):
    block_number = Column(Integer, nullable=False)
    block_timestamp = Column(Integer, nullable=False)
