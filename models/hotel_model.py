from sql_alchemy import database

class HotelModel(database.Model):
    __tablename__ = 'hotels'

    hotel_id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(40))
    city = database.Column(database.String(40))
    stars = database.Column(database.Float(precision = 1))
    price = database.Column(database.Float(precision = 2))
    site_id = database.Column(database.Integer, database.ForeignKey('sites.site_id')) #chave estrangeira

    def __init__(self, name, city, stars, price, site_id):
        self.name = name
        self.city = city
        self.stars = stars
        self.price = price
        self.site_id = site_id

    def to_json(self):
        return {
            'hotel_id' : self.hotel_id,
            'nome' : self.name,
            'city' : self.city,
            'stars' : self.stars,
            'price' : self.price,
            'site_id' : self.site_id 
        }

    @classmethod
    def all(cls):
        return cls.query.all()
    

    @classmethod
    def find_one(cls, hotel_id):

        # #metodo de consulta, filtrando por id, pegando o primeiro resultado
        hot = cls.query.filter_by(hotel_id = hotel_id).first()
        if hot:
            return hot
        return None

    def save_hotel(self):
        # #abre uma sessao e adciona o proprio obj ao banco
        database.session.add(self)
        database.session.commit() # #salvas as alteracoes

    def update(self, name, city, stars, price):
        self.name = name
        self.city = city
        self.stars = stars
        self.price = price

        self.save_hotel()

    def delete(self):
        database.session.delete(self)
        database.session.commit()