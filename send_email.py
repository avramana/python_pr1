from email.mime.text import MIMEText
import smtplib

def sendmail(toemail,height,count,avg_height):
    print("sending email")
    fromEmail="ramana.adapala@gmail.com"
    fromPassword="xxxxxxxx"

    subject="Height Data"
    message="Hey, your height is <strong>%s</strong>cm, average height of %s people is <strong>%s</strong>cm" % (height,count,avg_height)

    msg=MIMEText(message,'html')
    msg['Subject'] = subject
    msg['To'] = toemail
    msg['From'] = fromEmail

    gmail=smtplib.SMTP("smtp.gmail.com",587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(fromEmail,fromPassword)
    gmail.send_message(msg)
    print("Done...")