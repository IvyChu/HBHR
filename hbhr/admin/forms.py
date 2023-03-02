from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField, IntegerField, widgets
from wtforms.validators import InputRequired, Length

class ServiceForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired(), 
                                                           Length(max=255, message="Description is limited to 255 characters.")])
    submit = SubmitField('Add')
