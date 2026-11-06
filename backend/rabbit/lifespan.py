import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .connection import connect_rabbit

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Lifespan: connecting to RabbitMQ")
    connection = await connect_rabbit()
    logger.info("Lifespan: RabbitMQ connected")

    channel = await connection.channel()
    logger.info("Lifespan: channel created")

    app.state.rabbit_connection = connection
    app.state.rabbit_channel = channel

    try:
        yield
    finally:
        logger.info("Lifespan: closing RabbitMQ connection")
        await connection.close()
