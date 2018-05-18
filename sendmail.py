import smtplib
from email.mime.text import MIMEText

from config import by, to


def sendmail(subject, text):
    msg = MIMEText(text)

    msg['Subject'] = subject
    msg['From'] = by
    msg['To'] = to

    s = smtplib.SMTP('localhost')
    s.sendmail(by, [to], msg.as_string())
