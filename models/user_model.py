from sql_alchemy import database

class UserModel(database.Model):
    __tablename__ = 'users'

    user_id = database.Column(database.Integer, primary_key = True)
    login = database.Column(database.String(20))
    password = database.Column(database.String(20))

    def __init__(self, login, password, email):
        self.login = login
        self.password = password

    def to_json(self):
        return {
            'login' : self.login,
            'password' : self.password
        }

    @classmethod
    def find_one(cls, user_login):

        # #metodo de consulta, filtrando por id, pegando o primeiro resultado
        hot = cls.query.filter_by(login = user_login).first()
        if hot:
            return hot
        return None

    @classmethod
    def all(cls):
        return cls.query.all()

    def save(self):
        # #abre uma sessao e adciona o proprio obj ao banco
        database.session.add(self)
        database.session.commit() # #salvas as alteracoes

    def delete(self):
        database.session.delete(self)
        database.session.commit()