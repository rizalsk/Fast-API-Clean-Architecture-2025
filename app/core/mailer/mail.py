import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.dependencies.logger import log
from .message import Message
from app.core.config import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

class Mail:
    _message: Message = None
    _attachments: list = []

    @classmethod
    def to(cls, email: str):
        cls._message = Message()
        cls._message.to(email)
        return cls

    @classmethod
    def subject(cls, subject: str):
        cls._message.subject(subject)
        return cls

    @classmethod
    def text(cls, body: str):
        cls._message.text(body)

        body_html = body.replace("\n", "<br>")

        html_content = f"""<html>
        <body style="background-color: white; color: black; font-family: Arial, sans-serif; padding: 20px;">
            {body_html}
        </body>
        </html>"""

        cls._message.build_html = lambda: html_content
        return cls

    @classmethod
    def template(cls, template_file: str, context: dict = {}):
        cls._message.template(template_file, context)
        return cls

    @classmethod
    def attach(cls, file_path: str, filename: str = None):
        """
        Tambahkan attachment
        file_path: path file di server
        filename: nama file yang dikirim, default ambil nama file_path
        """
        path = Path(file_path)
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"Attachment not found: {file_path}")
        cls._attachments.append((file_path, filename or path.name))
        return cls

    @classmethod
    def send(cls):
        MAIL_HOST = settings.MAIL_HOST
        MAIL_PORT = settings.MAIL_PORT
        MAIL_USERNAME = settings.MAIL_USERNAME
        MAIL_PASSWORD = settings.MAIL_PASSWORD
        MAIL_ENCRYPTION = settings.MAIL_ENCRYPTION
        MAIL_FROM_ADDRESS = settings.MAIL_FROM_ADDRESS
        MAIL_FROM_NAME = settings.MAIL_FROM_NAME

        if not cls._message.to_email:
            raise ValueError("Recipient email (to) belum di-set")
        if not MAIL_FROM_ADDRESS:
            raise ValueError("MAIL_FROM_ADDRESS belum di-set")

        msg = MIMEMultipart()
        msg['From'] = f"{MAIL_FROM_NAME} <{MAIL_FROM_ADDRESS}>"
        msg['To'] = cls._message.to_email
        msg['Subject'] = cls._message.subject_text or "No Subject"

        html_content = cls._message.build_html()
        if html_content:
            msg.attach(MIMEText(html_content, "html"))
        if cls._message.text_body:
            msg.attach(MIMEText(cls._message.text_body, "plain"))

        if cls._attachments:
            for file_path, filename in cls._attachments:
                with open(file_path, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
                    msg.attach(part)

        # Kirim email via SMTP
        try:
            if MAIL_ENCRYPTION == "ssl":
                server = smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT)
            else:
                server = smtplib.SMTP(MAIL_HOST, MAIL_PORT)
                if MAIL_ENCRYPTION == "tls" or MAIL_ENCRYPTION == "":
                    server.starttls()

            if MAIL_USERNAME and MAIL_PASSWORD:
                server.login(MAIL_USERNAME, MAIL_PASSWORD)

            server.send_message(msg)
            server.quit()
            log.info(f"Email sent to {cls._message.to_email}")
            return {"status": "success", "to": cls._message.to_email}
        except Exception as e:
            log.error(f"Failed to send email: {e}")
            return {"status": "error", "error": str(e)}