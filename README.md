# Lazy-To-Send-Emails

Tired of sending the same emails constantly with just a few changes in the content / recipient, I decided it's time to write a script to automate the process

Inputs required:

- HTML file of the email content with the variables in curly braces
- CSV file with the required information that changes from email to email
- SMTP information of email / domain name
- Valid account address & password

With these inputs, upon successful logging in, the script can send out these emails automatically!

## Other Files

Initial Jupyter - This jupyter notebook file contains the code that I written initially and it was tested and it worked! However, further automation and modularization of the code was done after this stage so the updated code can be found in the python script in the main directory!

Intial Script - This python script contains the code that I written initially and it was tested and it worked! However, further automation and modularization of the code was done after this stage so the updated code can be found in the python script in the main directory!

## How to use ????

Firstly, download the email as a html file in the same directory as the python script and name it as 'email.html' with the variables being encoded in curly braces with their column name of the 'recipients.csv' as illustrated in the website below! Secondly, have the recipient information ready in csv format and store it in the same directory as 'recipients.csv'! Ensure that the 'domain_list.csv' is present in the directory as well!

**Tip for creating html**
_https://www.extendoffice.com/documents/outlook/3623-outlook-save-email-as-html.html_

Then run the script, and enter the following information after you are prompted:

- Your email domain
- Your email address
- Your email password

Then, your email will be sent out !!!!

## Testing of script

The script was tested using the recipients.csv in which various combinations as described by the remarks column was used to test the different use cases!

For the first 3 test cases, the script should send out the emails as they have at least one recipient although in the various patterns! As for the 4th test case without a recipient, the script would include it in a failure.csv file which is used to contain all rows that have failed!

## Authentication error even with the correct username and password ????

For certain domains such as Gmail, it is set by default to not allow python scripts to send out emails remotely and so users have to allow for 'less secure apps' for the script to function!

## Snapshots

![Received Emails](/Snapshots/Received-Emails.PNG)

![Sent Emails](/Snapshots/Sent-Emails.PNG)
