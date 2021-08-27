"""Models for ProduceSwap app"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.secret_key = "SECRET!"


def connect_to_db(app, produce_swap):
    """Connect to database."""

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{produce_swap}"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)


#-------------------- MODEL DEFINITIONS ---------------------------------------------#
# USER
class User(db.Model):
    """A user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String, unique=True)

   
    def __repr__(self):
        return f"<User user_id={self.user_id } email={self.email}>"

# VEGETABLE


class Produce(db.Model):
    """A vegetable entity"""

    __tablename__ = "produce"

    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    handpick = db.Column(db.String)
    store = db.Column(db.String)
    variety = db.Column(db.String)
    nutrient = db.Column(db.String)
    img_url = db.Column(db.Text)

    def __repr__(self):
        """Show human-readable info about vegetable"""

        return f"<Produce id={self.id} name={self.name}>"

    def as_dict(self):
        """Return object as a dictionary"""
        return {
            'img': self.produce.name,
            'produce_name': self.handpick,
            'condition': self.store,
            'quantity': self.variety,
            'email': self.nutrient,
        }


#------------------------ USER PRODUCE -------------------------------------------#

# USER PRODUCE
class UserProduce(db.Model):
    """A physical instance of a vegetable owned by user"""

    __tablename__ = "user_produce"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    produce_id = db.Column(db.Integer, db.ForeignKey(
        "produce.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.Text, nullable=False)

    user = db.relationship('User', backref="user_produce")
    produce = db.relationship('Produce', backref="user_produce")

    # Because of the one-one relationship between UserProduce and ExchangeProduce,
    # set uselist to False
    exchange = db.relationship('ExchangeProduce', backref="exchange_produce")

    def __repr__(self):
        """Show human-readable UserGame instance"""

        return f"<UserProduce id={self.id}"\
               f"user={self.user.username} produce={self.produce.name}>"


# EXCHANGE
class ExchangeProduce(db.Model):
    """Subset of user_vegetables that user wants to list"""

    __tablename__ = "exchange_produce"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('user_produce.id'))
    consumer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String)
    date = db.Column(db.Date, nullable=True)
    state = db.Column(db.String)

    supplier = db.relationship('UserProduce', backref="exchange_produce")

    produce = db.relationship('Produce', secondary='join(UserProduce, Produce, UserProduce.produce_id == Produce.id)',
                              uselist=False, viewonly=True, backref='exchange_produce', sync_backref=False)
    user = db.relationship('User', secondary='join(UserProduce, User, UserProduce.user_id == User.id)',
                           uselist=False, viewonly=True, backref='exchange_produce', sync_backref=False)

    def __repr__(self):
        """Show human-readable exchange_produce"""
        return f"<ExchangeProduce id={self.exchange_id} "\
               f"supplier={self.seller_produce.produce.name} buyer={self.buyer.users.username}>"

    def as_dict(self):
        """Return object as a dictionary"""
        return {
            'img': self.produce.img,
            'produce_name': self.produce.name,
            'condition': self.condition,
            'quantity': self.quantity,
            'email': self.user.email,
            'comment': self.comment,
            'zipcode': self.user.zipcode,
            'description': self.produce.description,
            'nutrient': self.produce.nutrient,
            'recipe': self.produce.recipe,
            'select': self.produce.select
        }


#-------------------------END--------------------------------#
if __name__ == "__main__":
    """CONNECT"""
    connect_to_db(app, "produce_swap")
