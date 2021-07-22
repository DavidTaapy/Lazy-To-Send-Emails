# Lazy-To-Send-Emails

Tired of sending the same emails constantly with just a few changes in the content / recipient, I decided it's time to write a script to automate the process

Inputs required:

- HTML file of the email content with the variables in curly braces
- CSV file with the required information that changes from email to email
- SMTP Information of Email / Domain Name
- Valid Account Address & Password

With these inputs, upon successful logging in, the script can send out these emails automatically!

## Other Files

Initial Jupyter - This jupyter notebook file contains the code that I written initially and it was tested and it worked! However, further automation and modularization of the code was done after this stage so the updated code can be found in the python script in the main directory!

Intial Script - This python script contains the code that I written initially and it was tested and it worked! However, further automation and modularization of the code was done after this stage so the updated code can be found in the python script in the main directory!

## How to use ????

Firstly, add the HTML email in the same directory as the python script! If you have a desired signature, add it to the same directory as well!

Then run the script, and enter the following information after you are prompted:

- Name of the HTML files
- Name of the images
- Your email domain
- Your email address
- Your email password

Then, your email will be sent out !!!!

## Testing of script

The script was tested using the recipients.csv in which various combinations as described by the remarks column was used to test the different use cases!

For the first 3 test cases, the script should send out the emails as they have at least one recipient although in the various patterns! As for the 4th test case without a recipient, the script would print a message to inform the user of the lack of recipient!
