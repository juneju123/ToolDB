#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      2:13 PM
@Author:    Juju
@File:      FileHelpers
@Project:   OptionToolDb
"""
import logging.config
import os

from pandas import read_excel

from src.pre_and_post import global_vars
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class GeneralHelpers:
    def __init__(self):
        pass

    @staticmethod
    def read_string_from_file(file_path):
        with open(file_path, 'r') as file:
            return file.readline()

    @staticmethod
    def read_symbol_list(file_path):
        return read_excel(file_path, sheet_name=0)['symbol'].tolist()

    @staticmethod
    def save_spread_to_csv(spread, spread_type, conditions):
        if not os.path.exists(global_vars.RESULT_FOLDER):
            os.makedirs(global_vars.RESULT_FOLDER)
        output_file = global_vars.RESULT_FOLDER + spread_type + '_' + '_'.join(conditions) + '.csv'
        spread.to_csv(output_file)
        return output_file

    @staticmethod
    def log_config():
        """
        Config log with dict
        Returns: None

        """
        log_config_dict = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'simple': {
                    'format': '%(asctime)-15s, %(levelname)s, %(name)s, Line: %(lineno)d, Process: %(process)d, Message: %(message)s',
                    'datefmt': '%a %d %b %Y %H:%M:%S'
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                    'formatter': 'simple',
                    'stream': 'ext://sys.stdout'
                },
                'info_file_handler': {
                    'class': 'logging.FileHandler',
                    'level': 'INFO',
                    'formatter': 'simple',
                    'filename': 'debug.log',
                    'encoding': 'utf8',
                    'mode': 'w'
                }
            },
            'loggers': {
                '': {
                    'level': 'INFO',
                    'handlers': ['console', 'info_file_handler'],
                    'propagate': False
                }
            }
        }
        logging.config.dictConfig(log_config_dict)
        return None

    def send_notification(self, subject, message, attachment_list):
        sender = self.read_string_from_file("src/private_info/sender_email")
        receiver = self.read_string_from_file("src/private_info/receiver_email")
        passwd = self.read_string_from_file("src/private_info/email_password")
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
