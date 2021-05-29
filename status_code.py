# python3 status_code.py 5 3
# will fetch status code of websites in the list 
# after intervals of 5 seconds and this program
# will run for 3 iterations
# total time = approx (no. of iterations * sleep time)


#importing libraries
import requests
import smtplib
import csv
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import click
import time
import validators
from datetime import datetime

#mailer address and password to set up SMTP and send mails
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

#constructing the email contents
def message_construct(resp):
    subject = "Bad response code from website"
    message = "Hi!\nThe website " + resp.url + f" is not working!\nError code: {resp.status_code}"
    message += "\nError: " + resp.reason
    email_msg = MIMEMultipart()
    email_msg['Subject'] = subject
    email_msg.attach(MIMEText(message, 'plain'))
    return email_msg

@click.command()
@click.argument('timer', default=10)
@click.argument('count', default=1)
def main(timer, count):

    #extracting contacts
    to_addr = contact_extract()

    #setting up SMTP
    smtp = smtplib.SMTP('smtp.gmail.com', port = '587')
    smtp.ehlo()
    smtp.starttls()
    smtp.login(SENDER_ADDRESS, PASSWORD)

    # to store the all the results
    file2 = open('log.txt', 'w')

    # keep running for count iterations
    while count > 0:
        # list.txt contains the list of websites to be tracked
        # keep reading it again to stay most updated
        file1 = open('list.txt', 'r')
        lines = file1.readlines()

        for line in lines:
            addr = "https://" + line.strip()
            #check if url is valid otherwise skip
            if validators.url(addr):
                print(addr)
            else:
                print(addr + " is not a valid url")
                continue

            resp = requests.get(addr)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            if resp.status_code == 200:
                str = current_time + " : " + addr + " is working\n"
                file2.write(str)
            else:
                str = current_time + " : " + addr + f" has error : {resp.status_code}\n"
                file2.write(str)

                #constructing a message
                msg = message_construct(resp)

                rcpt = to_addr.split(",")               #recipients list
                msg['To'] = to_addr
                smtp.sendmail(SENDER_ADDRESS, rcpt, msg.as_string())

        # repeat after timer seconds
        file1.close()
        time.sleep(timer)
        count -= 1
    
    smtp.quit()
    file2.close()
    
if __name__ == "__main__":
    main()