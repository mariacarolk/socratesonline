
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(), Email()])
    password = PasswordField('Senha', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    email = StringField('E-mail', validators=[InputRequired(), Email()])
    password = PasswordField('Senha', validators=[InputRequired(), Length(min=6)])
    categoria = SelectField('Categoria', coerce=int)
