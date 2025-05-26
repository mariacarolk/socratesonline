
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.fields.datetime import DateField
from wtforms.validators import InputRequired, Email, Length
from wtforms import StringField, TextAreaField

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(), Email()])
    password = PasswordField('Senha', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    email = StringField('E-mail', validators=[InputRequired(), Email()])
    password = PasswordField('Senha', validators=[InputRequired(), Length(min=6)])
    categoria = SelectField('Categoria', coerce=int)

class CircoForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    contato_responsavel = StringField('Contato do Responsável')
    observacoes = TextAreaField('Observações')


class CategoriaColaboradorForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])

class ColaboradorForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    id_categoria_colaborador = SelectField('Categoria', coerce=int)

class ElencoForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    cpf = StringField('CPF')
    endereco = StringField('Endereço')
    cidade = StringField('Cidade')
    estado = StringField('Estado')
    telefone = StringField('Telefone')
    email = StringField('E-mail')
    observacoes = TextAreaField('Observações')

class CategoriaFornecedorForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])

class FornecedorForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    telefone = StringField('Telefone')
    id_categoria_fornecedor = SelectField('Categoria', coerce=int)

class CategoriaReceitaForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])

class ReceitaForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    id_categoria_receita = SelectField('Categoria', coerce=int)

class CategoriaDespesaForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])

class DespesaForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    id_categoria_despesa = SelectField('Categoria', coerce=int)

class EventoForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    data_inicio = DateField('Data Início', format='%Y-%m-%d')
    data_fim = DateField('Data Fim', format='%Y-%m-%d')
    cidade = StringField('Cidade')
    estado = StringField('Estado')
    endereco = StringField('Endereço')
    id_circo = SelectField('Circo', coerce=int)
    id_produtor = SelectField('Produtor', coerce=int)
    status = SelectField('Status', choices=[
        ('a realizar', 'A Realizar'),
        ('em andamento', 'Em Andamento'),
        ('realizado', 'Realizado')
    ])
    observacoes = TextAreaField('Observações')
