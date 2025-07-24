import asyncio

from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown

from src.config import settings
from src.database.mongodb import mongodb_client
from src.logger import logger, setup_logging


@worker_process_init.connect
def setup_database(**kwargs):
    logger.info("Initializing database connection for worker...")
    asyncio.run(mongodb_client.init_db())
    logger.info("Database connection for worker initialized.")


@worker_process_shutdown.connect
def teardown_database(**kwargs):
    logger.info("Closing database connection for worker...")
    asyncio.run(mongodb_client.close_db())
    logger.info("Database connection for worker closed.")


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
