import smtplib
import imaplib 
import email
import time
from datetime import date
import init_script as init
import motor_script as motor

def sendProfileEmail():
    time = date.today()
    time = time.strftime("%d/%m/%Y")
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(init.sourceAdd, init.password)
    subject = "IoT Project - Profile"
    body = "User Tag: " + init.helper.userTag + " has logged in at " + time
    msg = f"Subject: {subject}\n\n{body}"

    s.sendmail(init.sourceAdd, init.destAdd, msg)
    s.quit()

def sendLEDNotificationEmail():
    time = date.today()
    time = time.strftime("%d/%m/%Y")
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(init.sourceAdd, init.password)

    subject = "LED Status Notification"
    body = "The LED was set to ON at " + time
    msg = f"Subject: {subject}\n\n{body}"

    s.sendmail(init.sourceAdd, init.destAdd, msg)
    s.quit()

def sendMotorNotificationEmail():
    time = date.today()
    time = time.strftime("%d/%m/%Y")
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(init.sourceAdd, init.password)

    subject = "Motor Status Notification"
    body = "The motor was set to ON at " + time + " and is currently running. Would you like to ENABLE the fan?\n\n Type 'ENABLE' to enable the fan or 'DISABLE' to disable the fan."
    msg = f"Subject: {subject}\n\n{body}"

    s.sendmail(init.sourceAdd, init.destAdd, msg)
    s.quit()

def receiveMail():
    while True:
        print("Waiting for email...")
        conn = imaplib.IMAP4_SSL(init.imap_srv, init.imap_port)
        conn.login(init.sourceAdd, init.password)
        conn.select('INBOX')
        status, data = init.sourceAdd.search(None, 'FROM ' + init.destAdd + ' SUBJECT "LED Status Notification" UNSEEN')
        mail_ids = []
        for block in data:
            mail_ids += block.split()
        for i in mail_ids:
            status, data = init.sourceAdd.fetch(i, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1].decode('utf-8'))
                    email_from = msg['from']
                    email_subject = msg['subject']
                    print('From: ' + email_from + '\n')
                    print('Subject: ' + email_subject + '\n')
                    if msg.is_multipart():
                        mail_content = ''
                        for part in msg.get_payload():
                            if part.get_content_type() == 'text/plain':
                                mail_content = part.get_payload()
                                reply = f'Content: {mail_content}'
                                if ("YES" in reply):
                                    init.helper.sentEmailCount += 1
                                    motor.spinMotor()
                                    init.helper.motorStatusMsg = "Motor is ON"
                                    return init.helper.motorStatusMsg
                    else:
                        mail_content = msg.get_payload()
                        return False
        time.sleep(10)