from flask import request, jsonify
from flask_restx import Resource, Namespace,fields
from app.models import User,Admin,DonorManager
from flask_jwt_extended import create_access_token
from app.utils import token_required
from app import bcrypt,db


auth_ns = Namespace('auth',description="Authentication operations")

register_model = auth_ns.model('Register',{
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email'),
    'password': fields.String(required=True, description='The password'),
    'role': fields.String(required=True, description='The role (Donor Manager,Admin,User)'),
})

user_request_model = auth_ns.model('UserRequest', {
    'email': fields.String(required=True, description='The email'),
    'password': fields.String(required=True, description='The password')
})


@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    #@auth_ns.marshal_with(register_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        
        password = data.get('password')
        email_id = data.get('email')
        role = data.get('role')
        hashed_passcode = bcrypt.generate_password_hash(password).decode('utf-8')
        if role == "admin":
            new_user = Admin(username=username,password=hashed_passcode,email_id=email_id)
        elif role == "Donor Manager":
            new_user = DonorManager(username=username,password=hashed_passcode,email_id=email_id)
        elif role == "user":
            new_user =  User(username=username,password=hashed_passcode,email_id=email_id)   
        else:
            return {"message" : "Invalid role"}, 400

        db.session.add(new_user)
        db.session.commit()

        return {"message" : "User registered successfully"}, 201


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(user_request_model)
    def post(self):
        data = request.get_json()
        email_id = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email_id=email_id).first() or Admin.query.filter_by(email_id=email_id).first() or DonorManager.query.filter_by(email_id=email_id).first()
        print("user",user)
        if user and bcrypt.check_password_hash(user.password,password):
            access_token = create_access_token(identity={'username': user.username, 'role': user.__class__.__name__.lower()})
            return {'access_token': f"Bearer {access_token}"}, 200
        return {'message': 'Invalid credentials'}, 401
    

@auth_ns.route('/test')
class test(Resource):
    @token_required
    def get(self):
        return {"message":"token is valid"}



    

    









