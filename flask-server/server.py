# Import required libraries
from flask import Flask, request
from flask_cors import CORS
from app import send_emails, get_domain_info

# Get required components
cors = CORS()

# Instantiate Flask Application
app = Flask(__name__)
cors.init_app(app)

# Route to handle email sending
@app.route("/sendEmails/", methods=["POST"])
def sendEmails():
    # Get the user inputs required
    domain = request.json['domain']
    email = request.json['email']
    password = request.json['password']
    subject = request.json['subject']
    content = request.json['content']
    # Get domain info
    smtp_server, port = get_domain_info(domain)
    # Send the emails
    failed = send_emails(email, password, smtp_server, port, subject, content)
    return failed

# Run the application
if __name__ == "__main__":
    app.run(debug=True)