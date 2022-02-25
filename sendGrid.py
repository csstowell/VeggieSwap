
import os
from flask import Flask
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


message = Mail(from_email='adamjackson397@gmail.com',
               to_emails='charlottestowell@berkeley.edu',
               subject='Saw your produce listing!',
               plain_text_content='would love to meet up for a swap.',
               html_content='<strong>would love to meet up for a swap.</strong>')
try:
    sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)



############### ##########################
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
from_email = Email("test@example.com")  # Change to your verified sender
to_email = To("test@example.com")  # Change to your recipient
subject = "Sending with SendGrid is Fun"
content = Content("text/plain", "and easy to do anywhere, even with Python")
mail = Mail(from_email, to_email, subject, content)

# Get a JSON-ready representation of the Mail object
mail_json = mail.get()

# Send an HTTP POST request to /mail/send
response = sg.client.mail.send.post(request_body=mail_json)
print(response.status_code)
print(response.headers)
