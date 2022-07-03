from flask import render_template, url_for, flash, redirect, request, Blueprint,current_app
from flask_login import login_user, current_user, logout_user, login_required
from ourapp.models import CourseRegistration , Attendance ,ClassAttendance
from ourapp import app,db
from ourapp.attendance.forms import CourseRegisterForm,classstregth
from PIL import Image
from deepface import DeepFace
from ourapp.attendance.utils import savepicture,saveattend
import pandas as pd
import os
from os import remove
import base64 
from io import BytesIO
from PIL import Image
import json
from datetime import datetime
from retinaface import RetinaFace 

attendance = Blueprint('attendance',__name__)

#The courses Dictionary
courses = {
    "A": "AI1001",
    "B" : "CS1011",
    "C" : "MA1001"
}

#Route for the Class Attendance info    
@attendance.route('/classattendance',methods=['GET','POST'])
def classattendance():
    return render_template("classroominfo.html") 


#Route for the course registration
@attendance.route('/courseregister',methods=['GET','POST'])
@login_required
def register():
    #course registration form
    form = CourseRegisterForm()
    if request.method=="POST":
        if form.validate_on_submit:

            #if the person is already registred for the course
            if(CourseRegistration.query.filter_by(RollNo = form.rollno.data,CourseCode = courses[form.course.data]).count() < 1):

                if form.picture.data :
                    #saving the picture
                    picture_file = savepicture(form.picture.data,form.course.data)

                #We will remove the present pickle file as we have added new image to the folder
                pickle_path = os.path.join(current_app.root_path, 'static/classattendance/courses/AI1001', 'representations_vgg_face.pkl')
                try:
                    remove(pickle_path)
                except:
                    pass

                #Adding the Student to the database
                student = CourseRegistration(RollNo = form.rollno.data , CourseCode = courses[form.course.data] , image_file = picture_file)
                db.session.add(student)
                db.session.commit() 
                flash("Succesfully registered for the course","success")
                return redirect(url_for('attendance.register'))
   
            else : 
                flash("You are already Registered for this course", "warning")

                   
    return render_template("classregister.html",form=form)


@attendance.route('/takeattend/A',methods=['GET','POST'])
@login_required
def takeattend():
        #If the Request is a Post Request
    if(request.method=='POST'):
        # Storing the picture of the user in a jpg format with image files name as 'username.jpg'
        picture_n ='imgattend.jpg'
        # Get only revelant data, deleting "data:image/png;base64,"
        data = request.data.decode().split(',')[1]
        #Encoding the data
        data = data.encode()
        #Writing the data to an image file
        im = Image.open(BytesIO(base64.b64decode(data)))
        #If we get image in a RGBPA or P mode then converting it to RGB mode
        if im.mode in ("RGBA", "P"): 
            im = im.convert("RGB")
        #the picture that user takes while logging in
        picture_path = os.path.join(current_app.root_path,'static',picture_n)
        #we will save the picture 
        im.save(picture_path)
        #database of the users path
        code = "A"
        if code == "A":
            db_path = os.path.join(current_app.root_path,'static/classattendance/courses/AI1001')
        elif code == "B":
            db_path = os.path.join(current_app.root_path,'static/classattendance/courses/CS1011')
        else :
            db_path = os.path.join(current_app.root_path,'static/classattendance/courses/MA1001')
        
        
        # Using the deepface library to verify the image with the already stored user image with the username
        print(picture_path)

        df = pd.DataFrame()
        try:
            df = DeepFace.find(img_path=picture_path ,db_path = db_path,enforce_detection=True)
        except:
            pass


        if (df.shape[0] == 0):
            return "error"
        else: 
            hell = df['identity'].astype('string')
            image = hell[0].split('/')[-1]
            # getting the image file
            date = datetime.now()
            date = date.strftime("%d/%m/%y")

            #Adding the attendance to the database

            atendee = CourseRegistration.query.filter_by(image_file = image).first()
            hasattend = Attendance(RollNo = atendee.RollNo , CourseCode = atendee.CourseCode , Attended = True , Date =  date)
            db.session.add(hasattend)
            db.session.commit()
            return atendee.RollNo
            #return match with your rollno so that it will know  
    return render_template("classattendance.html")

#class analytice route     
@attendance.route('/classanalytics',methods=['GET','POST'])
@login_required
def classanalytic():
    #classStregth Form
    form  = classstregth()
    if request.method == "POST":
        if(form.validate_on_submit):
            if form.picture.data :
                #save picture
                    picture_file = saveattend(form.picture.data,form.course.data)
            
            date = datetime.now()
            date = date.strftime("%d/%m/%y")
            course = courses[form.course.data]
            #Using the retine face to detect the no.of students in the class
            resp = RetinaFace.detect_faces(picture_file)
            count = len(resp)
            #Adding them to the database
            attend = ClassAttendance(Date = date,CourseCode = course,Strength = count)
            db.session.add(attend)
            db.session.commit()
            flash(f"The Strength of the class is {count}","success")
            return render_template("classanalytics.html",form=form,count = count)
    return render_template("classanalytics.html",form=form)


#Route for checking the attendance of the people
@attendance.route('/checkattendance',methods=['GET','POST'])
@login_required
def checkattend():
    attendance = Attendance.query.all()
    classattendance = ClassAttendance.query.all()
   
    return render_template("checkattend.html",attendance = attendance,classattendance = classattendance)





