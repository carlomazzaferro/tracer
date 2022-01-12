from celery import Celery  # type: ignore

from tracer.config import settings

celery_app = Celery("worker", backend="db+sqlite:///results.sqlite", broker=settings.REDIS_URI)
