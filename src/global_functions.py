import smtplib

from src.config import EMAIL, EMAIL_PASSWORD


def send_email(receiver, message):
    sender = EMAIL
    password = EMAIL_PASSWORD

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)
    except Exception as e:
        print(e)
