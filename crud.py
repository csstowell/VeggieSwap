"""CRUD operations"""
# IMPORT MODEL
from model import (db, User, Produce, UserProduce, ExchangeProduce, connect_to_db)

# CREATE USER
def create_user(username, email, password, address, city, zipcode, lat, lng, phone=None):
    """Create and return a new user"""

    user = User(username=username, email=email,
                password=password,
                address=address, city=city, zipcode=zipcode, 
                lat=lat, lng=lng,
                phone=phone)

    db.session.add(user)
    db.session.commit()

    return user

# CHECK USERNAME EXISTS
def lookup_user(username):
    """Returns True if username exists in User table"""

    user = User.query.filter_by(username=username).first()

    return user

# GET MATCHING PASSWORD
def get_password(username):
    """Takes in username and returns matching user's password"""

    password = db.session.query(User.password).filter_by(
        username=username).one()

    return password[0]

# CHECK EMAIL
def lookup_email(email):
    """Returns True if email exists in User table"""

    email = User.query.filter_by(email=email).first()

    return email

# GET USERNAME BY EMAIL
def get_email_by_username(username):
    """Takes in username and returns email of matching user"""

    user = User.query.filter_by(username=username).first()

    return user.email

# GET USER VEGGIES
def get_user_veggies(username):
    """Takes in a username and returns user's user_produce"""
    user_produce = db.session.query(UserProduce).select_from(UserProduce).join(User).join(Produce).filter(User.username==username).all()

    return user_produce

def get_user_veggies_by_id(user_id, produce_id):
    """Takes in a username and returns user's user_produce"""
    user_produce = db.session.query(UserProduce).select_from(UserProduce).join(User).join(Produce).filter(User.id==user_id).filter(UserProduce.produce_id==produce_id).one()

    return user_produce

def user_produce_exists(user_id, produce_id):
    """Returns true if you have an entery"""
    return db.session.query(UserProduce).select_from(UserProduce).join(User).join(Produce).filter(User.id==user_id).filter(UserProduce.produce_id==produce_id).first() is not None 



def user_produce_update(produce_id, quantity):
    """Takes ID of existing user_produce"""

    db.session.query(UserProduce).filter(UserProduce.produce_id==produce_id).update({'quantity': quantity)
    db.session.commit()

    return 








# MARKET PRODUCE BY ID
def get_produce_by_id(id):
    """Return a vegetable, given produce.id."""

    produce = Produce.query.filter_by(id=id).one()

    return produce


# ADD USER PRODUCE (/add_user_produce)
def add_user_produce(produce_id, user_id, quantity, condition):
    """Create & return an instance of produce owned by user"""
    
    user_produce = UserProduce(
        user_id=user_id, produce_id=produce_id, quantity=quantity, condition=condition)
    
    db.session.add(user_produce)
    db.session.commit()

    return user_produce
# update produce quantity - if existing

# ---------------------------------------------------------

# CREATE EXCHANGE PRODUCE
def add_exchange_produce(userproduce_id, amount, comment, userconsumer_id=None, state=None, date=None):
    exchange_items = ExchangeProduce(
        userproduce_id=userproduce_id, userconsumer_id=userconsumer_id, amount=amount, comment=comment, date=date, state=state)
    
    db.session.add(exchange_items)
    db.session.commit()

    return exchange_items




#------------------------- NEW WORKING CODE ------------------------------------------#




def get_user_produce_by_produce_id(userproduce_id):
    """Takes in string and finds match with Produce in db, if any"""

    existing_produce = db.session.query(
        UserProduce).filter_by(userproduce_id=userproduce_id).first()

    if existing_produce:
        return flash("existing")
    else:
        return None


def get_produce_by_name(name):
    """Takes in string and finds match with Produce in db, if any"""

    existing_produce = db.session.query(
        UserProduce).filter_by(user_id=user_id).first()

    if existing_produce:
        return flash("Already")
    else:
        return None




