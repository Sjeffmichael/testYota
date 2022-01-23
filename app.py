from this import d
from flask import Flask, redirect, render_template, request, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from datetime import datetime

#Models
from models.ModelUser import ModelUser

#Entities
from models.entities.User import User

from config import config

app = Flask(__name__)

db = MySQL(app)
loging_manager_app = LoginManager(app)

@loging_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['user'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))

            else:
                flash('Contraseña incorrecta')
                return render_template('login.html')

        else:
            flash('Usuario no encontrado')
            return render_template('login.html')

    else:
        return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/crear_gestion', methods = ['GET', 'POST'])
def nuevaGestion():
    if request.method == 'POST':
        visita = False
        if request.form['customRadio'] == 'SI':
            visita = True
        print((datetime.now()).date())
        try:
            cursor = db.connection.cursor()
            sql = f"""INSERT INTO gestion (nombreGestion, visita, fecha, Usuario_codigoUsuario)
                    VALUES ('{request.form['nombre_gestion']}', {visita}, '{(datetime.now()).date()}', '{current_user.id}')"""
            
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

        
        return render_template('crear_gestion.html')

    else:
        return render_template('crear_gestion.html')

@app.route('/gestiones', methods = ['GET', 'POST'])
def gestiones():
    if request.method == 'POST':
        print(request.form['buttom'])
        try:
            cursor = db.connection.cursor()

            sql1 = f"""SELECT idGestion, nombreGestion, visita, fecha, Usuario_codigoUsuario
                    FROM gestion WHERE Usuario_codigoUsuario = '{current_user.id}'"""

            cursor.execute(sql1)
            query1 = cursor.fetchall()

            sql_exist = f"""SELECT atendido, fecha, Gestion_idGestion FROM gestioncliente
                        WHERE Gestion_idGestion = {request.form['buttom']}"""
            
            cursor.execute(sql_exist)
            query2 = cursor.fetchone()
            if query2 is None:
                sql_insert = f"""INSERT INTO gestioncliente (atendido, fecha, Gestion_idGestion)
                            VALUES ({False}, '{(datetime.now()).date()}', {request.form['buttom']})"""

                cursor.execute(sql_insert)
                db.connection.commit()
            
        except Exception as ex:
            raise Exception(ex)

        return render_template('gestiones.html', query = query1)
        
    
    else:
        try:
            cursor = db.connection.cursor()
            sql = f"""SELECT idGestion, nombreGestion, visita, fecha, Usuario_codigoUsuario
                    FROM gestion WHERE Usuario_codigoUsuario = '{current_user.id}'"""

            cursor.execute(sql)
            query = cursor.fetchall()
            
        except Exception as ex:
            raise Exception(ex)

        return render_template('gestiones.html', query = query)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
        
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()