
from wtforms import Form, IntegerField,validators,StringField,BooleanField


class MyForm(Form):
    cap = IntegerField('cap', [validators.NumberRange(min=0,max=50000)])
    cantiere = BooleanField('cantiere')
    umarell = BooleanField('umarell')
    both = BooleanField('both')
    
class CantiereForm(Form):
    id = IntegerField('id', [validators.NumberRange(min=0,max=50000)])
    cap = IntegerField('cap', [validators.NumberRange(min=0,max=50000)])
    indirizzo = StringField('indirizzo')
