from flask import Flask, jsonify
from flask_restful import Resource, Api
from resources.hotel_resource import Hoteis, Hotel
from resources.user_resource import User, UserRegister, UserLogin, UserAll, UserLoggout, UserActivate #apagar
from resources.site_resource import Sites, Site
from flask_jwt_extended import JWTManager
from blacklist import BLASKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db' #caminho do bd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #para deixar o rastreio apenas para o flask
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone' #chave unica para garantir a criptografia
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_database():
    database.create_all()

@jwt.token_in_blacklist_loader
def blacklist_verify(token):
    return token['jti'] in BLASKLIST #verifica se o token esta na blacklist

@jwt.revoked_token_loader
def invalid_token_verify():
    return jsonify({'mensage': 'You have been logged out.'}), 401 #verifica se o token é invalido

api.add_resource(Hoteis, '/hotels')
api.add_resource(Hotel, '/hotels/<hotel_id>')
api.add_resource(User, '/user/<user_login>')
api.add_resource(UserRegister, '/singup')
api.add_resource(UserLogin, '/login')
api.add_resource(UserActivate, '/users/activate/<user_id>')
api.add_resource(UserAll, '/users') #apagar
api.add_resource(UserLoggout, '/logout')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<site_url>')

if __name__ == '__main__':
    from sql_alchemy import database

    database.init_app(app)
    app.run(debug=True)

 