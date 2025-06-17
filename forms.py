from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, FloatField
from wtforms.fields.datetime import DateField
from wtforms.validators import InputRequired, Email, Length, ValidationError, DataRequired, Optional
from wtforms import StringField, TextAreaField, SelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget
from flask_wtf.file import FileField, FileAllowed

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = StringField('Senha', validators=[InputRequired()])

class UsuarioForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Senha', validators=[Length(min=6, message="Senha deve ter pelo menos 6 caracteres")])
    
    def __init__(self, *args, **kwargs):
        self.is_edit = kwargs.pop('is_edit', False)
        super(UsuarioForm, self).__init__(*args, **kwargs)
        
        # Se for edição, senha não é obrigatória
        if not self.is_edit:
            self.password.validators.insert(0, InputRequired())

class RegisterForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = StringField('Senha', validators=[InputRequired()])
    categoria = SelectField('Categoria', coerce=int)

class CircoForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    contato_responsavel = StringField('Contato do Responsável')
    telefone_contato = StringField('Telefone de Contato')
    observacoes = StringField('Observações')

class CategoriaColaboradorForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])

class ColaboradorForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    categorias = MultiCheckboxField('Categorias', coerce=int, validators=[InputRequired(message="Selecione pelo menos uma categoria")])

class ElencoForm(FlaskForm):
    # Estados brasileiros
    ESTADOS_BRASILEIROS = [
        ('', 'Selecione o estado'),
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins')
    ]
    
    nome = StringField('Nome', validators=[InputRequired()])
    cpf = StringField('CPF')
    endereco = StringField('Endereço')
    cidade = StringField('Cidade')
    estado = SelectField('Estado', choices=ESTADOS_BRASILEIROS)
    telefone = StringField('Telefone')
    email = StringField('Email')
    observacoes = StringField('Observações')

class CategoriaFornecedorForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])

class FornecedorForm(FlaskForm):
    # Estados brasileiros
    ESTADOS_BRASILEIROS = [
        ('', 'Selecione o estado'),
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins')
    ]
    
    nome = StringField('Nome', validators=[InputRequired()])
    telefone = StringField('Telefone')
    cidade = StringField('Cidade')
    estado = SelectField('Estado', choices=ESTADOS_BRASILEIROS)
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
    id_tipo_despesa = SelectField('Tipo de Despesa', coerce=int, choices=[
        (1, 'Fixas - Evento'),
        (2, 'Variáveis - Evento'),
        (3, 'Fixas - SócratesOnline'),
        (4, 'Variáveis - SócratesOnline')
    ], validators=[InputRequired()])
    valor_medio_despesa = StringField('Valor Médio da Despesa')
    
    def validate_valor_medio_despesa(form, field):
        """Validar se o valor médio é obrigatório para despesas fixas"""
        if form.id_tipo_despesa.data in [1, 3]:  # Despesas fixas
            if not field.data or field.data.strip() == '':
                raise ValidationError('Valor médio é obrigatório para despesas fixas.')
            
            # Validar se é um número válido
            try:
                valor = field.data.replace(',', '.')
                float(valor)
            except ValueError:
                raise ValidationError('Valor médio deve ser um número válido.')

class EventoForm(FlaskForm):
    # Estados brasileiros
    ESTADOS_BRASILEIROS = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins')
    ]
    
    nome = StringField('Nome', validators=[InputRequired(message="Nome é obrigatório")])
    data_inicio = DateField('Data de Início', validators=[InputRequired(message="Data de início é obrigatória")])
    data_fim = DateField('Data de Fim', validators=[InputRequired(message="Data de fim é obrigatória")])
    cidade = StringField('Cidade', validators=[InputRequired(message="Cidade é obrigatória")])
    estado = SelectField('Estado', choices=ESTADOS_BRASILEIROS, validators=[InputRequired(message="Estado é obrigatório")])
    endereco = StringField('Endereço', validators=[InputRequired(message="Endereço é obrigatório")])
    id_circo = SelectField('Circo', coerce=int)
    id_produtor = SelectField('Produtor', coerce=int, validators=[InputRequired(message="Produtor é obrigatório")])
    status = SelectField('Status', choices=[
        ('planejamento', 'Planejamento'),
        ('a realizar', 'A Realizar'),
        ('em andamento', 'Em Andamento'),
        ('realizado', 'Realizado'),
        ('cancelado', 'Cancelado')
    ])
    observacoes = TextAreaField('Observações')

class CategoriaVeiculoForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])

class VeiculoForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    modelo = StringField('Modelo')
    marca = StringField('Marca')
    ano = IntegerField('Ano')
    placa = StringField('Placa')
    cor = StringField('Cor')
    combustivel = StringField('Combustível')
    capacidade_passageiros = IntegerField('Capacidade de Passageiros')
    observacoes = StringField('Observações')
    id_categoria_veiculo = SelectField('Categoria', coerce=int)

class EquipeEventoForm(FlaskForm):
    id_colaborador = SelectField('Colaborador', coerce=int, validators=[InputRequired(message="Selecione um colaborador")])
    funcao = StringField('Função')
    observacoes = TextAreaField('Observações')

class ElencoEventoForm(FlaskForm):
    id_elenco = SelectField('Elenco', coerce=int, validators=[InputRequired(message="Selecione um membro do elenco")])
    observacoes = TextAreaField('Observações')

class FornecedorEventoForm(FlaskForm):
    id_fornecedor = SelectField('Fornecedor', coerce=int, validators=[InputRequired(message="Selecione um fornecedor")])
    observacoes = TextAreaField('Observações')

class ReceitaEventoForm(FlaskForm):
    categoria_receita = SelectField('Categoria', coerce=int, validators=[DataRequired()])
    receita_id = SelectField('Receita', coerce=int, validators=[DataRequired()])
    data = DateField('Data', validators=[DataRequired()])
    valor = FloatField('Valor', validators=[DataRequired()])
    observacoes = TextAreaField('Observações')

class DespesaEventoForm(FlaskForm):
    categoria_despesa = SelectField('Categoria', coerce=int, validators=[DataRequired()])
    despesa_id = SelectField('Despesa', coerce=int, validators=[DataRequired()])
    data = DateField('Data', validators=[DataRequired()])
    valor = FloatField('Valor', validators=[DataRequired()])
    fornecedor_id = SelectField('Fornecedor', coerce=int, validators=[Optional()])
    status_pagamento = SelectField('Status', choices=[
        ('pendente', 'Pendente'),
        ('pago', 'Pago')
    ], validators=[DataRequired()])
    forma_pagamento = SelectField('Forma de Pagamento', choices=[
        ('débito', 'Débito'),
        ('crédito', 'Crédito'),
        ('espécie', 'Espécie'),
        ('pix', 'Pix')
    ], validators=[DataRequired()])
    pago_por = StringField('Pago por')
    observacoes = TextAreaField('Observações')
