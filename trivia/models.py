from trivia import bcrypt, db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

##################################################################################################


class Medal(db.Model):
    __tablename__ = 'medals'
    id = db.Column(db.Integer(), primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    imagen = db.Column(db.String(200))

##################################################################################################


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    nombre = db.Column(db.String(length=50), nullable=False)
    username = db.Column(db.String(length=20), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    genero = db.Column(db.String(length=15), nullable=False)
    fecha_nacimiento = db.Column(db.Date(), nullable=False)
    avatar = db.Column(db.String(1024))
    medals = db.relationship('Medal', secondary='user_medals', backref='users', lazy='dynamic')
    puntos = db.Column(db.Integer(), default=0)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def __repr__(self):
        return f'{self.username}'

##################################################################################################


class UserMedals(db.Model):
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    medal_id = db.Column(db.Integer(), db.ForeignKey('medals.id'), primary_key=True)
    fecha_obtencion = db.Column(db.Date(), nullable=True)

##################################################################################################


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer(), primary_key=True)
    api_id = db.Column(db.Integer(), nullable=False)
    pregunta = db.Column(db.String(length=500), nullable=False)
    opcion_a = db.Column(db.String(length=200), nullable=False)
    opcion_b = db.Column(db.String(length=200), nullable=False)
    opcion_c = db.Column(db.String(length=200), nullable=False)
    correcta = db.Column(db.String(length=1), nullable=False)
