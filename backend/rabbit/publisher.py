import logging
import aio_pika
import json
from aio_pika.abc import AbstractRobustChannel
from config.settings import settings

logger = logging.getLogger(__name__)


async def publish_email(
    channel: AbstractRobustChannel,
    email: str,
    username: str,
    code: str
) -> None:

    logger.info(
        "Publishing email for %s",
        email
    )

    payload = {
        "email": email,
        "username": username,
        "code": code
    }

    message = aio_pika.Message(
        body=json.dumps(payload).encode(),
        content_type="application/json",
        delivery_mode=aio_pika.DeliveryMode.PERSISTENT
    )

    await channel.default_exchange.publish(
        message,
        routing_key=settings.rabbit_queue_email,
        mandatory=True
    )

    logger.info(
        "Message published to queue %s",
        settings.rabbit_queue_email
    )
