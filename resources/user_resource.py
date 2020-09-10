from flask_restful import Resource, reqparse
from models.user_model import UserModel
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import jwt_required, get_raw_jwt
from blacklist import BLASKLIST
import traceback


body = reqparse.RequestParser()
body.add_argument('login', type= str, required=True, help="The fiel 'login' cannot be left blank")
body.add_argument('password', type= str, required=True, help="The fiel 'password' cannot be left blank")
body.add_argument('email', type= str)
body.add_argument('active', type= bool)


#Teste - APAGAR
class UserAll(Resource):
     def get(self):
        return {'users': [user.to_json() for user in UserModel.all()]}, 200

class UserRegister(Resource):
    
    def post(self):
        global body

        data = body.parse_args()
        if not data.get('email'):
            return {'mensage' : "the field 'email' cannot left blank!"}, 400
        if UserModel.find_one_login(data['login']):
            return {'mensage' : "User '{}' allready exist!".format(data['login'])}, 400
        if UserModel.find_one_email(data['email']):
            return {'mensage' : "User with email '{}' allready exist!".format(data['email'])}, 400
        user = UserModel(**data)
        user.active = False
        try:
            user.save()
            user.send_email_confirmantion()
            return {'mensage': "User '{}' created".format(user.login)}, 201
        except:
            traceback.print_exc()
            return {'mensage': 'An internal error ocurred trying create user'}, 500


class User(Resource):

    def get(self, user_login):
        try:
            user = UserModel.find_one_login(user_login)
            if user:
                return user.to_json(), 200
            return {'mensage': 'User with login: {} not found'.format(user_login)}, 404
        except:
            return {'mensage' : 'An internal error ocurred trying get user'}, 500

    @jwt_required
    def delete(self, user_login):
        user = UserModel.find_one_login(user_login)
        if user:
            try:
                user.delete()
                return {'mensage' : 'user {} deleted!'.format(user.login)}, 200
            except:
                return {'mensage' : 'An internal error ocurred trying delete user'}, 500
        return {'mensage': 'User with login: {} not found'.format(user_login)}, 404
    
    
class UserLogin(Resource):

    def post(self):
        global body
        data = body.parse_args()
        user = UserModel.find_one_login(data['login'])
        if user:
            if not user.active:
                return{'mensage': 'The user is not active'}, 401
            #safe_str_cmp é a maneira mais segura de fazer essa comparacao
            if safe_str_cmp(user.password, data['password']):
                #essa funcao do JWT que cria nosso access token
                token = create_access_token(identity=user.user_id)
                return {'access_token': token}, 200
        return {'mensage': 'The username or password is incorrect.'}, 401

class UserActivate(Resource):
    
    def get(self, user_id):
        user = UserModel.find_one_id(user_id)
        if not user:
            return {'mensage': 'User not found'}, 404
        user.active = True
        try:
            user.save()
            return {'mensage': 'User {} activate succesfully'.format(user_id)}, 200
        except:
            return {'mensage': 'An internal error ocurred trying activate the user'}, 500

class UserLoggout(Resource):

    @jwt_required #esse recurso precisa ser protegido!
    def post(self):
        jti = get_raw_jwt()['jti'] #json token identifier, pegamos o identificador do tokken
        BLASKLIST.add(jti) #adcionamos a nossa lista negra(set)
        return {'mensage': 'Logged out succesfuly.'}, 200
        #o resto fazemos no app