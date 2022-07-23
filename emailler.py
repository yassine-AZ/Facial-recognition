from  email.mime.multipart  import  MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.mime.image import MIMEImage

def sendemail(from_email,password,to_email,subject,message):
    msg =MIMEMultipart()
    msg["From"]=from_email
    msg["To"]=to_email
    msg["subject"]=subject
    msg.attach(MIMEText(message,"plain"))

    fp = open('personne_detecter.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)

    try:
        server=smtplib.SMTP_SSL("smtp.gmail.com",465)
        server.ehlo()
        server.login(from_email,password)
        server.sendmail(from_email,to_email,msg.as_string())
        server.close()
        return True
    except Exception as e:
        print("Erreur"+str(e))
        return False

