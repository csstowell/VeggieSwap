from flask import Flask
from flask_appbuilder import SQLA, AppBuilder



app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)


