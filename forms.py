from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SelectField, IntegerField, FloatField, TextAreaField, SelectMultipleField, HiddenField, BooleanField
from wtforms.fields.datetime import DateField
from wtforms.validators import InputRequired, Email, Length, ValidationError, DataRequired, Optional
from wtforms.widgets import CheckboxInput, ListWidget

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
    flag_alimentacao = BooleanField('Despesa de Alimentação', default=False)
    flag_combustivel = BooleanField('Despesa de Combustível', default=False)
    
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

class VeiculoEventoForm(FlaskForm):
    id_veiculo = SelectField('Veículo', coerce=int, validators=[InputRequired(message="Selecione um veículo")])
    id_motorista = SelectField('Motorista', coerce=int, validators=[InputRequired(message="Selecione um motorista")])
    data_inicio = DateField('Data de Início', validators=[InputRequired(message="Data de início é obrigatória")])
    data_devolucao = DateField('Data de Devolução', validators=[InputRequired(message="Data de devolução é obrigatória")])
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
    data_vencimento = DateField('Data de Vencimento', validators=[DataRequired()])
    data_pagamento = DateField('Data de Pagamento', validators=[Optional()])
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
    comprovante = FileField('Comprovante', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'], 'Apenas arquivos de imagem, PDF ou documento são permitidos')])
    qtd_dias = IntegerField('Quantidade de Dias', validators=[Optional()])
    qtd_pessoas = IntegerField('Quantidade de Pessoas', validators=[Optional()])

class DespesaEmpresaForm(FlaskForm):
    categoria_despesa = SelectField('Categoria', coerce=int, validators=[DataRequired()])
    despesa_id = SelectField('Despesa', coerce=int, validators=[DataRequired()])
    data_vencimento = DateField('Data de Vencimento', validators=[DataRequired()])
    data_pagamento = DateField('Data de Pagamento', validators=[Optional()])
    valor = StringField('Valor', validators=[DataRequired()])  # Mudou para StringField para aceitar formato brasileiro
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
    comprovante = FileField('Comprovante', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'], 'Apenas arquivos de imagem, PDF ou documento são permitidos')])
    qtd_dias = IntegerField('Quantidade de Dias', validators=[Optional()])
    qtd_pessoas = IntegerField('Quantidade de Pessoas', validators=[Optional()])
    
    def validate_valor(form, field):
        """Validar e converter valor do formato brasileiro para float"""
        if not field.data or field.data.strip() == '':
            raise ValidationError('Valor é obrigatório.')
        
        try:
            # Converter formato brasileiro (1.000,50) para formato americano (1000.50)
            valor_str = str(field.data).strip()
            
            # Se contém ponto e vírgula, é formato brasileiro (ex: 1.000,50)
            if '.' in valor_str and ',' in valor_str:
                # Remover pontos de milhares e trocar vírgula por ponto
                valor_str = valor_str.replace('.', '').replace(',', '.')
            # Se contém apenas vírgula, trocar por ponto
            elif ',' in valor_str and '.' not in valor_str:
                valor_str = valor_str.replace(',', '.')
            
            valor_float = float(valor_str)
            
            if valor_float <= 0:
                raise ValidationError('Valor deve ser maior que zero.')
                
            # Armazenar o valor convertido para uso posterior
            field.data = valor_float
            
        except (ValueError, TypeError):
            raise ValidationError('Valor deve ser um número válido. Use vírgula para separar decimais (ex: 10,50).')

class ReceitaEmpresaForm(FlaskForm):
    categoria_receita = SelectField('Categoria', coerce=int, validators=[DataRequired()])
    receita_id = SelectField('Receita', coerce=int, validators=[DataRequired()])
    data = DateField('Data', validators=[DataRequired()])
    valor = StringField('Valor', validators=[DataRequired()])  # Mudou para StringField para aceitar formato brasileiro
    observacoes = TextAreaField('Observações')
    
    def validate_valor(form, field):
        """Validador personalizado para aceitar valores em formato brasileiro"""
        if not field.data or field.data.strip() == '':
            raise ValidationError('Valor é obrigatório.')
        
        try:
            # Converter formato brasileiro (1.000,50) para formato americano (1000.50)
            valor_str = str(field.data).strip()
            
            # Se contém ponto e vírgula, é formato brasileiro (ex: 1.000,50)
            if '.' in valor_str and ',' in valor_str:
                # Remover pontos de milhares e trocar vírgula por ponto
                valor_str = valor_str.replace('.', '').replace(',', '.')
            # Se contém apenas vírgula, trocar por ponto
            elif ',' in valor_str and '.' not in valor_str:
                valor_str = valor_str.replace(',', '.')
            
            valor_float = float(valor_str)
            
            if valor_float <= 0:
                raise ValidationError('Valor deve ser maior que zero.')
                
            # Armazenar o valor convertido para uso posterior
            field.data = valor_float
            
        except (ValueError, TypeError):
            raise ValidationError('Valor deve ser um número válido. Use vírgula para separar decimais (ex: 10,50).')
