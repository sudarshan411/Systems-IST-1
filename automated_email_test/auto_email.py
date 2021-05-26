#importing modules
import smtplib
import csv
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SENDER_ADDRESS = "tmail42021@gmail.com"
PASSWORD = "abc123de45"

#extracting contacts from csv file
def contact_extract():
    contact = []
    with open('contacts.csv', 'r') as file:
        reader = csv.reader(file, delimiter = ',')
        for p in reader:        
            contact.append(p);
    contact = contact[1:]
    to_address = ""
    for c in contact:
        to_address += c[1]
        to_address += ','
    to_address = to_address[:-1]
    return to_address

#constructing the message - can be extended to include attachments
def message_construct():
    subject = "Test Message from Python!"
    message = """\
    Test mail 101: loremipsumdeloreanBACK
    To the future returns
    Automated Email generated through Python."""
    email_msg = MIMEMultipart()
    email_msg['Subject'] = subject
    email_msg.attach(MIMEText(message, 'plain'))
    return email_msg

def main():

    #extracting contacts
    to_addr = contact_extract()

    #constructing a message
    msg = message_construct()

    #setting up the SMTP server
    smtp = smtplib.SMTP('smtp.gmail.com', port = '587')
    smtp.ehlo()
    smtp.starttls()
    smtp.login(SENDER_ADDRESS, PASSWORD)

    rcpt = to_addr.split(",")

    msg['To'] = to_addr
    smtp.sendmail(SENDER_ADDRESS, rcpt, msg.as_string())
    smtp.quit()

if __name__ == "__main__":
    main()


