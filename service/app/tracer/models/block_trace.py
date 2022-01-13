from sqlalchemy import Column, Integer, JSON, String, ARRAY

from tracer.db.base_class import Base, IdMixin


class BlockTrace(IdMixin, Base):
    block_hash = Column(String, primary_key=True)
    block_number = Column(Integer, nullable=False, index=True)
    action = Column(JSON)
    result = Column(JSON, nullable=True)
    subtraces = Column(Integer)
    trace_address = Column(ARRAY(Integer))
    transaction_hash = Column(String)
    transaction_position = Column(Integer)
    type = Column(String)
    error = Column(String, nullable=True)
