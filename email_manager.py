from dotenv import load_dotenv
load_dotenv()

import os
from email.message import EmailMessage # email sending library
import ssl # secure sockets layer protection
import smtplib # Simple Mail Transfer Protocol - this one does the actual sending


def send_mail(contact: list[dict], message: str, subject: str = "Happy Birthday!") -> None:
    email_sender = os.environ.get("MY_EMAIL")
    email_password = os.environ.get("MY_EMAIL_PASS")
    email_receiver = contact[0]["email"]

    email_subject = subject
    body = message

    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = email_subject

    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


if __name__ == "__main__":
    person = [{"uid": "1704663936754301","name": "Gints","birthday": "1993.05.12", "email": "matissjansons1@gmail.com", "about": "smth", "congratulated": "False"}]
    send_mail(person, "test")