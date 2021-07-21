# Importing required libraries
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import pandas

# Setting up smtp and sender credentials
smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = input('Type your email address and press enter: ')
password = input('Type your password and press enter: ')

# Reading the recipient information
recipient_info = pandas.read_csv("recipients.csv")

# Create a secure SSL context
context = ssl.create_default_context()

# Message Template
msg = """\
    <html>
        <head></head>
        <body>
        <p style="font-size: 11pt; font-family: Calibri, sans-serif;">Dear {recipient_name},
        <br><br>
        Greetings from Singapore!
        <br><br>
        I’m Jolie, a programmer for Perspectives Film Festival (PFF), which will run from 21-31 October 2021, and I’m \
        writing to enquire about the film, \
        <span style="font-family: Cambria;font-size: 15px; font-weight: 700; background: rgb(255, 192, 0);">{film_name}</span>, \
        directed by {director_name}.
        <br><br>
        PFF is an annual arts event that is thematically curated, celebrating films from around the world. It is Singapore's \
        first and longest-running film festival by students, presenting breakthroughs in cinema. For more information about \
        our festival, please visit \
        <a href="https://www.perspectivesfilmfestival.com/">www.perspectivesfilmfestival.com</a>.
        <br><br>
        Due to the COVID-19 pandemic, our festival will be completely virtual this year. We will be working closely with local \
        exhibitors with Hollywood studio-grade level digital rights management (DRM) service that ensures playback only occurs \
        on an authenticated video player, geolocation locking, and is MPAA (Motion Pictures Association of America) compliant, \
        along with other security features to ensure content, payment, and privacy are secured.
        <br>
        </p>
        <p style="font-size:11pt; font-family:Calibri, sans-serif; margin-bottom: 0;">
        We have a few queries:
        <ul style="font-size:11pt; font-family:Calibri, sans-serif; margin-top: 0;">
            <li>Would the film be available for a Singapore premiere during our festival period?</li>
            <li>How much would the screening fee be? And does this change depending on the cap on viewers, if any?</li>
            <li>Could you send us a screener for our internal preview within the team to determine the film's suitability to our theme?</li>
        </ul>
        </p>
        <p style="font-size: 11pt; font-family: Calibri, sans-serif; margin-bottom: 0">
        For more info about virtual platforms that we’ll be working with:
        <ul style="font-size: 11pt; font-family: Calibri, sans-serif; margin-top: 0;">
            <li>P+ by The Projector: <a href="https://theprojector.sg/themes/now-on-vod/"">https://theprojector.sg/themes/now-on-vod/</a></li>
            <li>Kinolounge by Shaw Theatres: <a href="https://kinolounge.shaw.sg/">https://kinolounge.shaw.sg/</a></li>
        </ul>
        </p>
        <p style="font-size: 11pt; font-family: Calibri, sans-serif;">
        Thank you for your time and we hope to hear from you soon!
        <br><br>
        Warm regards,
        <br>
        <span style="font-family: Cambria; font-size: 12pt; font-weight: 700;">Jolie Fan</span><br>
        <span style="font-family: Cambria; font-size: 12pt;">Programming Executive</span><br><br>
        <img style="width: 200px; aspect-ratio: auto 200 / 89; height: 89px;" src="cid:image1"><br>
        <span style="font-family: Cambria; font-size: 12pt;">Mobile: +65 96557996</span>
        <br>
        <a style="font-family: Cambria; font-size: 12pt;" href="https://www.perspectivesfilmfestival.com/">Website</a> | \
        <a style="font-family: Cambria; font-size: 12pt;" href="https://www.instagram.com/wkwsci.perspectivesfilmfest/">Instagram</a> | \
        <a style="font-family: Cambria; font-size: 12pt;" href="https://www.facebook.com/wkwsci.perspectivesfilmfest/">Facebook</a>
        <br><br>
        <span style="color:rgb(59,56,56); font-family: sans-serif; font-size: 6pt;">
        CONFIDENTIALITY NOTICE:
        <br>
        This e-mail, including any attachment thereto, are intended only for use by the addressee(s) named herein and may contain legally privileged and/or confidential information. If you are not the intended recipient of this e-mail, please delete it immediately and notify the sender. 
        </span>
        </p>
    </body>
</html>
"""

# Attempt to login and send emails
try:
    server = smtplib.SMTP(smtp_server, port)
    server.starttls(context=context)  # Securing the connection
    server.login(sender_email, password)
    # Read signature image
    fp = open('./Logo.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    for index, row in recipient_info.iterrows():
        # Root message
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = "Enquiry on {film_name} for Perspectives Film Festival 2021".format(
            film_name=row["Film Name"])
        msgRoot['From'] = sender_email

        # Assigning recipients to 'To'
        recipients = row["Email"].split(",")
        msgRoot['To'] = ""
        for recipient in recipients:
            msgRoot['To'] += recipient

        # Adding body to root message
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        msg = msg.format(
            film_name=row["Film Name"], director_name=row["Director Name"], recipient_name=row["Recipient Name"])
        msgText = MIMEText(msg, 'html')
        msgAlternative.attach(msgText)

        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', '<image1>')
        msgRoot.attach(msgImage)

        # Sending to recipients
        for recipient in recipients:
            server.sendmail(sender_email, recipient, msgRoot.as_string())
except Exception as e:
    print(e)
finally:
    server.quit()
