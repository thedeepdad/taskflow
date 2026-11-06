import logging

import aio_pika
from aio_pika.abc import AbstractRobustConnection
from config.settings import settings

logger = logging.getLogger(__name__)


async def connect_rabbit() -> AbstractRobustConnection:
    logger.info("Connecting to RabbitMQ...")

    connection = await aio_pika.connect_robust(
        settings.rabbit_url,
    )

    logger.info("RabbitMQ connection established")
    return connection
