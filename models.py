from extensions import db

class CategoriaUsuario(db.Model):
    __tablename__ = 'categoria_usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    senha_hash = db.Column(db.String(200), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria_usuario.id'))
    categoria = db.relationship('CategoriaUsuario')

class Circo(db.Model):
    __tablename__ = 'circo'
    id_circo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    contato_responsavel = db.Column(db.String)
    observacoes = db.Column(db.String)

class CategoriaColaborador(db.Model):
    __tablename__ = 'categoria_colaborador'
    id_categoria_colaborador = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)

class Colaborador(db.Model):
    __tablename__ = 'colaborador'
    id_colaborador = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    id_categoria_colaborador = db.Column(db.Integer, db.ForeignKey('categoria_colaborador.id_categoria_colaborador'))
    categoria = db.relationship('CategoriaColaborador')

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

class Fornecedor(db.Model):
    __tablename__ = 'fornecedor'
    id_fornecedor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    telefone = db.Column(db.String)
    id_categoria_fornecedor = db.Column(db.Integer, db.ForeignKey('categoria_fornecedor.id_categoria_fornecedor'))
    categoria = db.relationship('CategoriaFornecedor')

class CategoriaReceita(db.Model):
    __tablename__ = 'categoria_receita'
    id_categoria_receita = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)

class Receita(db.Model):
    __tablename__ = 'receita'
    id_receita = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    id_categoria_receita = db.Column(db.Integer, db.ForeignKey('categoria_receita.id_categoria_receita'))
    categoria = db.relationship('CategoriaReceita')

class CategoriaDespesa(db.Model):
    __tablename__ = 'categoria_despesa'
    id_categoria_despesa = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)

class Despesa(db.Model):
    __tablename__ = 'despesa'
    id_despesa = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    id_categoria_despesa = db.Column(db.Integer, db.ForeignKey('categoria_despesa.id_categoria_despesa'))
    categoria = db.relationship('CategoriaDespesa')

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
    status = db.Column(db.String)
    observacoes = db.Column(db.String)
    circo = db.relationship('Circo')
    produtor = db.relationship('Colaborador')


class DespesaEvento(db.Model):
    __tablename__ = 'despesa_evento'
    id_despesa_evento = db.Column(db.Integer, primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id_evento'))
    id_despesa = db.Column(db.Integer, db.ForeignKey('despesa.id_despesa'))
    data = db.Column(db.Date)
    valor = db.Column(db.Numeric(10, 2))
    status_pagamento = db.Column(db.String)
    forma_pagamento = db.Column(db.String)
    pago_por = db.Column(db.String)
    observacoes = db.Column(db.String)

    evento = db.relationship('Evento')
    despesa = db.relationship('Despesa')


class ReceitaEvento(db.Model):
    __tablename__ = 'receita_evento'
    id_receita_evento = db.Column(db.Integer, primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id_evento'))
    id_receita = db.Column(db.Integer, db.ForeignKey('receita.id_receita'))
    valor = db.Column(db.Numeric(10, 2))
    observacoes = db.Column(db.String)

    evento = db.relationship('Evento')
    receita = db.relationship('Receita')


class ElencoEvento(db.Model):
    __tablename__ = 'elenco_evento'
    id_elenco_evento = db.Column(db.Integer, primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id_evento'))
    id_elenco = db.Column(db.Integer, db.ForeignKey('elenco.id_elenco'))
    observacoes = db.Column(db.String)

    evento = db.relationship('Evento')
    elenco = db.relationship('Elenco')


class EquipeEvento(db.Model):
    __tablename__ = 'equipe_evento'
    id_equipe_evento = db.Column(db.Integer, primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id_evento'))
    id_colaborador = db.Column(db.Integer, db.ForeignKey('colaborador.id_colaborador'))
    observacoes = db.Column(db.String)

    evento = db.relationship('Evento')
    colaborador = db.relationship('Colaborador')


class FornecedorEvento(db.Model):
    __tablename__ = 'fornecedor_evento'
    id_fornecedor_evento = db.Column(db.Integer, primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id_evento'))
    id_fornecedor = db.Column(db.Integer, db.ForeignKey('fornecedor.id_fornecedor'))
    observacoes = db.Column(db.String)

    evento = db.relationship('Evento')
    fornecedor = db.relationship('Fornecedor')
