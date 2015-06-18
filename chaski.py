#!/usr/bin/python
# -*- coding: utf-8 *-*

import getpass
import yaml
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os
import optparse
parser = optparse.OptionParser()
parser.add_option('-t', '--sender', dest="sender", action="store",
               help='Define the gmail E-mail sender')
parser.add_option('-r', '--recipient', dest="recipient", action="store", help="Define recipient")
parser.add_option('-a', '--attach', dest="attach", action="store", help="Define de complete path to attach")
parser.add_option('-s', '--subject', dest="subject", action="store",
               help='Define the E-mail subject')
parser.add_option('-m', '--message', dest="message", action="store",
               help='Define the E-mail body message')
options, args = parser.parse_args()
sender = options.sender
recipient = options.recipient
attach = options.attach
subject = options.subject
message = options.message

def mail(to, subject, text, attach):
   print '\nPlease enter password to connect with your Gmail account'
   password = getpass.getpass()
   msg = MIMEMultipart()

   msg['From'] = sender
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach, 'rb').read())
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
   msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(sender, password)
   mailServer.sendmail(sender, to, msg.as_string())
   mailServer.close()

mail('%s'% recipient,
   '%s'% subject,
   '%s'% message,
   '%s'% attach)