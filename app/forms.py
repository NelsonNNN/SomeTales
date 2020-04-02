from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), length(min =2, max =20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Sign in')
    remember = BooleanField('Remember me')