from functools import wraps
from flask import jsonify
from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, exceptions

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            # token = None
            # print("entering try")
            # print("request",request.headers)
            # print("cookies",request.cookies)
            # print(request._cached_json)
            # if 'Authorization' in request.headers:  
            #     token = request.headers.get('Authorization') 
            #     print(token)   
            # elif not token:
            #     return {'message' : 'Token is missing'}, 401    
            verify_jwt_in_request()
            print("req verified")
            token = get_jwt_identity()
            # print("token identity",token)
        except Exception as e:
            return {"message": f"{e}"}, 401
        return f(*args, **kwargs)
    return decorated
