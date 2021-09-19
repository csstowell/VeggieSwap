import crud
import googlemaps
import math
from flask import (Flask, render_template, request, flash, session, redirect, jsonify, url_for)
from models import Produce, User, UserProduce, ExchangeProduce, db, connect_to_db
from forms import ProduceSearchForm
from db_setup import init_db, db_session
from sqlalchemy import func
import requests
import simplejson as json

init_db()


app = Flask(__name__)
app.secret_key = "SECRET"

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

##############  TWILIO  #############

# -------------------------------------------

# INDEX
# @app.route('/')
# def index():
#     """View index page"""
#     if 'current_user' not in session:
#         return redirect('/login')
#     else:
#         username = session['current_user']
#         return redirect(f'/home')
#     return render_template('home.html')


# HOMEPAGE
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    """Home Page"""

    return render_template('home.html')


# PRODUCE PAGE
@app.route('/produce', methods=['GET', 'POST'])
def produce_page():
    """View all produce listings from database"""
    search = ProduceSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    items = Produce.query.all()

    return render_template('produce.html', items=items, form=search)


# SEARCH PRODUCE RESULTS
@app.route('/results')
def search_results(search):
    """return list of search results"""
    
    results = []
    form = ProduceSearchForm(request.form)
    search_string = form.data['search']

    if request.method == 'POST':
        qry = db_session.query(Produce).filter(func.lower(Produce.name) == func.lower(search_string))
        results = qry.all()
    if not results:
        flash('No results found!')
        return redirect('/produce')
    else:
        # display results
        return render_template('produce.html', items=results, form=form)


# USER-PAGE
@app.route('/user', methods=['GET', 'POST'])
def user_page():
    """View all user produce"""

    search = ProduceSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    items = Produce.query.all()

    if 'current_user' in session:
        username = session['current_user']
        user_produce = crud.get_user_veggies(username)

    else:
        return redirect('/login')

    return render_template("user.html", user_produce=user_produce, form=search)

# SHOW PRODUCE BY ID
@app.route('/produce/<produce_id>', methods=['POST', 'GET'])
def show_produce(produce_id):
    '''Return produce details & provide button to add produce.'''
    produce = crud.get_produce_by_id(produce_id)

    return render_template("display_details.html", display_produce=produce)


# ADD USER PRODUCE
@app.route('/add_user_produce/<int:produce_id>', methods=['POST', 'GET'])
def add_user_produce(produce_id):
    """add user produce to user_page"""

    if request.method == 'POST':
        user_id = session['current_user_id']

        session['quantity'] = request.form['quantity']
        session['condition'] = request.form['condition']
        new_quantity = int(session['quantity'])
        condition = session['condition']

        if (crud.user_produce_exists(user_id, produce_id)):
            # do an update
            crud.update_user_produce_amount(user_id, produce_id, new_quantity)


        else:
            user_produce = crud.add_user_produce(
                produce_id, user_id, new_quantity, condition)
            session['quantity'] = user_produce.quantity
            # current_quantity = session['quantity']
            # print('QUANTITY IS CURRENTLY:', current_quantity)
            
            
        flash('Produce has been added to your garden!')
        return redirect('/user')
    return render_template('user.html', user_produce=user_produce, new_quantity=new_quantity)


# DELETE USERPRODUCE
@app.route("/user/delete/<int:id>", methods=['GET', 'POST'])
def delete_user_produce(id):
    if request.method == 'POST':
        user_produce_id = UserProduce.query.get(id)
        db.session.delete(user_produce_id)
        db.session.commit()
        flash('Produce has been deleted!')

    return redirect('/user')


# ADD EXCHANGE PRODUCE & UPDATE
@app.route('/user/exchange/<int:id>', methods=['GET', 'POST'])
def add_exchange_produce(id):
    """Adds vegetable from user's produce to the exchange"""

    if request.method == 'POST':
        user_id = session['current_user_id']
        userproduce_id = id
        if(crud.user_exchange_exists(userproduce_id)):
            flash('Produce has already been added!')
            return redirect('/user')

        else:
            
            comment = request.form['comment']
            amount = int(request.form['amount'])

            # create new user exchange produce & add to db
            exchange_items = crud.add_exchange_produce(userproduce_id, amount, comment)
            
            current_quantity = session['quantity']
            new_produce_amount = (current_quantity - amount)
            
            # update user produce to reflect exchange
            crud.update_user_produce_quantity(userproduce_id, new_produce_amount)
            
            print('QUANTITY IS CURRENTLY:', current_quantity)
            print('UPDATED USER PRODUCE???', new_produce_amount)

            db.session.commit()
        flash('Added to the exchange!')

    return redirect('/exchange')
    return render_template('exchange.html', exchange_items=exchange_items, user_produce=user_produce)


# DISPLAY EXCHANGE PAGE
@app.route('/exchange')
def exchange():
    """Show exchange page"""

    radius_in_miles = request.args.get('distance')

    if (radius_in_miles == None):
        radius_in_miles = 20
    
    radius_in_miles = float(radius_in_miles)
    
    # we are passing in 'miles', need to convert to meters
    METERS_IN_MILE = 1609.34
    radius = radius_in_miles * METERS_IN_MILE
    
    zipcode = request.args.get('zipcode')
    if (zipcode == None):
        zipcode = '94114'

    # get user session-- check if logged in -- save zipcode

    # call geocoder.geocode
    gmaps = googlemaps.Client(key='AIzaSyDIYpD84hN93_pAL4oomppVemp3JYSvaRE')

    geocode_result = gmaps.geocode(zipcode)
    center_lat = geocode_result[0]['geometry']['location']['lat']
    center_lng = geocode_result[0]['geometry']['location']['lng']
    exchange_items = crud.get_exchange_by_distance(center_lat, center_lng, radius)
    
    #exchange_items = ExchangeProduce.query.all()

    return render_template('exchange.html', exchange_items=exchange_items, zipcode=zipcode, radius=radius  )


################### TWILIO SENDGRID API ROUTE #################
@app.route('/exchange/contact/<int:id>', methods=['GET', 'POST'])
def email_exchange(id):
    """Sends email to user using Twilio SendGrid API"""
    if request.method == 'POST':
        # look up the user's email address by id
        user = crud.lookup_user_by_id(id)
        recipient_email = user.email
        
        # TEMP: hardcode email to ME for the demos!!!
        recipient_email = "charlottestowell@berkeley.edu"
        
        msg = Message('Twilio Test Email', recipients=[recipient_email])
        msg.body = ('Hello! I saw your post & would love to meet-up.'
                    'Let me know!')
        msg.html = ('<h1>Twilio SendGrid Test Email</h1>'
                    '<p>Hello! I saw your post & would love to meet-up '
                    '<b>Let me know!</b>!</p>')
        mail.send(msg)
        flash(f'A test message was sent to {recipient_email}.')
        return redirect(url_for('exchange'))
    return render_template('exchange.html')

################### TWILIO SENDGRID API ROUTE #################





#--------------------------- LOGIN/REGISTER HANDLERS ------------------------------------------#

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """View login page"""

    return render_template('login.html')

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    """View sign up form"""

    return render_template('register.html')


# LOGIN HANDLER
@app.route('/handle-login', methods=['POST'])
def handle_login():
    """Log user into site"""

    username = request.form['username']
    password = request.form['password']

    user = crud.lookup_user(username)
    if not user:
        flash("No account with this username. Please sign up.")
        return redirect('/register')

    if password == crud.get_password(username):
        session['current_user'] = username
        session['current_user_id'] = user.id
        return redirect("/home")
    else:
        flash("Wrong password. Please try again.")
        return redirect('/login')


# REGISTER HANDLER
@app.route('/handle-register', methods=['GET', 'POST'])
def handle_register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        zipcode = request.form.get('zipcode')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('user already exists.', category='error')
        elif len(email) < 4:
            flash('email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            # # construct full address
            full_address = address + "," + city + "," + state + "," + zipcode

            # call gmaps.geocode to get lat/lng
            gmaps = googlemaps.Client(
                key='AIzaSyDIYpD84hN93_pAL4oomppVemp3JYSvaRE')

            # Geocoding an address
            geocode_result = gmaps.geocode(full_address)
            # print (geocode_result[0]["geometry"]["location"])
            lat = geocode_result[0]["geometry"]["location"]["lat"]
            lng = geocode_result[0]["geometry"]["location"]["lng"]

            user = crud.create_user(
                username, email, password1, address, city, zipcode, lat, lng)
            session['current_user'] = username.title()
            session['current_user_id'] = user.id
            session['user_lat'] = lat
            session['user_lng'] = lng

            flash(f"Welcome to the Community, {username}")
            return redirect(f'/user')

# LOGOUT PAGE


@app.route('/logout')
def handle_logout():
    """Logs player out"""

    del session['current_user']
    del session['current_user_id']

    flash(f"You've successfully logged out.")
    return redirect('/login')

#--------------------------- NEW ------------------------------------------#

API_KEY = '94016bc42734493084e87bba6984b963'

###################   SPOONACULAR API    ###################################


@app.route('/', methods=['GET', 'POST'])
def recipes():
    """Returns recipes based on ingredient"""
    if request.method == 'POST':
        content = requests.get(
            "https://api.spoonacular.com/recipes/findByIngredients?ingredients=" +
            (request.form['restaurant_name']) +
            "&apiKey=" + API_KEY)
        json_response = json.loads(content.text)
        print(json_response)
        return render_template("recipes.html", response=json_response) if json_response != [] else render_template(
            "recipes.html", response="")
    else:
        return render_template("recipes.html")
############################## SPOONACULAR API ###################################






#-------------------------END--------------------------------#
if __name__ == "__main__":
    app.debug = True
    connect_to_db(app, "produce_swap")
    app.run(host='0.0.0.0')
