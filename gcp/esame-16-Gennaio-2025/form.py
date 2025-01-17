from wtforms import Form, validators, TextAreaField, IntegerField

class participantForm(Form):
    email = TextAreaField('Email', [validators.DataRequired(), validators.length(min=0, max=255)])
    nome = TextAreaField('Nome', [validators.DataRequired(), validators.length(min=0, max=255)])
    cognome = TextAreaField('Cognome', [validators.DataRequired(), validators.length(min=0, max=255)])

class toForm(Form):
    email2 = TextAreaField('Email', [validators.DataRequired(), validators.length(min=0, max=255)])
