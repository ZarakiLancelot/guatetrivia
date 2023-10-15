from trivia import db


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nombre = db.Column(db.String(length=50), nullable=False)
    username = db.Column(db.String(length=20), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    gender = db.Column(db.String(length=15), nullable=False)

    def __repr__(self):
        return f'User {self.username}'
