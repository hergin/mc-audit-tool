from imapclient import IMAPClient
import email
import time

EMAIL_ADDRESS = ''
PASSWORD = ''

server = IMAPClient('smtp.office365.com', use_uid=True)
server.login(EMAIL_ADDRESS,PASSWORD)
server.select_folder('INBOX')

while True:
    new_msgs = server.search('UNSEEN') # a list of IDs for new emails
    if len(new_msgs)>0:
        for msg_id in new_msgs:
            message_data = server.fetch(msg_id, 'RFC822')[msg_id] # get first message
            email_message = email.message_from_bytes(message_data[b'RFC822'])
            print("From: " + email_message.get('From'))
            print("Subject: " + email_message.get('Subject'))
            if email_message.get_payload()[0] is str:
                print("Content: " + email_message.get_payload()[0])
            else:
                print("Content: " + email_message.get_payload()[0].get_payload())
    
    time.sleep(30)        

server.logout()
