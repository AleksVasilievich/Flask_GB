# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, IntegerField, SelectField
# from wtforms.validators import DataRequired, EqualTo, Email, Length
#
#
# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#
#
# class RegisterForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired()])
#     age = IntegerField('Age', validators=[DataRequired()])
#     gender = SelectField('Gender', choices=[('male', 'Мужчина'), ('female', 'Женщина')])
#
# class RegistrationForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, Length

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = StringField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])