import os
import secrets
from PIL import Image
from flask import current_app
from datetime import datetime

#Function For Saving the pictures
def savepicture(form_picture,code):
    #keeping Image file name as a random hex
    random_hex = secrets.token_hex(10)
    _, f_ext = os.path.splitext(form_picture.filename)
    #making the extension as jpg
    picture_fn = random_hex + '.jpg'
    if code == "A":
        picture_path = os.path.join(current_app.root_path, 'static/classattendance/courses/AI1001', picture_fn)
    elif (code == "B"):
        picture_path = os.path.join(current_app.root_path, 'static/classattendance/courses/CS1011', picture_fn)
    else :
        picture_path = os.path.join(current_app.root_path, 'static/classattendance/courses/MA1001', picture_fn)

#saving the picture
    i = Image.open(form_picture)
    i.save(picture_path)
    return picture_fn


#saving the attendance
def saveattend(form_picture,code):
    _, f_ext = os.path.splitext(form_picture.filename)

    date = datetime.now()
    date = date.strftime("%d-%m-%y")

    picture_fn = date + '.jpg'
    if code == "A":
        picture_path = os.path.join(current_app.root_path, 'static/classattendance/Attended/AI1001', picture_fn)
    elif (code == "B"):
        picture_path = os.path.join(current_app.root_path, 'static/classattendance/Attended/CS1011', picture_fn)
    else :
        picture_path = os.path.join(current_app.root_path, 'static/classattendance/Attended/MA1001', picture_fn)
    
    i = Image.open(form_picture)
    i.save(picture_path)
    return picture_path

