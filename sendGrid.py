
import os
from flask import Flask
# from flask_mail import Mail, Message
import twilio
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



# ----------------------------------------------------------------------------------------
##############  TWILIO  #############
# import os
# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_mail import Mail, Message

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'top-secret!'
# app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'apikey'
# app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
# #app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
# app.config['MAIL_DEFAULT_SENDER'] = "adamjackson397@gmail.com"
# mail = Mail(app)





################### TWILIO SENDGRID API ROUTE #################
# @app.route('/exchange/contact/<int:id>', methods=['GET', 'POST'])
# def email_exchange(id):
#     """Sends email to user using Twilio SendGrid API"""

#     if 'current_user' not in session:
#         return redirect('/login')

#     if request.method == 'POST':
#         # look up the user's email address by id
#         user = crud.lookup_user_by_id(id)
#         recipient_email = user.email
        
#         # TEMP: hardcode email to ME for the demos!!!
#         # recipient_email = "charlottestowell@berkeley.edu"
        
#         message = Mail(from_email='adamjackson397@gmail.com',
#                     to_emails='charlottestowell@berkeley.edu',
#                     subject='Saw your produce listing!',
#                     plain_text_content='would love to meet up and do a swap.',
#                     html_content='<strong>would love to meet up and do a swap.</strong>')
#         try:
#             sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
#             response = sg.send(message)
#             print(response.status_code)
#             print(response.body)
#             print(response.headers)
#         except Exception as e:
#             print(e.message)
#             flash(f'A test message was sent to {recipient_email}.')
#             return redirect(url_for('exchange'))
#     return render_template('exchange.html')
#####################################################