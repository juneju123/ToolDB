import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.helpers.file_helpers import FileHelpers


def send_notification(subject, message, attachment_list):
    sender = FileHelpers.read_string_from_file("src/private_info/sender_email")
    receiver = FileHelpers.read_string_from_file("src/private_info/receiver_email")
    passwd = FileHelpers.read_string_from_file("src/private_info/email_password")
    # instance of MIMEMultipart
    msg = MIMEMultipart()
    # storing the senders email address
    msg['From'] = sender
    # storing the receivers email address
    msg['To'] = receiver
    # storing the subject
    msg['Subject'] = subject
    # string to store the body of the mail
    body = message
    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    # open the file to be sent

    for file in attachment_list:
        # instance of MIMEBase and named as p
        part = MIMEBase('application', 'octet-stream')
        # To change the payload into encoded form
        part.set_payload(open(file, "rb").read())
        # encode into base64
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % file)
        # attach the instance 'p' to instance 'msg'
        msg.attach(part)

    # creates SMTP session
    smtp_session = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_session.ehlo()
    # start TLS for security
    smtp_session.starttls()
    smtp_session.ehlo()
    # Authentication
    smtp_session.login(sender, passwd)
    # Converts the Multipart msg into a string
    text = msg.as_string()
    # sending the mail
    smtp_session.sendmail(sender, receiver, text)

    # terminating the session
    smtp_session.quit()
