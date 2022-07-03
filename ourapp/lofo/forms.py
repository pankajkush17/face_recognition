from flask import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from ourapp.models import User


#The Lost And Found Form
class LostFoundForm(FlaskForm):
    NameofPerson = StringField('Name of Person', validators=[Length(min=2,max=20)])
    ContactPerson = StringField('Contact Number to Contact',validators = [Length(min=2,max=20)])
    AddresstoVisit = StringField('Address to Visit', validators=[Length(min=2,max=100)])
    picture = FileField('Upload Picture', validators=[DataRequired(),FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Find')
