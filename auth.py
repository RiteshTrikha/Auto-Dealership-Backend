from flask_restx import Resource,fields, Namespace
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from flask import request,jsonify



auth_ns = Namespace('auth', description='Authentication related operations')

sign_up_model=auth_ns.model("Signup",{
    "email":fields.String(),
    "f_name":fields.String(),
    "l_name":fields.String(),
    "password":fields.String()
})

login_model=auth_ns.model("Login",{
    "email":fields.String(),
    "password":fields.String()
})

@auth_ns.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
    
@auth_ns.route('/signup')
class SignupResource(Resource):
    @auth_ns.marshal_with(sign_up_model)
    @auth_ns.expect(sign_up_model)
    def post(self):
        data=request.get_json()
        email=data.get("email")
        db_email=User.query.filter_by(email=email).first()
        if db_email is not None:
            return jsonify({"message":"Email already exists"},400)

        new_user=User(
            email=email,
            f_name=data.get("f_name"),
            l_name=data.get("l_name"),
            password=generate_password_hash(data.get("password"))
        )
        new_user.save()
        return jsonify({"message":"User created"},201)
    
@auth_ns.route('/login')
class LoginResource(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data=request.get_json()
        email=data.get("email")
        password=data.get("password")
        user=User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            access_token=create_access_token(identity=user.id)
            refresh_token=create_refresh_token(identity=user.id)
            return jsonify({"access_token":access_token,"refresh_token":refresh_token})
        else:
            return {"message":"Invalid credentials"},401
