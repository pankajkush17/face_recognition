#importing the required libraraies
from flask import render_template, url_for, flash, redirect, request, Blueprint,current_app
from flask_login import login_user, current_user, logout_user, login_required
from ourapp.models import LostAndFound
from ourapp import app,db
from ourapp.lofo.forms import LostFoundForm
from PIL import Image
from deepface import DeepFace
from ourapp.lofo.utils import savepicture
import pandas as pd
import os
import json
from os import execlpe, remove
from PIL import Image

lofo = Blueprint('lofo',__name__)

#info Route
@lofo.route("/lostfound",methods=['GET','POST'])
def lostfound():
    return render_template("lostfoundexplanation.html",title="Lost And Found")

#lost portal api
@lofo.route("/lost",methods=['GET','POST'])
@login_required
def lost():
    #form for the lost and found
    form = LostFoundForm()

    #if request is a post request
    if request.method=='POST':
        #checking if form is valid on submit
        if form.validate_on_submit():
            if form.picture.data :
                #saving the picture
                picture_file,valid = savepicture(form.picture.data,"lost")
            if valid:
                #getting the saved location of the picture
                imagepath = os.path.join(current_app.root_path, 'static/missingpeople/lost', picture_file)
                #getting the db path where we have to search for the image (Found people database)
                db_path = os.path.join(current_app.root_path, 'static/missingpeople/found')
                #initialsing an empty data frame
                df = pd.DataFrame()
                try:
                    df = DeepFace.find(img_path = imagepath,db_path=db_path, enforce_detection=True)
                except:
                    pass
                #if we found any image then
                if(df.shape[0]!=0):
                    #getting the image name from the databse
                    hell = df['identity'].astype('string')
                    image = hell[0].split('/')[-1]
                    #if getting the details of the found image 
                    yayfound = LostAndFound.query.filter_by(image_file=image).first()
                    #getting the image file path
                    image_file = os.path.join('/static/missingpeople/found',image)
                    flash("Congo We Found a match","success")
                    #removing the image to save the storage
                    remove(imagepath)
                    return render_template("Lost.html",title="LostFound",form=form,yayfound = yayfound,image_file = image_file)
                else:

                    #we will remove the pickle file present as we have added a new image to the folder.Deep face will generate it again
                
                    pickle_path = os.path.join(current_app.root_path, 'static/missingpeople/lost', 'representations_vgg_face.pkl')
                    try:
                        remove(pickle_path)
                    except:
                        pass

                    #We will add the person to our lost people databse so if anybody finds them they can reach them

                    lost = LostAndFound(NameofPerson = form.NameofPerson.data,ContactPerson = form.ContactPerson.data, AdresstoVisit = form.AddresstoVisit.data, image_file= picture_file)
                    db.session.add(lost)
                    db.session.commit()

                    
                    flash("Sorry but keep hope we have added the details to our database, so that people might find him/her :)","warning")
            else:
                flash("Upload image with a human face","danger")
    return render_template("Lost.html",title="Lost",form=form)

# the Found api

#explanation similar to above
@lofo.route("/found",methods=['GET','POST'])
@login_required
def found():
    form = LostFoundForm()
    if request.method=='POST':

        if form.validate_on_submit():
            if form.picture.data: 
                picture_file,valid = savepicture(form.picture.data,"found")
                
            if valid:
                imagepath = os.path.join(current_app.root_path,'static/missingpeople/found', picture_file)

                db_path = os.path.join(current_app.root_path, 'static/missingpeople/lost')
                df = pd.DataFrame()
                
                try:
                    df = DeepFace.find(img_path = imagepath,db_path=db_path, enforce_detection=True)
                except:
                    pass


                if(df.shape[0]!=0):
                    hell = df['identity'].astype('string')
                    image = hell[0].split('/')[-1]
                    yayfound = LostAndFound.query.filter_by(image_file=image).first()
                    image_file = os.path.join('/static/missingpeople/lost',image)
                    flash("We found someone looking for him","success")
                    remove(imagepath)
                    return render_template("Found.html",title="LostFound",form=form,yayfound = yayfound,image_file = image_file)
                else:
                    #we will remove the pickle file present as we have added a new image to the folder.Deep face will generate it again
                    pickle_path = os.path.join(current_app.root_path, 'static/missingpeople/found', 'representations_vgg_face.pkl')
                    try:
                        remove(pickle_path)
                    except:
                        pass 

                    #We will add the person to our found people databse so if anybody is looking for them they can reach them

                    found = LostAndFound(NameofPerson = form.NameofPerson.data,ContactPerson = form.ContactPerson.data, AdresstoVisit = form.AddresstoVisit.data, image_file= picture_file)
                    db.session.add(found)
                    db.session.commit()
                    flash("Sorry We couldnt find any match if anyone is looking for him we will give them their contact number","warning")
            else:
                flash("Upload image with a human face","danger")

    return render_template("Found.html",title="Found",form=form)


