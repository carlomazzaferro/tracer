from sqlalchemy import Column, Integer

from tracer.db.base_class import Base


class Block(Base):
    block_number = Column(Integer, nullable=False, index=True, primary_key=True)
    block_timestamp = Column(Integer, nullable=False, index=True)
