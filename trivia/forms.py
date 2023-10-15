from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegisterForm(FlaskForm):
    username = StringField(label='username')
    nombre = StringField(label="nombre")
    email = EmailField(label='email')
    password = PasswordField(label='password', validators=[DataRequired(),
                                                           EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField(label='confirm password', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    submit = SubmitField(label='submit')
