from sqlite3 import Cursor

from models.entities.User import User


class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = f"""SELECT codigoUsuario, login, password, nombre, apellido FROM usuario
                    WHERE login = '{user.username}'"""

            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3], row[4])
                return user

            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = f"""SELECT codigoUsuario, login, nombre, apellido FROM usuario
                    WHERE codigoUsuario = '{id}'"""
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], None, row[2], row[3])
                return user

            else:
                return None
        except Exception as ex:
            raise Exception(ex)
