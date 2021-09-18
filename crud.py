"""CRUD operations"""
# IMPORT MODEL
import math
from models import (db, User, Produce, UserProduce,
                    ExchangeProduce, connect_to_db)

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

# GET USER VEGGIES
def get_user_veggies(username):
    """Takes in a username and returns user's user_produce"""
    user_produce = db.session.query(UserProduce).select_from(UserProduce).join(
        User).join(Produce).filter(User.username == username).all()

    return user_produce

# GET USER VEGGIES BY ID
def get_user_veggies_by_id(user_id, produce_id):
    """Takes in a username and returns user's user_produce"""
    user_produce = db.session.query(UserProduce).select_from(UserProduce).join(User).join(
        Produce).filter(User.id == user_id).filter(UserProduce.produce_id == produce_id).one()

    return user_produce

# CHECK IF USER PRODUCE EXISTS
def user_produce_exists(user_id, produce_id):
    """Returns true if you have an entry"""
    return db.session.query(UserProduce).select_from(UserProduce).join(User).join(Produce).filter(User.id == user_id).filter(UserProduce.produce_id == produce_id).first() is not None



def update_user_produce(id, amount, user_id):
    userProduce = db.session.query(UserProduce).filter(
        UserProduce.user_id == user_id).filter(UserProduce.produce_id == id).first()
    # userProduce.quantity -= amount
    amount = userProduce.quantity
    print('NEW QUANTITY IS:', amount)
    
    db.session.commit()
    return 


def update_user_produce_quantity(userproduce_id, new_produce_amount):
    """Takes user produce id and updates the quantity"""
    
    # Get the record
    userProduce = db.session.query(UserProduce).filter(
        UserProduce.id == userproduce_id).first()
    
    #set the amount
    userProduce.quantity = new_produce_amount
    
    # save the value
    db.session.commit()
    return 
    
# # GET USER'S PRODUCE
# def get_user_produce_by_id(userId):
#     """Returns True if email exists in User table"""

#     exchange_items = db.session.query(UserProduce).all()

#     return exchange_items

# UPDATE USER PRODUCE (QUANTITY)
def update_user_produce_amount(user_id, produce_id, new_quantity):
    """Takes ID of existing user_produce"""
    
    userProduce = db.session.query(UserProduce).filter(
        UserProduce.user_id == user_id).filter(UserProduce.produce_id == produce_id).first()
    userProduce.quantity += new_quantity

    new_quantity = userProduce.quantity
    print('NEW QUANTITY IS:', new_quantity)
    
    db.session.commit()
    return 


# ---------------------------------------------------------

# CHECK USER_EXCHANGE EXISTS
def user_exchange_exists(userproduce_id):
    """Returns true if user has a user_exchange entry"""

    # if user exchange produce exists
    # flash something
    
    return ExchangeProduce.query.filter_by(userproduce_id=userproduce_id).first() is not None


# CREATE EXCHANGE PRODUCE
def add_exchange_produce(userproduce_id, amount, comment, userconsumer_id=None, state=None, date=None):
    """Creates a new user exchange produce & adds to the db"""
    exchange_items = ExchangeProduce(
        userproduce_id=userproduce_id, userconsumer_id=userconsumer_id, amount=amount, comment=comment, date=date, state=state)

    
    db.session.add(exchange_items)
    
    db.session.commit()
    


    return exchange_items





def get_exchange_by_distance(center_lat, center_lng, radius_miles):
    """Returns exchanges within the specified radius"""
    R = 6371e3; # earth's mean radius in metres
    π = math.pi;
    
    # we are passing in 'miles', need to convert to meters
    METERS_IN_MILE = 1609.34
    radius = radius_miles * METERS_IN_MILE
    


    minLat =  center_lat - radius/R*180/π,
    maxLat = center_lat + radius/R*180/π,
    minLng=  center_lng - radius/R*180/π / math.cos(center_lat*π/180),
    maxLng= center_lng + radius/R*180/π / math.cos(center_lat*π/180),

    # Select Id, Postcode, Lat, Lon
    # From MyTable
    # Where Lat Between: minLat And: maxLat
    #  And Lon Between: minLon And: maxLon`;
    exchangesBoundedBox = ExchangeProduce.query.filter(User.lat.between(minLat, maxLat)).filter(User.lng.between(minLng, maxLng)).all()

    exchangesWithinCircle = []
    # add in distance d = acos( sinφ₁⋅sinφ₂ + cosφ₁⋅cosφ₂⋅cosΔλ ) ⋅ R
    for exchange in exchangesBoundedBox:
        distance = math.acos(math.sin(exchange.user.lat*π/180)*math.sin(center_lat*π/180) +
            math.cos(exchange.user.lat*π/180)*math.cos(center_lat*π/180)*math.cos(exchange.user.Lng*π/180-center_lng*π/180)) * R 
        
        if (distance < radius):
            exchangesWithinCircle.append(exchange)

    # sort the exchanges 
    # filter for points with distance from bounding circle centre less than radius, and sort
    # exchangesWithinCircle = pointsBoundingBox.filter(p => p.d < radius).sort((a, b) => a.d - b.d);
    
    return exchangesWithinCircle




#------------------------- NEW  ------------------------------------------#


def get_exchanges_by_zipcode(zipcode):
    """Return a list of exchanges by zipcode"""
    
    exchanges = db.session.query(ExchangeProduce).join(User).filter(User.zipcode==zipcode).all()
    print('exchanges EQUALS:', exchanges)
    
    return exchanges









#--------------------------MISC--------------------------------#





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
