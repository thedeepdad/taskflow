import asyncio
import json
import logging
from aio_pika.abc import AbstractIncomingMessage
from config.settings import settings
from rabbit.connection import connect_rabbit
from services.email_service import send_registration_email

logger = logging.getLogger(__name__)


async def main() -> None:
    connection = await connect_rabbit()
    channel = await connection.channel()

    try:
        queue = await channel.declare_queue(
            settings.rabbit_queue_email,
            durable=True
        )

        await channel.set_qos(prefetch_count=1)

        async def callback(
            message: AbstractIncomingMessage
        ) -> None:
            async with message.process():
                payload = json.loads(
                    message.body.decode()
                )

                if not isinstance(payload, dict):
                    raise ValueError("Invalid email payload")

                email = payload.get('email')
                username = payload.get('username')
                code = payload.get("code")

                if not email:
                    raise ValueError("Missing email")
                if not username:
                    raise ValueError("Missing username")
                if not code:
                    raise ValueError("Missing verification code")

                await send_registration_email(
                    email=email,
                    username=username,
                    code=code
                )

                logger.info(
                    "Registration email sent to %s",
                    email
                )

        await queue.consume(callback)

        logger.info(
            "Waiting for message in queue '%s'",
            settings.rabbit_queue_email
        )

        await asyncio.Future()

    finally:
        await connection.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Work is done")
