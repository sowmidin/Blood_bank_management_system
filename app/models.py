from app import db

class BloodDatabase(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    blood_group = db.Column(db.String(3),nullable= False)
    units= db.Column(db.Integer,nullable = False,default=0)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50),unique = True, nullable = False)
    password = db.Column(db.String(255),nullable = True)
    email_id = db.Column(db.String(25),nullable=False)

class DonorManager(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50),unique = True, nullable = False)
    password = db.Column(db.String(255),nullable = True)
    email_id = db.Column(db.String(25),nullable=False)    

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50),unique = True, nullable = False)
    password = db.Column(db.String(255),nullable = True)
    email_id = db.Column(db.String(25),nullable=False)      

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100),nullable= False)
    age =  db.Column(db.Integer,nullable = False)
    blood_group = db.Column(db.String(3),nullable=False)  
    email_id = db.Column(db.String(25),nullable=False)


      


