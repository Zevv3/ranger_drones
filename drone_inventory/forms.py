from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

# This form can be repurposed for really any form you want to use to submit data

class UserLoginForm(FlaskForm):
    # email, password, submit_button
    # validators is always a list - checks data exists and it is a valid email
    email = StringField('Email', validators = [DataRequired(), Email()])
    first_name = StringField('First Name') #No validators because the user does not need to provide their name
    last_name = StringField('Last Name')
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()
    # These classes have html in them btw