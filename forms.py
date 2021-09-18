from wtforms import Form, StringField, SelectField
from flask_appbuilder import IndexView

class ProduceSearchForm(Form):
    choices = [('produce', 'produce'), ('name', 'name'), ('variety', 'variety')]
    select = SelectField('Search for veggies:', choices=choices)
    search = StringField('')

    

