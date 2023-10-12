from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guatetrivia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'df46a34613411bda580e017b'
db = SQLAlchemy(app)


def create_db():
    with app.app_context():
        db.create_all()


from trivia import routes


create_db()
