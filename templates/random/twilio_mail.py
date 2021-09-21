
# --------------------------------------- FLASK_MAIL TWILIO -------------------------------
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'top-secret!'
# app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'apikey'
# app.config['MAIL_PASSWORD'] = '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'
# app.config['MAIL_DEFAULT_SENDER'] = "adamjackson397@gmail.com"
# mail = Mail(app)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         recipient = request.form['recipient']
#         msg = Message('Twilio SendGrid Test Email', recipients=[recipient])
#         msg.body = ('Congratulations! You have sent a test email with '
#                     'Twilio SendGrid!')
#         msg.html = ('<h1>Twilio SendGrid Test Email</h1>'
#                     '<p>Congratulations! You have sent a test email with '
#                     '<b>Twilio SendGrid</b>!</p>')
#         mail.send(msg)
#         flash(f'A test message was sent to {recipient}.')
#         return redirect(url_for('index'))
#     return render_template('index.html')



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
#         recipient_email = "charlottestowell@berkeley.edu"
        
#         msg = Message('Twilio Test Email', recipients=[recipient_email])
#         msg.body = ('Hello! I saw your post & would love to meet-up.'
#                     'Let me know!')
#         msg.html = ('<h1>Twilio SendGrid Test Email</h1>'
#                     '<p>Hello! I saw your post & would love to meet-up '
#                     '<b>Let me know!</b>!</p>')
#         mail.send(msg)
#         flash(f'A test message was sent to {recipient_email}.')
#         return redirect(url_for('exchange'))
#     return render_template('exchange.html')
# --------------------------------------- FLASK_MAIL TWILIO -------------------------------