from trivia import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from trivia.forms import RegisterForm, LoginForm
from trivia.models import User
from trivia import db
from flask_login import login_user, logout_user, login_required


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              nombre=form.nombre.data,
                              email=form.email.data,
                              genero=form.genero.data,
                              password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"¡Cuenta creada exitosamente Ya puedes ingresar como {user_to_create.username}!", category="success")
        return redirect(url_for('login'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            print(f'Hay errores al crear el usuario: {err_msg}')
            flash(f'Hay errores al crear el usuario: {err_msg}', category='danger')

    return render_template('register.html', form=form)


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


@app.route('/logout')
def logout():
    logout_user()
    flash(f'Haz cerrado sesión correctamente', category='info')
    return redirect(url_for('home_page'))
