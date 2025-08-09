import os
from email.message import EmailMessage
from dotenv import load_dotenv
import aiosmtplib

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_FROM = os.getenv("EMAIL_FROM")

async def send(to_email: str, subject: str, body: str, html: str = None):
    message = EmailMessage()
    message["From"] = EMAIL_FROM
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    if html is not None:
        message.add_alternative(html)

    try:
        await aiosmtplib.send(
            message,
            hostname=EMAIL_HOST,
            port=EMAIL_PORT,
            username=EMAIL_USER,
            password=EMAIL_PASS,
            start_tls=True,
        )
    except Exception as e:
        print(f"Error: {e}")
        return None