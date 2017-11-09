from __future__ import unicode_literals
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import namedtuple
from random import shuffle

import os, sys
import csv

#enter your gmail credentials to see result!
HOST_EMAIL = ""
HOST_PASSWORD = ""
SUBJECT = "[WOODSTOCK] stań się mikołajem "

def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        # SMTP_SSL Example
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo()  # optional, called by login()
        server_ssl.login(gmail_user, gmail_pwd)
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
        server_ssl.sendmail(FROM, TO, message)
        # server_ssl.quit()
        server_ssl.close()
        print('successfully sent the mailfrom %s to %s'%(FROM,TO))
    except:
        print("failed to send mail:\n",sys.exc_info()[0])

class Mikolajki:
    def __init__(self,text_file,forbidden,host_email,host_pwd):
        self.text_file = text_file
        self.forbidden = forbidden
        self.host_email = host_email
        self.host_pwd = host_pwd


        self.load_participants()
        self.load_rules()
        self.shuffle()
        self.list_participants()


    def load_participants(self):

        self.givers = []

        try:
            with open(self.text_file, 'r', encoding='utf-8-sig') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for i, row in enumerate(spamreader):
                    Giver = namedtuple("Giver", "email, name")
                    Giver.email = row[0]
                    Giver.name = row[1] + " " + row[2]
                    self.givers.append(Giver)
                    print(Giver.email,Giver.name)
        except:
            print(sys.exc_info())
        self.receivers = self.givers[:]

    def list_participants(self):
        for giver, receiver in zip(self.givers, self.receivers):
            print(giver.email," has to buy something for ",receiver.email)

    def shuffle(self):
        counter = 0
        while self.check_rules() != True:
            shuffle(self.receivers)
            counter+=1
        print("\nAfter " + str(counter) + " shuffles, the shuffle gave correct giver-receiver list\n ")

    def load_rules(self):
        self.rules = {}
        try:
            with open(self.forbidden, 'r', encoding='utf-8-sig') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for i, row in enumerate(spamreader):
                    forbidden_giver = row[0]
                    forbidden_receiver = row[1]
                    self.rules[forbidden_giver] = forbidden_receiver
                    print(forbidden_giver + " cannot buy anything for " + forbidden_receiver)
        except:
            print(sys.exc_info())

    def check_rules(self):
        for giver, receiver in zip(self.givers, self.receivers):
            if giver.email == receiver.email:
                return False
            elif giver.email in self.rules and self.rules[giver.email] == receiver.email:
                return False
        return True

    def send_info(self):
        for giver, receiver in zip(self.givers, self.receivers):
            subject = SUBJECT + giver.name
            text_content = """\
            Drogi {0}!

            Komputery internetowe wylosowały dla Ciebie {1}.

            Wesołych Świąt!
            """.format(giver.name, receiver.name)
            send_email(HOST_EMAIL,  HOST_PASSWORD, giver.email, subject, text_content)



Mikolajki("lista.txt","forbidden.txt",HOST_EMAIL,HOST_PASSWORD)