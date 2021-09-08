from wtforms import Form, StringField, SelectField

class ProduceSearchForm(Form):
    choices = [('Produce', 'Produce'),
               ('ExchangeProduce', 'ExchangeProduce')]
    select = SelectField('Search for veggies:', choices=choices)
    search = StringField('')



