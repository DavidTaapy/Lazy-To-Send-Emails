# Importing required libraries
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import pandas
import codecs
import os

# Getting user inputs - Domain, Email & Password


def run_app():
    domain, sender_email, password = get_inputs()
    domain_info = get_domain_info(domain)
    if domain_info:
        smtp_server, port = domain_info
    else:
        print("Apologies! You domain is not in our list of domains!")
        return 0  # End Application
    send_emails(sender_email, password, smtp_server, port)


def get_inputs():
    domain = input(
        'Please enter whether you are using Outlook / Gmail / Hotmail: ')
    sender_email = input('Type your email address and press enter: ')
    password = input('Type your password and press enter: ')
    return domain, sender_email, password


def get_domain_info(domain):
    domain_info = pandas.read_csv("./Data/domain_list.csv")
    domain = domain.lower()
    if not domain in domain_info["Domain_Name"].to_list():
        return False
    row_selector = (domain_info["Domain_Name"] == domain)
    domain_index = [i for i, val in enumerate(row_selector) if val][0]
    smtp_server = domain_info.loc[domain_index, "SMTP_Address"]
    port = int(domain_info.loc[domain_index, "Port_TLS"])  # For starttls
    return smtp_server, port


def read_content():
    f = codecs.open("Email.htm", 'r', "utf-16")
    return f.read()


def get_body(msg):
    start_index = msg.index(
        "<p><span style=\'mso-bookmark:_MailOriginal\'>")
    return msg[start_index:]


def get_subject(msg):
    left_index = msg.index("Subject:</b> ") + len("Subject:</b> ")
    right_index = msg.index("<o:p></o:p>")
    return msg[left_index:right_index]


def clean_body(msgFirst):
    msg = "<html><head></head><body><div>"
    msg += get_body(msgFirst)
    return msg


def send_emails(sender_email, password, smtp_server, port):
    # Reading email content in html format while removing whitespaces
    msgFull = read_content().replace("\r\n", " ")
    # Getting subject
    subject = get_subject(msgFull)
    # Extracting the body content
    msg = clean_body(msgFull)
    # Reading the recipient information
    recipient_info = pandas.read_csv("./Data/recipients.csv")
    variables = list(recipient_info.keys())
    # Create a secure SSL context
    context = ssl.create_default_context()
    # Setting up the server
    server = smtplib.SMTP(smtp_server, port)
    server.starttls(context=context)  # Securing the connection
    # Login to the server
    try:
        server.login(sender_email, password)
    except:
        print('Incorrect user credentials!')
        return 0
    try:
        # Sending email for each movie
        for index, row in recipient_info.iterrows():
            # Creating the Root message
            msgRoot = MIMEMultipart('related')

            # Setting the subject
            msgRoot['Subject'] = subject.format(
                Title=row["Title"], Year=row['Year'])

            # Adding sender email
            msgRoot['From'] = sender_email

            # Assigning recipients to 'To'
            if isinstance(row["Email"], str):
                msgRoot['To'] = row["Email"]
            else:
                recipient_info.loc[index, "Failure Reason"] = "No recipients!"
                continue

            # Handling CC
            if isinstance(row["CC"], str):  # If there are people to CC
                msgRoot['Cc'] = row["CC"]

            # Adding body to root message
            msgAlternative = MIMEMultipart('alternative')
            msgRoot.attach(msgAlternative)

            # Replacing keywords using information in the recipients information
            msgHere = msg
            for variable in variables:
                to_replace = '{' + variable + '}'
                msgHere = msgHere.replace(to_replace, str(row[variable]))

            # Replacing images with appropriate text
            filelist = [f for f in os.listdir(
                'Email_files') if f.endswith('.png')]
            imageNum = 1
            for image in filelist:
                file_to_replace = 'Email_files/' + image
                msgHere = msgHere.replace(
                    file_to_replace, "cid: image" + str(imageNum))
                imageNum += 1

            # Attaching to email
            msgText = MIMEText(msgHere, 'html')
            msgAlternative.attach(msgText)

            # Define the image's ID as referenced above
            imageNum = 1
            for image in filelist:
                fp = open('./Email_files/' + image, 'rb')
                msgImage = MIMEImage(fp.read())
                fp.close()
                msgImage.add_header(
                    'Content-ID', '<image' + str(imageNum) + '>')
                msgRoot.attach(msgImage)
                imageNum += 1

            # Sending to recipients
            toSend = list(row["Email"].split(","))
            if isinstance(row["CC"], str):  # If CC exists
                toSend += list(row["CC"].split(","))
            server.sendmail(sender_email, toSend, msgRoot.as_string())
    except Exception as e:
        print(e)
    finally:
        server.quit()
    # Output failure list
    failed_rows = recipient_info['Failure Reason'].apply(
        lambda x: type(x) == str)
    failed = recipient_info.loc[failed_rows]


if __name__ == '__main__':
    run_app()
