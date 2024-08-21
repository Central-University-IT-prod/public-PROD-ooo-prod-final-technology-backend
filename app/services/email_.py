import aiosmtplib
from core.config import Config
from email.message import EmailMessage


class EmailService:
    def __init__(self) -> None:
        self.smtp = aiosmtplib.SMTP(hostname=Config.EMAIL_HOST, port=Config.EMAIL_PORT, start_tls=True)

    async def send(self, sender_name: str, recipient_email: str, subject: str, content: str) -> None:
        message = EmailMessage()
        message['From'] = f'{sender_name} <{Config.EMAIL_USER}>'
        message['To'] = recipient_email
        message['Subject'] = subject
        message.set_content(content)

        try:
            await self.smtp.connect()
            await self.smtp.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
            await self.smtp.send_message(message)

        finally:
            await self.smtp.quit()

    async def send_list(self, emails: list[str], event_title: str, subject: str, content: str) -> None:
        sender_name = f"Олимпиада {event_title}"
        for email in emails:
            await self.send(sender_name, email, subject, content)
        

email_service = EmailService()
