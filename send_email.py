# import libraries for sending emails
from email.mime.text import MIMEText
import smtplib

# function for sending email that includes variables below
def send_email(email, height, average_height, count):
    # mail data from the sender
    from_email = "bashooff@gmail.com"
    from_password = "Dragon007"
    to_email = email

    # contents
    subject = "Height data"
    message = "Hey there you, your height is <strong>%s</strong>. Average height of all is %s and that is calculated out %s of people " % (height, average_height, count)
    

    msg = MIMEText(message, 'html')
    msg["Subject"] = subject
    msg["To"] = to_email
    msg["From"] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)