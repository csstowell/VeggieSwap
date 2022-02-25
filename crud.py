"""CRUD operations"""
# IMPORT MODEL
import math
from sqlalchemy import func
from models import (db, User, Produce, UserProduce,
                    ExchangeProduce, connect_to_db)
#==============
# Create a user
#==============
def create_user(username, email, password, address, city, state, zipcode, lat, lng, phone=None):
    """Create and return a new user"""

    user = User(username=username, email=email,
                password=password,
                address=address, city=city, state=state, zipcode=zipcode,
                lat=lat, lng=lng,
                phone=phone)

    db.session.add(user)
    db.session.commit()

    return user

#=============================
# Look the user up by their id
#=============================
def lookup_user_by_id(id):
    """Returns the user matching the userId"""

    user = User.query.filter_by(id=id).first()

    return user

#=============================
# Look up the user by username
#=============================
def lookup_user(username):
    """Returns True if username exists in User table"""

    user = User.query.filter_by(username=username).first()

    return user

#================================
# Get the password for a username
#================================
def get_password(username):
    """Takes in username and returns matching user's password"""

    password = db.session.query(User.password).filter_by(
        username=username).one()

    return password[0]

#===========================================
# Returns True if email exists in User table
#===========================================
def lookup_email(email):
    """Returns True if email exists in User table"""

    email = User.query.filter_by(email=email).first()

    return email

#=====================================================
# Lookup the email address of a user by their username
#=====================================================
def get_email_by_username(username):
    """Takes in username and returns email of matching user"""

    user = User.query.filter_by(username=username).first()

    return user.email

#=========================
# Return produce by its ID
#=========================
def get_produce_by_id(id):
    """Return a vegetable, given produce.id."""
    produce = Produce.query.filter_by(id=id).one()

    return produce

#=====================================================
# Create & return an instance of produce owned by user
#=====================================================
def add_user_produce(produce_id, user_id, quantity, condition):
    """Create & return an instance of produce owned by user"""
    user_produce = UserProduce(
        user_id=user_id, produce_id=produce_id, quantity=quantity, condition=condition)

    db.session.add(user_produce)
    db.session.commit()
    return user_produce

#================================================
# Get the produce for a user using their username
#================================================
def get_user_veggies(username):
    """Takes in a username and returns user's user_produce"""
    user_produce = db.session.query(UserProduce).select_from(UserProduce).join(
        User).join(Produce).filter(func.lower(User.username) == func.lower(username)).all()

    return user_produce


#==================================================================
# Get the produce for a user using both their id and the produce id
#==================================================================
def get_user_veggies_by_id(user_id, produce_id):
    """Takes in a username and returns user's user_produce"""
    user_produce = db.session.query(UserProduce).select_from(UserProduce).join(User).join(
        Produce).filter(User.id == user_id).filter(UserProduce.produce_id == produce_id).one()

    return user_produce

#==============================
# Check if the user has produce
#==============================
def user_produce_exists(user_id, produce_id):
    """Returns true if you have an entry"""
    return db.session.query(UserProduce).select_from(UserProduce).join(User).join(Produce).filter(User.id == user_id).filter(UserProduce.produce_id == produce_id).first() is not None

#=======================================
# update the produce quantity for a user
#=======================================
def update_user_produce(id, amount, user_id):
    userProduce = db.session.query(UserProduce).filter(
        UserProduce.user_id == user_id).filter(UserProduce.produce_id == id).first()
    # userProduce.quantity -= amount
    amount = userProduce.quantity
    print('NEW QUANTITY IS:', amount)
    
    db.session.commit()
    return 

#====================================
# Update the produce qantity for user
#====================================
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

#===============================
# Update user produce (quantity)
#===============================
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

#======================================
# Check if user exchange exists already
#======================================
def user_exchange_exists(userproduce_id):
    """Returns true if user has a user_exchange entry"""

    # if user exchange produce exists
    # flash something
    
    return ExchangeProduce.query.filter_by(userproduce_id=userproduce_id).first() is not None


#========================
# Create exchange produce
#========================
def add_exchange_produce(userproduce_id, amount, comment, userconsumer_id=None, state=None, date=None):
    """Creates a new user exchange produce & adds to the db"""
    exchange_items = ExchangeProduce(
        userproduce_id=userproduce_id, userconsumer_id=userconsumer_id, amount=amount, comment=comment, date=date, state=state)

    
    db.session.add(exchange_items)
    
    db.session.commit()
    


    return exchange_items




#=================================
# Get exchange produce by distance
#=================================
def get_exchange_by_distance(center_lat, center_lng, radius):
    """Returns exchanges within the specified radius (in meters) """
    R = 6371e3; # earth's mean radius in metres
    π = math.pi;
    
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
        distance = math.acos(math.sin(exchange.userProduce.user.lat*π/180)*math.sin(center_lat*π/180) +
            math.cos(exchange.userProduce.user.lat*π/180)*math.cos(center_lat*π/180)*math.cos(exchange.userProduce.user.lng*π/180-center_lng*π/180)) * R 
        
        if (distance < radius):
            exchangesWithinCircle.append(exchange)


    # sort the exchanges 
    # filter for points with distance from bounding circle centre less than radius, and sort
    # exchangesWithinCircle = pointsBoundingBox.filter(p => p.d < radius).sort((a, b) => a.d - b.d);
    
    return exchangesWithinCircle




#------------------------- NEW  ------------------------------------------#

#================================
# Get exchange produce by zipcode
#================================
def get_exchanges_by_zipcode(zipcode):
    """Return a list of exchanges by zipcode"""
    
    exchanges = db.session.query(ExchangeProduce).join(User).filter(User.zipcode==zipcode).all()
    print('exchanges EQUALS:', exchanges)
    
    return exchanges









#--------------------------MISC--------------------------------#




#=================================
# Get user's produce by produce id
#=================================

def get_user_produce_by_produce_id(userproduce_id):
    """Takes in string and finds match with Produce in db, if any"""

    existing_produce = db.session.query(
        UserProduce).filter_by(userproduce_id=userproduce_id).first()

    if existing_produce:
        return flash("existing")
    else:
        return None

#===============================
# Get user's produce by username
#===============================
def get_produce_by_name(name):
    """Takes in string and finds match with Produce in db, if any"""

    existing_produce = db.session.query(
        UserProduce).filter_by(user_id=user_id).first()

    if existing_produce:
        return flash("Already")
    else:
        return None



##################################################

