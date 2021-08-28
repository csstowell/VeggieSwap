"""CRUD operations"""

# IMPORT MODEL
from model import (db, User, Produce, UserProduce, ExchangeProduce, connect_to_db)

# PRODUCE BY ID (/MARKET)
def get_produce_by_id(id):
    """Return a vegetable, given produce.id."""

    produce = Produce.query.filter_by(id=id).one()

    return produce

# GET USER'S PRODUCE
def get_user_produce(user_id):
    print("USER ID = ", user_id)
    user_produce = UserProduce.query.filter_by(user_id=user_id)

    return user_produce


# ADD USER PRODUCE (/add_user_produce)
def add_user_produce(produce_id, user_id, quantity, condition):
    """Create & return an instance of produce owned by user"""
    
    user_produce = UserProduce(
        user_id=user_id, produce_id=produce_id, quantity=quantity, condition=condition)

    db.session.add(user_produce)
    db.session.commit()

    return user_produce


# ---------------------------------------------------------



#------------------------- NEW WORKING CODE ------------------------------------------#
def get_user_produce_by_produce_id(produce_id):
    """Takes in string and finds match with Produce in db, if any"""

    existing_produce = db.session.query(
        UserProduce).filter_by(produce_id=produce_id).first()

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




