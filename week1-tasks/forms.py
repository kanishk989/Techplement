from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
  firstname = StringField('First Name', validators=[DataRequired(), Length(max=20)])
  lastname = StringField('Last Name', validators=[DataRequired(), Length(max=20)])
  username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  contact = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=13), ])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign Up')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError(f"That username is already taken. Please choose a different one.")

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError(f"That email is already in use. Please choose a different one.")
  
  def validate_contact(self, contact):
    user = User.query.filter_by(contact=contact.data).first()
    if user:
      raise ValidationError(f"That Phone number is already in use. Please choose a different one.")

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Login')