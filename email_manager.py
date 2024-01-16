from dotenv import load_dotenv

load_dotenv()

import os
from email.message import EmailMessage  # email sending library
import ssl  # secure sockets layer protection
import smtplib  # Simple Mail Transfer Protocol - this one does the actual sending


class WrongEmail(Exception):
    pass


def send_mail(
    contact: list[dict], message: str, subject: str = "Happy Birthday!"
) -> None:
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

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

    # The smtplib.SMTPRecipientsRefused exception is raised when the recipient’s email server refuses the email.
    # This will only work if your SMTP server (in this case, Gmail’s server) is set to reject emails to invalid addresses immediately
    except smtplib.SMTPRecipientsRefused:
        raise WrongEmail(
            "Email could not be delivered. Probably, wrong e-mail address."
        )


if __name__ == "__main__":
    ...
