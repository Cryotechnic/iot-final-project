import smtplib
import imaplib 
import email
import time
from datetime import date
import init_script as init
# import motor_script as motor



sender = "pythonmailer9843098432@gmail.com"
password = "monkeyman123?"

def sendProfileEmail():
    time = date.today()
    time = time.strftime("%d/%m/%Y")
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo()
    s.login(sender, password)
    subject = "IoT Project - Profile"
    body = "User Tag: " + init.helper.userTag + " has logged in at " + time
    msg = f"Subject: {subject}\n\n{body}"

    s.sendmail(sender, sender, msg)
    s.quit()

def sendLEDNotificationEmail():
    time = date.today()
    time = time.strftime("%d/%m/%Y")
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo()
    s.login(sender, password)

    subject = "LED Status Notification"
    body = "The LED was set to ON at " + time
    msg = f"Subject: {subject}\n\n{body}"

    s.sendmail(sender, sender, msg)
    s.quit()

def sendMotorNotificationEmail():
    time = date.today()
    time = time.strftime("%d/%m/%Y")
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo()
    s.login(sender, password)

    subject = "Motor Status Notification"
    body = "The motor was set to ON at " + time + " and is currently running. Would you like to ENABLE the fan?\n\n Type 'ENABLE' to enable the fan or 'DISABLE' to disable the fan."
    msg = f"Subject: {subject}\n\n{body}"

    s.sendmail(sender, sender, msg)
    s.quit()

def receiveMail():

    while True:
    # get most recent email
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(sender, password)
            mail.list()
            mail.select('inbox')
            result, data = mail.uid('search', None, 'ALL')
            inbox_item_list = data[0].split()
            most_recent = inbox_item_list[-1]
            result, data = mail.uid('fetch', most_recent, '(RFC822)')
            raw_email = data[0][1].decode('utf-8')
            email_message = email.message_from_string(raw_email)
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    body = body.decode('utf-8')
                    if body.lower().startswith("enable"):
                        print("Motor is enabled")
                        mail.logout()
                        return True
        except Exception as e:
            mail.logout()
            print("No new emails")

if __name__ == "__main__":
    receiveMail()