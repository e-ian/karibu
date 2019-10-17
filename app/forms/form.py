from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])
    remember = BooleanField('remember me')

class SignupForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])
    confirm = PasswordField('confirm password', validators=[InputRequired(), EqualTo('password', message='Passwords must match')])

class ArticleForm(FlaskForm):
    title = StringField('title', validators=[InputRequired(), Length(min=4)])
    content = TextAreaField('content', validators=[InputRequired(), Length(min=5)])

