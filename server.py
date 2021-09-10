from flask import (Flask, render_template, request, flash, session, redirect, jsonify, url_for)
from models import Produce, User, UserProduce, ExchangeProduce, db, connect_to_db
import crud
import googlemaps
# import geocoder
from forms import ProduceSearchForm
from db_setup import init_db, db_session
init_db()

app = Flask(__name__)
app.secret_key = "SECRET"
# ---------------------------------------------------------

#INDEX
@app.route('/')
def index():
    """View index page"""
    if 'current_user' not in session:
        return redirect('/login')
    else:
        username = session['current_user']
        return redirect(f'/home')
    return render_template('home.html')


# HOMEPAGE
@app.route('/home', methods=['GET', 'POST'])
def home_page():

    if request.method == 'POST':
        # Save the form data to the session object
        session['address'] = request.form['home_address']
        return redirect(url_for('user_info'))
    return render_template('home.html')

# USER-INFO
@app.route('/home/user_info', methods=['GET', 'POST'])
def user_info():
    """Show user's info"""
    return render_template('user_info.html')


# MARKET
@app.route('/market', methods=['GET', 'POST'])
def market_page():
    """View all produce listings from database"""
    search = ProduceSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    items = Produce.query.all()

    return render_template('market.html', items=items, form=search)



# SEARCH RESULTS
@app.route('/results')
def search_results(search):
    results = []

    form = ProduceSearchForm(request.form)
    search_string = form.data['search']

    if request.method == 'POST':
        qry = db_session.query(Produce).filter_by(name=search_string)
        results = qry.all()
    if not results:
        flash('No results found!')
        return redirect('/market')
    else:
        # display results
        return render_template('market.html', items=results, form=form)

# USER
@app.route('/user', methods=['GET', 'POST'])
def user_page():
    """View all user produce"""
    if 'current_user' in session: 
        username= session['current_user']
        user_produce = crud.get_user_veggies(username)

    else:
        return redirect('/login')
    return render_template("user.html", user_produce=user_produce)




    # if 'current_user_id' in session:
    #     session['current_user_id'] = (UserProduce.user_id)
    #     user_id = session['current_user_id']
    #     print("USER ID IS: !!!!!!", user_id)
    #     user_produce = crud.get_user_produce(user_id)
    #     print("USER PRODUCE IS: !!!!!!!", user_produce)


# SHOW PRODUCE BY ID
@app.route('/market/<produce_id>', methods=['POST', 'GET'])
def show_produce(produce_id):
    '''Return produce details & provide button to add produce.'''
    produce = crud.get_produce_by_id(produce_id)

    return render_template("display_details.html", display_produce=produce)


# ADD TO USERPRODUCE
@app.route('/add_user_produce/<int:produce_id>', methods=['POST', 'GET'])
def add_user_produce(produce_id):
    '''add user produce to user_page'''
            
    if request.method == 'POST':
        user_id = session['current_user_id']
        session['quantity'] = request.form['quantity']
        session['condition'] = request.form['condition']
        new_quantity = int(session['quantity'])
        print('QUANTITY!!!!!!!!', new_quantity)
        condition = session['condition']
        
        if (crud.user_produce_exists(user_id, produce_id)):
            # do an update 
            crud.user_produce_update(user_idproduce_id, new_quantity)
            flash('Produce has been updated!')
            # session['quantity'] = session['quantity'] + 
            
        else:
            user_produce = crud.add_user_produce(produce_id, user_id, new_quantity, condition)
            # print("user produce is :", user_produce)
            # <UserProduce id=67user=kyle produce=Asparagus>
            # print("user produce USER :", user_produce.user)
            # user produce USER : <User id=8 email=kyle_marks@hotmail.com username=kyle>
            # print("user produce USER :", user_produce.user_id)
            # user produce USER : 8
        flash('Produce has been added to your garden!')
        return redirect('/user')
    return render_template('user.html', user_produce=user_produce)


# DELETE USERPRODUCE
@app.route("/user/delete/<int:id>", methods=['GET', 'POST'])
def delete_user_produce(id):
    if request.method == 'POST':
        user_produce_id = UserProduce.query.get(id)
        db.session.delete(user_produce_id)
        db.session.commit()
        flash('Produce has been deleted!')

    return redirect('/user')


# -----------------  EXCHANGE PRODUCE ------------------------->

# ADD USER EXCHANGE PRODUCE
@app.route('/user/exchange/<int:id>', methods=['GET', 'POST'])
def add_exchange_produce(id):
    """Adds vegetable from user's produce to the exchange"""

    if request.method == 'POST':
        session['userproduce_id'] = (id)
        userproduce_id = session['userproduce_id']
        amount = 3
        comment = 'Msg me for phone number'
        exchange_items = crud.add_exchange_produce(userproduce_id, amount, comment)
        flash('Produce has been added to the exchange!')

        # user_produce_id = UserProduce.query.get(id)
        # # print('USERPRODUCE_ID IS: ', user_produce_id)
        # # <UserProduce id=78user=bella produce=Kale>
        # db.session.delete(user_produce_id)
        # db.session.commit()
        # flash('Produce has been removed from garden!')
        
        return redirect('/user')
    return render_template('exchange.html', exchange_items=exchange_items)


# DISPLAY EXCHANGE PAGE
@app.route('/exchange')
def exchange():
    """Show exchange page"""
    
    #username= session['current_user']
    #userId = session['current_user_id']
    #exchange_items = crud.get_user_produce_by_id(userId)
    exchange_items = ExchangeProduce.query.all()
    produce1 = exchange_items[0].userProduce
    # print(produce1)
    print('!!!!!!!!!!!!!!', exchange_items)
    for item in exchange_items:
        print(item.userProduce.produce.name + ' name\n')
    ## grab user produce id --- find the usernames associated with it -- return 

    return render_template('exchange.html', exchange_items=exchange_items)


# # DELETE USER EXCHANGE PRODUCE
# @app.route("/exchange/delete/<int:id>", methods=['GET', 'POST'])
# def delete_user_exchange_item(id):
#     if request.method == 'POST':
#         user_exchange_produce_id = ExchangeProduce.query.get(user_produce.id)
#         print('EXCHANGE ID IS!!!!!!!! : ', user_exchange_produce_id)
#         db.session.delete(user_exchange_produce_id)
#         db.session.commit()
#         flash('Produce has been deleted!')

#     return redirect('/exchange')
#---------------------------LOGIN/REGISTER HANDLERS------------------------------------------#


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
            gmaps = googlemaps.Client(key='AIzaSyDIYpD84hN93_pAL4oomppVemp3JYSvaRE')

            # Geocoding an address
            geocode_result = gmaps.geocode(full_address)
# print (geocode_result[0]["geometry"]["location"])
            lat = geocode_result[0]["geometry"]["location"]["lat"]
            lng = geocode_result[0]["geometry"]["location"]["lng"]

            
            user = crud.create_user(
                username, email, password1, address, city, zipcode, lat, lng)
            session['current_user'] = username
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
#---------------------------------NEW BELOW (MISC) ------------------------------------------#






















#-------------------------END--------------------------------#
if __name__ == "__main__":
    app.debug = True
    connect_to_db(app, "produce_swap")
    app.run(host='0.0.0.0')
