from email.message import EmailMessage
from config.settings import settings
import aiosmtplib
import logging

logger = logging.getLogger(__name__)


async def send_registration_email(
    email: str,
    username: str,
    code: str
) -> None:

    message = EmailMessage()
    message['From'] = settings.smtp_from
    message['To'] = email
    message['Subject'] = "Hello, It's TaskFlow"

    message.set_content(
        f"Hello, {username}!\n"
        f"It's your verification code: {code}"
    )

    await aiosmtplib.send(
        message,
        hostname=settings.smtp_host,
        port=settings.smtp_port,
        username=settings.smtp_user,
        password=settings.smtp_password,
        start_tls=True
    )

    logger.info("Message sent")
