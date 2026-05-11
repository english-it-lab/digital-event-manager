import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


def send_email(to: str, subject: str, body: str):
    smtp_host = settings.smtp_host
    smtp_port = settings.smtp_port
    smtp_user = settings.smtp_user
    smtp_password = settings.smtp_password
    from_email = settings.smtp_from_email

    # Создание сообщения
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to
    msg["Subject"] = subject

    # Текст письма
    msg.attach(MIMEText(body, "plain", "utf-8"))

    # Отправка
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()  # Включаем шифрование TLS
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
    except Exception as e:
        print(f"Ошибка при отправке: {e}")
