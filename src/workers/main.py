from celery import Celery

from src.config import settings
from src.logger import logger, setup_logging


def create_celery_app():
    setup_logging()

    logger.info(f"MONGODB_URL: {settings.MONGODB_URL}")
    logger.info(f"REDIS_URL: {settings.REDIS_URL}")

    celery_app = Celery(
        "tips-ai-service",
        broker=settings.REDIS_URL,
        backend=settings.MONGODB_URL,
        include=["src.workers.tasks.test"],
    )

    celery_app.conf.update(
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        enable_utc=True,
    )

    celery_app.conf.worker_hijack_root_logger = False

    return celery_app


celery_app = create_celery_app()
