from extensions import db
from flask_login import UserMixin
from datetime import datetime

# Constantes para tipos de despesa
TIPOS_DESPESA = {
    1: 'Fixas - Evento',
    2: 'Variáveis - Evento', 
    3: 'Fixas - SócratesOnline',
    4: 'Variáveis - SócratesOnline'
}

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    id_colaborador = db.Column(db.Integer, db.ForeignKey('colaborador.id_colaborador'), nullable=False)
    
    # Relacionamento com colaborador
    colaborador = db.relationship('Colaborador', backref='usuario', uselist=False)
    
    @property
    def categoria_principal(self):
        """Retorna a primeira categoria do colaborador para compatibilidade"""
        if self.colaborador and self.colaborador.categorias:
            return self.colaborador.categorias[0]
        return None

class Circo(db.Model):
    __tablename__ = 'circo'
    id_circo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    contato_responsavel = db.Column(db.String)
    telefone_contato = db.Column(db.String)
    observacoes = db.Column(db.String)
    
    # Proteger circo se tiver eventos usando
    eventos = db.relationship('Evento', backref='circo', foreign_keys='Evento.id_circo')

class CategoriaColaborador(db.Model):
    __tablename__ = 'categoria_colaborador'
    id_categoria_colaborador = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    
    # Proteger categoria se tiver colaboradores usando
    colaborador_categorias = db.relationship('ColaboradorCategoria', backref='categoria_colaborador')

class ColaboradorCategoria(db.Model):
    __tablename__ = 'colaborador_categoria'
    id_colaborador = db.Column(db.Integer, db.ForeignKey('colaborador.id_colaborador'), primary_key=True)
    id_categoria_colaborador = db.Column(db.Integer, db.ForeignKey('categoria_colaborador.id_categoria_colaborador'), primary_key=True)
    colaborador = db.relationship('Colaborador', back_populates='categorias_associacao')

class Colaborador(db.Model):
    __tablename__ = 'colaborador'
    id_colaborador = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    telefone = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    
    # CASCADE DELETE para as associações de categoria quando colaborador é deletado
    categorias_associacao = db.relationship('ColaboradorCategoria', back_populates='colaborador', cascade='all, delete-orphan')
    categorias = db.relationship('CategoriaColaborador', secondary='colaborador_categoria', 
                                overlaps="categorias_associacao,categoria_colaborador,colaborador")
    
    # Proteger colaborador se for produtor de eventos
    eventos_produzidos = db.relationship('Evento', backref='produtor', foreign_keys='Evento.id_produtor')
    
    @property
    def tem_categoria_produtor(self):
        return any(cat.nome.lower() == 'produtor' for cat in self.categorias)
    
    @property
    def categoria_nomes(self):
        """Retorna uma lista com os nomes das categorias do colaborador"""
        return [cat.nome for cat in self.categorias]

class Elenco(db.Model):
    __tablename__ = 'elenco'
    id_elenco = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    cpf = db.Column(db.String)
    endereco = db.Column(db.String)
    cidade = db.Column(db.String)
    estado = db.Column(db.String)
    telefone = db.Column(db.String)
    email = db.Column(db.String)
    observacoes = db.Column(db.String)

class CategoriaFornecedor(db.Model):
    __tablename__ = 'categoria_fornecedor'
    id_categoria_fornecedor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    
    # Proteger categoria se tiver fornecedores usando
    fornecedores = db.relationship('Fornecedor', backref='categoria')

class Fornecedor(db.Model):
    __tablename__ = 'fornecedor'
    id_fornecedor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    telefone = db.Column(db.String)
    cidade = db.Column(db.String)
    estado = db.Column(db.String)
    id_categoria_fornecedor = db.Column(db.Integer, db.ForeignKey('categoria_fornecedor.id_categoria_fornecedor'))

class CategoriaReceita(db.Model):
    __tablename__ = 'categoria_receita'
    id_categoria_receita = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    
    # Proteger categoria se tiver receitas usando
    receitas = db.relationship('Receita', backref='categoria')

class Receita(db.Model):
    __tablename__ = 'receita'
    id_receita = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    id_categoria_receita = db.Column(db.Integer, db.ForeignKey('categoria_receita.id_categoria_receita'))
    
    # Proteger receita se tiver eventos usando
    receita_eventos = db.relationship('ReceitaEvento', back_populates='receita')

class CategoriaDespesa(db.Model):
    __tablename__ = 'categoria_despesa'
    id_categoria_despesa = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    
    # Proteger categoria se tiver despesas usando
    despesas = db.relationship('Despesa', backref='categoria')

class Despesa(db.Model):
    __tablename__ = 'despesa'
    id_despesa = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    id_categoria_despesa = db.Column(db.Integer, db.ForeignKey('categoria_despesa.id_categoria_despesa'))
    id_tipo_despesa = db.Column(db.Integer, nullable=False, default=1)  # 1=Fixas-Evento, 2=Variáveis-Evento, 3=Fixas-SócratesOnline, 4=Variáveis-SócratesOnline
    valor_medio_despesa = db.Column(db.Numeric(10, 2))
    flag_alimentacao = db.Column(db.Boolean, nullable=False, default=False)
    flag_combustivel = db.Column(db.Boolean, nullable=False, default=False)
    
    # Proteger despesa se tiver eventos usando
    despesa_eventos = db.relationship('DespesaEvento', back_populates='despesa')
    
    @property
    def tipo_nome(self):
        """Retorna o nome do tipo da despesa"""
        return TIPOS_DESPESA.get(self.id_tipo_despesa, 'Tipo não definido')
    
    @property
    def eh_tipo_evento(self):
        """Verifica se a despesa é do tipo evento (1 ou 2)"""
        return self.id_tipo_despesa in [1, 2]

class Evento(db.Model):
    __tablename__ = 'evento'
    id_evento = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)
    cidade = db.Column(db.String)
    estado = db.Column(db.String)
    endereco = db.Column(db.String)
    id_circo = db.Column(db.Integer, db.ForeignKey('circo.id_circo'))
    id_produtor = db.Column(db.Integer, db.ForeignKey('colaborador.id_colaborador'))
    status = db.Column(db.String, default='planejamento')
    observacoes = db.Column(db.String)

    # CASCADE DELETE para tabelas dependentes quando evento é deletado
    despesas_evento = db.relationship('DespesaEvento', back_populates='evento', cascade='all, delete-orphan')
    receitas_evento = db.relationship('ReceitaEvento', back_populates='evento', cascade='all, delete-orphan')
    equipes_evento = db.relationship('EquipeEvento', backref='evento_equipe', cascade='all, delete-orphan')
    elencos_evento = db.relationship('ElencoEvento', backref='evento_elenco', cascade='all, delete-orphan')
    fornecedores_evento = db.relationship('FornecedorEvento', backref='evento_fornecedor', cascade='all, delete-orphan')
    veiculos_evento = db.relationship('VeiculoEvento', backref='evento_veiculo', cascade='all, delete-orphan')

class DespesaEvento(db.Model):
    __tablename__ = 'despesas_evento'
    id_despesa_evento = db.Column(db.Integer, primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id_evento'), nullable=False)
    id_despesa = db.Column(db.Integer, db.ForeignKey('despesa.id_despesa'), nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    data_pagamento = db.Column(db.Date, nullable=True)
    valor = db.Column(db.Float, nullable=False)
    id_fornecedor = db.Column(db.Integer, db.ForeignKey('fornecedor.id_fornecedor'))
    status_pagamento = db.Column(db.String(20), nullable=False)
    forma_pagamento = db.Column(db.String(20), nullable=False)
    pago_por = db.Column(db.String(100))
    observacoes = db.Column(db.Text)
    despesa_cabeca = db.Column(db.Boolean, default=False, nullable=False)
    comprovante = db.Column(db.String(255))
    qtd_dias = db.Column(db.Integer, nullable=True)
    qtd_pessoas = db.Column(db.Integer, nullable=True)
    evento = db.relationship('Evento', back_populates='despesas_evento')
    despesa = db.relationship('Despesa', back_populates='despesa_eventos')
    fornecedor = db.relationship('Fornecedor', backref='despesas_evento')

class ReceitaEvento(db.Model):
    __tablename__ = 'receitas_evento'
    id_receita_evento = db.Column(db.Integer, primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id_evento'), nullable=False)
    id_receita = db.Column(db.Integer, db.ForeignKey('receita.id_receita'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    observacoes = db.Column(db.Text)
    evento = db.relationship('Evento', back_populates='receitas_evento')
    receita = db.relationship('Receita', back_populates='receita_eventos')

class CategoriaVeiculo(db.Model):
    __tablename__ = 'categoria_veiculo'
    id_categoria_veiculo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    
    # Proteger categoria se tiver veículos usando
    veiculos = db.relationship('Veiculo', backref='categoria')

class Veiculo(db.Model):
    __tablename__ = 'veiculo'
    id_veiculo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    modelo = db.Column(db.String)
    marca = db.Column(db.String)
    ano = db.Column(db.Integer)
    placa = db.Column(db.String)
    cor = db.Column(db.String)
    combustivel = db.Column(db.String)
    capacidade_passageiros = db.Column(db.Integer)
    media_km_litro = db.Column(db.Float)
    observacoes = db.Column(db.String)
    id_categoria_veiculo = db.Column(db.Integer, db.ForeignKey('categoria_veiculo.id_categoria_veiculo'))

class EquipeEvento(db.Model):
    __tablename__ = 'equipe_evento'
    id_equipe_evento = db.Column(db.Integer, primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id_evento'), nullable=False)
    id_colaborador = db.Column(db.Integer, db.ForeignKey('colaborador.id_colaborador'), nullable=False)
    funcao = db.Column(db.String, nullable=True)
    observacoes = db.Column(db.String)
    
    # Relacionamentos
    colaborador = db.relationship('Colaborador', backref='equipe_eventos')

class ElencoEvento(db.Model):
    __tablename__ = 'elenco_evento'
    id_elenco_evento = db.Column(db.Integer, primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id_evento'), nullable=False)
    id_elenco = db.Column(db.Integer, db.ForeignKey('elenco.id_elenco'), nullable=False)
    observacoes = db.Column(db.String)
    
    # Relacionamentos
    elenco = db.relationship('Elenco', backref='elenco_eventos')

class FornecedorEvento(db.Model):
    __tablename__ = 'fornecedor_evento'
    id_fornecedor_evento = db.Column(db.Integer, primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id_evento'), nullable=False)
    id_fornecedor = db.Column(db.Integer, db.ForeignKey('fornecedor.id_fornecedor'), nullable=False)
    observacoes = db.Column(db.String)
    
    # Relacionamentos
    fornecedor = db.relationship('Fornecedor', backref='fornecedor_eventos')

class DespesaEmpresa(db.Model):
    __tablename__ = 'despesas_empresa'
    id_despesa_empresa = db.Column(db.Integer, primary_key=True)
    id_despesa = db.Column(db.Integer, db.ForeignKey('despesa.id_despesa'), nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    data_pagamento = db.Column(db.Date, nullable=True)
    valor = db.Column(db.Float, nullable=False)
    id_fornecedor = db.Column(db.Integer, db.ForeignKey('fornecedor.id_fornecedor'))
    status_pagamento = db.Column(db.String(20), nullable=False)
    forma_pagamento = db.Column(db.String(20), nullable=False)
    pago_por = db.Column(db.String(100))
    observacoes = db.Column(db.Text)
    comprovante = db.Column(db.String(255))
    qtd_dias = db.Column(db.Integer, nullable=True)
    qtd_pessoas = db.Column(db.Integer, nullable=True)
    
    # Relacionamentos
    despesa = db.relationship('Despesa', backref='despesas_empresa')
    fornecedor = db.relationship('Fornecedor', backref='despesas_empresa')

class ReceitaEmpresa(db.Model):
    __tablename__ = 'receitas_empresa'
    id_receita_empresa = db.Column(db.Integer, primary_key=True)
    id_receita = db.Column(db.Integer, db.ForeignKey('receita.id_receita'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    observacoes = db.Column(db.Text)
    
    # Relacionamentos
    receita = db.relationship('Receita', backref='receitas_empresa')

class VeiculoEvento(db.Model):
    __tablename__ = 'veiculos_evento'
    id_veiculo_evento = db.Column(db.Integer, primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id_evento'), nullable=False)
    id_veiculo = db.Column(db.Integer, db.ForeignKey('veiculo.id_veiculo'), nullable=False)
    id_motorista = db.Column(db.Integer, db.ForeignKey('colaborador.id_colaborador'), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_devolucao = db.Column(db.Date, nullable=True)
    hora_inicio = db.Column(db.Time, nullable=True)
    hora_fim = db.Column(db.Time, nullable=True)
    km_inicio = db.Column(db.Integer, nullable=True)
    km_fim = db.Column(db.Integer, nullable=True)
    observacoes = db.Column(db.String)
    
    # Relacionamentos
    veiculo = db.relationship('Veiculo', backref='veiculo_eventos')
    motorista = db.relationship('Colaborador', backref='motorista_eventos')
    evento = db.relationship('Evento', backref='evento_veiculos')

class Parametro(db.Model):
    __tablename__ = 'parametro'
    id = db.Column(db.Integer, primary_key=True)
    parametro = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.String(100))
    observacoes = db.Column(db.Text)

class Escola(db.Model):
    __tablename__ = 'escola'
    id_escola = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    endereco = db.Column(db.String(300), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    email = db.Column(db.String(200), nullable=True)
    whatsapp = db.Column(db.String(20), nullable=True)
    nome_contato = db.Column(db.String(100), nullable=False)
    cargo_contato = db.Column(db.String(100), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    
    # Relacionamentos
    visitas = db.relationship('VisitaEscola', back_populates='escola', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Escola {self.nome}>'

class VisitaEscola(db.Model):
    __tablename__ = 'visita_escola'
    id_visita = db.Column(db.Integer, primary_key=True)
    id_escola = db.Column(db.Integer, db.ForeignKey('escola.id_escola'), nullable=False)
    data_visita = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_promotor = db.Column(db.Integer, db.ForeignKey('colaborador.id_colaborador'), nullable=False)
    email_enviado = db.Column(db.Boolean, default=False, nullable=False)
    whatsapp_enviado = db.Column(db.Boolean, default=False, nullable=False)
    data_email_enviado = db.Column(db.DateTime, nullable=True)
    data_whatsapp_enviado = db.Column(db.DateTime, nullable=True)
    observacoes_visita = db.Column(db.Text, nullable=True)
    status_visita = db.Column(db.String(50), default='agendada', nullable=False)  # agendada, realizada, cancelada
    
    # Relacionamentos
    escola = db.relationship('Escola', back_populates='visitas')
    promotor = db.relationship('Colaborador', backref='visitas_escolas')
    
    def __repr__(self):
        return f'<VisitaEscola {self.escola.nome} - {self.data_visita}>'

class LogSistema(db.Model):
    __tablename__ = 'log_sistema'
    id_log = db.Column(db.Integer, primary_key=True)
    acao = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relacionamento com usuário
    usuario = db.relationship('Usuario', backref='logs_sistema')
    
    def __repr__(self):
        return f'<LogSistema {self.acao} - {self.usuario.nome} - {self.data_hora}>'
