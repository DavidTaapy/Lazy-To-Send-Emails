# Importing required libraries
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import pandas


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


def replace_vars(variables, row, content):
    for variable in variables:
        to_replace = '{' + variable + '}'
        content = content.replace(to_replace, str(row[variable]))
    return content


def send_emails(sender_email, password, smtp_server, port, subject, content):
    # Replace \n to <br> which is used in emails
    content = content.replace('\n', '<br>')
    # Reading the recipient information
    data = pandas.read_csv("./Data/data.csv")
    variables = list(data.keys())
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
        for index, row in data.iterrows():
            # Creating the Root message
            msgRoot = MIMEMultipart('related')

            # Setting the subject
            msgRoot['Subject'] = replace_vars(variables, row, subject)

            # Adding sender email
            msgRoot['From'] = sender_email

            # Assigning recipients to 'To'
            if isinstance(row["Email"], str):
                msgRoot['To'] = row["Email"]
            else:
                data.loc[index, "Failure Reason"] = "No recipients!"
                continue

            # Handling CC
            if isinstance(row["CC"], str):  # If there are people to CC
                msgRoot['Cc'] = row["CC"]

            # Adding body to root message
            msgAlternative = MIMEMultipart('alternative')
            msgRoot.attach(msgAlternative)

            # Replacing keywords using information in the recipients information
            msgHere = replace_vars(variables, row, content)

            # Attaching to email
            msgText = MIMEText(msgHere, 'html')
            msgAlternative.attach(msgText)

            # Sending to recipients
            toSend = list(row["Email"].split(","))
            if isinstance(row["CC"], str):  # If CC exists
                toSend += list(row["CC"].split(","))
            server.sendmail(sender_email, toSend, msgRoot.as_string())
