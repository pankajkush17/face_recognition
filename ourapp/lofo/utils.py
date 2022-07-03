import os
import secrets
from PIL import Image
from flask import current_app

from deepface import DeepFace
#FUnction for saving the picture
def savepicture(form_picture,code):
    #generating a random hex to store the image name and keeping its extenion as jpg
    random_hex = secrets.token_hex(10)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + '.jpg'


    
    #checking whether to store image in the lost databsse or the found databse
    if code == "lost":
        picture_path = os.path.join(current_app.root_path, 'static/missingpeople/lost', picture_fn)
    else:
        picture_path = os.path.join(current_app.root_path, 'static/missingpeople/found', picture_fn)

    #storing images in the less size so that space gets saved
    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    #saving the image
    i.save(picture_path)
    valid = 1
    #returninh the picture name
    return picture_fn, valid

