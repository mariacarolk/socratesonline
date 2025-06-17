from datetime import date, timedelta, datetime
import os
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, send_from_directory
from models import (
    Usuario, Circo, CategoriaColaborador, Colaborador, ColaboradorCategoria,
    Elenco, CategoriaFornecedor, Fornecedor, CategoriaReceita, Receita,
    CategoriaDespesa, Despesa, Evento, DespesaEvento, ReceitaEvento,
    CategoriaVeiculo, Veiculo, EquipeEvento, ElencoEvento, FornecedorEvento, TIPOS_DESPESA
)
from forms import (
    UsuarioForm, RegisterForm, LoginForm, CircoForm, CategoriaColaboradorForm, ColaboradorForm,
    ElencoForm, CategoriaFornecedorForm, FornecedorForm, CategoriaReceitaForm, ReceitaForm,
    CategoriaDespesaForm, DespesaForm, EventoForm, CategoriaVeiculoForm, VeiculoForm,
    EquipeEventoForm, ElencoEventoForm, FornecedorEventoForm, DespesaEventoForm
)
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from extensions import db, login_manager
from sqlalchemy import func
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, login_required, logout_user, current_user

load_dotenv()  # Carrega variÃ¡veis do .env

app = Flask(__name__)
env = os.getenv("FLASK_ENV", "development")
if env == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

# ConfiguraÃ§Ãµes
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# InicializaÃ§Ã£o das extensÃµes
db.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db)

# User loader para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Obter informaÃ§Ãµes do usuÃ¡rio logado
    usuario = Usuario.query.get(session['user_id'])
    if not usuario or not usuario.colaborador:
        flash('Erro ao carregar informaÃ§Ãµes do usuÃ¡rio.', 'danger')
        return redirect(url_for('login'))
    
    # Verificar se Ã© administrador ou produtor
    is_admin = any(cat.nome.lower() == 'administrativo' for cat in usuario.colaborador.categorias)
    is_produtor = any(cat.nome.lower() == 'produtor' for cat in usuario.colaborador.categorias)

    # Filtro de datas do grÃ¡fico
    period = request.args.get('period', '7dias')
    if period == 'hoje':
        data_inicio = data_fim = date.today()
    elif period == 'ontem':
        data_inicio = data_fim = date.today() - timedelta(days=1)
    elif period == '7dias':
        data_fim = date.today()
        data_inicio = data_fim - timedelta(days=6)
    elif period == 'mes':
        data_fim = date.today()
        data_inicio = data_fim.replace(day=1)
    elif period == 'custom':
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        if data_inicio and data_fim:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        else:
            data_fim = date.today()
            data_inicio = data_fim - timedelta(days=6)
    else:
        data_fim = date.today()
        data_inicio = data_fim - timedelta(days=6)

    # Filtro de eventos baseado no tipo de usuÃ¡rio
    if is_admin:
        # Administrador vÃª todos os eventos
        eventos_base_query = db.session.query(ReceitaEvento.data, 
                                            func.sum(ReceitaEvento.valor).label('receitas'),
                                            func.sum(DespesaEvento.valor).label('despesas'))\
                           .outerjoin(DespesaEvento, ReceitaEvento.data == DespesaEvento.data)
    else:
        # Produtor vÃª apenas seus eventos
        eventos_do_produtor = db.session.query(Evento.id_evento)\
                             .filter_by(id_produtor=usuario.colaborador.id_colaborador)\
                             .subquery()
        
        eventos_base_query = db.session.query(ReceitaEvento.data,
                                            func.sum(ReceitaEvento.valor).label('receitas'),
                                            func.sum(DespesaEvento.valor).label('despesas'))\
                           .filter(ReceitaEvento.id_evento.in_(eventos_do_produtor))\
                           .outerjoin(DespesaEvento, 
                                    db.and_(DespesaEvento.data == ReceitaEvento.data,
                                          DespesaEvento.id_evento.in_(eventos_do_produtor)))

    # Lucro por dia no perÃ­odo
    lucro_por_dia = []
    dias = []
    current = data_inicio
    while current <= data_fim:
        if is_admin:
            receitas = db.session.query(func.sum(ReceitaEvento.valor)).filter(ReceitaEvento.data == current).scalar() or 0
            despesas = db.session.query(func.sum(DespesaEvento.valor)).filter(DespesaEvento.data == current).scalar() or 0
        else:
            # Filtrar por eventos do produtor
            eventos_do_produtor = db.session.query(Evento.id_evento)\
                                 .filter_by(id_produtor=usuario.colaborador.id_colaborador)
            
            receitas = db.session.query(func.sum(ReceitaEvento.valor))\
                      .filter(ReceitaEvento.data == current,
                             ReceitaEvento.id_evento.in_(eventos_do_produtor)).scalar() or 0
            
            despesas = db.session.query(func.sum(DespesaEvento.valor))\
                      .filter(DespesaEvento.data == current,
                             DespesaEvento.id_evento.in_(eventos_do_produtor)).scalar() or 0
        
        lucro = receitas - despesas
        lucro_por_dia.append(lucro)
        dias.append(current.strftime('%d/%m'))
        current += timedelta(days=1)

    # Filtro de datas da lista de eventos do dashboard
    eventos_period = request.args.get('eventos_period', '7dias')
    if eventos_period == 'hoje':
        eventos_data_inicio = eventos_data_fim = date.today()
    elif eventos_period == 'ontem':
        eventos_data_inicio = eventos_data_fim = date.today() - timedelta(days=1)
    elif eventos_period == '7dias':
        eventos_data_fim = date.today()
        eventos_data_inicio = eventos_data_fim - timedelta(days=6)
    elif eventos_period == 'mes':
        eventos_data_fim = date.today()
        eventos_data_inicio = eventos_data_fim.replace(day=1)
    elif eventos_period == 'custom':
        eventos_data_inicio = request.args.get('eventos_data_inicio')
        eventos_data_fim = request.args.get('eventos_data_fim')
        if eventos_data_inicio and eventos_data_fim:
            eventos_data_inicio = datetime.strptime(eventos_data_inicio, '%Y-%m-%d').date()
            eventos_data_fim = datetime.strptime(eventos_data_fim, '%Y-%m-%d').date()
        else:
            eventos_data_fim = date.today()
            eventos_data_inicio = eventos_data_fim - timedelta(days=6)
    else:
        eventos_data_fim = date.today()
        eventos_data_inicio = eventos_data_fim - timedelta(days=6)

    # Filtrar eventos baseado no tipo de usuÃ¡rio
    eventos_query = Evento.query.filter(Evento.status.in_(['planejamento', 'a realizar', 'em andamento', 'realizado']))
    
    if not is_admin:
        # Produtores veem apenas seus eventos
        eventos_query = eventos_query.filter_by(id_produtor=usuario.colaborador.id_colaborador)
    
    if eventos_data_inicio:
        eventos_query = eventos_query.filter(Evento.data_inicio >= eventos_data_inicio)
    if eventos_data_fim:
        eventos_query = eventos_query.filter(Evento.data_inicio <= eventos_data_fim)
    
    eventos = eventos_query.order_by(Evento.data_inicio.desc()).all()

    return render_template(
        'dashboard.html',
        lucro_por_dia=lucro_por_dia,
        dias=dias,
        data_inicio=data_inicio.strftime('%Y-%m-%d'),
        data_fim=data_fim.strftime('%Y-%m-%d'),
        period=period,
        eventos=eventos,
        eventos_data_inicio=eventos_data_inicio,
        eventos_data_fim=eventos_data_fim,
        eventos_period=eventos_period,
        is_admin=is_admin,
        is_produtor=is_produtor,
        usuario=usuario
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and check_password_hash(usuario.senha_hash, form.password.data):
            session['user_id'] = usuario.id
            # Usar a primeira categoria do colaborador para compatibilidade
            if usuario.colaborador and usuario.colaborador.categorias:
                session['categoria'] = usuario.colaborador.categorias[0].nome.lower()
            else:
                session['categoria'] = 'administrativo'  # padrÃ£o
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('categoria', None)
    return redirect(url_for('login'))

@app.route('/cadastros/circos', methods=['GET', 'POST'])
def cadastrar_circo():
    form = CircoForm()
    if form.validate_on_submit():
        novo = Circo(
            nome=form.nome.data,
            contato_responsavel=form.contato_responsavel.data,
            telefone_contato=form.telefone_contato.data,
            observacoes=form.observacoes.data
        )
        db.session.add(novo)
        db.session.commit()
        flash('Circo cadastrado com sucesso!', 'success')
        return redirect(url_for('cadastrar_circo'))
    circos = Circo.query.all()
    return render_template('cadastrar_circo.html', form=form, circos=circos)

@app.route('/cadastros/circos/editar/<int:id>', methods=['GET', 'POST'])
def editar_circo(id):
    circo = Circo.query.get_or_404(id)
    form = CircoForm(obj=circo)
    if form.validate_on_submit():
        circo.nome = form.nome.data
        circo.contato_responsavel = form.contato_responsavel.data
        circo.telefone_contato = form.telefone_contato.data
        circo.observacoes = form.observacoes.data
        db.session.commit()
        flash('Circo atualizado com sucesso!', 'success')
        return redirect(url_for('cadastrar_circo'))
    circos = Circo.query.all()
    return render_template('cadastrar_circo.html', form=form, circos=circos)

@app.route('/cadastros/circos/excluir/<int:id>')
def excluir_circo(id):
    circo = Circo.query.get_or_404(id)
    
    # Verificar se existem eventos usando este circo
    eventos_usando = Evento.query.filter_by(id_circo=id).count()
    if eventos_usando > 0:
        flash(f'NÃ£o Ã© possÃ­vel excluir este circo pois existem {eventos_usando} evento(s) associado(s) a ele.', 'danger')
        return redirect(url_for('cadastrar_circo'))
    
    db.session.delete(circo)
    db.session.commit()
    flash('Circo excluÃ­do com sucesso!', 'success')
    return redirect(url_for('cadastrar_circo'))

@app.route('/cadastros/categorias-colaborador', methods=['GET', 'POST'])
def cadastrar_categoria_colaborador():
    form = CategoriaColaboradorForm()
    if form.validate_on_submit():
        nova = CategoriaColaborador(nome=form.nome.data)
        db.session.add(nova)
        db.session.commit()
        flash('Categoria cadastrada com sucesso!', 'success')
        return redirect(url_for('cadastrar_categoria_colaborador'))
    categorias = CategoriaColaborador.query.all()
    return render_template('categorias_colaborador.html', form=form, categorias=categorias)

@app.route('/cadastros/colaboradores', methods=['GET', 'POST'])
def cadastrar_colaborador():
    # Verificar se existem categorias
    categorias_existentes = CategoriaColaborador.query.all()
    if not categorias_existentes:
        flash('Ã‰ necessÃ¡rio cadastrar pelo menos uma categoria de colaborador antes de cadastrar colaboradores.', 'warning')
        return redirect(url_for('cadastrar_categoria_colaborador'))
    
    form = ColaboradorForm()
    form.categorias.choices = [(c.id_categoria_colaborador, c.nome) for c in categorias_existentes]
    if form.validate_on_submit():
        novo = Colaborador(nome=form.nome.data)
        db.session.add(novo)
        db.session.flush()  # Para obter o ID do colaborador
        
        # Adicionar as categorias selecionadas
        for categoria_id in form.categorias.data:
            nova_associacao = ColaboradorCategoria(
                id_colaborador=novo.id_colaborador,
                id_categoria_colaborador=categoria_id
            )
            db.session.add(nova_associacao)
        
        db.session.commit()
        flash('Colaborador cadastrado com sucesso!', 'success')
        return redirect(url_for('cadastrar_colaborador'))
    colaboradores = Colaborador.query.all()
    return render_template('colaboradores.html', form=form, colaboradores=colaboradores)

@app.route('/cadastros/categorias-colaborador/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria_colaborador(id):
    categoria = CategoriaColaborador.query.get_or_404(id)
    form = CategoriaColaboradorForm(obj=categoria)
    if form.validate_on_submit():
        categoria.nome = form.nome.data
        db.session.commit()
        flash('Categoria atualizada com sucesso!', 'success')
        return redirect(url_for('cadastrar_categoria_colaborador'))
    categorias = CategoriaColaborador.query.all()
    return render_template('categorias_colaborador.html', form=form, categorias=categorias)

@app.route('/cadastros/categorias-colaborador/excluir/<int:id>')
def excluir_categoria_colaborador(id):
    categoria = CategoriaColaborador.query.get_or_404(id)
    
    # Verificar se existem colaboradores usando esta categoria
    colaboradores_usando = ColaboradorCategoria.query.filter_by(id_categoria_colaborador=id).count()
    if colaboradores_usando > 0:
        flash(f'NÃ£o Ã© possÃ­vel excluir esta categoria pois existem {colaboradores_usando} colaborador(es) associado(s) a ela.', 'danger')
        return redirect(url_for('cadastrar_categoria_colaborador'))
    
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoria excluÃ­da com sucesso!', 'success')
    return redirect(url_for('cadastrar_categoria_colaborador'))

@app.route('/cadastros/colaboradores/editar/<int:id>', methods=['GET', 'POST'])
def editar_colaborador(id):
    # Verificar se existem categorias
    categorias_existentes = CategoriaColaborador.query.all()
    if not categorias_existentes:
        flash('Ã‰ necessÃ¡rio cadastrar pelo menos uma categoria de colaborador antes de editar colaboradores.', 'warning')
        return redirect(url_for('cadastrar_categoria_colaborador'))
    
    colaborador = Colaborador.query.get_or_404(id)
    form = ColaboradorForm()
    
    # Configurar as choices sempre, antes de qualquer validaÃ§Ã£o
    form.categorias.choices = [(c.id_categoria_colaborador, c.nome) for c in categorias_existentes]
    
    # Se for GET, preencher com os dados atuais do colaborador
    if request.method == 'GET':
        form.nome.data = colaborador.nome
        # PrÃ©-selecionar as categorias atuais do colaborador
        categorias_atuais = [assoc.id_categoria_colaborador for assoc in colaborador.categorias_associacao]
        form.categorias.data = categorias_atuais
    
    if form.validate_on_submit():
        colaborador.nome = form.nome.data
        
        # Obter categorias selecionadas do formulÃ¡rio
        categorias_selecionadas = form.categorias.data
        
        # Se o campo do formulÃ¡rio estiver vazio, tentar pegar do request.form
        if not categorias_selecionadas:
            categorias_selecionadas = request.form.getlist('categorias')
            categorias_selecionadas = [int(cat_id) for cat_id in categorias_selecionadas if cat_id.isdigit()]
        
        # Debug: Mostrar que categorias foram selecionadas
        print(f"Categorias selecionadas: {categorias_selecionadas}")
        
        if not categorias_selecionadas:
            flash('Ã‰ necessÃ¡rio selecionar pelo menos uma categoria.', 'danger')
            colaboradores = Colaborador.query.all()
            return render_template('colaboradores.html', form=form, colaboradores=colaboradores)
        
        try:
            # Remover todas as associaÃ§Ãµes existentes
            ColaboradorCategoria.query.filter_by(id_colaborador=colaborador.id_colaborador).delete()
            
            # Adicionar as novas categorias selecionadas
            for categoria_id in categorias_selecionadas:
                nova_associacao = ColaboradorCategoria(
                    id_colaborador=colaborador.id_colaborador,
                    id_categoria_colaborador=categoria_id
                )
                db.session.add(nova_associacao)
            
            db.session.commit()
            flash('Colaborador atualizado com sucesso!', 'success')
            return redirect(url_for('cadastrar_colaborador'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar colaborador: {e}")
            flash(f'Erro ao atualizar colaborador: {str(e)}', 'danger')
    else:
        # Debug: Mostrar erros de validaÃ§Ã£o
        if form.errors:
            print(f"Erros de validaÃ§Ã£o: {form.errors}")
    
    colaboradores = Colaborador.query.all()
    return render_template('colaboradores.html', form=form, colaboradores=colaboradores)

@app.route('/cadastros/colaboradores/excluir/<int:id>')
def excluir_colaborador(id):
    colaborador = Colaborador.query.get_or_404(id)
    
    # Verificar se Ã© produtor de eventos
    eventos_produzindo = Evento.query.filter_by(id_produtor=id).count()
    if eventos_produzindo > 0:
        flash(f'NÃ£o Ã© possÃ­vel excluir este colaborador pois ele Ã© produtor de {eventos_produzindo} evento(s).', 'danger')
        return redirect(url_for('cadastrar_colaborador'))
    
    # Verificar se tem usuÃ¡rio associado
    usuario_associado = Usuario.query.filter_by(id_colaborador=id).first()
    if usuario_associado:
        flash(f'NÃ£o Ã© possÃ­vel excluir este colaborador pois ele possui um usuÃ¡rio associado. Exclua o usuÃ¡rio primeiro.', 'danger')
        return redirect(url_for('cadastrar_colaborador'))
    
    db.session.delete(colaborador)
    db.session.commit()
    flash('Colaborador excluÃ­do com sucesso!', 'success')
    return redirect(url_for('cadastrar_colaborador'))

@app.route('/colaboradores/<int:id>/criar-usuario', methods=['GET', 'POST'])
def criar_usuario(id):
    if session.get('categoria', '').lower() != 'administrativo':
        flash('Apenas administradores podem criar usuÃ¡rios.', 'danger')
        return redirect(url_for('cadastrar_colaborador'))
    
    colaborador = Colaborador.query.get_or_404(id)
    
    # Verificar se jÃ¡ existe usuÃ¡rio para este colaborador
    usuario_existente = Usuario.query.filter_by(id_colaborador=id).first()
    if usuario_existente:
        flash(f'JÃ¡ existe um usuÃ¡rio para o colaborador {colaborador.nome}.', 'warning')
        return redirect(url_for('cadastrar_colaborador'))
    
    form = UsuarioForm()
    
    # PrÃ©-preencher o nome com o nome do colaborador
    if request.method == 'GET':
        form.nome.data = colaborador.nome
    
    if form.validate_on_submit():
        # Verificar se email jÃ¡ existe
        email_existente = Usuario.query.filter_by(email=form.email.data).first()
        if email_existente:
            flash('Este email jÃ¡ estÃ¡ sendo usado por outro usuÃ¡rio.', 'danger')
            return render_template('criar_usuario.html', form=form, colaborador=colaborador)
        
        # Criar usuÃ¡rio
        hashed_password = generate_password_hash(form.password.data)
        novo_usuario = Usuario(
            nome=form.nome.data,
            email=form.email.data,
            senha_hash=hashed_password,
            id_colaborador=colaborador.id_colaborador
        )
        
        db.session.add(novo_usuario)
        db.session.commit()
        flash(f'UsuÃ¡rio criado com sucesso para o colaborador {colaborador.nome}!', 'success')
        return redirect(url_for('cadastrar_colaborador'))
    
    return render_template('criar_usuario.html', form=form, colaborador=colaborador)

@app.route('/colaboradores/<int:id>/editar-usuario', methods=['GET', 'POST'])
def editar_usuario(id):
    if session.get('categoria', '').lower() != 'administrativo':
        flash('Apenas administradores podem editar usuÃ¡rios.', 'danger')
        return redirect(url_for('cadastrar_colaborador'))
    
    colaborador = Colaborador.query.get_or_404(id)
    usuario = Usuario.query.filter_by(id_colaborador=id).first()
    
    if not usuario:
        flash(f'NÃ£o existe usuÃ¡rio para o colaborador {colaborador.nome}.', 'warning')
        return redirect(url_for('cadastrar_colaborador'))
    
    form = UsuarioForm(obj=usuario, is_edit=True)
    
    if form.validate_on_submit():
        # Verificar se email jÃ¡ existe (exceto o prÃ³prio usuÃ¡rio)
        email_existente = Usuario.query.filter(Usuario.email == form.email.data, Usuario.id != usuario.id).first()
        if email_existente:
            flash('Este email jÃ¡ estÃ¡ sendo usado por outro usuÃ¡rio.', 'danger')
            return render_template('editar_usuario.html', form=form, colaborador=colaborador, usuario=usuario)
        
        # Atualizar usuÃ¡rio
        usuario.nome = form.nome.data
        usuario.email = form.email.data
        if form.password.data:  # SÃ³ atualiza senha se foi preenchida
            usuario.senha_hash = generate_password_hash(form.password.data)
        
        db.session.commit()
        flash(f'UsuÃ¡rio do colaborador {colaborador.nome} atualizado com sucesso!', 'success')
        return redirect(url_for('cadastrar_colaborador'))
    
    return render_template('editar_usuario.html', form=form, colaborador=colaborador, usuario=usuario)

@app.route('/colaboradores/<int:id>/excluir-usuario')
def excluir_usuario(id):
    if session.get('categoria', '').lower() != 'administrativo':
        flash('Apenas administradores podem excluir usuÃ¡rios.', 'danger')
        return redirect(url_for('cadastrar_colaborador'))
    
    colaborador = Colaborador.query.get_or_404(id)
    usuario = Usuario.query.filter_by(id_colaborador=id).first()
    
    if not usuario:
        flash(f'NÃ£o existe usuÃ¡rio para o colaborador {colaborador.nome}.', 'warning')
        return redirect(url_for('cadastrar_colaborador'))
    
    db.session.delete(usuario)
    db.session.commit()
    flash(f'UsuÃ¡rio do colaborador {colaborador.nome} excluÃ­do com sucesso!', 'success')
    return redirect(url_for('cadastrar_colaborador'))

@app.route('/cadastros/elenco', methods=['GET', 'POST'])
def cadastrar_elenco():
    form = ElencoForm()
    if form.validate_on_submit():
        novo = Elenco(
            nome=form.nome.data,
            cpf=form.cpf.data,
            endereco=form.endereco.data,
            cidade=form.cidade.data,
            estado=form.estado.data,
            telefone=form.telefone.data,
            email=form.email.data,
            observacoes=form.observacoes.data
        )
        db.session.add(novo)
        db.session.commit()
        flash('Integrante do elenco cadastrado com sucesso!', 'success')
        return redirect(url_for('cadastrar_elenco'))
    elenco = Elenco.query.all()
    return render_template('elenco.html', form=form, elenco=elenco)

@app.route('/cadastros/elenco/editar/<int:id>', methods=['GET', 'POST'])
def editar_elenco(id):
    integrante = Elenco.query.get_or_404(id)
    form = ElencoForm(obj=integrante)
    if form.validate_on_submit():
        integrante.nome = form.nome.data
        integrante.cpf = form.cpf.data
        integrante.endereco = form.endereco.data
        integrante.cidade = form.cidade.data
        integrante.estado = form.estado.data
        integrante.telefone = form.telefone.data
        integrante.email = form.email.data
        integrante.observacoes = form.observacoes.data
        db.session.commit()
        flash('Integrante atualizado com sucesso!', 'success')
        return redirect(url_for('cadastrar_elenco'))
    elenco = Elenco.query.all()
    return render_template('elenco.html', form=form, elenco=elenco)

@app.route('/cadastros/elenco/excluir/<int:id>')
def excluir_elenco(id):
    integrante = Elenco.query.get_or_404(id)
    db.session.delete(integrante)
    db.session.commit()
    flash('Integrante excluÃ­do com sucesso!', 'success')
    return redirect(url_for('cadastrar_elenco'))

@app.route('/cadastros/categorias-fornecedor', methods=['GET', 'POST'])
def cadastrar_categoria_fornecedor():
    form = CategoriaFornecedorForm()
    if form.validate_on_submit():
        nova = CategoriaFornecedor(nome=form.nome.data)
        db.session.add(nova)
        db.session.commit()
        flash('Categoria cadastrada com sucesso!', 'success')
        return redirect(url_for('cadastrar_categoria_fornecedor'))
    categorias = CategoriaFornecedor.query.all()
    return render_template('categorias_fornecedor.html', form=form, categorias=categorias)

@app.route('/cadastros/fornecedores', methods=['GET', 'POST'])
def cadastrar_fornecedor():
    # Verificar se existem categorias
    categorias_existentes = CategoriaFornecedor.query.all()
    if not categorias_existentes:
        flash('Ã‰ necessÃ¡rio cadastrar pelo menos uma categoria de fornecedor antes de cadastrar fornecedores.', 'warning')
        return redirect(url_for('cadastrar_categoria_fornecedor'))
    
    form = FornecedorForm()
    form.id_categoria_fornecedor.choices = [(c.id_categoria_fornecedor, c.nome) for c in categorias_existentes]
    if form.validate_on_submit():
        novo = Fornecedor(
            nome=form.nome.data,
            telefone=form.telefone.data,
            cidade=form.cidade.data,
            estado=form.estado.data,
            id_categoria_fornecedor=form.id_categoria_fornecedor.data
        )
        db.session.add(novo)
        db.session.commit()
        flash('Fornecedor cadastrado com sucesso!', 'success')
        return redirect(url_for('cadastrar_fornecedor'))
    fornecedores = Fornecedor.query.all()
    return render_template('fornecedores.html', form=form, fornecedores=fornecedores)

@app.route('/cadastros/categorias-fornecedor/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria_fornecedor(id):
    categoria = CategoriaFornecedor.query.get_or_404(id)
    form = CategoriaFornecedorForm(obj=categoria)
    if form.validate_on_submit():
        categoria.nome = form.nome.data
        db.session.commit()
        flash('Categoria atualizada com sucesso!', 'success')
        return redirect(url_for('cadastrar_categoria_fornecedor'))
    categorias = CategoriaFornecedor.query.all()
    return render_template('categorias_fornecedor.html', form=form, categorias=categorias)

@app.route('/cadastros/categorias-fornecedor/excluir/<int:id>')
def excluir_categoria_fornecedor(id):
    categoria = CategoriaFornecedor.query.get_or_404(id)
    
    # Verificar se existem fornecedores usando esta categoria
    fornecedores_usando = Fornecedor.query.filter_by(id_categoria_fornecedor=id).count()
    if fornecedores_usando > 0:
        flash(f'NÃ£o Ã© possÃ­vel excluir esta categoria pois existem {fornecedores_usando} fornecedor(es) associado(s) a ela.', 'danger')
        return redirect(url_for('cadastrar_categoria_fornecedor'))
    
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoria excluÃ­da com sucesso!', 'success')
    return redirect(url_for('cadastrar_categoria_fornecedor'))

@app.route('/cadastros/fornecedores/editar/<int:id>', methods=['GET', 'POST'])
def editar_fornecedor(id):
    # Verificar se existem categorias
    categorias_existentes = CategoriaFornecedor.query.all()
    if not categorias_existentes:
        flash('Ã‰ necessÃ¡rio cadastrar pelo menos uma categoria de fornecedor antes de editar fornecedores.', 'warning')
        return redirect(url_for('cadastrar_categoria_fornecedor'))
    
    fornecedor = Fornecedor.query.get_or_404(id)
    form = FornecedorForm(obj=fornecedor)
    form.id_categoria_fornecedor.choices = [(c.id_categoria_fornecedor, c.nome) for c in categorias_existentes]
    if form.validate_on_submit():
        fornecedor.nome = form.nome.data
        fornecedor.telefone = form.telefone.data
        fornecedor.cidade = form.cidade.data
        fornecedor.estado = form.estado.data
        fornecedor.id_categoria_fornecedor = form.id_categoria_fornecedor.data
        db.session.commit()
        flash('Fornecedor atualizado com sucesso!', 'success')
        return redirect(url_for('cadastrar_fornecedor'))
    fornecedores = Fornecedor.query.all()
    return render_template('fornecedores.html', form=form, fornecedores=fornecedores)

@app.route('/cadastros/fornecedores/excluir/<int:id>')
def excluir_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    # Fornecedores normalmente nÃ£o tÃªm dependÃªncias diretas no sistema atual
    # Mas se houver tabelas de relacionamento no futuro, adicionar aqui
    db.session.delete(fornecedor)
    db.session.commit()
    flash('Fornecedor excluÃ­do com sucesso!', 'success')
    return redirect(url_for('cadastrar_fornecedor'))

@app.route('/cadastros/receitas', methods=['GET', 'POST'])
def cadastrar_receita():
    # Verificar se existem categorias
    categorias_existentes = CategoriaReceita.query.all()
    if not categorias_existentes:
        flash('Ã‰ necessÃ¡rio cadastrar pelo menos uma categoria de receita antes de cadastrar receitas.', 'warning')
        return redirect(url_for('cadastrar_categoria_receita'))
    
    form = ReceitaForm()
    form.id_categoria_receita.choices = [(c.id_categoria_receita, c.nome) for c in categorias_existentes]
    if form.validate_on_submit():
        nova = Receita(nome=form.nome.data, id_categoria_receita=form.id_categoria_receita.data)
        db.session.add(nova)
        db.session.commit()
        flash('Receita cadastrada com sucesso!', 'success')
        return redirect(url_for('cadastrar_receita'))
    receitas = Receita.query.all()
    return render_template('receitas.html', form=form, receitas=receitas)

@app.route('/cadastros/receitas/editar/<int:id>', methods=['GET', 'POST'])
def editar_receita(id):
    # Verificar se existem categorias
    categorias_existentes = CategoriaReceita.query.all()
    if not categorias_existentes:
        flash('Ã‰ necessÃ¡rio cadastrar pelo menos uma categoria de receita antes de editar receitas.', 'warning')
        return redirect(url_for('cadastrar_categoria_receita'))
    
    receita = Receita.query.get_or_404(id)
    form = ReceitaForm(obj=receita)
    form.id_categoria_receita.choices = [(c.id_categoria_receita, c.nome) for c in categorias_existentes]
    if form.validate_on_submit():
        receita.nome = form.nome.data
        receita.id_categoria_receita = form.id_categoria_receita.data
        db.session.commit()
        flash('Receita atualizada com sucesso!', 'success')
        return redirect(url_for('cadastrar_receita'))
    receitas = Receita.query.all()
    return render_template('receitas.html', form=form, receitas=receitas)

@app.route('/cadastros/receitas/excluir/<int:id>')
def excluir_receita(id):
    receita = Receita.query.get_or_404(id)
    
    # Verificar se existem eventos usando esta receita
    eventos_usando = ReceitaEvento.query.filter_by(id_receita=id).count()
    if eventos_usando > 0:
        flash(f'NÃ£o Ã© possÃ­vel excluir esta receita pois existem {eventos_usando} registro(s) de receita em evento(s) associado(s) a ela.', 'danger')
        return redirect(url_for('cadastrar_receita'))
    
    db.session.delete(receita)
    db.session.commit()
    flash('Receita excluÃ­da com sucesso!', 'success')
    return redirect(url_for('cadastrar_receita'))

@app.route('/cadastros/categorias-receita', methods=['GET', 'POST'])
def cadastrar_categoria_receita():
    form = CategoriaReceitaForm()
    if form.validate_on_submit():
        nova = CategoriaReceita(nome=form.nome.data)
        db.session.add(nova)
        db.session.commit()
        flash('Categoria cadastrada com sucesso!', 'success')
        return redirect(url_for('cadastrar_categoria_receita'))
    categorias = CategoriaReceita.query.all()
    return render_template('categorias_receita.html', form=form, categorias=categorias)

@app.route('/cadastros/categorias-receita/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria_receita(id):
    categoria = CategoriaReceita.query.get_or_404(id)
    form = CategoriaReceitaForm(obj=categoria)
    if form.validate_on_submit():
        categoria.nome = form.nome.data
        db.session.commit()
        flash('Categoria atualizada com sucesso!', 'success')
        return redirect(url_for('cadastrar_categoria_receita'))
    categorias = CategoriaReceita.query.all()
    return render_template('categorias_receita.html', form=form, categorias=categorias)

@app.route('/cadastros/categorias-receita/excluir/<int:id>')
def excluir_categoria_receita(id):
    categoria = CategoriaReceita.query.get_or_404(id)
    
    # Verificar se existem receitas usando esta categoria
    receitas_usando = Receita.query.filter_by(id_categoria_receita=id).count()
    if receitas_usando > 0:
        flash(f'NÃ£o Ã© possÃ­vel excluir esta categoria pois existem {receitas_usando} receita(s) associada(s) a ela.', 'danger')
        return redirect(url_for('cadastrar_categoria_receita'))
    
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoria excluÃ­da com sucesso!', 'success')
    return redirect(url_for('cadastrar_categoria_receita'))

@app.route('/cadastros/categorias-despesa', methods=['GET', 'POST'])
def cadastrar_categoria_despesa():
    form = CategoriaDespesaForm()
    if form.validate_on_submit():
        nova = CategoriaDespesa(nome=form.nome.data)
        db.session.add(nova)
        db.session.commit()
        flash('Categoria cadastrada com sucesso!', 'success')
        return redirect(url_for('cadastrar_categoria_despesa'))
    categorias = CategoriaDespesa.query.all()
    return render_template('categorias_despesa.html', form=form, categorias=categorias)

@app.route('/cadastros/categorias-despesa/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria_despesa(id):
    categoria = CategoriaDespesa.query.get_or_404(id)
    form = CategoriaDespesaForm(obj=categoria)
    if form.validate_on_submit():
        categoria.nome = form.nome.data
        db.session.commit()
        flash('Categoria atualizada com sucesso!', 'success')
        return redirect(url_for('cadastrar_categoria_despesa'))
    categorias = CategoriaDespesa.query.all()
    return render_template('categorias_despesa.html', form=form, categorias=categorias)

@app.route('/cadastros/categorias-despesa/excluir/<int:id>')
def excluir_categoria_despesa(id):
    categoria = CategoriaDespesa.query.get_or_404(id)
    
    # Verificar se existem despesas usando esta categoria
    despesas_usando = Despesa.query.filter_by(id_categoria_despesa=id).count()
    if despesas_usando > 0:
        flash(f'NÃ£o Ã© possÃ­vel excluir esta categoria pois existem {despesas_usando} despesa(s) associada(s) a ela.', 'danger')
        return redirect(url_for('cadastrar_categoria_despesa'))
    
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoria excluÃ­da com sucesso!', 'success')
    return redirect(url_for('cadastrar_categoria_despesa'))

@app.route('/eventos')
def listar_eventos():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Obter informaÃ§Ãµes do usuÃ¡rio logado
    usuario = Usuario.query.get(session['user_id'])
    if not usuario or not usuario.colaborador:
        flash('Erro ao carregar informaÃ§Ãµes do usuÃ¡rio.', 'danger')
        return redirect(url_for('login'))
    
    # Verificar se Ã© administrador
    is_admin = any(cat.nome.lower() == 'administrativo' for cat in usuario.colaborador.categorias)

    limite_passado = date.today() - timedelta(days=90)
    print(f"Data limite (90 dias atrÃ¡s): {limite_passado}")
    print(f"Data hoje: {date.today()}")
    
    # Filtrar eventos baseado no tipo de usuÃ¡rio
    eventos_query = Evento.query.filter(
        Evento.status.in_(['planejamento', 'a realizar', 'em andamento', 'realizado']),
        # Mostrar eventos dos Ãºltimos 90 dias em diante (inclui eventos futuros)
        Evento.data_inicio >= limite_passado
    )
    
    if not is_admin:
        # Produtores veem apenas seus eventos
        eventos_query = eventos_query.filter_by(id_produtor=usuario.colaborador.id_colaborador)
        print(f"Filtrado para produtor ID: {usuario.colaborador.id_colaborador}")
    
    eventos = eventos_query.order_by(Evento.data_inicio.desc()).all()
    
    print(f"Eventos filtrados encontrados: {len(eventos)}")
    for evento in eventos:
        print(f"Evento filtrado: {evento.nome}, Data: {evento.data_inicio}, Status: {evento.status}")
    
    # Buscar dados para os modais de adiÃ§Ã£o rÃ¡pida
    categorias_receita = CategoriaReceita.query.all()
    categorias_despesa = CategoriaDespesa.query.filter(
        CategoriaDespesa.id_categoria_despesa.in_(
            db.session.query(Despesa.id_categoria_despesa).filter(
                Despesa.id_tipo_despesa.in_([1, 2])
            ).distinct()
        )
    ).all()
    fornecedores = Fornecedor.query.order_by(Fornecedor.nome).all()
    current_date = date.today().strftime('%Y-%m-%d')
    
    return render_template('eventos.html', 
                         eventos=eventos, 
                         is_admin=is_admin, 
                         usuario=usuario,
                         categorias_receita=categorias_receita,
                         categorias_despesa=categorias_despesa,
                         fornecedores=fornecedores,
                         current_date=current_date)

# Endpoints de API para carregamento dinÃ¢mico nos modais
@app.route('/api/despesas-por-categoria/<int:categoria_id>')
def api_despesas_por_categoria(categoria_id):
    try:
        # Filtrar apenas despesas de evento (tipos 1 e 2)
        despesas = Despesa.query.filter_by(id_categoria_despesa=categoria_id).filter(
            Despesa.id_tipo_despesa.in_([1, 2])
        ).all()
        despesas_data = []
        
        for despesa in despesas:
            # Usar o valor mÃ©dio jÃ¡ cadastrado na despesa ou calcular dinamicamente
            valor_medio = despesa.valor_medio_despesa
            
            # Se nÃ£o tem valor mÃ©dio cadastrado, calcular baseado nos eventos
            if not valor_medio:
                despesas_evento = DespesaEvento.query.filter_by(id_despesa=despesa.id_despesa).all()
                if despesas_evento:
                    valores = [de.valor for de in despesas_evento if de.valor]
                    if valores:
                        valor_medio = sum(valores) / len(valores)
            
            despesas_data.append({
                'id_despesa': despesa.id_despesa,
                'nome': despesa.nome,
                'valor_medio': float(valor_medio) if valor_medio else None,
                'tipo_despesa': despesa.id_tipo_despesa
            })
        
        return jsonify(despesas_data)
    except Exception as e:
        print(f"Erro no endpoint despesas-por-categoria: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/receitas-por-categoria/<int:categoria_id>')
def api_receitas_por_categoria(categoria_id):
    try:
        receitas = Receita.query.filter_by(id_categoria_receita=categoria_id).all()
        receitas_data = []
        
        for receita in receitas:
            receitas_data.append({
                'id_receita': receita.id_receita,
                'nome': receita.nome
            })
        
        return jsonify(receitas_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/eventos/<int:id_evento>/salvar-receita', methods=['POST'])
def salvar_receita_individual(id_evento):
    try:
        data = request.get_json()
        
        # Validar dados obrigatÃ³rios
        if not data.get('receita_id') or not data.get('valor'):
            return jsonify({'success': False, 'message': 'Receita e valor sÃ£o obrigatÃ³rios'})
        
        # Verificar se o evento existe
        evento = Evento.query.get(id_evento)
        if not evento:
            return jsonify({'success': False, 'message': 'Evento nÃ£o encontrado'})
        
        # Converter valor - tratar tanto formato brasileiro quanto americano
        try:
            valor_str = str(data['valor']).strip()
            
            # Se contÃ©m ponto e vÃ­rgula, Ã© formato brasileiro (ex: 1.000,50)
            if '.' in valor_str and ',' in valor_str:
                # Remover pontos de milhares e trocar vÃ­rgula por ponto
                valor_str = valor_str.replace('.', '').replace(',', '.')
            # Se contÃ©m apenas vÃ­rgula, trocar por ponto
            elif ',' in valor_str and '.' not in valor_str:
                valor_str = valor_str.replace(',', '.')
            
            valor = float(valor_str)
            
            if valor <= 0:
                return jsonify({'success': False, 'message': 'Valor deve ser maior que zero'})
                
        except (ValueError, TypeError) as e:
            print(f"Erro ao converter valor '{data['valor']}': {e}")
            return jsonify({'success': False, 'message': 'Valor invÃ¡lido'})
        
        # Converter data
        try:
            data_receita = datetime.strptime(data['data'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'success': False, 'message': 'Data invÃ¡lida'})
        
        # Criar receita do evento
        receita_evento = ReceitaEvento(
            id_evento=id_evento,
            id_receita=int(data['receita_id']),
            valor=valor,
            data=data_receita,
            observacoes=data.get('observacoes', '')
        )
        
        db.session.add(receita_evento)
        db.session.commit()
        
        # Buscar nome da receita para retorno
        receita = Receita.query.get(data['receita_id'])
        receita_nome = receita.nome if receita else 'Receita'
        
        print(f"âœ… Receita salva: {receita_nome} - R$ {valor:,.2f}")
        
        return jsonify({
            'success': True, 
            'message': 'Receita adicionada com sucesso',
            'receita_evento_id': receita_evento.id_receita_evento,
            'receita_nome': receita_nome,
            'valor_salvo': valor
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"âŒ Erro ao salvar receita: {e}")
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})

@app.route('/eventos/novo', methods=['GET', 'POST'])
def novo_evento():
    form = EventoForm()
    form.id_circo.choices = [(c.id_circo, c.nome) for c in Circo.query.all()]
    
    # Filtrar apenas colaboradores que sÃ£o produtores
    produtores = [p for p in Colaborador.query.all() if p.tem_categoria_produtor]
    if not produtores:
        flash('Ã‰ necessÃ¡rio cadastrar pelo menos um colaborador como produtor antes de criar eventos.', 'warning')
        return redirect(url_for('cadastrar_colaborador'))
    
    form.id_produtor.choices = [(p.id_colaborador, p.nome) for p in produtores]
    
    categorias_receita = CategoriaReceita.query.all()
    
    # Filtrar apenas categorias que tÃªm despesas de evento (tipos 1 e 2)
    categorias_despesa = CategoriaDespesa.query.filter(
        CategoriaDespesa.id_categoria_despesa.in_(
            db.session.query(Despesa.id_categoria_despesa).filter(
                Despesa.id_tipo_despesa.in_([1, 2])
            ).distinct()
        )
    ).all()

    if form.validate_on_submit():
        # Debug: Verificar o tipo dos dados recebidos
        print(f"Tipo data_inicio: {type(form.data_inicio.data)}, valor: {form.data_inicio.data}")
        print(f"Tipo data_fim: {type(form.data_fim.data)}, valor: {form.data_fim.data}")
        
        # Processamento manual das datas se necessÃ¡rio
        data_inicio = form.data_inicio.data
        data_fim = form.data_fim.data
        
        # Converter strings para objetos date se necessÃ¡rio
        if isinstance(data_inicio, str):
            if '/' in data_inicio:
                # Formato brasileiro DD/MM/YYYY
                data_inicio = datetime.strptime(data_inicio, '%d/%m/%Y').date()
            else:
                # Formato ISO YYYY-MM-DD
                data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        
        if isinstance(data_fim, str):
            if '/' in data_fim:
                # Formato brasileiro DD/MM/YYYY
                data_fim = datetime.strptime(data_fim, '%d/%m/%Y').date()
            else:
                # Formato ISO YYYY-MM-DD
                data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
        novo = Evento(
            nome=form.nome.data,
            data_inicio=data_inicio,
            data_fim=data_fim,
            cidade=form.cidade.data,
            estado=form.estado.data,
            endereco=form.endereco.data,
            id_circo=form.id_circo.data,
            id_produtor=form.id_produtor.data,
            status=form.status.data,
            observacoes=form.observacoes.data
        )
        
        print(f"Evento criado: {novo.nome}, ID antes do add: {novo.id_evento}")
        db.session.add(novo)
        print(f"Evento adicionado Ã  sessÃ£o")
        
        try:
            db.session.flush()
            print(f"Flush executado, ID do evento: {novo.id_evento}")
        except Exception as e:
            print(f"Erro no flush: {e}")
            raise

        # 1. Processar receitas
        receitas_ids = request.form.getlist('receita_id[]')
        receita_datas = request.form.getlist('receita_data[]')
        valores = request.form.getlist('valor[]')
        observacoes = request.form.getlist('obs[]')

        for i in range(len(receitas_ids)):
            try:
                valor = float(valores[i].replace(',', '.'))
                data_receita = receita_datas[i] if i < len(receita_datas) else None
                data = datetime.strptime(data_receita, '%Y-%m-%d').date() if data_receita else None
            except:
                continue
            if receitas_ids[i] and valor:
                db.session.add(ReceitaEvento(
                    id_evento=novo.id_evento,
                    id_receita=int(receitas_ids[i]),
                    valor=valor,
                    data=data,
                    observacoes=observacoes[i]
                ))

        # 2. Processar despesas variÃ¡veis do formulÃ¡rio
        despesa_ids = request.form.getlist('despesa_id[]')
        datas_desp = request.form.getlist('despesa_data[]')
        valores_desp = request.form.getlist('despesa_valor[]')
        status_pag = request.form.getlist('despesa_status_pagamento[]')
        forma_pag = request.form.getlist('despesa_forma_pagamento[]')
        pago_por = request.form.getlist('despesa_pago_por[]')
        obs_desp = request.form.getlist('despesa_obs[]')

        for i in range(len(despesa_ids)):
            try:
                # Verificar se tem ID da despesa (obrigatÃ³rio)
                if not despesa_ids[i]:
                    continue
                    
                # Verificar se tem valor preenchido
                if not valores_desp[i] or valores_desp[i].strip() == '':
                    continue
                    
                valor = float(valores_desp[i].replace(',', '.'))
                data = datetime.strptime(datas_desp[i], '%Y-%m-%d').date() if datas_desp[i] else date.today()
            except (ValueError, IndexError):
                continue
                
            # Adicionar despesa ao evento
            db.session.add(DespesaEvento(
                id_evento=novo.id_evento,
                id_despesa=int(despesa_ids[i]),
                data=data,
                valor=valor,
                status_pagamento=status_pag[i] if i < len(status_pag) else 'pendente',
                forma_pagamento=forma_pag[i] if i < len(forma_pag) else 'dÃ©bito',
                pago_por=pago_por[i] if i < len(pago_por) else '',
                observacoes=obs_desp[i] if i < len(obs_desp) else ''
            ))

        # 3. Cadastrar TODAS as despesas fixas automaticamente (UMA VEZ)
        despesas_fixas = Despesa.query.filter_by(id_tipo_despesa=1).all()
        
        for despesa_fixa in despesas_fixas:
            valor_automatico = despesa_fixa.valor_medio_despesa or 0
            db.session.add(DespesaEvento(
                id_evento=novo.id_evento,
                id_despesa=despesa_fixa.id_despesa,
                data=novo.data_inicio or date.today(),
                valor=valor_automatico,
                status_pagamento='pendente',
                forma_pagamento='dÃ©bito',
                pago_por='',
                observacoes='Despesa fixa adicionada automaticamente'
            ))

        try:
            db.session.commit()
            print(f"âœ… COMMIT executado com sucesso! Evento ID: {novo.id_evento}")
            
            # Verificar se o evento foi realmente salvo
            evento_verificacao = Evento.query.get(novo.id_evento)
            if evento_verificacao:
                print(f"âœ… Evento verificado no banco: {evento_verificacao.nome}")
            else:
                print("âŒ ERRO: Evento nÃ£o encontrado no banco apÃ³s commit!")
            
            # Verificar as despesas APÃ“S o commit
            despesas_depois = DespesaEvento.query.filter_by(id_evento=novo.id_evento).all()
            print(f"\n=== DESPESAS NO EVENTO APÃ“S O COMMIT ===")
            for desp in despesas_depois:
                print(f"ID Despesa: {desp.id_despesa}, Valor SALVO: {desp.valor}, Tipo: {desp.despesa.id_tipo_despesa}")
            
            flash('Evento e despesas/receitas cadastrados com sucesso!', 'success')
            return redirect(url_for('editar_evento', id=novo.id_evento))
            
        except Exception as e:
            print(f"âŒ ERRO no commit: {e}")
            db.session.rollback()
            flash(f'Erro ao salvar evento: {str(e)}', 'danger')
            # NÃ£o fazer redirect em caso de erro para debugar

    # Para a exibiÃ§Ã£o inicial (antes de salvar), mostrar todas as despesas disponÃ­veis
    categorias_receita_dict = {
        c.id_categoria_receita: [{'id_receita': r.id_receita, 'nome': r.nome}
                                 for r in Receita.query.filter_by(id_categoria_receita=c.id_categoria_receita)]
        for c in categorias_receita
    }

    # Criar estrutura de despesas organizada por tipo para exibiÃ§Ã£o
    categorias_despesa_dict = {}
    for categoria in categorias_despesa:
        despesas_categoria = Despesa.query.filter_by(
            id_categoria_despesa=categoria.id_categoria_despesa
        ).filter(Despesa.id_tipo_despesa.in_([1, 2])).all()
        
        despesas_fixas = [d for d in despesas_categoria if d.id_tipo_despesa == 1]
        despesas_variaveis = [d for d in despesas_categoria if d.id_tipo_despesa == 2]
        
        categorias_despesa_dict[categoria.id_categoria_despesa] = {
            'fixas': [{
                'id_despesa': d.id_despesa, 
                'nome': d.nome,
                'valor_medio': float(d.valor_medio_despesa) if d.valor_medio_despesa else None,
                'tipo': 1,
                'ja_cadastrada': False  # No cadastro, nenhuma estÃ¡ cadastrada ainda
            } for d in despesas_fixas],
            'variaveis': [{
                'id_despesa': d.id_despesa, 
                'nome': d.nome,
                'valor_medio': float(d.valor_medio_despesa) if d.valor_medio_despesa else None,
                'tipo': 2,
                'ja_cadastrada': False  # No cadastro, nenhuma estÃ¡ cadastrada ainda
            } for d in despesas_variaveis]
        }

    return render_template(
        'novo_evento.html',
        form=form,
        categorias_receita=categorias_receita,
        categorias_receita_dict=categorias_receita_dict,
        categorias_despesa=categorias_despesa,
        categorias_despesa_dict=categorias_despesa_dict,
        fornecedores=[{'id_fornecedor': f.id_fornecedor, 'nome': f.nome} for f in Fornecedor.query.all()],
        receitas_salvas=[],
        despesas_salvas=[],
        current_date=date.today().isoformat(),
        is_editing=False
    )

@app.route('/eventos/editar/<int:id>', methods=['GET', 'POST'])
def editar_evento(id):
    evento = Evento.query.get_or_404(id)
    form = EventoForm(obj=evento)
    form.id_circo.choices = [(c.id_circo, c.nome) for c in Circo.query.all()]
    
    # Filtrar apenas colaboradores que sÃ£o produtores
    produtores = [p for p in Colaborador.query.all() if p.tem_categoria_produtor]
    if not produtores:
        flash('Ã‰ necessÃ¡rio cadastrar pelo menos um colaborador como produtor antes de editar eventos.', 'warning')
        return redirect(url_for('cadastrar_colaborador'))
    
    form.id_produtor.choices = [(p.id_colaborador, p.nome) for p in produtores]
    
    categorias_receita = CategoriaReceita.query.all()
    
    # Filtrar apenas categorias que tÃªm despesas de evento (tipos 1 e 2)
    categorias_despesa = CategoriaDespesa.query.filter(
        CategoriaDespesa.id_categoria_despesa.in_(
            db.session.query(Despesa.id_categoria_despesa).filter(
                Despesa.id_tipo_despesa.in_([1, 2])
            ).distinct()
        )
    ).all()

    # Obter receitas e despesas jÃ¡ cadastradas
    receitas_salvas = ReceitaEvento.query.filter_by(id_evento=id).all()
    despesas_salvas = DespesaEvento.query.filter_by(id_evento=id).all()

    if form.validate_on_submit():
        # Processamento manual das datas se necessÃ¡rio
        data_inicio = form.data_inicio.data
        data_fim = form.data_fim.data
        
        # Converter strings para objetos date se necessÃ¡rio
        if isinstance(data_inicio, str):
            if '/' in data_inicio:
                # Formato brasileiro DD/MM/YYYY
                data_inicio = datetime.strptime(data_inicio, '%d/%m/%Y').date()
            else:
                # Formato ISO YYYY-MM-DD
                data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        
        if isinstance(data_fim, str):
            if '/' in data_fim:
                # Formato brasileiro DD/MM/YYYY
                data_fim = datetime.strptime(data_fim, '%d/%m/%Y').date()
            else:
                # Formato ISO YYYY-MM-DD
                data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
        evento.nome = form.nome.data
        evento.data_inicio = data_inicio
        evento.data_fim = data_fim
        evento.cidade = form.cidade.data
        evento.estado = form.estado.data
        evento.endereco = form.endereco.data
        evento.id_circo = form.id_circo.data
        evento.id_produtor = form.id_produtor.data
        evento.status = form.status.data
        evento.observacoes = form.observacoes.data

        # Exclui os itens marcados
        excluir_receitas = request.form.get('excluir_receita_ids', '')
        excluir_despesas = request.form.get('excluir_despesa_ids', '')

        if excluir_receitas:
            for rid in excluir_receitas.split(','):
                if rid.strip():
                    ReceitaEvento.query.filter_by(id_receita_evento=int(rid)).delete()

        if excluir_despesas:
            for did in excluir_despesas.split(','):
                if did.strip():
                    DespesaEvento.query.filter_by(id_despesa_evento=int(did)).delete()

        # Processar novas receitas
        receitas_ids = request.form.getlist('receita_id[]')
        receita_datas = request.form.getlist('receita_data[]')
        valores = request.form.getlist('valor[]')
        observacoes = request.form.getlist('obs[]')
        for i in range(len(receitas_ids)):
            try:
                valor = float(valores[i].replace(',', '.'))
                data_receita = receita_datas[i] if i < len(receita_datas) else None
                data = datetime.strptime(data_receita, '%Y-%m-%d').date() if data_receita else None
            except:
                continue
            if receitas_ids[i] and valor:
                db.session.add(ReceitaEvento(
                    id_evento=evento.id_evento,
                    id_receita=int(receitas_ids[i]),
                    valor=valor,
                    data=data,
                    observacoes=observacoes[i]
                ))

        # Processar despesas (novas e editadas)
        despesa_ids = request.form.getlist('despesa_id[]')
        datas_desp = request.form.getlist('despesa_data[]')
        valores_desp = request.form.getlist('despesa_valor[]')
        status_pag = request.form.getlist('despesa_status_pagamento[]')
        forma_pag = request.form.getlist('despesa_forma_pagamento[]')
        pago_por = request.form.getlist('despesa_pago_por[]')
        obs_desp = request.form.getlist('despesa_obs[]')
        
        print(f"=== DEBUG DESPESAS COMPLETO ===")
        print(f"Total de despesas recebidas: {len(despesa_ids)}")
        print(f"despesa_ids: {despesa_ids}")
        print(f"valores_desp: {valores_desp}")
        print(f"datas_desp: {datas_desp}")
        print(f"status_pag: {status_pag}")
        print(f"forma_pag: {forma_pag}")
        print(f"pago_por: {pago_por}")
        print(f"obs_desp: {obs_desp}")
        
        # Verificar todas as despesas jÃ¡ cadastradas no evento ANTES do processamento
        despesas_antes = DespesaEvento.query.filter_by(id_evento=evento.id_evento).all()
        print(f"\n=== DESPESAS NO EVENTO ANTES DO PROCESSAMENTO ===")
        for desp in despesas_antes:
            print(f"ID Despesa: {desp.id_despesa}, Valor atual: {desp.valor}, Tipo: {desp.despesa.id_tipo_despesa}")
        
        for i in range(len(despesa_ids)):
            try:
                # Verificar se tem ID da despesa (obrigatÃ³rio)
                if not despesa_ids[i]:
                    print(f"Ãndice {i}: ID da despesa vazio, pulando...")
                    continue
                    
                # Verificar se tem valor preenchido
                if not valores_desp[i] or valores_desp[i].strip() == '':
                    print(f"Ãndice {i}: Valor da despesa vazio, pulando...")
                    continue
                    
                valor = float(valores_desp[i].replace(',', '.'))
                data = datetime.strptime(datas_desp[i], '%Y-%m-%d').date() if datas_desp[i] else date.today()
                id_despesa = int(despesa_ids[i])
                
                print(f"\n--- Processando ÃNDICE {i} ---")
                print(f"ID Despesa: {id_despesa}")
                print(f"Valor recebido: '{valores_desp[i]}'")
                print(f"Valor convertido: {valor}")
                print(f"Data: {data}")
                print(f"Status: {status_pag[i] if i < len(status_pag) else 'pendente'}")
                print(f"Forma: {forma_pag[i] if i < len(forma_pag) else 'dÃ©bito'}")
                
            except (ValueError, IndexError) as e:
                print(f"ERRO ao processar despesa Ã­ndice {i}: {e}")
                continue
            
            # Verificar se jÃ¡ existe uma DespesaEvento para esta despesa neste evento
            despesa_evento_existente = DespesaEvento.query.filter_by(
                id_evento=evento.id_evento,
                id_despesa=id_despesa
            ).first()
            
            if despesa_evento_existente:
                # ATUALIZAR despesa existente
                print(f"âœ… ENCONTROU despesa existente!")
                print(f"   - Valor antigo: {despesa_evento_existente.valor}")
                print(f"   - Valor novo: {valor}")
                print(f"   - ID DespesaEvento: {despesa_evento_existente.id_despesa_evento}")
                
                despesa_evento_existente.data = data
                despesa_evento_existente.valor = valor
                despesa_evento_existente.status_pagamento = status_pag[i] if i < len(status_pag) else 'pendente'
                despesa_evento_existente.forma_pagamento = forma_pag[i] if i < len(forma_pag) else 'dÃ©bito'
                despesa_evento_existente.pago_por = pago_por[i] if i < len(pago_por) else ''
                despesa_evento_existente.observacoes = obs_desp[i] if i < len(obs_desp) else ''
                
                print(f"   - Despesa atualizada na sessÃ£o!")
            else:
                # CRIAR nova despesa no evento
                print(f"ðŸ†• NÃƒO encontrou despesa existente, criando nova...")
                nova_despesa_evento = DespesaEvento(
                    id_evento=evento.id_evento,
                    id_despesa=id_despesa,
                    data=data,
                    valor=valor,
                    status_pagamento=status_pag[i] if i < len(status_pag) else 'pendente',
                    forma_pagamento=forma_pag[i] if i < len(forma_pag) else 'dÃ©bito',
                    pago_por=pago_por[i] if i < len(pago_por) else '',
                    observacoes=obs_desp[i] if i < len(obs_desp) else ''
                )
                db.session.add(nova_despesa_evento)
                print(f"   - Nova despesa adicionada Ã  sessÃ£o!")

        try:
            db.session.commit()
            print(f"âœ… COMMIT executado com sucesso! Evento ID: {evento.id_evento}")
            
            # Verificar se o evento foi realmente salvo
            evento_verificacao = Evento.query.get(evento.id_evento)
            if evento_verificacao:
                print(f"âœ… Evento verificado no banco: {evento_verificacao.nome}")
            else:
                print("âŒ ERRO: Evento nÃ£o encontrado no banco apÃ³s commit!")
            
            # Verificar as despesas APÃ“S o commit
            despesas_depois = DespesaEvento.query.filter_by(id_evento=evento.id_evento).all()
            print(f"\n=== DESPESAS NO EVENTO APÃ“S O COMMIT ===")
            for desp in despesas_depois:
                print(f"ID Despesa: {desp.id_despesa}, Valor SALVO: {desp.valor}, Tipo: {desp.despesa.id_tipo_despesa}")
            
            flash('Evento atualizado com sucesso!', 'success')
            return redirect(url_for('listar_eventos'))
            
        except Exception as e:
            print(f"âŒ ERRO no commit: {e}")
            db.session.rollback()
            flash(f'Erro ao salvar evento: {str(e)}', 'danger')
            # NÃ£o fazer redirect em caso de erro para debugar

    categorias_receita_dict = {
        c.id_categoria_receita: [{'id_receita': r.id_receita, 'nome': r.nome}
                                 for r in Receita.query.filter_by(id_categoria_receita=c.id_categoria_receita)]
        for c in categorias_receita
    }

    # Criar estrutura de despesas para ediÃ§Ã£o - mostrar apenas as que faltam cadastrar
    categorias_despesa_dict = {}
    for categoria in categorias_despesa:
        # Obter todas as despesas disponÃ­veis desta categoria
        despesas_categoria = Despesa.query.filter_by(
            id_categoria_despesa=categoria.id_categoria_despesa
        ).filter(Despesa.id_tipo_despesa.in_([1, 2])).all()
        
        despesas_fixas = [d for d in despesas_categoria if d.id_tipo_despesa == 1]
        despesas_variaveis = [d for d in despesas_categoria if d.id_tipo_despesa == 2]
        
        # IDs das despesas jÃ¡ cadastradas neste evento
        despesas_ja_cadastradas = set(d.id_despesa for d in despesas_salvas)
        
        # Criar um dicionÃ¡rio para acesso rÃ¡pido aos dados das despesas jÃ¡ cadastradas
        despesas_evento_dict = {d.id_despesa: d for d in despesas_salvas}
        
        # Para as despesas fixas: sempre mostrar TODAS, mas com valores reais se jÃ¡ cadastradas
        categorias_despesa_dict[categoria.id_categoria_despesa] = {
            'fixas': [{
                'id_despesa': d.id_despesa, 
                'nome': d.nome,
                'valor_medio': float(d.valor_medio_despesa) if d.valor_medio_despesa else None,
                'tipo': 1,
                'ja_cadastrada': d.id_despesa in despesas_ja_cadastradas,
                # Se jÃ¡ foi cadastrada, usar valores reais do evento
                'valor_atual': float(despesas_evento_dict[d.id_despesa].valor) if d.id_despesa in despesas_ja_cadastradas else (float(d.valor_medio_despesa) if d.valor_medio_despesa else None),
                'data_atual': despesas_evento_dict[d.id_despesa].data.strftime('%Y-%m-%d') if d.id_despesa in despesas_ja_cadastradas else None,
                'status_atual': despesas_evento_dict[d.id_despesa].status_pagamento if d.id_despesa in despesas_ja_cadastradas else 'pendente',
                'forma_atual': despesas_evento_dict[d.id_despesa].forma_pagamento if d.id_despesa in despesas_ja_cadastradas else 'dÃ©bito',
                'fornecedor_atual': despesas_evento_dict[d.id_despesa].id_fornecedor if d.id_despesa in despesas_ja_cadastradas else None,
                'pago_por_atual': despesas_evento_dict[d.id_despesa].pago_por if d.id_despesa in despesas_ja_cadastradas else '',
                'obs_atual': despesas_evento_dict[d.id_despesa].observacoes if d.id_despesa in despesas_ja_cadastradas else 'Despesa fixa automÃ¡tica',
                'id_despesa_evento': despesas_evento_dict[d.id_despesa].id_despesa_evento if d.id_despesa in despesas_ja_cadastradas else None
            } for d in despesas_fixas],  # TODAS as despesas fixas
            'variaveis': [{
                'id_despesa': d.id_despesa, 
                'nome': d.nome,
                'valor_medio': float(d.valor_medio_despesa) if d.valor_medio_despesa else None,
                'tipo': 2,
                'ja_cadastrada': d.id_despesa in despesas_ja_cadastradas,
                # Se jÃ¡ foi cadastrada, usar valores reais do evento
                'valor_atual': float(despesas_evento_dict[d.id_despesa].valor) if d.id_despesa in despesas_ja_cadastradas else (float(d.valor_medio_despesa) if d.valor_medio_despesa else None),
                'data_atual': despesas_evento_dict[d.id_despesa].data.strftime('%Y-%m-%d') if d.id_despesa in despesas_ja_cadastradas else None,
                'status_atual': despesas_evento_dict[d.id_despesa].status_pagamento if d.id_despesa in despesas_ja_cadastradas else 'pendente',
                'forma_atual': despesas_evento_dict[d.id_despesa].forma_pagamento if d.id_despesa in despesas_ja_cadastradas else 'dÃ©bito',
                'fornecedor_atual': despesas_evento_dict[d.id_despesa].id_fornecedor if d.id_despesa in despesas_ja_cadastradas else None,
                'pago_por_atual': despesas_evento_dict[d.id_despesa].pago_por if d.id_despesa in despesas_ja_cadastradas else '',
                'obs_atual': despesas_evento_dict[d.id_despesa].observacoes if d.id_despesa in despesas_ja_cadastradas else '',
                'id_despesa_evento': despesas_evento_dict[d.id_despesa].id_despesa_evento if d.id_despesa in despesas_ja_cadastradas else None
            } for d in despesas_variaveis]  # TODAS as despesas variÃ¡veis (cadastradas e nÃ£o cadastradas)
        }

    return render_template(
        'novo_evento.html',
        form=form,
        categorias_receita=categorias_receita,
        categorias_receita_dict=categorias_receita_dict,
        categorias_despesa=categorias_despesa,
        categorias_despesa_dict=categorias_despesa_dict,
        fornecedores=[{'id_fornecedor': f.id_fornecedor, 'nome': f.nome} for f in Fornecedor.query.all()],
        receitas_salvas=receitas_salvas,
        despesas_salvas=despesas_salvas,
        current_date=date.today().isoformat(),
        is_editing=True
    )

@app.route('/eventos/excluir/<int:id>')
def excluir_evento(id):
    if session.get('categoria', '').lower() != 'administrativo':
        flash('VocÃª nÃ£o tem permissÃ£o para excluir eventos.', 'danger')
        return redirect(url_for('listar_eventos'))
    evento = Evento.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    flash('Evento excluÃ­do com sucesso!', 'success')
    return redirect(url_for('listar_eventos'))

@app.route('/relatorios/lucratividade-periodo')
def relatorios_lucratividade_periodo():
    if session.get('categoria', '').lower() != 'administrativo':
        flash('Acesso restrito a administradores.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Filtro de datas para perÃ­odo de anÃ¡lise
    period = request.args.get('period', 'ano')
    if period == 'mes':
        # Ãšltimos 12 meses
        data_fim = date.today().replace(day=1)  # Primeiro dia do mÃªs atual
        data_inicio = (data_fim - timedelta(days=365)).replace(day=1)  # 12 meses atrÃ¡s
    elif period == '6meses':
        # Ãšltimos 6 meses
        data_fim = date.today().replace(day=1)
        data_inicio = (data_fim - timedelta(days=180)).replace(day=1)
    elif period == 'ano':
        # Este ano
        data_fim = date.today()
        data_inicio = date(data_fim.year, 1, 1)
    elif period == 'custom':
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        if data_inicio and data_fim:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        else:
            data_fim = date.today()
            data_inicio = date(data_fim.year, 1, 1)
    else:
        data_fim = date.today()
        data_inicio = date(data_fim.year, 1, 1)

    # Lucro por mÃªs no perÃ­odo
    lucro_por_mes = []
    meses = []
    receitas_por_mes = []
    despesas_por_mes = []
    
    # Gerar lista de meses no perÃ­odo
    current_date = data_inicio.replace(day=1)  # Primeiro dia do mÃªs inicial
    end_date = data_fim.replace(day=1)  # Primeiro dia do mÃªs final
    
    while current_date <= end_date:
        # Calcular primeiro e Ãºltimo dia do mÃªs
        primeiro_dia = current_date
        if current_date.month == 12:
            ultimo_dia = date(current_date.year + 1, 1, 1) - timedelta(days=1)
        else:
            ultimo_dia = date(current_date.year, current_date.month + 1, 1) - timedelta(days=1)
        
        # Buscar receitas e despesas do mÃªs
        receitas = db.session.query(func.sum(ReceitaEvento.valor)).filter(
            ReceitaEvento.data >= primeiro_dia,
            ReceitaEvento.data <= ultimo_dia
        ).scalar() or 0
        
        despesas = db.session.query(func.sum(DespesaEvento.valor)).filter(
            DespesaEvento.data >= primeiro_dia,
            DespesaEvento.data <= ultimo_dia
        ).scalar() or 0
        
        lucro = receitas - despesas
        
        lucro_por_mes.append(float(lucro))
        receitas_por_mes.append(float(receitas))
        despesas_por_mes.append(float(despesas))
        meses.append(current_date.strftime('%m/%Y'))  # Formato MM/AAAA
        
        # PrÃ³ximo mÃªs
        if current_date.month == 12:
            current_date = date(current_date.year + 1, 1, 1)
        else:
            current_date = date(current_date.year, current_date.month + 1, 1)

    # Totais do perÃ­odo
    total_receitas_periodo = sum(receitas_por_mes)
    total_despesas_periodo = sum(despesas_por_mes)
    total_lucro_periodo = total_receitas_periodo - total_despesas_periodo

    return render_template(
        'relatorios_lucratividade_periodo.html',
        lucro_por_mes=lucro_por_mes,
        receitas_por_mes=receitas_por_mes,
        despesas_por_mes=despesas_por_mes,
        meses=meses,
        data_inicio=data_inicio.strftime('%Y-%m-%d'),
        data_fim=data_fim.strftime('%Y-%m-%d'),
        period=period,
        total_receitas_periodo=total_receitas_periodo,
        total_despesas_periodo=total_despesas_periodo,
        total_lucro_periodo=total_lucro_periodo
    )

@app.route('/relatorios/faturamento-evento')
def relatorios_faturamento_evento():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Obter informaÃ§Ãµes do usuÃ¡rio logado
    usuario = Usuario.query.get(session['user_id'])
    if not usuario or not usuario.colaborador:
        flash('Erro ao carregar informaÃ§Ãµes do usuÃ¡rio.', 'danger')
        return redirect(url_for('login'))
    
    # Verificar se Ã© administrador
    is_admin = any(cat.nome.lower() == 'administrativo' for cat in usuario.colaborador.categorias)
    
    if not is_admin:
        # Verificar se Ã© produtor
        is_produtor = any(cat.nome.lower() == 'produtor' for cat in usuario.colaborador.categorias)
        if not is_produtor:
            flash('Acesso restrito a administradores e produtores.', 'danger')
            return redirect(url_for('dashboard'))
    
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    # Filtrar eventos baseado no tipo de usuÃ¡rio
    eventos_query = Evento.query
    
    if not is_admin:
        # Produtores veem apenas seus eventos
        eventos_query = eventos_query.filter_by(id_produtor=usuario.colaborador.id_colaborador)
    
    if data_inicio:
        eventos_query = eventos_query.filter(Evento.data_inicio >= datetime.strptime(data_inicio, '%Y-%m-%d').date())
    if data_fim:
        eventos_query = eventos_query.filter(Evento.data_fim <= datetime.strptime(data_fim, '%Y-%m-%d').date())
    
    eventos = eventos_query.order_by(Evento.data_inicio.desc()).all()
    
    # Calcular lucratividade dos eventos para o grÃ¡fico
    eventos_lucratividade = []
    for evento in eventos:
        # Calcular receitas do evento
        total_receitas = db.session.query(func.sum(ReceitaEvento.valor)).filter_by(id_evento=evento.id_evento).scalar() or 0
        
        # Calcular despesas do evento
        total_despesas = db.session.query(func.sum(DespesaEvento.valor)).filter_by(id_evento=evento.id_evento).scalar() or 0
        
        # Calcular lucro
        lucro = total_receitas - total_despesas
        
        eventos_lucratividade.append({
            'nome': evento.nome,
            'receitas': float(total_receitas),
            'despesas': float(total_despesas),
            'lucro': float(lucro),
            'evento': evento
        })
    
    # Ordenar por lucro (do maior para o menor) e pegar top 10
    eventos_mais_lucrativos = sorted(eventos_lucratividade, key=lambda x: x['lucro'], reverse=True)[:10]
    
    # Preparar dados para o grÃ¡fico
    nomes_eventos = [e['nome'][:20] + '...' if len(e['nome']) > 20 else e['nome'] for e in eventos_mais_lucrativos]
    lucros_eventos = [e['lucro'] for e in eventos_mais_lucrativos]
    receitas_eventos = [e['receitas'] for e in eventos_mais_lucrativos]
    despesas_eventos = [e['despesas'] for e in eventos_mais_lucrativos]
    
    return render_template(
        'relatorios_faturamento_evento.html', 
        eventos=eventos, 
        data_inicio=data_inicio, 
        data_fim=data_fim,
        nomes_eventos=nomes_eventos,
        lucros_eventos=lucros_eventos,
        receitas_eventos=receitas_eventos,
        despesas_eventos=despesas_eventos,
        total_eventos=len(eventos),
        is_admin=is_admin,
        usuario=usuario
    )

@app.route('/relatorios/faturamento-evento/<int:id_evento>')
def relatorio_faturamento_evento(id_evento):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Obter informaÃ§Ãµes do usuÃ¡rio logado
    usuario = Usuario.query.get(session['user_id'])
    if not usuario or not usuario.colaborador:
        flash('Erro ao carregar informaÃ§Ãµes do usuÃ¡rio.', 'danger')
        return redirect(url_for('login'))
    
    # Verificar se Ã© administrador
    is_admin = any(cat.nome.lower() == 'administrativo' for cat in usuario.colaborador.categorias)
    
    evento = Evento.query.get_or_404(id_evento)
    
    # Verificar se o usuÃ¡rio tem permissÃ£o para ver este evento
    if not is_admin:
        # Verificar se Ã© produtor
        is_produtor = any(cat.nome.lower() == 'produtor' for cat in usuario.colaborador.categorias)
        if not is_produtor:
            flash('Acesso restrito a administradores e produtores.', 'danger')
            return redirect(url_for('dashboard'))
        
        # Verificar se Ã© o produtor deste evento
        if evento.id_produtor != usuario.colaborador.id_colaborador:
            flash('VocÃª sÃ³ pode visualizar relatÃ³rios dos seus prÃ³prios eventos.', 'danger')
            return redirect(url_for('relatorios_faturamento_evento'))
    
    receitas = ReceitaEvento.query.filter_by(id_evento=id_evento).all()
    despesas = DespesaEvento.query.filter_by(id_evento=id_evento).all()
    receitas_labels = [r.receita.nome for r in receitas]
    receitas_values = [float(r.valor) for r in receitas]
    despesas_labels = [d.despesa.nome for d in despesas]
    despesas_values = [float(d.valor) for d in despesas]
    
    return render_template(
        'relatorio_faturamento_evento.html', 
        evento=evento, 
        receitas_labels=receitas_labels, 
        receitas_values=receitas_values, 
        despesas_labels=despesas_labels, 
        despesas_values=despesas_values,
        is_admin=is_admin,
        usuario=usuario
    )

@app.route('/cadastros/categorias-veiculo', methods=['GET', 'POST'])
def cadastrar_categoria_veiculo():
    form = CategoriaVeiculoForm()
    if form.validate_on_submit():
        nova = CategoriaVeiculo(nome=form.nome.data)
        db.session.add(nova)
        db.session.commit()
        flash('Categoria cadastrada com sucesso!', 'success')
        return redirect(url_for('cadastrar_categoria_veiculo'))
    categorias = CategoriaVeiculo.query.all()
    return render_template('categorias_veiculo.html', form=form, categorias=categorias)

@app.route('/cadastros/categorias-veiculo/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria_veiculo(id):
    categoria = CategoriaVeiculo.query.get_or_404(id)
    form = CategoriaVeiculoForm(obj=categoria)
    if form.validate_on_submit():
        categoria.nome = form.nome.data
        db.session.commit()
        flash('Categoria atualizada com sucesso!', 'success')
        return redirect(url_for('cadastrar_categoria_veiculo'))
    categorias = CategoriaVeiculo.query.all()
    return render_template('categorias_veiculo.html', form=form, categorias=categorias)

@app.route('/cadastros/categorias-veiculo/excluir/<int:id>')
def excluir_categoria_veiculo(id):
    categoria = CategoriaVeiculo.query.get_or_404(id)
    
    # Verificar se existem veÃ­culos usando esta categoria
    veiculos_usando = Veiculo.query.filter_by(id_categoria_veiculo=id).count()
    if veiculos_usando > 0:
        flash(f'NÃ£o Ã© possÃ­vel excluir esta categoria pois existem {veiculos_usando} veÃ­culo(s) associado(s) a ela.', 'danger')
        return redirect(url_for('cadastrar_categoria_veiculo'))
    
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoria excluÃ­da com sucesso!', 'success')
    return redirect(url_for('cadastrar_categoria_veiculo'))

@app.route('/cadastros/veiculos', methods=['GET', 'POST'])
def cadastrar_veiculo():
    # Verificar se existem categorias
    categorias_existentes = CategoriaVeiculo.query.all()
    if not categorias_existentes:
        flash('Ã‰ necessÃ¡rio cadastrar pelo menos uma categoria de veÃ­culo antes de cadastrar veÃ­culos.', 'warning')
        return redirect(url_for('cadastrar_categoria_veiculo'))
    
    form = VeiculoForm()
    form.id_categoria_veiculo.choices = [(c.id_categoria_veiculo, c.nome) for c in categorias_existentes]
    if form.validate_on_submit():
        novo = Veiculo(
            nome=form.nome.data,
            modelo=form.modelo.data,
            marca=form.marca.data,
            ano=form.ano.data,
            placa=form.placa.data,
            cor=form.cor.data,
            combustivel=form.combustivel.data,
            capacidade_passageiros=form.capacidade_passageiros.data,
            observacoes=form.observacoes.data,
            id_categoria_veiculo=form.id_categoria_veiculo.data
        )
        db.session.add(novo)
        db.session.commit()
        flash('VeÃ­culo cadastrado com sucesso!', 'success')
        return redirect(url_for('cadastrar_veiculo'))
    veiculos = Veiculo.query.all()
    return render_template('veiculos.html', form=form, veiculos=veiculos)

@app.route('/cadastros/veiculos/editar/<int:id>', methods=['GET', 'POST'])
def editar_veiculo(id):
    # Verificar se existem categorias
    categorias_existentes = CategoriaVeiculo.query.all()
    if not categorias_existentes:
        flash('Ã‰ necessÃ¡rio cadastrar pelo menos uma categoria de veÃ­culo antes de editar veÃ­culos.', 'warning')
        return redirect(url_for('cadastrar_categoria_veiculo'))
    
    veiculo = Veiculo.query.get_or_404(id)
    form = VeiculoForm(obj=veiculo)
    form.id_categoria_veiculo.choices = [(c.id_categoria_veiculo, c.nome) for c in categorias_existentes]
    if form.validate_on_submit():
        veiculo.nome = form.nome.data
        veiculo.modelo = form.modelo.data
        veiculo.marca = form.marca.data
        veiculo.ano = form.ano.data
        veiculo.placa = form.placa.data
        veiculo.cor = form.cor.data
        veiculo.combustivel = form.combustivel.data
        veiculo.capacidade_passageiros = form.capacidade_passageiros.data
        veiculo.observacoes = form.observacoes.data
        veiculo.id_categoria_veiculo = form.id_categoria_veiculo.data
        db.session.commit()
        flash('VeÃ­culo atualizado com sucesso!', 'success')
        return redirect(url_for('cadastrar_veiculo'))
    veiculos = Veiculo.query.all()
    return render_template('veiculos.html', form=form, veiculos=veiculos)

@app.route('/cadastros/veiculos/excluir/<int:id>')
def excluir_veiculo(id):
    veiculo = Veiculo.query.get_or_404(id)
    # VeÃ­culos normalmente nÃ£o tÃªm dependÃªncias diretas no sistema atual
    # Mas se houver tabelas de relacionamento no futuro, adicionar aqui
    db.session.delete(veiculo)
    db.session.commit()
    flash('VeÃ­culo excluÃ­do com sucesso!', 'success')
    return redirect(url_for('cadastrar_veiculo'))

@app.route('/cadastros/despesas', methods=['GET', 'POST'])
def cadastrar_despesa():
    # Verificar se existem categorias
    categorias_existentes = CategoriaDespesa.query.all()
    if not categorias_existentes:
        flash('Ã‰ necessÃ¡rio cadastrar pelo menos uma categoria de despesa antes de cadastrar despesas.', 'warning')
        return redirect(url_for('cadastrar_categoria_despesa'))
    
    form = DespesaForm()
    form.id_categoria_despesa.choices = [(c.id_categoria_despesa, c.nome) for c in categorias_existentes]
    
    if form.validate_on_submit():
        # Converter valor mÃ©dio para float
        valor_medio = None
        if form.valor_medio_despesa.data:
            try:
                valor_medio = float(form.valor_medio_despesa.data.replace(',', '.'))
            except ValueError:
                flash('Valor mÃ©dio deve ser um nÃºmero vÃ¡lido.', 'danger')
                despesas = Despesa.query.all()
                return render_template('despesas.html', form=form, despesas=despesas)
        
        nova = Despesa(
            nome=form.nome.data, 
            id_categoria_despesa=form.id_categoria_despesa.data,
            id_tipo_despesa=form.id_tipo_despesa.data,
            valor_medio_despesa=valor_medio
        )
        db.session.add(nova)
        db.session.commit()
        flash('Despesa cadastrada com sucesso!', 'success')
        return redirect(url_for('cadastrar_despesa'))
    despesas = Despesa.query.order_by(Despesa.nome).all()
    return render_template('despesas.html', form=form, despesas=despesas)

@app.route('/cadastros/despesas/editar/<int:id>', methods=['GET', 'POST'])
def editar_despesa(id):
    # Verificar se existem categorias
    categorias_existentes = CategoriaDespesa.query.all()
    if not categorias_existentes:
        flash('Ã‰ necessÃ¡rio cadastrar pelo menos uma categoria de despesa antes de editar despesas.', 'warning')
        return redirect(url_for('cadastrar_categoria_despesa'))
    
    despesa = Despesa.query.get_or_404(id)
    form = DespesaForm(obj=despesa)
    form.id_categoria_despesa.choices = [(c.id_categoria_despesa, c.nome) for c in categorias_existentes]
    
    # Preencher o valor mÃ©dio no formato brasileiro
    if request.method == 'GET' and despesa.valor_medio_despesa:
        form.valor_medio_despesa.data = str(despesa.valor_medio_despesa).replace('.', ',')
    
    if form.validate_on_submit():
        # Converter valor mÃ©dio para float
        valor_medio = None
        if form.valor_medio_despesa.data:
            try:
                valor_medio = float(form.valor_medio_despesa.data.replace(',', '.'))
            except ValueError:
                flash('Valor mÃ©dio deve ser um nÃºmero vÃ¡lido.', 'danger')
                despesas = Despesa.query.all()
                return render_template('despesas.html', form=form, despesas=despesas)
        
        despesa.nome = form.nome.data
        despesa.id_categoria_despesa = form.id_categoria_despesa.data
        despesa.id_tipo_despesa = form.id_tipo_despesa.data
        despesa.valor_medio_despesa = valor_medio
        db.session.commit()
        flash('Despesa atualizada com sucesso!', 'success')
        return redirect(url_for('cadastrar_despesa'))
    despesas = Despesa.query.all()
    return render_template('despesas.html', form=form, despesas=despesas)

@app.route('/cadastros/despesas/excluir/<int:id>')
def excluir_despesa(id):
    despesa = Despesa.query.get_or_404(id)
    
    # Verificar se existem eventos usando esta despesa
    eventos_usando = DespesaEvento.query.filter_by(id_despesa=id).count()
    if eventos_usando > 0:
        flash(f'NÃ£o Ã© possÃ­vel excluir esta despesa pois existem {eventos_usando} registro(s) de despesa em evento(s) associado(s) a ela.', 'danger')
        return redirect(url_for('cadastrar_despesa'))
    
    db.session.delete(despesa)
    db.session.commit()
    flash('Despesa excluÃ­da com sucesso!', 'success')
    return redirect(url_for('cadastrar_despesa'))

@app.route('/eventos/<int:id_evento>/despesas', methods=['GET', 'POST'])
def cadastrar_despesa_evento(id_evento):
    evento = Evento.query.get_or_404(id_evento)
    
    # Verificar se existem categorias
    categorias_existentes = CategoriaDespesa.query.all()
    if not categorias_existentes:
        flash('Ã‰ necessÃ¡rio cadastrar pelo menos uma categoria de despesa antes de cadastrar despesas.', 'warning')
        return redirect(url_for('cadastrar_categoria_despesa'))
    
    form = DespesaForm()
    form.id_categoria_despesa.choices = [(c.id_categoria_despesa, c.nome) for c in categorias_existentes]
    # Filtrar apenas tipos de evento (1 e 2)
    form.id_tipo_despesa.choices = [
        (1, 'Fixas - Evento'),
        (2, 'VariÃ¡veis - Evento')
    ]
    
    if form.validate_on_submit():
        # Converter valor mÃ©dio para float
        valor_medio = None
        if form.valor_medio_despesa.data:
            try:
                valor_medio = float(form.valor_medio_despesa.data.replace(',', '.'))
            except ValueError:
                flash('Valor mÃ©dio deve ser um nÃºmero vÃ¡lido.', 'danger')
                # Buscar apenas despesas de evento
                despesas = Despesa.query.filter(Despesa.id_tipo_despesa.in_([1, 2])).all()
                return render_template('despesas_evento.html', form=form, despesas=despesas, evento=evento)
        
        nova = Despesa(
            nome=form.nome.data, 
            id_categoria_despesa=form.id_categoria_despesa.data,
            id_tipo_despesa=form.id_tipo_despesa.data,
            valor_medio_despesa=valor_medio
        )
        db.session.add(nova)
        db.session.commit()
        flash('Despesa cadastrada com sucesso!', 'success')
        return redirect(url_for('cadastrar_despesa_evento', id_evento=id_evento))
    
    # Buscar apenas despesas de evento
    despesas = Despesa.query.filter(Despesa.id_tipo_despesa.in_([1, 2])).all()
    return render_template('despesas_evento.html', form=form, despesas=despesas, evento=evento)

@app.route('/eventos/<int:id_evento>/salvar-despesa', methods=['POST'])
def salvar_despesa_individual(id_evento):
    """Salva ou atualiza uma despesa individual via AJAX"""
    evento = Evento.query.get_or_404(id_evento)
    
    try:
        data = request.get_json()
        
        # Validar dados
        despesa_id = data.get('despesa_id')
        valor_str = data.get('valor', '')
        data_despesa = data.get('data')
        status_pagamento = data.get('status_pagamento', 'pendente')
        forma_pagamento = data.get('forma_pagamento', 'dÃ©bito')
        pago_por = data.get('pago_por', '')
        observacoes = data.get('observacoes', '')
        id_fornecedor = data.get('id_fornecedor', None)  # Novo campo
        is_fixa = data.get('is_fixa', False)  # Flag para identificar despesas fixas
        
        print(f"=== SALVAMENTO INDIVIDUAL VIA AJAX ===")
        print(f"Despesa ID: {despesa_id}")
        print(f"Valor recebido: '{valor_str}'")
        print(f"Fornecedor ID: {id_fornecedor}")
        print(f"Ã‰ despesa fixa: {is_fixa}")
        
        if not despesa_id or not valor_str:
            return jsonify({'success': False, 'message': 'Despesa e valor sÃ£o obrigatÃ³rios'})
        
        # Converter valor - tratar tanto formato brasileiro quanto americano
        try:
            valor_str = str(valor_str).strip()
            
            # Se contÃ©m ponto e vÃ­rgula, Ã© formato brasileiro (ex: 1.000,50)
            if '.' in valor_str and ',' in valor_str:
                # Remover pontos de milhares e trocar vÃ­rgula por ponto
                valor_str = valor_str.replace('.', '').replace(',', '.')
            # Se contÃ©m apenas vÃ­rgula, trocar por ponto
            elif ',' in valor_str and '.' not in valor_str:
                valor_str = valor_str.replace(',', '.')
            
            valor_float = float(valor_str)
            
            if valor_float <= 0:
                return jsonify({'success': False, 'message': 'Valor deve ser maior que zero'})
                
        except (ValueError, TypeError) as e:
            print(f"Erro ao converter valor '{data.get('valor')}': {e}")
            return jsonify({'success': False, 'message': 'Valor invÃ¡lido'})
        
        # Verificar se a despesa jÃ¡ existe para este evento
        despesa_existente = DespesaEvento.query.filter_by(
            id_evento=id_evento, 
            id_despesa=despesa_id
        ).first()
        
        # Converter data
        data_obj = datetime.strptime(data_despesa, '%Y-%m-%d').date() if data_despesa else date.today()
        fornecedor_id = int(id_fornecedor) if id_fornecedor and id_fornecedor != '0' else None
        
        if despesa_existente:
            # ATUALIZAR despesa existente (comum para despesas fixas)
            print(f"âœ… Atualizando despesa existente ID {despesa_existente.id_despesa_evento}")
            print(f"   Valor antigo: {despesa_existente.valor} â†' Valor novo: {valor_float}")
            
            despesa_existente.data = data_obj
            despesa_existente.valor = valor_float
            despesa_existente.status_pagamento = status_pagamento
            despesa_existente.forma_pagamento = forma_pagamento
            despesa_existente.pago_por = pago_por
            despesa_existente.observacoes = observacoes
            despesa_existente.id_fornecedor = fornecedor_id  # Novo campo
            
            # Se foi informado um fornecedor, adicionar automaticamente na tabela fornecedor_evento
            if fornecedor_id:
                fornecedor_evento_existente = FornecedorEvento.query.filter_by(
                    id_evento=id_evento,
                    id_fornecedor=fornecedor_id
                ).first()
                
                if not fornecedor_evento_existente:
                    novo_fornecedor_evento = FornecedorEvento(
                        id_evento=id_evento,
                        id_fornecedor=fornecedor_id,
                        observacoes=observacoes if observacoes else ''
                    )
                    db.session.add(novo_fornecedor_evento)
                    print(f"âœ… Fornecedor {fornecedor_id} adicionado automaticamente ao evento")
            
            db.session.commit()
            
            print(f"âœ… Despesa atualizada com sucesso!")
            
            # Buscar dados da despesa para retornar
            despesa = Despesa.query.get(despesa_id)
            fornecedor = Fornecedor.query.get(fornecedor_id) if fornecedor_id else None
            
            return jsonify({
                'success': True, 
                'message': 'Despesa atualizada com sucesso!',
                'despesa_evento_id': despesa_existente.id_despesa_evento,
                'despesa_nome': despesa.nome,
                'fornecedor_nome': fornecedor.nome if fornecedor else None,
                'valor_salvo': valor_float,
                'action': 'updated'
            })
        else:
            # CRIAR nova despesa no evento (comum para despesas variÃ¡veis)
            print(f"ðŸ†• Criando nova despesa no evento")
            
            nova_despesa = DespesaEvento(
                id_evento=id_evento,
                id_despesa=int(despesa_id),
                data=data_obj,
                valor=valor_float,
                status_pagamento=status_pagamento,
                forma_pagamento=forma_pagamento,
                pago_por=pago_por,
                observacoes=observacoes,
                id_fornecedor=fornecedor_id  # Novo campo
            )
            
            db.session.add(nova_despesa)
            
            # Se foi informado um fornecedor, adicionar automaticamente na tabela fornecedor_evento
            if fornecedor_id:
                fornecedor_evento_existente = FornecedorEvento.query.filter_by(
                    id_evento=id_evento,
                    id_fornecedor=fornecedor_id
                ).first()
                
                if not fornecedor_evento_existente:
                    novo_fornecedor_evento = FornecedorEvento(
                        id_evento=id_evento,
                        id_fornecedor=fornecedor_id,
                        observacoes=observacoes if observacoes else ''
                    )
                    db.session.add(novo_fornecedor_evento)
                    print(f"âœ… Fornecedor {fornecedor_id} adicionado automaticamente ao evento")
            
            db.session.commit()
            
            print(f"âœ… Nova despesa criada com sucesso! ID: {nova_despesa.id_despesa_evento}")
            
            # Buscar dados da despesa para retornar
            despesa = Despesa.query.get(despesa_id)
            fornecedor = Fornecedor.query.get(fornecedor_id) if fornecedor_id else None
            
            return jsonify({
                'success': True, 
                'message': 'Despesa salva com sucesso!',
                'despesa_evento_id': nova_despesa.id_despesa_evento,
                'despesa_nome': despesa.nome,
                'fornecedor_nome': fornecedor.nome if fornecedor else None,
                'valor_salvo': valor_float,
                'action': 'created'
            })
        
    except Exception as e:
        db.session.rollback()
        print(f"âŒ ERRO ao salvar despesa: {e}")
        return jsonify({'success': False, 'message': f'Erro ao salvar despesa: {str(e)}'})

@app.template_filter('date_br')
def date_br(value):
    if isinstance(value, str) and '-' in value:
        y, m, d = value.split('-')
        return f'{d}/{m}/{y}'
    if isinstance(value, (date, datetime)):
        return value.strftime('%d/%m/%Y')
    return value

# =============== ROTAS PARA EQUIPE DO EVENTO ===============
@app.route('/eventos/<int:id_evento>/equipe', methods=['GET', 'POST'])
def equipe_evento(id_evento):
    evento = Evento.query.get_or_404(id_evento)
    
    # Verificar se existem colaboradores
    colaboradores_existentes = Colaborador.query.all()
    if not colaboradores_existentes:
        flash('Ã‰ necessÃ¡rio cadastrar pelo menos um colaborador antes de adicionar equipe ao evento.', 'warning')
        return redirect(url_for('cadastrar_colaborador'))
    
    form = EquipeEventoForm()
    form.id_colaborador.choices = [(0, 'Selecione um colaborador')] + [(c.id_colaborador, c.nome) for c in colaboradores_existentes]
    
    if form.validate_on_submit():
        # Verificar se o colaborador jÃ¡ estÃ¡ na equipe do evento
        equipe_existente = EquipeEvento.query.filter_by(
            id_evento=id_evento,
            id_colaborador=form.id_colaborador.data
        ).first()
        
        if equipe_existente:
            flash('Este colaborador jÃ¡ faz parte da equipe deste evento.', 'warning')
        else:
            nova_equipe = EquipeEvento(
                id_evento=id_evento,
                id_colaborador=form.id_colaborador.data,
                funcao=form.funcao.data,
                observacoes=form.observacoes.data
            )
            db.session.add(nova_equipe)
            db.session.commit()
            flash('Colaborador adicionado Ã  equipe com sucesso!', 'success')
        return redirect(url_for('equipe_evento', id_evento=id_evento))
    
    equipe_evento = EquipeEvento.query.filter_by(id_evento=id_evento).all()
    return render_template('equipe_evento.html', form=form, equipe_evento=equipe_evento, evento=evento)

@app.route('/eventos/<int:id_evento>/equipe/editar/<int:id>', methods=['GET', 'POST'])
def editar_equipe_evento(id_evento, id):
    evento = Evento.query.get_or_404(id_evento)
    equipe = EquipeEvento.query.get_or_404(id)
    
    colaboradores_existentes = Colaborador.query.all()
    form = EquipeEventoForm(obj=equipe)
    form.id_colaborador.choices = [(c.id_colaborador, c.nome) for c in colaboradores_existentes]
    
    if form.validate_on_submit():
        # Verificar se outro colaborador jÃ¡ estÃ¡ na equipe (exceto o atual)
        equipe_existente = EquipeEvento.query.filter_by(
            id_evento=id_evento,
            id_colaborador=form.id_colaborador.data
        ).filter(EquipeEvento.id_equipe_evento != id).first()
        
        if equipe_existente:
            flash('Este colaborador jÃ¡ faz parte da equipe deste evento.', 'warning')
        else:
            equipe.id_colaborador = form.id_colaborador.data
            equipe.funcao = form.funcao.data
            equipe.observacoes = form.observacoes.data
            db.session.commit()
            flash('Equipe atualizada com sucesso!', 'success')
        return redirect(url_for('equipe_evento', id_evento=id_evento))
    
    equipe_evento = EquipeEvento.query.filter_by(id_evento=id_evento).all()
    return render_template('equipe_evento.html', form=form, equipe_evento=equipe_evento, evento=evento)

@app.route('/eventos/<int:id_evento>/equipe/excluir/<int:id>')
def excluir_equipe_evento(id_evento, id):
    equipe = EquipeEvento.query.get_or_404(id)
    db.session.delete(equipe)
    db.session.commit()
    flash('Colaborador removido da equipe com sucesso!', 'success')
    return redirect(url_for('equipe_evento', id_evento=id_evento))

# =============== ROTAS PARA ELENCO DO EVENTO ===============
@app.route('/eventos/<int:id_evento>/elenco', methods=['GET', 'POST'])
def elenco_evento(id_evento):
    evento = Evento.query.get_or_404(id_evento)
    
    # Verificar se existem membros do elenco
    elencos_existentes = Elenco.query.all()
    if not elencos_existentes:
        flash('Ã‰ necessÃ¡rio cadastrar pelo menos um membro do elenco antes de adicionar ao evento.', 'warning')
        return redirect(url_for('cadastrar_elenco'))
    
    form = ElencoEventoForm()
    form.id_elenco.choices = [(0, 'Selecione um membro do elenco')] + [(e.id_elenco, e.nome) for e in elencos_existentes]
    
    if form.validate_on_submit():
        # Verificar se o elenco jÃ¡ estÃ¡ no evento
        elenco_existente = ElencoEvento.query.filter_by(
            id_evento=id_evento,
            id_elenco=form.id_elenco.data
        ).first()
        
        if elenco_existente:
            flash('Este membro do elenco jÃ¡ faz parte deste evento.', 'warning')
        else:
            novo_elenco = ElencoEvento(
                id_evento=id_evento,
                id_elenco=form.id_elenco.data,
                observacoes=form.observacoes.data
            )
            db.session.add(novo_elenco)
            db.session.commit()
            flash('Membro do elenco adicionado ao evento com sucesso!', 'success')
        return redirect(url_for('elenco_evento', id_evento=id_evento))
    
    elenco_evento = ElencoEvento.query.filter_by(id_evento=id_evento).all()
    return render_template('elenco_evento.html', form=form, elenco_evento=elenco_evento, evento=evento)

@app.route('/eventos/<int:id_evento>/elenco/editar/<int:id>', methods=['GET', 'POST'])
def editar_elenco_evento(id_evento, id):
    evento = Evento.query.get_or_404(id_evento)
    elenco_evt = ElencoEvento.query.get_or_404(id)
    
    elencos_existentes = Elenco.query.all()
    form = ElencoEventoForm(obj=elenco_evt)
    form.id_elenco.choices = [(e.id_elenco, e.nome) for e in elencos_existentes]
    
    if form.validate_on_submit():
        # Verificar se outro elenco jÃ¡ estÃ¡ no evento (exceto o atual)
        elenco_existente = ElencoEvento.query.filter_by(
            id_evento=id_evento,
            id_elenco=form.id_elenco.data
        ).filter(ElencoEvento.id_elenco_evento != id).first()
        
        if elenco_existente:
            flash('Este membro do elenco jÃ¡ faz parte deste evento.', 'warning')
        else:
            elenco_evt.id_elenco = form.id_elenco.data
            elenco_evt.observacoes = form.observacoes.data
            db.session.commit()
            flash('Elenco do evento atualizado com sucesso!', 'success')
        return redirect(url_for('elenco_evento', id_evento=id_evento))
    
    elenco_evento = ElencoEvento.query.filter_by(id_evento=id_evento).all()
    return render_template('elenco_evento.html', form=form, elenco_evento=elenco_evento, evento=evento)

@app.route('/eventos/<int:id_evento>/elenco/excluir/<int:id>')
def excluir_elenco_evento(id_evento, id):
    elenco_evt = ElencoEvento.query.get_or_404(id)
    db.session.delete(elenco_evt)
    db.session.commit()
    flash('Membro do elenco removido do evento com sucesso!', 'success')
    return redirect(url_for('elenco_evento', id_evento=id_evento))

# =============== ROTAS PARA FORNECEDORES DO EVENTO ===============
@app.route('/eventos/<int:id_evento>/fornecedores', methods=['GET', 'POST'])
def fornecedor_evento(id_evento):
    evento = Evento.query.get_or_404(id_evento)
    
    # Verificar se existem fornecedores
    fornecedores_existentes = Fornecedor.query.all()
    if not fornecedores_existentes:
        flash('Ã‰ necessÃ¡rio cadastrar pelo menos um fornecedor antes de adicionar ao evento.', 'warning')
        return redirect(url_for('cadastrar_fornecedor'))
    
    form = FornecedorEventoForm()
    form.id_fornecedor.choices = [(0, 'Selecione um fornecedor')] + [(f.id_fornecedor, f.nome) for f in fornecedores_existentes]
    
    if form.validate_on_submit():
        # Verificar se o fornecedor jÃ¡ estÃ¡ no evento
        fornecedor_existente = FornecedorEvento.query.filter_by(
            id_evento=id_evento,
            id_fornecedor=form.id_fornecedor.data
        ).first()
        
        if fornecedor_existente:
            flash('Este fornecedor jÃ¡ faz parte deste evento.', 'warning')
        else:
            novo_fornecedor = FornecedorEvento(
                id_evento=id_evento,
                id_fornecedor=form.id_fornecedor.data,
                observacoes=form.observacoes.data
            )
            db.session.add(novo_fornecedor)
            db.session.commit()
            flash('Fornecedor adicionado ao evento com sucesso!', 'success')
        return redirect(url_for('fornecedor_evento', id_evento=id_evento))
    
    fornecedor_evento = FornecedorEvento.query.filter_by(id_evento=id_evento).all()
    return render_template('fornecedor_evento.html', form=form, fornecedor_evento=fornecedor_evento, evento=evento)

@app.route('/eventos/<int:id_evento>/fornecedores/editar/<int:id>', methods=['GET', 'POST'])
def editar_fornecedor_evento(id_evento, id):
    evento = Evento.query.get_or_404(id_evento)
    fornecedor_evt = FornecedorEvento.query.get_or_404(id)
    
    fornecedores_existentes = Fornecedor.query.all()
    form = FornecedorEventoForm(obj=fornecedor_evt)
    form.id_fornecedor.choices = [(f.id_fornecedor, f.nome) for f in fornecedores_existentes]
    
    if form.validate_on_submit():
        # Verificar se outro fornecedor jÃ¡ estÃ¡ no evento (exceto o atual)
        fornecedor_existente = FornecedorEvento.query.filter_by(
            id_evento=id_evento,
            id_fornecedor=form.id_fornecedor.data
        ).filter(FornecedorEvento.id_fornecedor_evento != id).first()
        
        if fornecedor_existente:
            flash('Este fornecedor jÃ¡ faz parte deste evento.', 'warning')
        else:
            fornecedor_evt.id_fornecedor = form.id_fornecedor.data
            fornecedor_evt.observacoes = form.observacoes.data
            db.session.commit()
            flash('Fornecedor do evento atualizado com sucesso!', 'success')
        return redirect(url_for('fornecedor_evento', id_evento=id_evento))
    
    fornecedor_evento = FornecedorEvento.query.filter_by(id_evento=id_evento).all()
    return render_template('fornecedor_evento.html', form=form, fornecedor_evento=fornecedor_evento, evento=evento)

@app.route('/eventos/<int:id_evento>/fornecedores/excluir/<int:id>')
def excluir_fornecedor_evento(id_evento, id):
    fornecedor_evt = FornecedorEvento.query.get_or_404(id)
    db.session.delete(fornecedor_evt)
    db.session.commit()
    flash('Fornecedor removido do evento com sucesso!', 'success')
    return redirect(url_for('fornecedor_evento', id_evento=id_evento))

@app.route('/eventos/<int:id_evento>/excluir-receita/<int:receita_evento_id>', methods=['DELETE'])
def excluir_receita_evento(id_evento, receita_evento_id):
    try:
        # Verificar se o evento existe
        evento = Evento.query.get(id_evento)
        if not evento:
            return jsonify({'success': False, 'message': 'Evento nÃ£o encontrado'})
        
        # Buscar a receita do evento
        receita_evento = ReceitaEvento.query.filter_by(
            id_receita_evento=receita_evento_id,
            id_evento=id_evento
        ).first()
        
        if not receita_evento:
            return jsonify({'success': False, 'message': 'Receita nÃ£o encontrada neste evento'})
        
        # Excluir a receita do evento
        db.session.delete(receita_evento)
        db.session.commit()
        
        print(f"âœ… Receita excluÃ­da do evento: ID {receita_evento_id}")
        
        return jsonify({
            'success': True, 
            'message': 'Receita excluÃ­da com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"âŒ Erro ao excluir receita: {e}")
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})

@app.route('/eventos/<int:id_evento>/atualizar-receita/<int:receita_evento_id>', methods=['PUT'])
def atualizar_receita_evento(id_evento, receita_evento_id):
    try:
        # Verificar se o evento existe
        evento = Evento.query.get(id_evento)
        if not evento:
            return jsonify({'success': False, 'message': 'Evento nÃ£o encontrado'})
        
        # Buscar a receita do evento
        receita_evento = ReceitaEvento.query.filter_by(
            id_receita_evento=receita_evento_id,
            id_evento=id_evento
        ).first()
        
        if not receita_evento:
            return jsonify({'success': False, 'message': 'Receita nÃ£o encontrada neste evento'})
        
        data = request.get_json()
        
        # Validar dados obrigatÃ³rios
        if not data.get('valor') or not data.get('data'):
            return jsonify({'success': False, 'message': 'Data e valor sÃ£o obrigatÃ³rios'})
        
        # Converter valor - tratar tanto formato brasileiro quanto americano
        try:
            valor_str = str(data['valor']).strip()
            
            # Se contÃ©m ponto e vÃ­rgula, Ã© formato brasileiro (ex: 1.000,50)
            if '.' in valor_str and ',' in valor_str:
                # Remover pontos de milhares e trocar vÃ­rgula por ponto
                valor_str = valor_str.replace('.', '').replace(',', '.')
            # Se contÃ©m apenas vÃ­rgula, trocar por ponto
            elif ',' in valor_str and '.' not in valor_str:
                valor_str = valor_str.replace(',', '.')
            
            valor = float(valor_str)
            
            if valor <= 0:
                return jsonify({'success': False, 'message': 'Valor deve ser maior que zero'})
                
        except (ValueError, TypeError) as e:
            print(f"Erro ao converter valor '{data['valor']}': {e}")
            return jsonify({'success': False, 'message': 'Valor invÃ¡lido'})
        
        # Converter data
        try:
            data_receita = datetime.strptime(data['data'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'success': False, 'message': 'Data invÃ¡lida'})
        
        # Atualizar receita do evento
        receita_evento.valor = valor
        receita_evento.data = data_receita
        receita_evento.observacoes = data.get('observacoes', '')
        
        db.session.commit()
        
        print(f"âœ… Receita atualizada no evento: ID {receita_evento_id}")
        
        return jsonify({
            'success': True, 
            'message': 'Receita atualizada com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"âŒ Erro ao atualizar receita: {e}")
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})

@app.route('/eventos/<int:id_evento>/excluir-despesa/<int:despesa_evento_id>', methods=['DELETE'])
def excluir_despesa_evento(id_evento, despesa_evento_id):
    try:
        # Verificar se o evento existe
        evento = Evento.query.get(id_evento)
        if not evento:
            return jsonify({'success': False, 'message': 'Evento nÃ£o encontrado'})
        
        # Buscar a despesa do evento
        despesa_evento = DespesaEvento.query.filter_by(
            id_despesa_evento=despesa_evento_id,
            id_evento=id_evento
        ).first()
        
        if not despesa_evento:
            return jsonify({'success': False, 'message': 'Despesa nÃ£o encontrada neste evento'})
        
        # Excluir a despesa do evento
        db.session.delete(despesa_evento)
        db.session.commit()
        
        print(f"âœ… Despesa excluÃ­da do evento: ID {despesa_evento_id}")
        
        return jsonify({
            'success': True, 
            'message': 'Despesa excluÃ­da com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"âŒ Erro ao excluir despesa: {e}")
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})

@app.route('/api/cidades/<string:estado>')
def api_cidades_por_estado(estado):
    """API para buscar cidades por estado"""
    try:
        # Dicionário de cidades por estado (pode ser movido para um arquivo separado)
        cidades_por_estado = {
            'AC': ['Rio Branco', 'Cruzeiro do Sul', 'Sena Madureira', 'Tarauacá', 'Feijó', 'Senador Guiomard', 'Plácido de Castro', 'Brasiléia', 'Xapuri', 'Epitaciolândia'],
            'AL': ['Maceió', 'Arapiraca', 'Palmeira dos Índios', 'Rio Largo', 'Penedo', 'União dos Palmares', 'São Miguel dos Campos', 'Santana do Ipanema', 'Delmiro Gouveia', 'Coruripe'],
            'AP': ['Macapá', 'Santana', 'Laranjal do Jari', 'Oiapoque', 'Mazagão', 'Porto Grande', 'Tartarugalzinho', 'Vitória do Jari', 'Ferreira Gomes', 'Pedra Branca do Amapari'],
            'AM': ['Manaus', 'Parintins', 'Itacoatiara', 'Manacapuru', 'Coari', 'Tefé', 'Tabatinga', 'Maués', 'São Gabriel da Cachoeira', 'Humaitá'],
            'BA': ['Salvador', 'Feira de Santana', 'Vitória da Conquista', 'Camaçari', 'Juazeiro', 'Ilhéus', 'Itabuna', 'Lauro de Freitas', 'Jequié', 'Teixeira de Freitas', 'Alagoinhas', 'Barreiras', 'Simões Filho', 'Paulo Afonso', 'Eunápolis', 'Porto Seguro'],
            'CE': ['Fortaleza', 'Caucaia', 'Juazeiro do Norte', 'Maracanaú', 'Sobral', 'Crato', 'Itapipoca', 'Maranguape', 'Iguatu', 'Quixadá', 'Canindé', 'Aquiraz', 'Pacatuba', 'Crateús', 'Russas'],
            'DF': ['Brasília', 'Gama', 'Taguatinga', 'Ceilândia', 'Sobradinho', 'Planaltina', 'Samambaia', 'Santa Maria', 'São Sebastião', 'Recanto das Emas'],
            'ES': ['Vitória', 'Cariacica', 'Serra', 'Vila Velha', 'Linhares', 'Colatina', 'Guarapari', 'São Mateus', 'Cachoeiro de Itapemirim', 'Aracruz', 'Viana', 'Nova Venécia', 'Barra de São Francisco'],
            'GO': ['Goiânia', 'Aparecida de Goiânia', 'Anápolis', 'Rio Verde', 'Luziânia', 'Águas Lindas de Goiás', 'Valparaíso de Goiás', 'Trindade', 'Formosa', 'Novo Gama', 'Itumbiara', 'Senador Canedo', 'Catalão', 'Jataí', 'Planaltina'],
            'MA': ['São Luís', 'Imperatriz', 'São José de Ribamar', 'Timon', 'Caxias', 'Codó', 'Paço do Lumiar', 'Açailândia', 'Bacabal', 'Balsas', 'Barra do Corda', 'Santa Inês', 'Pinheiro', 'Pedreiras'],
            'MT': ['Cuiabá', 'Várzea Grande', 'Rondonópolis', 'Sinop', 'Tangará da Serra', 'Cáceres', 'Sorriso', 'Lucas do Rio Verde', 'Barra do Garças', 'Primavera do Leste', 'Alta Floresta', 'Ponta Porã'],
            'MS': ['Campo Grande', 'Dourados', 'Três Lagoas', 'Corumbá', 'Ponta Porã', 'Naviraí', 'Nova Andradina', 'Sidrolândia', 'Maracaju', 'São Gabriel do Oeste', 'Coxim', 'Aquidauana'],
            'MG': ['Belo Horizonte', 'Uberlândia', 'Contagem', 'Juiz de Fora', 'Betim', 'Montes Claros', 'Ribeirão das Neves', 'Uberaba', 'Governador Valadares', 'Ipatinga', 'Sete Lagoas', 'Divinópolis', 'Santa Luzia', 'Ibirité', 'Poços de Caldas', 'Patos de Minas', 'Pouso Alegre', 'Teófilo Otoni', 'Barbacena', 'Sabará', 'Vespasiano', 'Conselheiro Lafaiete', 'Varginha', 'Itabira', 'Passos'],
            'PA': ['Belém', 'Ananindeua', 'Santarém', 'Marabá', 'Parauapebas', 'Castanhal', 'Abaetetuba', 'Cametá', 'Marituba', 'Bragança', 'Altamira', 'Itaituba', 'Tucuruí', 'Benevides'],
            'PB': ['João Pessoa', 'Campina Grande', 'Santa Rita', 'Patos', 'Bayeux', 'Sousa', 'Cajazeiras', 'Cabedelo', 'Guarabira', 'Mamanguape', 'Sapé', 'Itabaiana', 'Monteiro', 'Pombal'],
            'PR': ['Curitiba', 'Londrina', 'Maringá', 'Ponta Grossa', 'Cascavel', 'São José dos Pinhais', 'Foz do Iguaçu', 'Colombo', 'Guarapuava', 'Paranaguá', 'Araucária', 'Toledo', 'Apucarana', 'Pinhais', 'Campo Largo', 'Arapongas', 'Almirante Tamandaré', 'Umuarama', 'Paranavaí', 'Sarandi'],
            'PE': ['Recife', 'Jaboatão dos Guararapes', 'Olinda', 'Caruaru', 'Petrolina', 'Paulista', 'Cabo de Santo Agostinho', 'Camaragibe', 'Garanhuns', 'Vitória de Santo Antão', 'Igarassu', 'São Lourenço da Mata', 'Santa Cruz do Capibaribe', 'Abreu e Lima', 'Ipojuca', 'Serra Talhada', 'Araripina', 'Gravatá', 'Carpina'],
            'PI': ['Teresina', 'Parnaíba', 'Picos', 'Piripiri', 'Floriano', 'Campo Maior', 'Barras', 'União', 'Altos', 'Pedro II', 'Valença do Piauí', 'Esperantina', 'São Raimundo Nonato', 'Cocal'],
            'RJ': ['Rio de Janeiro', 'São Gonçalo', 'Duque de Caxias', 'Nova Iguaçu', 'Niterói', 'Belford Roxo', 'São João de Meriti', 'Campos dos Goytacazes', 'Petrópolis', 'Volta Redonda', 'Magé', 'Macaé', 'Itaboraí', 'Cabo Frio', 'Angra dos Reis', 'Nova Friburgo', 'Barra Mansa', 'Teresópolis', 'Mesquita', 'Nilópolis'],
            'RN': ['Natal', 'Mossoró', 'Parnamirim', 'São Gonçalo do Amarante', 'Macaíba', 'Ceará-Mirim', 'Caicó', 'Assu', 'Currais Novos', 'Nova Cruz', 'São José de Mipibu', 'Apodi', 'João Câmara', 'Pau dos Ferros'],
            'RS': ['Porto Alegre', 'Caxias do Sul', 'Pelotas', 'Canoas', 'Santa Maria', 'Gravataí', 'Viamão', 'Novo Hamburgo', 'São Leopoldo', 'Rio Grande', 'Alvorada', 'Passo Fundo', 'Sapucaia do Sul', 'Uruguaiana', 'Santa Cruz do Sul', 'Cachoeirinha', 'Bagé', 'Bento Gonçalves', 'Erechim', 'Guaíba', 'Cachoeira do Sul'],
            'RO': ['Porto Velho', 'Ji-Paraná', 'Ariquemes', 'Vilhena', 'Cacoal', 'Rolim de Moura', 'Guajará-Mirim', 'Jaru', 'Ouro Preto do Oeste', 'Machadinho do Oeste'],
            'RR': ['Boa Vista', 'Rorainópolis', 'Caracaraí', 'Alto Alegre', 'Mucajaí', 'São Luiz', 'São João da Baliza', 'Pacaraima', 'Iracema', 'Amajari'],
            'SC': ['Florianópolis', 'Joinville', 'Blumenau', 'São José', 'Criciúma', 'Chapecó', 'Itajaí', 'Lages', 'Jaraguá do Sul', 'Palhoça', 'Balneário Camboriú', 'Brusque', 'Tubarão', 'São Bento do Sul', 'Caçador', 'Camboriú', 'Navegantes', 'Concórdia', 'Rio do Sul', 'Araranguá'],
            'SP': ['São Paulo', 'Guarulhos', 'Campinas', 'São Bernardo do Campo', 'Santo André', 'Osasco', 'Ribeirão Preto', 'Sorocaba', 'Mauá', 'São José dos Campos', 'Mogi das Cruzes', 'Diadema', 'Jundiaí', 'Carapicuíba', 'Piracicaba', 'Bauru', 'Itaquaquecetuba', 'São Vicente', 'Franca', 'Guarujá', 'Taubaté', 'Praia Grande', 'Limeira', 'Suzano', 'Taboão da Serra', 'Sumaré', 'Barueri', 'Embu das Artes', 'São Carlos', 'Marília'],
            'SE': ['Aracaju', 'Nossa Senhora do Socorro', 'Lagarto', 'Itabaiana', 'São Cristóvão', 'Estância', 'Tobias Barreto', 'Simão Dias', 'Propriá', 'Capela'],
            'TO': ['Palmas', 'Araguaína', 'Gurupi', 'Porto Nacional', 'Paraíso do Tocantins', 'Colinas do Tocantins', 'Guaraí', 'Tocantinópolis', 'Miracema do Tocantins', 'Dianópolis']
        }
        
        estado_upper = estado.upper()
        
        if estado_upper not in cidades_por_estado:
            return jsonify({
                'success': False,
                'message': 'Estado não encontrado'
            }), 404
        
        cidades = cidades_por_estado[estado_upper]
        
        return jsonify({
            'success': True,
            'estado': estado_upper,
            'cidades': cidades,
            'total': len(cidades)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar cidades: {str(e)}'
        }), 500

@app.route('/api/fornecedores-busca')
def api_fornecedores_busca():
    """API para buscar fornecedores com priorizaÃ§Ã£o por localizaÃ§Ã£o"""
    try:
        # ParÃ¢metros de busca
        termo_busca = request.args.get('q', '').strip()
        cidade_evento = request.args.get('cidade', '').strip()
        estado_evento = request.args.get('estado', '').strip()
        
        # Query base
        query = Fornecedor.query
        
        # Se hÃ¡ termo de busca, filtrar por nome
        if termo_busca:
            query = query.filter(Fornecedor.nome.ilike(f'%{termo_busca}%'))
        
        # Buscar todos os fornecedores que atendem ao critÃ©rio
        fornecedores = query.all()
        
        # Separar fornecedores por prioridade
        fornecedores_locais = []
        fornecedores_outros = []
        
        for fornecedor in fornecedores:
            # Priorizar fornecedores da mesma cidade/estado
            if (fornecedor.cidade and fornecedor.estado and 
                cidade_evento and estado_evento and
                fornecedor.cidade.lower() == cidade_evento.lower() and 
                fornecedor.estado.lower() == estado_evento.lower()):
                fornecedores_locais.append(fornecedor)
            else:
                fornecedores_outros.append(fornecedor)
        
        # Ordenar alfabeticamente dentro de cada grupo
        fornecedores_locais.sort(key=lambda x: x.nome.lower())
        fornecedores_outros.sort(key=lambda x: x.nome.lower())
        
        # Combinar listas (locais primeiro)
        fornecedores_ordenados = fornecedores_locais + fornecedores_outros
        
        # Preparar resposta JSON
        resultado = []
        for fornecedor in fornecedores_ordenados:
            resultado.append({
                'id': fornecedor.id_fornecedor,
                'nome': fornecedor.nome,
                'telefone': fornecedor.telefone or '',
                'cidade': fornecedor.cidade or '',
                'estado': fornecedor.estado or '',
                'categoria': fornecedor.categoria.nome if fornecedor.categoria else '',
                'is_local': fornecedor in fornecedores_locais
            })
        
        return jsonify({
            'success': True,
            'fornecedores': resultado,
            'total': len(resultado),
            'locais': len(fornecedores_locais),
            'outros': len(fornecedores_outros)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar fornecedores: {str(e)}'
        }), 500


# Rota para servir os arquivos
if __name__ == '__main__':
    app.run(debug=True)
