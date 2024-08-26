from flask import Flask
from json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restx import Api
from flask_migrate import Migrate
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,JWTManager

authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
    }
}

db = SQLAlchemy()
bcrypt = Bcrypt()
api = Api(authorizations=authorizations,security='Bearer')
jwt = JWTManager()



def create_app():
    app = Flask(__name__)
    app.json_encoder = None
    app.config.from_object('app.config.Config')
    db.init_app(app)
    migrate = Migrate(app,db)
    bcrypt.init_app(app)
    jwt.init_app(app)    
    api.init_app(app)


    from app.resources.donor import donor_ns
    from app.resources.inventory import inventory_ns
    from app.resources.request import blood_request_ns
    from app.resources.auth import auth_ns
    api.add_namespace(donor_ns,path='/donors')
    api.add_namespace(inventory_ns,path='/inventory')
    api.add_namespace(blood_request_ns,path='/blood_request')
    api.add_namespace(auth_ns,path='/auth')
   


    return app

