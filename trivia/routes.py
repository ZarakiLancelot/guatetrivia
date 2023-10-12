from trivia import app
from flask import render_template
from trivia.forms import RegisterForm


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    form = RegisterForm()
    return render_template('/register.html', form=form)
