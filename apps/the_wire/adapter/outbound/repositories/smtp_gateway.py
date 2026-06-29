import os
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
import core.config  # noqa: F401  — .env 로드 보장

from the_wire.app.dtos.email_dto import EmailCommand, EmailResult
from the_wire.app.ports.output.n8n_gateway_port import N8nGatewayPort

class SmtpGateway(N8nGatewayPort):
    async def send(self, command: EmailCommand, body: str) -> EmailResult:
        gmail_user = os.getenv("GMAIL_USER", "")
        gmail_password = os.getenv("GMAIL_APP_PASSWORD", "")

        msg = MIMEMultipart()
        msg["Subject"] = Header(command.subject, "utf-8")
        msg["From"] = gmail_user
        msg["To"] = command.to
        msg.attach(MIMEText(body, "plain", "utf-8"))

        raw = msg.as_bytes()

        smtp = aiosmtplib.SMTP(
            hostname="smtp.gmail.com",
            port=465,
            use_tls=True,
        )
        await smtp.connect()
        await smtp.login(gmail_user, gmail_password)
        await smtp.sendmail(gmail_user, [command.to], raw)
        await smtp.quit()

        return EmailResult(success=True, detail="sent")
