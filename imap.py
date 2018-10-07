from imapclient import IMAPClient
import smtplib
from email.mime.text import MIMEText
import email
import time
import re
import configparser
import os.path
import sys
import audit_trail_adder

if not os.path.exists('info.ini'):
    print("please create a file named 'info.ini' for email and password information.")
    print("content of this file will be as below:")
    print("[email]")
    print("user = PUT_EMAIL_HERE")
    print("password = PUT_PASSWORD_HERE")
    print("[sosym]")
    print("user = SOSYM_USER_EMAIL_HERE")
    print("password = SOSYM_USER_PASSWORD_HERE")
    sys.exit()

config = configparser.ConfigParser()
config.read('info.ini')

EMAIL_ADDRESS = config['email']['user']
PASSWORD = config['email']['password']

server = IMAPClient('imap.gmail.com', use_uid=True)
server.login(EMAIL_ADDRESS,PASSWORD)

while True:
    server.select_folder('INBOX')
    new_msgs = server.search('UNSEEN') # a list of IDs for new emails
    print("NEW_MSGS: "+str(new_msgs))
    if len(new_msgs)>0:
        for msg_id in new_msgs:
            message_data = server.fetch(msg_id, 'RFC822')[msg_id] # get first message
            email_message = email.message_from_bytes(message_data[b'RFC822'])
            print("From: " + email_message.get('From'))
            print("Subject: " + email_message.get('Subject'))

            content = ""
                
            if email_message.get_payload()[0] is str:
                content = email_message.get_payload()[0]
            else:
                content = email_message.get_payload()[0].get_payload()

            audittrailcontent = re.compile('<audittrail>(.*?)</audittrail>',re.DOTALL | re.IGNORECASE).findall(content)
            
            if len(audittrailcontent)>0:
                content = audittrailcontent[0]
            print("Content: " + content)

            necessary_parts = email_message.get('Subject').split('|')
            sosym_id = necessary_parts[0]
            sosym_from = necessary_parts[1]
            sosym_to = necessary_parts[2]
            sosym_subject = necessary_parts[3]

            result = audit_trail_adder.add(config['sosym']['user'],config['sosym']['password'],sosym_id,sosym_from,sosym_to,sosym_subject,content,WAIT_TIME=5)

            send_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            send_server.login(EMAIL_ADDRESS,PASSWORD)
            msg = MIMEText(result)
            msg['Subject'] = "RE: "+email_message.get('Subject')
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = email_message.get('From')
            send_server.sendmail(EMAIL_ADDRESS,email_message.get('From'),msg.as_string())
            send_server.quit()

    
    time.sleep(30)        

server.logout()
