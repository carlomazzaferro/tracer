# Import all the models, so that Base has them before being
# imported by Alembic
from tracer.db.base_class import Base  # noqa: F401
from tracer.models.block import Block  # noqa: F401
from tracer.models.block_trace import BlockTrace  # noqa: F401
