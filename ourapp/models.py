from ourapp import db,login_manager
from flask_login import UserMixin

#login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Table for the storing the lost and found people
class LostAndFound(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    NameofPerson = db.Column(db.String(100),unique=False,nullable=True)
    ContactPerson = db.Column(db.String(20),unique=False,nullable=True)
    AdresstoVisit = db.Column(db.String(100),unique=False,nullable=True)  
    image_file = db.Column(db.String(30),unique=True,nullable=True)
    def __repr__(self):
        return f"User('{self.NameofPerson}','{self.ContactPerson}')"

#Table for the data of the course registration
class CourseRegistration(db.Model):
    RollNo = db.Column(db.String(100),unique=False,nullable=False,primary_key= True)
    CourseCode = db.Column(db.String(20),unique=False,nullable=False,primary_key= True)
    image_file = db.Column(db.String(30),unique=True,nullable=False)
    def __repr__(self):
        return f"User('{self.RollNo}','{self.image_file}')"


#Table for the data of the student attendance
class Attendance(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    RollNo = db.Column(db.String(100),unique=False,nullable=False)
    CourseCode = db.Column(db.String(20),unique=False,nullable=False)
    Attended = db.Column(db.Boolean, server_default=u'false')
    Date = db.Column(db.String(100), unique=False, nullable=False) 
    def __repr__(self):
        return f"User('{self.RollNo}','{self.Date}' ,'{self.Attended}')"

#Table for the Data of the class participation
class ClassAttendance(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    Date = db.Column(db.String(100), unique=False, nullable=False)
    CourseCode = db.Column(db.String(20),unique=False,nullable=False)
    Strength = db.Column(db.Integer, server_default=u'false')
    

#Table for the Data of the Users
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    image_file = db.Column(db.String(20),unique=True,nullable=False)
    def __repr__(self):
        return f"User('{self.username}','{self.image_file}')"




