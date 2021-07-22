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
        Greetings from Lazy Land!
        <br><br>
        I’m David from Lazy Land and I’m writing to enquire about the film, \
        <span style="font-family: Cambria;font-size: 15px; font-weight: 700; background: rgb(255, 192, 0);">{film_name}({film_year})</span>, \
        directed by {director_name}.
        <br><br>
        I love watching films and my favourite film festival can be found at \
        <a href="https://www.perspectivesfilmfestival.com/">www.perspectivesfilmfestival.com</a>.
        <br><br>
        Due to the COVID-19 pandemic, their festival will be completely virtual this year. They will be working closely with local \
        exhibitors with Hollywood studio-grade level digital rights management (DRM) service that ensures playback only occurs \
        on an authenticated video player, geolocation locking, and is MPAA (Motion Pictures Association of America) compliant, \
        along with other security features to ensure content, payment, and privacy are secured.
        <br>
        </p>
        <p style="font-size:11pt; font-family:Calibri, sans-serif; margin-bottom: 0;">
        They have a few queries:
        <ul style="font-size:11pt; font-family:Calibri, sans-serif; margin-top: 0;">
            <li>This is my first query!</li>
            <li>This is my second query!</li>
            <li>This is my third query!</li>
        </ul>
        </p>
        <p style="font-size: 11pt; font-family: Calibri, sans-serif; margin-bottom: 0">
        For more info about virtual platforms that they will be working with:
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
        <span style="font-family: Cambria; font-size: 12pt; font-weight: 700;">Lazy David</span><br>
        <span style="font-family: Cambria; font-size: 12pt;">Programming Executive</span><br><br>
        <img style="width: 200px; aspect-ratio: auto 200 / 89; height: 89px;" src="cid:image1"><br>
        <span style="font-family: Cambria; font-size: 12pt;">Mobile: +65 12345678</span>
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
    # Setting up the server
    server = smtplib.SMTP(smtp_server, port)
    server.starttls(context=context)  # Securing the connection
    server.login(sender_email, password)

    # Read signature image
    fp = open('./logo.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Sending email for each movie
    for index, row in recipient_info.iterrows():
        # Root message
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = "Enquiry on {film_name}({film_year}) for Perspectives Film Festival 2021".format(
            film_name=row["Title"], film_year=row['Year'])

        # Adding sender email
        msgRoot['From'] = sender_email

        # Assigning recipients to 'To'
        msgRoot['To'] = row["Email"]

        # Handling CC
        if isinstance(row["CC"], str):  # If there are people to CC
            msgRoot['Cc'] = row["CC"]

        # Adding body to root message
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        msgHere = msg.format(
            film_name=row["Title"], director_name=row["Director"], recipient_name=row["Distributor Name"], film_year=row["Year"])
        msgText = MIMEText(msgHere, 'html')
        msgAlternative.attach(msgText)

        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', '<image1>')
        msgRoot.attach(msgImage)

        # Sending to recipients
        toSend = list(row["Email"].split(","))
        if isinstance(row["CC"], str):  # If CC exists
            toSend += list(row["CC"].split(","))
        server.sendmail(sender_email, toSend, msgRoot.as_string())
except Exception as e:
    print(e)
finally:
    server.quit()
