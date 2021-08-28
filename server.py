from flask import (Flask, render_template, request, flash,
                   session, redirect, jsonify, url_for)

from model import Produce, User, UserProduce, ExchangeProduce, db, connect_to_db
import crud

app = Flask(__name__)
app.secret_key = "SECRET"


# HOMEPAGE ROUTE
@app.route('/')
@app.route('/home')
def home_page():
    """Show homepage"""

    return render_template('base.html')


# MARKET ROUTE
@app.route('/market')
def market_page():
    """View all produce listings from database"""

    items = Produce.query.all()

    return render_template('market.html', items=items)


# USER PROFILE
@app.route('/user', methods=['GET', 'POST'])
def user_page():
    """View all user produce"""

    user_id = session['current_user']
    user_produce = crud.get_user_produce(user_id)

    return render_template("user.html", user_produce=user_produce)


# PRODUCE BY ID
@app.route('/market/<produce_id>')
def show_produce(produce_id):
    '''Return produce details & provide button to add produce.'''
    produce = crud.get_produce_by_id(produce_id)

    return render_template("display_details.html", display_produce=produce)


# ADD TO USERPRODUCE
@app.route('/add_user_produce/<produce_id>')
def add_user_produce(produce_id):
    '''add user produce to user_page'''

    # temp
    quantity = 1
    condition = "Good"
    crud.add_user_produce(
        produce_id, session['current_user_id'], quantity, condition)

    if 'user_produce' in session:
        user_produce = session['user_produce']
        flash("Produce successfully added to basket.")
    else:
        user_produce = session['user_produce'] = {}
    return redirect("/user")


@app.route("/user/delete/<int:id>", methods=['GET', 'POST'])
def delete_user_produce(id):

    if request.method == 'POST':
        user_produce_id = UserProduce.query.get(id)
        db.session.delete(user_produce_id)
        db.session.commit()
        flash('Produce has been deleted!')

    return redirect('/user')


#-------------------------END--------------------------------#
if __name__ == "__main__":
    app.debug = True
    connect_to_db(app, "produce_swap")
    app.run(host='0.0.0.0')
