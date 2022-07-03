# importing all the required things

from email.mime import base
from flask import render_template, url_for, flash, redirect, request, Blueprint,current_app
from flask_login import login_user, current_user, logout_user, login_required
import base64 
from flask_session import Session
from ourapp.models import User
from ourapp import app,db
from itsdangerous import base64_decode

#Blueprint
users = Blueprint('users',__name__)


from io import BytesIO
import os
from PIL import Image
from deepface import DeepFace
from os import remove
import secrets

#Home Route
@users.route('/',methods=['GET','POST'])
def home():
    return render_template("home.html")


#Logout Route
@users.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("You are logged out successfully.","primary")
    return redirect(url_for("users.login"))



# Login Route 
@users.route('/login',methods=['GET','POST'])
def login():
    #If the Request is a Post Request
    if current_user.is_authenticated:
        flash("You are already logged in ","info")
        return redirect(url_for("users.home"))
    if(request.method=='POST'):
        #Getting the Username
        username = request.form['username']
        #If the username doesnt Exist in the database it will raise an error
        if(username):
            print(1)
        else:
        #remove the picuture so as to save the space in the server
            return "user"

        try:
        #trying searching the user in the database if the user is not found then it will raise an error
            user = User.query.filter_by(username = username).first()
        except:
            return "user"
        #Storing them using a random filename because not to clash
        random_hex = secrets.token_hex(10)
        # Storing the picture of the user in a jpg format with image files name as 'username.jpg'
        picture_n = random_hex +'.jpg'
        # Get only revelant data, deleting "data:image/png;base64,"
        data = request.form['userpic'].split(',')[1]
        #Encoding the data
        data = data.encode()
        #Writing the data to an image file
        im = Image.open(BytesIO(base64.b64decode(data)))
        #If we get image in a RGBPA or P mode then converting it to RGB mode
        if im.mode in ("RGBA", "P"): 
            im = im.convert("RGB")
        
        #database of the users path
        db_path = os.path.join(current_app.root_path,'static/users')
        #the picture that user takes while logging in
        picture_path = os.path.join(current_app.root_path,'static',picture_n)
        #we will save the picture 
        im.save(picture_path)
        
        
        
        # Using the deepface library to verify the image with the already stored user image with the username if the user is notfound then it will raise an error
        try : 
            df = DeepFace.verify(img1_path=picture_path ,img2_path=os.path.join(db_path,user.image_file),enforce_detection=True)
        except :
            remove(picture_path)
            return "nomatch"

        #if it returns True then user gets logged in 
        if (df['verified']):
            login_user(user)
            #And then We Remove the user picture that he used to login
            remove(picture_path)
            #it sends the message to the javascript then it handlees the route
            flash(f"You are loggedin successfully.","success")
            return "match"
        else:
            #And then We Remove the user picture that he used to login so as to save space
            remove(picture_path)
            return "nomatch"
        
    return render_template('login.html',title='Login')


@users.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in. Logout to register for a new account!","info")
        return redirect(url_for("users.home"))
    #If the Request is a Post Request
    if(request.method=='POST'):
        try:
           #Getting the Username
            username = request.form['username']
            #If an  username is not chosen then it raises an error 
        except:
            return "error"

        if(not username):
            return "error"

        #it only goes into this conditional only if the username is unique otherwise it doesnt go into this
        if db.session.query(User).filter_by(username= username).count()<1:
            # Storing the picture of the user in a jpg format with image files name as 'username.jpg'
            picture_n = username + '.jpg'
            picture_path = os.path.join(current_app.root_path,'static/users',picture_n)
            # Get only revelant data, deleting "data:image/png;base64,"
            data = request.form['userpic'].split(',')[1]
            #encoding the data
            data = data.encode()
            #Writing the data to an image file
            im = Image.open(BytesIO(base64.b64decode(data)))
            #If we get image in a RGBPA or P mode then converting it to RGB mode
            if im.mode in ("RGBA", "P"): 
                im = im.convert("RGB")
            #saving the picture in our database
            im.save(picture_path)
            try:
                DeepFace.analyze(picture_path)
            except:
                remove(picture_path)
                return "error"
            #Adding the User to the database
            user = User(username = username, image_file = picture_n)
            db.session.add(user)
            db.session.commit()
            #And returining to the login screen
            flash("You are registered successfully. Now u can login with Your Credentials","success")
            return "/login"
        else: 
            #if the username is not unique then it will also raise an error
            return "username"

   
    #If the request is get request
    return render_template('register.html',title='Register')




