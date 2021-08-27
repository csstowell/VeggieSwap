"""CRUD operations"""

# IMPORT MODEL
from model import (db, User, Produce, UserProduce,
                   ExchangeProduce, connect_to_db)

# PRODUCE BY ID
def get_produce_by_id(id):
    """Return a vegetable, given produce.id."""
    
    produce= Produce.query.filter_by(id=id).one()

    return produce


# ADD USER PRODUCE
def add_user_produce(produce_id, user_id, quantity, condition):
    """Create & return an instance of produce owned by user"""

    user_produce = UserProduce(
        user_id=user_id, produce_id=produce_id, quantity=quantity, condition=condition)

    db.session.add(user_produce)
    db.session.commit()

    return user_produce


# GET USER PRODUCE BY ID
def get_user_produce(user_id):
    """Get user_produce by username"""

    user_produce = UserProduce.query.filter_by()

    return user_produce
#------------------------- WORKING CODE ------------------------------------------#

# SHOW USERPRODUCE FOR USER IN SESSION
# def show_user_produce(user_id):
#     user_produce = UserProduce.query.filter_by(user_id=produce_id)


# def del_user_produce():
