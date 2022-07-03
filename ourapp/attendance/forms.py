from random import choices
from flask import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError



#Form For the COurse Registration
class CourseRegisterForm(FlaskForm):
    rollno = StringField("Enter You Roll No.", validators=[DataRequired()])
    course = SelectField("Select the course" , choices=[('A','AI1001 - Artificial Intelligence'),('B','CS1001 - Intro to Computing'),('C','MA1001 - Intro to Statistics')], validators=[DataRequired()])
    picture = FileField('Upload Your Picture', validators=[DataRequired(),FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Register')


#Form For the class strength
class classstregth(FlaskForm):
    course = SelectField("Select the course" , choices=[('A','AI1001 - Artificial Intelligence'),('B','CS1001 - Intro to Computing'),('C','MA1001 - Intro to Statistics')], validators=[DataRequired()])
    picture = FileField('Upload the picture of class', validators=[DataRequired(),FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Get Strength')









