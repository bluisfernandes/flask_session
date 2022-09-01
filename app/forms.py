from app import api_uri
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import requests

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=20)])
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    conf_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = requests.get(f'{api_uri}/users', params={"username":username.data}).json()['users']
        if user:
            raise ValidationError('username already in use')

    def validate_email(self, email):
        user = requests.get(f'{api_uri}/users', params={"email":email.data}).json()['users']
        if user:
            raise ValidationError('email already in use')

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember Me')
    submit = SubmitField('Login')


class PasswordForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    conf_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change')

    def validate_email(self, email):
        user = requests.get(f'{api_uri}/users', params={"email":email.data}).json()['users']
        if not user:
            raise ValidationError('email not found')
