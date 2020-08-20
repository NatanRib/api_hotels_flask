from sql_alchemy import database

class SiteModel(database.Model):
    __tablename__ = 'sites'

    site_id = database.Column(database.Integer, primary_key = True)
    url = database.Column(database.String(40))
    hotels = database.relationship('HotelModel') #lista de hoteis relacionados a esse site

    def __init__(self, url):
        self.url = url

    def to_json(self):
        return {
            'site_id' : self.site_id,
            'url' : self.url,
            'hotels' : [hotel.to_json() for hotel in self.hotels]
        }

    @classmethod
    def find_by_id(cls, site_id):

        # #metodo de consulta, filtrando por id, pegando o primeiro resultado
        site = cls.query.filter_by(site_id = site_id).first()
        if site:
            return site
        return None

    @classmethod
    def find_by_url(cls, site_url):
        site = cls.query.filter_by(url = site_url).first()
        if site:
            return site
        return None

    @classmethod
    def all(cls):
        return cls.query.all()

    def save(self):
        # #abre uma sessao e adciona o proprio obj ao banco
        database.session.add(self)
        database.session.commit() # #salvas as alteracoes

    def delete(self):
        [hotel.delete() for hotel in self.hotels]
        database.session.delete(self)
        database.session.commit()