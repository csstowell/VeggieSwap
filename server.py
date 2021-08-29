from flask import (Flask, render_template, request, flash, session, redirect, jsonify, url_for)

from model import Produce, User, UserProduce, ExchangeProduce, db, connect_to_db
import crud

app = Flask(__name__)
app.secret_key = "SECRET"
# ---------------------------------------------------------

# INDEX
@app.route('/')
def index():
    """Login/register page"""
    return render_template('base.html')

# HOMEPAGE 
@app.route('/home', methods=['GET','POST'])
def home_page():
    """Show homepage"""
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
@app.route('/market')
def market_page():
    """View all produce listings from database"""

    items = Produce.query.all()

    return render_template('market.html', items=items)


# USER 
@app.route('/user', methods=['GET', 'POST'])
def user_page():
    """View all user produce"""

    user_id = session['current_user_id']
    user_produce = crud.get_user_produce(user_id)

    return render_template("user.html", user_produce=user_produce)


# SHOW PRODUCE BY ID
@app.route('/market/<produce_id>')
def show_produce(produce_id):
    '''Return produce details & provide button to add produce.'''
    produce = crud.get_produce_by_id(produce_id)

    return render_template("display_details.html", display_produce=produce)


# ADD TO USERPRODUCE
@app.route('/add_user_produce/<produce_id>')
def add_user_produce(produce_id):
    '''add user produce to user_page'''
    if request.method == 'POST':
    # save session quantity
        session['quantity'] = request.form['produce_quantity']
        quantity = session['quantity']
        session['condition'] = request.form['produce_condition']
        condition =  session['condition']
        crud.add_user_produce(produce_id, session['current_user_id'], quantity, condition)

    if 'user_produce' in session:
        user_produce = session['user_produce']
        flash("Produce successfully added to basket.")
    else:
        user_produce = session['user_produce'] = {}
    return redirect("/market/1")

# DELETE USERPRODUCE
@app.route("/user/delete/<int:id>", methods=['GET', 'POST'])
def delete_user_produce(id):
    if request.method == 'POST':
        user_produce_id = UserProduce.query.get(id)
        db.session.delete(user_produce_id)
        db.session.commit()
        flash('Produce has been deleted!')

    return redirect('/user')


#-----------------EXCHANGE--------->
# DISPLAY EXCHANGE PAGE
@app.route('/exchange')
def exchange():
    """Show exchange page"""

    exchange_items = ExchangeProduce.query.all()

    return render_template('exchange.html', exchange_items=exchange_items)


# ADD USER EXCHANGE PRODUCE
@app.route('/user/exchange/<int:id>', methods = ['GET', 'POST'])
def add_exchange_produce(id):
    """Adds vegetable from user's produce to the exchange"""
    
    if request.method == 'POST':
        session["userproduce_id"] = request.form["exchange_produce"]
        if "userproduce_id" in session:
            exchange_produce = session["userproduce_id"]

            amount = 2
            comment = 'Email me!'
            user_exchange = crud.add_exchange_produce(exchange_produce, amount, comment)
            flash('Produce has been added to the exchange!')
        return redirect('/user', user_exchange=exchange_items)



#---------------------------------NEW BELOW--------------------------------#








#-------------------------END--------------------------------#
if __name__ == "__main__":
    app.debug = True
    connect_to_db(app, "produce_swap")
    app.run(host='0.0.0.0')
