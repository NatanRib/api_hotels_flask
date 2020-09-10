from sql_alchemy import database
from flask import request, url_for
from requests import post

MAILGUN_DOMAIN = 'seu_dominio_mailgun'
MAINGUN_API_KEY = 'sua_api_key'
FROM_TITLE = 'NO REPLY'
FROM_EMAIL = 'no-reply@apihotels.com'

class UserModel(database.Model):
    __tablename__ = 'users'

    user_id = database.Column(database.Integer, primary_key = True)
    login = database.Column(database.String(20), unique=True, nullable=False)
    password = database.Column(database.String(20), nullable=False)
    email = database.Column(database.String(40), unique=True, nullable=False)
    active = database.Column(database.Boolean)

    def __init__(self, login, password, email, active):
        self.login = login
        self.password = password
        self.email = email
        self.active = active

    def to_json(self):
        return {
            'login' : self.login,
            'password' : self.password,
            'email': self.email,
            'active': self.active
        }

    @classmethod
    def find_one_login(cls, user_login):

        # #metodo de consulta, filtrando por id, pegando o primeiro resultado
        user = cls.query.filter_by(login = user_login).first()
        if user:
            return user
        return None

    @classmethod
    def find_one_id(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_one_email(cls, user_email):
        user = cls.query.filter_by(email=user_email).first()
        if user:
            return user
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

    def send_email_confirmantion(self):
        link = request.url_root[:-1] + url_for('useractivate', user_id=self.user_id)
        return post('https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN),
            auth=('api', MAINGUN_API_KEY),
            data={'from': '{} <{}>'.format(FROM_TITLE, FROM_EMAIL),
                'to': self.email,
                'subject': 'No reply - Account confirmation',
                'text': 'Confirme sua conta no hotels clicando no link a seguir {}'.format(link),
                'html': '<html><p>Confirme sua conta no hotels clicando no link a seguir\
                     <a href="{}">CONFIRMAR EMAIL</a></p></html>'.format(link)
            }
        )

    antonio cote 84 - esquina com a sp
    orcar mailho 3341 1427