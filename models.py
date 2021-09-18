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
    address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    phone = db.Column(db.String, unique=True)
    
    produce = db.relationship("Produce", secondary="user_produce")
    
    def __repr__(self):
        return f"<User id={self.id } email={self.email} username={self.username} lat={self.lat} lng={self.lng}>"


# PRODUCE
class Produce(db.Model):
    """A vegetable entity"""

    __tablename__ = "produce"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    handpick = db.Column(db.String)
    store = db.Column(db.String)
    variety = db.Column(db.String)
    nutrient = db.Column(db.String)
    img_url = db.Column(db.Text)

    def __repr__(self):
        """Show human-readable info about vegetable"""

        return f"<Produce id={self.id} name={self.name} variety={self.variety}>"



#------------------------ USER PRODUCE -------------------------------------------#

# USER PRODUCE
class UserProduce(db.Model):
    """A physical instance of a vegetable owned by user"""

    __tablename__ = "user_produce"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", primary_key=True), nullable=False)
    produce_id = db.Column(db.Integer, db.ForeignKey("produce.id", primary_key=True), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.Text, nullable=False)

    user = db.relationship('User')
    produce = db.relationship('Produce')
    
    userproduce_id = db.relationship('ExchangeProduce', backref="user_produce")

    def __repr__(self):
        """Show human-readable UserGame instance"""
        return f"<UserProduce id={self.id}"\
            f"user={self.user.username} produce={self.produce.name}>"


    def as_dict(self):
        """Return object as a dictionary"""

        return {
            'name': self.produce.name,
            'img_url': self.produce.img_url,
            'condition': self.condition,
            'quantity': self.quantity,
            'email': self.user.email,
            'username': self.user.username,
            'zipcode': self.user.zipcode
        }




# EXCHANGE PRODUCE
class ExchangeProduce(db.Model):
    """Subset of user_produce that user wants to exchange"""
    
    __tablename__ = "exchange_produce"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    userconsumer_id = db.Column(db.Integer, db.ForeignKey('users.id')) # BUYER ID 
    userproduce_id = db.Column(db.Integer, db.ForeignKey('user_produce.id')) # Seller's goods ID

    amount = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String)
    date = db.Column(db.Date, nullable=True)
    state = db.Column(db.String)

    #X = db.relationship('UserProduce', secondary='join(ExchangeProduce, UserProduce, ExchangeProduce.userproduce_id == UserProduce.id)', uselist=False, viewonly=True, backref='exchange_produce', sync_backref=False)
    userProduce = db.relationship('UserProduce',  backref="exchange_produce")
    produce = db.relationship('Produce', secondary='join(UserProduce, Produce, UserProduce.produce_id == Produce.id)', uselist=False, viewonly=True, backref='exchange_produce', sync_backref=False)

    def __repr__(self):
        """Show human-readable exchange_produce"""
        return f"<ExchangeProduce id={self.id} "\
            f"userproduce_id={self.userproduce_id} userProduce={self.userProduce} username={self.userProduce.user.username}  userconsumer_id={self.userconsumer_id}>"
            
    
    
    
    
    


#-------------------------END--------------------------------#
if __name__ == "__main__":
    """CONNECT"""
    connect_to_db(app, "produce_swap")
