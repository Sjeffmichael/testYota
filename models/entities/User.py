import re
from flask_login import UserMixin



class User(UserMixin):

    def __init__(self, id, username, password, nombre = '', apellido = ''):
        self.id = id
        self.username = username
        self.password = password
        self.nombre = nombre
        self.apellido = apellido

    @classmethod
    def check_password(self, query_password, login_password):
        if query_password == login_password:
            return True

        else:
            return False
