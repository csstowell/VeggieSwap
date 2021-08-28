"""CRUD operations"""

# IMPORT MODEL
from model import (db, User, Produce, UserProduce, ExchangeProduce, connect_to_db)

# PRODUCE BY ID (/MARKET)
def get_produce_by_id(id):
    """Return a vegetable, given produce.id."""

    produce = Produce.query.filter_by(id=id).one()

    return produce

# GET USER PRODUCE BY ID (/USER)
def get_user_produce(user_produce):
    """Get user_produce by username"""

    user_produce = UserProduce.query.filter()
    return user_produce

# ADD USER PRODUCE (/add_user_produce)
def add_user_produce(produce_id, user_id, quantity, condition):
    """Create & return an instance of produce owned by user"""

    user_produce = UserProduce(
        user_id=user_id, produce_id=produce_id, quantity=quantity, condition=condition)

    db.session.add(user_produce)
    db.session.commit()

    return user_produce

def get_user_produce(user_id):
    print("USER ID = ", user_id)
    user_produce = UserProduce.query.filter_by(user_id=user_id)

    return user_produce
# ---------------------------------------------------------



def get_user_produce_by_id(id):
    user_produce_id = db.session.query(UserProduce).filter_by(id=id).first()

    return user_produce_id

# ADD USER PRODUCE






#------------------------- WORKING CODE ------------------------------------------#
def get_produce_by_name(name):
    """Takes in string and finds match with Produce in db, if any"""

    existing_produce = db.session.query(
        UserProduce).filter_by(user_id=user_id).first()

    if existing_produce:
        return flash("Already")
    else:
        return None


def get_user_produce_by_produce(produce_id):
    user_produce = UserProduce.query.filter()

    return user_produce
# SHOW USERPRODUCE FOR USER IN SESSION
# def show_user_produce(user_id):
#     user_produce = UserProduce.query.filter_by(user_id=produce_id)

# DELETE PRODUCE


def del_user_produce(produce_id):
    user_produce = UserProduce.query.filter_by(
        produce_id == produce_id).first()

    db.session.delete(user_produce)
    db.session.commit()

    return user_produce


def get_name_by_id(id):
    """Takes in id and returns name of matching produce"""

    user_produce = UserProduce.query.filter_by(id=id).first()

    return user_produce.name


