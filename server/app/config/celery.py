import os

from celery import Celery


celery_app = Celery(
    "worker",
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    include=['app.tasks'],
)
