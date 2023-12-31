import json
import ast
import os

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.orm import load_only
from werkzeug.utils import secure_filename
from random import choice

from trivia import app, ALLOWED_EXTENSIONS, BASE_DIR
from trivia import db
from trivia.forms import RegisterForm, LoginForm
from trivia.models import User, UserMedals
from trivia.services import PreguntasService


pregunta_actual = 0


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


##################################################################################################


@app.route('/')
def home_page():
    return render_template('home.html')


##################################################################################################


@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    medals = UserMedals.query.filter_by(user_id=user.id).all()
    print("MEDALLAS:")
    print(medals)
    return render_template('dashboard.html', user=user, medals=medals)


##################################################################################################


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.avatar.data:
            avatar = form.avatar.data
            if avatar and allowed_file(avatar.filename):
                filename = secure_filename(avatar.filename)
                print("NOMBRE DEL ARCHIVO:")
                print(filename)
                path = os.path.join(BASE_DIR, 'static', 'images', 'avatar', filename)
                avatar.save(os.path.relpath(path))
                avatar_url = os.path.join('images', 'avatar', filename)
            else:
                avatar_url = None
        else:
            avatar_url = None

        user_to_create = User(username=form.username.data,
                              nombre=form.nombre.data,
                              email=form.email.data,
                              genero=form.genero.data,
                              fecha_nacimiento=form.fecha_nacimiento.data,
                              avatar=avatar_url,
                              password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f"¡Cuenta creada exitosamente Ya puedes ingresar como {user_to_create.username}!", category="success")
        return redirect(url_for('login'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            print(f'Hay errores al crear el usuario: {err_msg}')
            flash(f'Hay errores al crear el usuario: {err_msg}', category='danger')

    return render_template('register.html', form=form)


##################################################################################################


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        print(attempted_user)
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'¡Éxito! Has iniciado sesión como {attempted_user.username}', category="success")
            return redirect(url_for('dashboard'))
        else:
            flash(f'El usuario y/o contraseña ingresados no concuerdan con ninguno registrado en el sistema,'
                  f'por favor intenta de nuevo', category="danger")

    return render_template('login.html', form=form)


##################################################################################################


@app.route('/logout')
def logout():
    logout_user()
    flash(f'Haz cerrado sesión correctamente', category='info')
    return redirect(url_for('home_page'))


##################################################################################################


@app.route('/trivias')
@login_required
def trivias():
    global pregunta_actual
    base_url = 'http://3.135.193.178/preguntas.php?id='
    servicio_trivia = PreguntasService(base_url)
    preguntas = servicio_trivia.obtener_preguntas()

    if preguntas:
        # servicio_trivia.guardar_en_bd(pregunta_data)
        pregunta = choice(range(len(preguntas)))
        pregunta_escogida = preguntas[pregunta]
        print(f"La pregunta elegida es: {pregunta_escogida}")
        pregunta_formateada = {
            'pregunta': pregunta_escogida['pregunta'],
            'respuestas': {opcion: respuesta for opcion, respuesta in pregunta_escogida['respuestas'].items()
                           if opcion != 'correcta'}
        }
        return render_template('trivias.html', pregunta_escogida=pregunta_formateada, preguntas=preguntas)
    else:
        return "ERROR al obtener la pregunta de la API"

##################################################################################################


@app.route('/verificar_respuesta', methods=['POST'])
def verificar_respuesta():
    global pregunta_actual

    respuesta_usuario = request.form['respuesta']
    pregunta_actual_id = pregunta_actual
    pregunta_actual += 1
    preguntas_json = request.form['preguntas']
    preguntas_python = ast.literal_eval(preguntas_json)
    preguntas_json_corregido = json.dumps(preguntas_python)
    print(f"El JSON es: {preguntas_json_corregido}")
    preguntas = json.loads(preguntas_json_corregido)

    if pregunta_actual_id < len(preguntas):
        siguiente_pregunta = preguntas[pregunta_actual_id]
        pregunta_formateada = {
            'pregunta': siguiente_pregunta['pregunta'],
            'respuestas': {opcion: respuesta for opcion, respuesta in siguiente_pregunta['respuestas'].items()
                           if opcion != 'correcta'}
        }
    else:
        return redirect(url_for('dashboard'))

    return render_template('trivias.html', pregunta_escogida=pregunta_formateada, preguntas=preguntas)
