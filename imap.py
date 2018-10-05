from imapclient import IMAPClient
import email
import time
import re

EMAIL_ADDRESS = 'addaudittrail@gmail.com'
PASSWORD = ''

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
            
            if len(audittrailcontent)==0:
                print("Content: " + content)
            else:
                print("Content: " + audittrailcontent[0])
    
    time.sleep(30)        

server.logout()
