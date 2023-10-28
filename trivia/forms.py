from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from trivia.models import User
from password_strength import PasswordPolicy


class RegisterForm(FlaskForm):
    @staticmethod
    def validate_password(self, password_field):
        policy = PasswordPolicy.from_names(
            length=8,
            uppercase=1,
            numbers=1,
            special=1,
            nonletters=0,
        )
        password = password_field.data
        if not policy.test(password):
            raise ValidationError('La contraseña debe contener al menos 8 caracteres,'
                                  'una letra mayúscula, un número y un carácter especial.')

    @staticmethod
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('El nombre de usuario ya existe, por favor intenta con otro nombre de usuario')

    @staticmethod
    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('El correo electrónico ya existe, por favor intenta con otro correo electrónico')

    username = StringField(label='Usuario', validators=[Length(min=6, max=20), DataRequired()])
    nombre = StringField(label="Nombre", validators=[DataRequired()])
    email = EmailField(label='Correo Electrónico', validators=[DataRequired(), Email()])
    fecha_nacimiento = DateField(label="Fecha de Nacimiento")
    password = PasswordField(label='Contraseña',
                             validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(label='Confirmar contraseña',
                                     validators=[DataRequired(),
                                                 EqualTo('password', message='Las contraseñas deben de ser iguales')
                                                 ])
    genero = SelectField('Género', choices=[('masculino', 'Masculino'), ('femenino', 'Femenino')],
                         validators=[DataRequired()])
    avatar = FileField('Avatar', validators=[FileAllowed(['jpg', 'png', 'jpeg'],
                                                         'Solo se permiten imágenes con extensión JPG, JPEG y PNG')])
    submit = SubmitField(label='Crear Cuenta')


class LoginForm(FlaskForm):
    username = StringField(label="Usuario", validators=[DataRequired()])
    password = PasswordField(label="Contraseña", validators=[DataRequired()])
    submit = SubmitField(label="Iniciar Sesión")
