from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SelectField, IntegerField, FloatField, TextAreaField, SelectMultipleField, HiddenField, BooleanField, DecimalField
from wtforms.fields.datetime import DateField, TimeField, DateTimeLocalField
from wtforms.validators import InputRequired, Email, Length, ValidationError, DataRequired, Optional, NumberRange
from wtforms.widgets import CheckboxInput, ListWidget
from datetime import date, datetime

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Senha', validators=[InputRequired()])

class UsuarioForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Senha', validators=[Length(min=6, message="Senha deve ter pelo menos 6 caracteres")])
    confirm_password = PasswordField('Confirmar Senha', validators=[Length(min=6, message="Confirmação deve ter pelo menos 6 caracteres")])
    
    def __init__(self, *args, **kwargs):
        self.is_edit = kwargs.pop('is_edit', False)
        self.colaborador_email = kwargs.pop('colaborador_email', None)
        super(UsuarioForm, self).__init__(*args, **kwargs)
        
        # Se for edição, senha não é obrigatória
        if not self.is_edit:
            self.password.validators.insert(0, InputRequired())
            self.confirm_password.validators.insert(0, InputRequired())
        
        # Se tiver email do colaborador, pré-preencher e tornar readonly
        if self.colaborador_email and not self.is_edit:
            self.email.data = self.colaborador_email
    
    def validate_confirm_password(self, field):
        # Validar confirmação de senha tanto na criação quanto na edição (se senha foi preenchida)
        if self.password.data and self.password.data != field.data:
            raise ValidationError('As senhas não coincidem.')
        
        # Se for edição e senha foi preenchida, confirmar senha também deve estar preenchida
        if self.is_edit and self.password.data and not field.data:
            raise ValidationError('Confirme a nova senha.')



class CircoForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    contato_responsavel = StringField('Contato do Responsável')
    telefone_contato = StringField('Telefone de Contato')
    observacoes = StringField('Observações')

class CategoriaColaboradorForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])

class ColaboradorForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired()])
    telefone = StringField('Telefone', validators=[Optional(), Length(max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    categorias = MultiCheckboxField('Categorias', coerce=int, validators=[InputRequired(message="Selecione pelo menos uma categoria")])
    
    # Campos de senha (opcionais para edição, obrigatórios para cadastro)
    password = PasswordField('Senha', validators=[Optional(), Length(min=6, message="Senha deve ter pelo menos 6 caracteres")])
    confirm_password = PasswordField('Confirmar Senha', validators=[Optional(), Length(min=6, message="Confirmação deve ter pelo menos 6 caracteres")])
    
    def __init__(self, *args, **kwargs):
        self.colaborador_id = kwargs.pop('colaborador_id', None)
        self.is_edit_mode = kwargs.pop('is_edit_mode', False)
        super(ColaboradorForm, self).__init__(*args, **kwargs)
        
        # Se não for modo de edição (cadastro), tornar senhas obrigatórias
        if not self.is_edit_mode:
            self.password.validators = [InputRequired(message="Senha é obrigatória"), Length(min=6, message="Senha deve ter pelo menos 6 caracteres")]
            self.confirm_password.validators = [InputRequired(message="Confirmação de senha é obrigatória"), Length(min=6, message="Confirmação deve ter pelo menos 6 caracteres")]
    
    def validate_email(self, field):
        from models import Colaborador, Usuario
        
        # Se não há dados no email, pular validação (será capturado por InputRequired)
        if not field.data or not field.data.strip():
            return
            
        email_limpo = field.data.strip().lower()
        
        try:
            # Verificar se email já existe em outro colaborador
            existing_colaborador = Colaborador.query.filter_by(email=email_limpo).first()
            if existing_colaborador and (not self.colaborador_id or existing_colaborador.id_colaborador != self.colaborador_id):
                raise ValidationError('Este email já está sendo usado por outro colaborador.')
            
            # Verificar se email já existe em usuários (que não sejam do colaborador atual)
            existing_usuario = Usuario.query.filter_by(email=email_limpo).first()
            if existing_usuario and (not self.colaborador_id or existing_usuario.id_colaborador != self.colaborador_id):
                raise ValidationError('Este email já está sendo usado por outro usuário no sistema.')
        except Exception as e:
            # Em caso de erro na validação, registrar mas não bloquear
            print(f"DEBUG: Erro na validação de email: {str(e)}")
            # Não re-raise o erro para não bloquear o cadastro por problemas de DB
    
    def validate_confirm_password(self, field):
        if self.password.data and field.data and field.data != self.password.data:
            raise ValidationError('As senhas não coincidem.')

class AutoCadastroForm(FlaskForm):
    # Dados pessoais
    nome = StringField('Nome Completo', validators=[InputRequired(message="Nome é obrigatório")])
    telefone = StringField('Telefone', validators=[Optional(), Length(max=20)])
    email = StringField('Email', validators=[InputRequired(message="Email é obrigatório"), Email(message="Email inválido")])
    
    # Categoria (exceto administrativo)
    categoria = SelectField('Categoria', coerce=int, validators=[InputRequired(message="Selecione uma categoria")])
    
    # Dados de login
    password = PasswordField('Senha', validators=[
        InputRequired(message="Senha é obrigatória"), 
        Length(min=6, message="Senha deve ter pelo menos 6 caracteres")
    ])
    confirm_password = PasswordField('Confirmar Senha', validators=[
        InputRequired(message="Confirmação de senha é obrigatória"),
        Length(min=6, message="Confirmação deve ter pelo menos 6 caracteres")
    ])
    
    def validate_email(self, field):
        from models import Colaborador, Usuario
        
        # Verificar se email já existe em colaboradores
        existing_colaborador = Colaborador.query.filter_by(email=field.data).first()
        if existing_colaborador:
            raise ValidationError('Este email já está sendo usado por outro colaborador.')
        
        # Verificar se email já existe em usuários
        existing_usuario = Usuario.query.filter_by(email=field.data).first()
        if existing_usuario:
            raise ValidationError('Este email já está sendo usado por outro usuário.')
    
    def validate_confirm_password(self, field):
        if field.data != self.password.data:
            raise ValidationError('As senhas não coincidem.')

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
    media_km_litro = StringField('Média KM/Litro')
    observacoes = StringField('Observações')
    id_categoria_veiculo = SelectField('Categoria', coerce=int)
    
    def validate_media_km_litro(form, field):
        """Validador personalizado para aceitar valores em formato brasileiro"""
        if field.data and field.data.strip() != '':
            try:
                # Converter formato brasileiro (8,5) para formato americano (8.5)
                valor_str = str(field.data).strip()
                
                # Se contém ponto e vírgula, é formato brasileiro (ex: 10,5)
                if '.' in valor_str and ',' in valor_str:
                    # Remover pontos de milhares e trocar vírgula por ponto
                    valor_str = valor_str.replace('.', '').replace(',', '.')
                # Se contém apenas vírgula, trocar por ponto
                elif ',' in valor_str and '.' not in valor_str:
                    valor_str = valor_str.replace(',', '.')
                
                valor_float = float(valor_str)
                
                if valor_float <= 0:
                    raise ValidationError('Média km/litro deve ser maior que zero.')
                    
                # Armazenar o valor convertido para uso posterior
                field.data = valor_float
                
            except (ValueError, TypeError):
                raise ValidationError('Média km/litro deve ser um número válido. Use vírgula para separar decimais (ex: 8,5).')

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
    data_inicio = DateField('Data de Início', validators=[InputRequired(message="Data de início é obrigatória")], default=date.today)
    data_devolucao = DateField('Data de Devolução (opcional)', validators=[Optional()])
    hora_inicio = TimeField('Hora de Início', validators=[InputRequired(message="Hora de início é obrigatória")], default=lambda: datetime.now().time())
    hora_fim = TimeField('Hora de Fim (opcional)', validators=[Optional()])
    km_inicio = IntegerField('KM Inicial', validators=[InputRequired(message="KM inicial é obrigatório")])
    km_fim = IntegerField('KM Final (opcional)', validators=[Optional()])
    observacoes = TextAreaField('Observações')
    
    def validate_data_devolucao(self, field):
        if field.data and self.data_inicio.data and field.data < self.data_inicio.data:
            raise ValidationError('A data de devolução não pode ser anterior à data de início.')
    
    def validate_hora_fim(self, field):
        if field.data and self.hora_inicio.data:
            # Se é o mesmo dia, hora fim deve ser posterior à hora início
            if not self.data_devolucao.data or self.data_devolucao.data == self.data_inicio.data:
                if field.data <= self.hora_inicio.data:
                    raise ValidationError('A hora de fim deve ser posterior à hora de início.')
    
    def validate_km_fim(self, field):
        if field.data and self.km_inicio.data and field.data <= self.km_inicio.data:
            raise ValidationError('A quilometragem final deve ser maior que a inicial.')
    
    def validate(self, extra_validators=None):
        # Chamar validação padrão primeiro
        if not super().validate(extra_validators):
            return False
        
        # Validação customizada: se qualquer um dos 3 campos de "finalização" for preenchido,
        # todos devem ser preenchidos
        campos_finalizacao = [
            (self.data_devolucao.data, 'data de devolução'),
            (self.hora_fim.data, 'hora de fim'),
            (self.km_fim.data, 'quilometragem final')
        ]
        
        # Verificar quais campos foram preenchidos
        preenchidos = [(valor, nome) for valor, nome in campos_finalizacao if valor is not None]
        
        # Se pelo menos um foi preenchido, todos devem estar preenchidos
        if preenchidos and len(preenchidos) < 3:
            campos_faltando = [nome for valor, nome in campos_finalizacao if valor is None]
            
            # Adicionar erros nos campos que faltam
            if not self.data_devolucao.data:
                self.data_devolucao.errors.append('Campo obrigatório quando há informações de finalização.')
            if not self.hora_fim.data:
                self.hora_fim.errors.append('Campo obrigatório quando há informações de finalização.')
            if not self.km_fim.data:
                self.km_fim.errors.append('Campo obrigatório quando há informações de finalização.')
                
            return False
        
        return True

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
    valor = FloatField('Valor Real', validators=[DataRequired()])
    valor_pago_socrates = FloatField('Valor Pago Sócrates Online', validators=[Optional()])
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
    valor = StringField('Valor Real', validators=[DataRequired()])  # Mudou para StringField para aceitar formato brasileiro
    valor_pago_socrates = StringField('Valor Pago Sócrates Online', validators=[Optional()])
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

class ParametroForm(FlaskForm):
    parametro = StringField('Parâmetro', validators=[InputRequired()])
    valor = StringField('Valor')
    observacoes = TextAreaField('Observações')

class EscolaForm(FlaskForm):
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
    
    nome = StringField('Nome da Escola', validators=[InputRequired(message="Nome da escola é obrigatório")])
    endereco = StringField('Endereço', validators=[InputRequired(message="Endereço é obrigatório")])
    cidade = StringField('Cidade', validators=[InputRequired(message="Cidade é obrigatória")])
    estado = SelectField('Estado', choices=ESTADOS_BRASILEIROS, validators=[InputRequired(message="Estado é obrigatório")])
    email = StringField('E-mail da Escola', validators=[InputRequired(message="E-mail é obrigatório"), Email(message="E-mail inválido")])
    whatsapp = StringField('WhatsApp da Escola', validators=[InputRequired(message="WhatsApp é obrigatório")])
    nome_contato = StringField('Nome do Contato', validators=[InputRequired(message="Nome do contato é obrigatório")])
    cargo_contato = StringField('Cargo do Contato', validators=[Optional()])
    observacoes = TextAreaField('Observações', validators=[Optional()])
    
    def validate_whatsapp(form, field):
        """Validador personalizado para WhatsApp"""
        if field.data and field.data.strip():
            # Remover caracteres especiais para validação
            whatsapp_clean = ''.join(filter(str.isdigit, field.data))
            
            # Verificar se tem pelo menos 10 dígitos (formato mínimo brasileiro)
            if len(whatsapp_clean) < 10:
                raise ValidationError('WhatsApp deve ter pelo menos 10 dígitos.')
            
            # Verificar se não tem mais de 15 dígitos (formato internacional)
            if len(whatsapp_clean) > 15:
                raise ValidationError('WhatsApp não pode ter mais de 15 dígitos.')
    
    def validate(self, extra_validators=None):
        # Chamar validação padrão primeiro
        if not super().validate(extra_validators):
            return False
        
        # Validação customizada: pelo menos email OU whatsapp deve estar preenchido
        if not self.email.data and not self.whatsapp.data:
            self.email.errors.append('Pelo menos um meio de contato (e-mail ou WhatsApp) deve ser fornecido.')
            self.whatsapp.errors.append('Pelo menos um meio de contato (e-mail ou WhatsApp) deve ser fornecido.')
            return False
        
        return True

class VisitaEscolaForm(FlaskForm):
    id_escola = SelectField('Escola', coerce=int, validators=[InputRequired(message="Escola é obrigatória")])
    id_promotor = SelectField('Promotor Responsável', coerce=int, validators=[InputRequired(message="Promotor responsável é obrigatório")])
    data_visita = DateField('Data da Visita', validators=[InputRequired(message="Data da visita é obrigatória")], default=date.today)
    observacoes_visita = TextAreaField('Observações da Visita', validators=[Optional()])
    status_visita = SelectField('Status da Visita', 
                               choices=[
                                   ('agendada', 'Agendada'),
                                   ('realizada', 'Realizada'),
                                   ('cancelada', 'Cancelada')
                               ],
                               default='agendada',
                               validators=[InputRequired(message="Status é obrigatório")])

# Formulários para serviços de veículos

class MultaVeiculoForm(FlaskForm):
    numero_ait = StringField('Número do AIT', validators=[Optional()])
    data_infracao = DateField('Data da Infração', validators=[InputRequired(message="Data da infração é obrigatória")], default=date.today)
    data_vencimento = DateField('Data de Vencimento', validators=[InputRequired(message="Data de vencimento é obrigatória")])
    data_pagamento = DateField('Data de Pagamento', validators=[Optional()])
    valor_original = DecimalField('Valor Original (R$)', validators=[InputRequired(message="Valor original é obrigatório"), NumberRange(min=0.01, message="Valor deve ser maior que zero")], places=2)
    valor_pago = DecimalField('Valor Pago (R$)', validators=[Optional()], places=2)
    local_infracao = StringField('Local da Infração', validators=[Optional()])
    tipo_infracao = StringField('Tipo de Infração', validators=[InputRequired(message="Tipo de infração é obrigatório")])
    orgao_autuador = StringField('Órgão Autuador', validators=[Optional()])
    status = SelectField('Status', 
                        choices=[
                            ('Pendente', 'Pendente'),
                            ('Pago', 'Pago'),
                            ('Contestado', 'Contestado')
                        ],
                        default='Pendente',
                        validators=[InputRequired(message="Status é obrigatório")])
    observacoes = TextAreaField('Observações', validators=[Optional()])
    
    def validate_data_vencimento(self, field):
        if field.data and self.data_infracao.data and field.data < self.data_infracao.data:
            raise ValidationError('A data de vencimento não pode ser anterior à data da infração.')
    
    def validate_data_pagamento(self, field):
        if field.data and self.data_infracao.data and field.data < self.data_infracao.data:
            raise ValidationError('A data de pagamento não pode ser anterior à data da infração.')
    
    def validate_valor_pago(self, field):
        if field.data and self.valor_original.data and float(field.data) > float(self.valor_original.data) * 1.5:
            raise ValidationError('Valor pago parece muito alto comparado ao valor original. Verifique os dados.')

class IpvaVeiculoForm(FlaskForm):
    ano_exercicio = IntegerField('Ano de Exercício', validators=[InputRequired(message="Ano de exercício é obrigatório"), NumberRange(min=2000, max=2050, message="Ano deve estar entre 2000 e 2050")])
    data_vencimento = DateField('Data de Vencimento', validators=[InputRequired(message="Data de vencimento é obrigatória")])
    data_pagamento = DateField('Data de Pagamento', validators=[Optional()])
    valor_ipva = DecimalField('Valor do IPVA (R$)', validators=[InputRequired(message="Valor do IPVA é obrigatório"), NumberRange(min=0.01, message="Valor deve ser maior que zero")], places=2)
    valor_taxa_detran = DecimalField('Taxa DETRAN (R$)', validators=[Optional()], places=2)
    valor_multa_juros = DecimalField('Multa/Juros (R$)', validators=[Optional()], places=2)
    valor_total = DecimalField('Valor Total (R$)', validators=[InputRequired(message="Valor total é obrigatório"), NumberRange(min=0.01, message="Valor deve ser maior que zero")], places=2)
    valor_pago = DecimalField('Valor Pago (R$)', validators=[Optional()], places=2)
    numero_documento = StringField('Número do Documento', validators=[Optional()])
    status = SelectField('Status', 
                        choices=[
                            ('Pendente', 'Pendente'),
                            ('Pago', 'Pago'),
                            ('Atrasado', 'Atrasado')
                        ],
                        default='Pendente',
                        validators=[InputRequired(message="Status é obrigatório")])
    observacoes = TextAreaField('Observações', validators=[Optional()])
    
    def validate_ano_exercicio(self, field):
        current_year = datetime.now().year
        if field.data and (field.data < current_year - 10 or field.data > current_year + 1):
            raise ValidationError(f'Ano de exercício deve estar entre {current_year - 10} e {current_year + 1}.')

class LicenciamentoVeiculoForm(FlaskForm):
    ano_exercicio = IntegerField('Ano de Exercício', validators=[InputRequired(message="Ano de exercício é obrigatório"), NumberRange(min=2000, max=2050, message="Ano deve estar entre 2000 e 2050")])
    data_vencimento = DateField('Data de Vencimento', validators=[InputRequired(message="Data de vencimento é obrigatória")])
    data_pagamento = DateField('Data de Pagamento', validators=[Optional()])
    valor_licenciamento = DecimalField('Valor do Licenciamento (R$)', validators=[InputRequired(message="Valor do licenciamento é obrigatório"), NumberRange(min=0.01, message="Valor deve ser maior que zero")], places=2)
    valor_taxa_detran = DecimalField('Taxa DETRAN (R$)', validators=[Optional()], places=2)
    valor_multa_juros = DecimalField('Multa/Juros (R$)', validators=[Optional()], places=2)
    valor_total = DecimalField('Valor Total (R$)', validators=[InputRequired(message="Valor total é obrigatório"), NumberRange(min=0.01, message="Valor deve ser maior que zero")], places=2)
    valor_pago = DecimalField('Valor Pago (R$)', validators=[Optional()], places=2)
    numero_documento = StringField('Número do Documento', validators=[Optional()])
    status = SelectField('Status', 
                        choices=[
                            ('Pendente', 'Pendente'),
                            ('Pago', 'Pago'),
                            ('Atrasado', 'Atrasado')
                        ],
                        default='Pendente',
                        validators=[InputRequired(message="Status é obrigatório")])
    observacoes = TextAreaField('Observações', validators=[Optional()])
    
    def validate_ano_exercicio(self, field):
        current_year = datetime.now().year
        if field.data and (field.data < current_year - 10 or field.data > current_year + 1):
            raise ValidationError(f'Ano de exercício deve estar entre {current_year - 10} e {current_year + 1}.')

class ManutencaoVeiculoForm(FlaskForm):
    data_servico = DateField('Data do Serviço', validators=[InputRequired(message="Data do serviço é obrigatória")], default=date.today)
    tipo_manutencao = SelectField('Tipo de Manutenção', 
                                 choices=[
                                     ('Preventiva', 'Preventiva'),
                                     ('Corretiva', 'Corretiva'),
                                     ('Revisão', 'Revisão'),
                                     ('Troca de Óleo', 'Troca de Óleo'),
                                     ('Pneus', 'Pneus'),
                                     ('Freios', 'Freios'),
                                     ('Ar Condicionado', 'Ar Condicionado'),
                                     ('Elétrica', 'Elétrica'),
                                     ('Motor', 'Motor'),
                                     ('Transmissão', 'Transmissão'),
                                     ('Suspensão', 'Suspensão'),
                                     ('Outros', 'Outros')
                                 ],
                                 validators=[InputRequired(message="Tipo de manutenção é obrigatório")])
    descricao = TextAreaField('Descrição do Serviço', validators=[InputRequired(message="Descrição é obrigatória")])
    fornecedor_servico = StringField('Fornecedor/Oficina', validators=[Optional()])
    km_veiculo = IntegerField('KM do Veículo', validators=[Optional(), NumberRange(min=0, message="KM não pode ser negativo")])
    valor_servico = DecimalField('Valor do Serviço (R$)', validators=[InputRequired(message="Valor do serviço é obrigatório"), NumberRange(min=0.01, message="Valor deve ser maior que zero")], places=2)
    valor_pecas = DecimalField('Valor das Peças (R$)', validators=[Optional()], places=2)
    valor_total = DecimalField('Valor Total (R$)', validators=[InputRequired(message="Valor total é obrigatório"), NumberRange(min=0.01, message="Valor deve ser maior que zero")], places=2)
    data_proxima_revisao = DateField('Próxima Revisão', validators=[Optional()])
    km_proxima_revisao = IntegerField('KM Próxima Revisão', validators=[Optional(), NumberRange(min=0, message="KM não pode ser negativo")])
    garantia_dias = IntegerField('Garantia (dias)', validators=[Optional(), NumberRange(min=0, message="Garantia não pode ser negativa")])
    observacoes = TextAreaField('Observações', validators=[Optional()])
    
    def validate_data_proxima_revisao(self, field):
        if field.data and self.data_servico.data and field.data <= self.data_servico.data:
            raise ValidationError('A data da próxima revisão deve ser posterior à data do serviço.')
    
    def validate_km_proxima_revisao(self, field):
        if field.data and self.km_veiculo.data and field.data <= self.km_veiculo.data:
            raise ValidationError('A quilometragem da próxima revisão deve ser maior que a atual.')
    
    def validate_valor_total(self, field):
        if field.data and self.valor_servico.data:
            valor_pecas = self.valor_pecas.data or 0
            valor_esperado = float(self.valor_servico.data) + float(valor_pecas)
            if abs(float(field.data) - valor_esperado) > 0.01:
                raise ValidationError('Valor total deve ser igual à soma do valor do serviço e das peças.')

class FluxoCaixaForm(FlaskForm):
    data_referencia = DateField('Data de Referência', validators=[InputRequired()], default=date.today)
    saldo_inicial = FloatField('Saldo Inicial em Caixa', validators=[InputRequired()], default=0.0)
    observacoes = TextAreaField('Observações')
