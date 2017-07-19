# Import system modules
import smtplib
from email.mime.text import MIMEText

def sendEmail(message,subject,receiver):
    """ Send an e-mail.
    message = message to send in the e-mail
    subject = the subject for the e-mail
    receiver = a list of recipient(s) for the e-mail
    """
    # the e-mail address sending the message
    sender = ""
    # username for the sender e-mail
    username = ""
    # password for the sender e-mail
    password = ""

    # message to be sent
    msg = MIMEText(message)
    # e-mails subject
    msg['Subject'] = subject
    # sender
    msg['From'] = sender
    # receiver
    COMMASPACE = ', ' # used to seperate e-mail addresses in list of recipients
    msg['To'] = COMMASPACE.join(receiver)

    # create a connection to server
    server = smtplib.SMTP_SSL('your mail server', 'port number as integar')
    # login to server
    server.login(username,password)
    # send e-mail
    server.sendmail(sender,receiver, msg.as_string())
    # close server
    server.quit()
# end  sendEmail