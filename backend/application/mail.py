import os
from smtplib import SMTP
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.application import MIMEApplication
from email import encoders

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_EMAIL = "librarian@admin.com"
SENDER_PASSWORD = ""


def send_message(to, subject, content_body, attach_file=None):
    msg = MIMEMultipart()
    msg["To"] = to
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg.attach(MIMEText(content_body, "html"))

    if attach_file:
        with open(attach_file, "rb") as file:
            attachment_content = file.read()
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment_content)
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(attach_file)}",
            )
            msg.attach(part)

    with SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT) as client:
        client.login(SENDER_EMAIL, SENDER_PASSWORD)
        client.send_message(msg)

    return True
