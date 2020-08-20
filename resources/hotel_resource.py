from flask_restful import Resource, reqparse #reqparse é a lib que vai nos trazer os corpo da req
from models.hotel_model import HotelModel
from flask_jwt_extended import jwt_required #é a funcao que traz a autorizacao do token
import sqlite3
from resources.filters import city_query, none_city_query
from models.site_model import SiteModel

body = reqparse.RequestParser()  # #o metodo por onde pegaremos nossos argumentos
body.add_argument('name', required=True, type= str, help="The field 'name' cannot be left blank.")
body.add_argument('city', required=True, type= str, help="The field 'city' cannot be left blank.")
body.add_argument('stars', required=True, type= float, help="The field 'stars' cannot be left blank.")
body.add_argument('price', required=True, type=float, help="The field 'price' cannot be left blank.")
body.add_argument('site_id', required=True, type=int , help="The field 'site_id' cannot be left blank.")


#/hoteis?city=Santos&star_min=4.0&price_max=340.00
path_params = reqparse.RequestParser()
path_params.add_argument('city', type= str, default= None)
path_params.add_argument('stars_min', type= float, default= 0)
path_params.add_argument('stars_max', type= float, default= 5)
path_params.add_argument('price_min', type= float, default= 0)
path_params.add_argument('price_max', type= float, default= 10000)
path_params.add_argument('limit', type= int, default= 50)
path_params.add_argument('offset', type= int, default= 0)


class Hoteis(Resource):
    
    def get(self):

        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        global path_params
        data = path_params.parse_args()
        #selecionamos apenas os dados validos:
        valid_data = {key:data[key] for key in data if data[key] is not None}

        if valid_data.get('city'):
            #se existir a cidade nos parametros nos usamos essa consulta
            query = city_query
        else:
            #se nao existir precisamos tirar ela da consulta
            query = none_city_query

        #para executar a consulta precisamos passar uma tuple com os parametros, nao um dict
        tuple_params = tuple([valid_data[key] for key in valid_data])
        results = cursor.execute(query, tuple_params)
        hotels= []
        #nos resultado apenas recebemos os valores do bd, precisamos iteralos e atribuir chaves
        for line in results:
            hotels.append(
                {
                    'id' : line[0],
                    'name' : line[1],
                    'city' : line[2],
                    'stars' : line[3],
                    'price' : line[4],
                    'site_id' : line[5]
                }
            )
        return {'hotels' : hotels}, 200

    @jwt_required
    def post(self):
        global body

        data = body.parse_args()

        if SiteModel.find_by_id(data['site_id']):
            hotel = HotelModel(**data)
            try:
                hotel.save_hotel()
                return hotel.to_json(), 201
            except:
                return 'An error ocurred trying save hotel', 500
        return {'mensage': "The site with id: '{}' not exist.".format(data['site_id'])}, 400
# #aparentemente n podemos ter metodos com assinaturas diferente, temos que criar outra classe


class Hotel(Resource):
    body = reqparse.RequestParser()  # #o metodo por onde pegaremos nossos argumentos
    body.add_argument('hotel_id', type= str)
    body.add_argument('name', required=True, type= str, help="The field 'name' cannot be left blank.")
    body.add_argument('city', required=True, type= str, help="The field 'city' cannot be left blank.")
    body.add_argument('stars', required=True, type= float, help="The field 'stars' cannot be left blank.")
    body.add_argument('price', required=True, type=float, help="The field 'price' cannot be left blank.")  
    # #montamos a estrura do body adcionando os argumentos

    def get(self, hotel_id):

        hotel = HotelModel.find_one(hotel_id)

        if hotel:
            return hotel.to_json(), 200
        
        return {'mensage': 'not found hotel with id: {} '.format(hotel_id)}, 404  # status code 404

    @jwt_required
    def put(self, hotel_id):

        data = self.body.parse_args()  # #recebemos os argumentos da requicisao na estrutura previamente
        # #montada, precisamos ter uma requicisao ativa para isso, por isso esta dentro do metodo
        hotel_encotrado = HotelModel.find_one(hotel_id)
        if hotel_encotrado:
            try:
                hotel_encotrado.update(data['name'], data['city'], data['stars'], data['price'])
                return hotel_encotrado.to_json(), 200
            except:
                return 'An error ocurred trying update hotel', 500
        return{'mensage': 'The hotel does not exist.'}, 400

    @jwt_required
    def delete(self, hotel_id):

        hotel = HotelModel.find_one(hotel_id)
        if hotel:
            try:
                hotel.delete()
                return {'mensage' : 'Hotel  id: {} deleted'.format(hotel_id)}, 200
            except:
                return 'An error ocurred trying delete hotel', 500

        return {'mensage': 'not found hotel with id: {} '.format(hotel_id)}, 404
