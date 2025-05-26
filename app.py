from datetime import date, timedelta, datetime
import os
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from models import Circo, CategoriaColaborador, Colaborador, Elenco, CategoriaFornecedor, Fornecedor, CategoriaDespesa, CategoriaReceita, Despesa, Receita, Evento, ReceitaEvento, DespesaEvento
from forms import CircoForm, LoginForm, RegisterForm, CategoriaFornecedorForm, FornecedorForm, CategoriaDespesaForm, CategoriaReceitaForm, DespesaForm, ReceitaForm, EventoForm, CategoriaColaboradorForm, ColaboradorForm, ElencoForm
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from extensions import db

load_dotenv()  # Carrega variáveis do .env

app = Flask(__name__)
env = os.getenv("FLASK_ENV", "development")
if env == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

db.init_app(app)

from models import Usuario, CategoriaUsuario

@app.route('/')
def dashboard():
    print("Sessão atual:", dict(session)) #Carol retirar
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and check_password_hash(usuario.senha_hash, form.password.data):
            session['user_id'] = usuario.id
            session['categoria'] = usuario.categoria.nome.lower()
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('categoria', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    form.categoria.choices = [(c.id, c.nome) for c in CategoriaUsuario.query.all()]
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        novo = Usuario(
            nome=form.nome.data,
            email=form.email.data,
            senha_hash=hashed_password,
            categoria_id=form.categoria.data
        )
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/cadastros/circos', methods=['GET', 'POST'])
def cadastrar_circo():
    form = CircoForm()
    if form.validate_on_submit():
        novo = Circo(
            nome=form.nome.data,
            contato_responsavel=form.contato_responsavel.data,
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
        circo.observacoes = form.observacoes.data
        db.session.commit()
        flash('Circo atualizado com sucesso!', 'success')
        return redirect(url_for('cadastrar_circo'))
    circos = Circo.query.all()
    return render_template('cadastrar_circo.html', form=form, circos=circos)

@app.route('/cadastros/circos/excluir/<int:id>')
def excluir_circo(id):
    circo = Circo.query.get_or_404(id)
    db.session.delete(circo)
    db.session.commit()
    flash('Circo excluído com sucesso!', 'success')
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
    form = ColaboradorForm()
    form.id_categoria_colaborador.choices = [(c.id_categoria_colaborador, c.nome) for c in CategoriaColaborador.query.all()]
    if form.validate_on_submit():
        novo = Colaborador(
            nome=form.nome.data,
            id_categoria_colaborador=form.id_categoria_colaborador.data
        )
        db.session.add(novo)
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
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoria excluída com sucesso!', 'success')
    return redirect(url_for('cadastrar_categoria_colaborador'))

@app.route('/cadastros/colaboradores/editar/<int:id>', methods=['GET', 'POST'])
def editar_colaborador(id):
    colaborador = Colaborador.query.get_or_404(id)
    form = ColaboradorForm(obj=colaborador)
    form.id_categoria_colaborador.choices = [(c.id_categoria_colaborador, c.nome) for c in CategoriaColaborador.query.all()]
    if form.validate_on_submit():
        colaborador.nome = form.nome.data
        colaborador.id_categoria_colaborador = form.id_categoria_colaborador.data
        db.session.commit()
        flash('Colaborador atualizado com sucesso!', 'success')
        return redirect(url_for('cadastrar_colaborador'))
    colaboradores = Colaborador.query.all()
    return render_template('colaboradores.html', form=form, colaboradores=colaboradores)

@app.route('/cadastros/colaboradores/excluir/<int:id>')
def excluir_colaborador(id):
    colaborador = Colaborador.query.get_or_404(id)
    db.session.delete(colaborador)
    db.session.commit()
    flash('Colaborador excluído com sucesso!', 'success')
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
    flash('Integrante excluído com sucesso!', 'success')
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
    form = FornecedorForm()
    form.id_categoria_fornecedor.choices = [(c.id_categoria_fornecedor, c.nome) for c in CategoriaFornecedor.query.all()]
    if form.validate_on_submit():
        novo = Fornecedor(
            nome=form.nome.data,
            telefone=form.telefone.data,
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
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoria excluída com sucesso!', 'success')
    return redirect(url_for('cadastrar_categoria_fornecedor'))

@app.route('/cadastros/fornecedores/editar/<int:id>', methods=['GET', 'POST'])
def editar_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    form = FornecedorForm(obj=fornecedor)
    form.id_categoria_fornecedor.choices = [(c.id_categoria_fornecedor, c.nome) for c in CategoriaFornecedor.query.all()]
    if form.validate_on_submit():
        fornecedor.nome = form.nome.data
        fornecedor.telefone = form.telefone.data
        fornecedor.id_categoria_fornecedor = form.id_categoria_fornecedor.data
        db.session.commit()
        flash('Fornecedor atualizado com sucesso!', 'success')
        return redirect(url_for('cadastrar_fornecedor'))
    fornecedores = Fornecedor.query.all()
    return render_template('fornecedores.html', form=form, fornecedores=fornecedores)

@app.route('/cadastros/fornecedores/excluir/<int:id>')
def excluir_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    db.session.delete(fornecedor)
    db.session.commit()
    flash('Fornecedor excluído com sucesso!', 'success')
    return redirect(url_for('cadastrar_fornecedor'))

@app.route('/cadastros/receitas', methods=['GET', 'POST'])
def cadastrar_receita():
    form = ReceitaForm()
    form.id_categoria_receita.choices = [(c.id_categoria_receita, c.nome) for c in CategoriaReceita.query.all()]
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
    receita = Receita.query.get_or_404(id)
    form = ReceitaForm(obj=receita)
    form.id_categoria_receita.choices = [(c.id_categoria_receita, c.nome) for c in CategoriaReceita.query.all()]
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
    db.session.delete(receita)
    db.session.commit()
    flash('Receita excluída com sucesso!', 'success')
    return redirect(url_for('cadastrar_receita'))


@app.route('/cadastros/despesas', methods=['GET', 'POST'])
def cadastrar_despesa():
    form = DespesaForm()
    form.id_categoria_despesa.choices = [(c.id_categoria_despesa, c.nome) for c in CategoriaDespesa.query.all()]
    if form.validate_on_submit():
        nova = Despesa(nome=form.nome.data, id_categoria_despesa=form.id_categoria_despesa.data)
        db.session.add(nova)
        db.session.commit()
        flash('Despesa cadastrada com sucesso!', 'success')
        return redirect(url_for('cadastrar_despesa'))
    despesas = Despesa.query.all()
    return render_template('despesas.html', form=form, despesas=despesas)

@app.route('/cadastros/despesas/editar/<int:id>', methods=['GET', 'POST'])
def editar_despesa(id):
    despesa = Despesa.query.get_or_404(id)
    form = DespesaForm(obj=despesa)
    form.id_categoria_despesa.choices = [(c.id_categoria_despesa, c.nome) for c in CategoriaDespesa.query.all()]
    if form.validate_on_submit():
        despesa.nome = form.nome.data
        despesa.id_categoria_despesa = form.id_categoria_despesa.data
        db.session.commit()
        flash('Despesa atualizada com sucesso!', 'success')
        return redirect(url_for('cadastrar_despesa'))
    despesas = Despesa.query.all()
    return render_template('despesas.html', form=form, despesas=despesas)

@app.route('/cadastros/despesas/excluir/<int:id>')
def excluir_despesa(id):
    despesa = Despesa.query.get_or_404(id)
    db.session.delete(despesa)
    db.session.commit()
    flash('Despesa excluída com sucesso!', 'success')
    return redirect(url_for('cadastrar_despesa'))

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
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoria excluída com sucesso!', 'success')
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
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoria excluída com sucesso!', 'success')
    return redirect(url_for('cadastrar_categoria_despesa'))

@app.route('/eventos')
def listar_eventos():
    limite = date.today() - timedelta(days=90)
    eventos = Evento.query.filter(
        Evento.status.in_(['a realizar', 'em andamento', 'realizado']),
        Evento.data_inicio >= limite
    ).all()
    return render_template('eventos.html', eventos=eventos)

@app.route('/eventos/novo', methods=['GET', 'POST'])
def novo_evento():
    form = EventoForm()
    form.id_circo.choices = [(c.id_circo, c.nome) for c in Circo.query.all()]
    form.id_produtor.choices = [(p.id_colaborador, p.nome) for p in Colaborador.query.all()]
    categorias_receita = CategoriaReceita.query.all()
    categorias_despesa = CategoriaDespesa.query.all()

    if form.validate_on_submit():
        novo = Evento(
            nome=form.nome.data,
            data_inicio=form.data_inicio.data,
            data_fim=form.data_fim.data,
            cidade=form.cidade.data,
            estado=form.estado.data,
            endereco=form.endereco.data,
            id_circo=form.id_circo.data,
            id_produtor=form.id_produtor.data,
            status=form.status.data,
            observacoes=form.observacoes.data
        )
        db.session.add(novo)
        db.session.flush()

        receitas_ids = request.form.getlist('receita_id[]')
        valores = request.form.getlist('valor[]')
        observacoes = request.form.getlist('obs[]')

        for i in range(len(receitas_ids)):
            try:
                valor = float(valores[i].replace(',', '.'))
            except:
                continue
            if receitas_ids[i] and valor:
                db.session.add(ReceitaEvento(
                    id_evento=novo.id_evento,
                    id_receita=int(receitas_ids[i]),
                    valor=valor,
                    observacoes=observacoes[i]
                ))

        despesa_ids = request.form.getlist('despesa_id[]')
        datas_desp = request.form.getlist('despesa_data[]')
        valores_desp = request.form.getlist('despesa_valor[]')
        status_pag = request.form.getlist('despesa_status_pagamento[]')
        forma_pag = request.form.getlist('despesa_forma_pagamento[]')
        pago_por = request.form.getlist('despesa_pago_por[]')
        obs_desp = request.form.getlist('despesa_obs[]')

        for i in range(len(despesa_ids)):
            try:
                valor = float(valores_desp[i].replace(',', '.'))
                data = datetime.strptime(datas_desp[i], '%Y-%m-%d').date()
            except:
                continue
            if despesa_ids[i] and valor:
                db.session.add(DespesaEvento(
                    id_evento=novo.id_evento,
                    id_despesa=int(despesa_ids[i]),
                    data=data,
                    valor=valor,
                    status_pagamento=status_pag[i],
                    forma_pagamento=forma_pag[i],
                    pago_por=pago_por[i],
                    observacoes=obs_desp[i]
                ))

        db.session.commit()
        flash('Evento e despesas/receitas cadastrados com sucesso!', 'success')
        return redirect(url_for('listar_eventos'))

    categorias_receita_dict = {
        c.id_categoria_receita: [{'id_receita': r.id_receita, 'nome': r.nome}
                                 for r in Receita.query.filter_by(id_categoria_receita=c.id_categoria_receita)]
        for c in categorias_receita
    }

    categorias_despesa_dict = {
        c.id_categoria_despesa: [{'id_despesa': d.id_despesa, 'nome': d.nome}
                                 for d in Despesa.query.filter_by(id_categoria_despesa=c.id_categoria_despesa)]
        for c in categorias_despesa
    }

    return render_template(
        'novo_evento.html',
        form=form,
        categorias_receita=categorias_receita,
        categorias_receita_dict=categorias_receita_dict,
        categorias_despesa=categorias_despesa,
        categorias_despesa_dict=categorias_despesa_dict,
        receitas_salvas=[],
        despesas_salvas=[],
        current_date=date.today().isoformat()
    )

@app.route('/eventos/editar/<int:id>', methods=['GET', 'POST'])
def editar_evento(id):
    evento = Evento.query.get_or_404(id)
    form = EventoForm(obj=evento)
    form.id_circo.choices = [(c.id_circo, c.nome) for c in Circo.query.all()]
    form.id_produtor.choices = [(p.id_colaborador, p.nome) for p in Colaborador.query.all()]
    categorias_receita = CategoriaReceita.query.all()
    categorias_despesa = CategoriaDespesa.query.all()

    if form.validate_on_submit():
        evento.nome = form.nome.data
        evento.data_inicio = form.data_inicio.data
        evento.data_fim = form.data_fim.data
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

        db.session.commit()

        receitas_ids = request.form.getlist('receita_id[]')
        valores = request.form.getlist('valor[]')
        observacoes = request.form.getlist('obs[]')
        for i in range(len(receitas_ids)):
            try:
                valor = float(valores[i].replace(',', '.'))
            except:
                continue
            if receitas_ids[i] and valor:
                db.session.add(ReceitaEvento(
                    id_evento=evento.id_evento,
                    id_receita=int(receitas_ids[i]),
                    valor=valor,
                    observacoes=observacoes[i]
                ))

        despesa_ids = request.form.getlist('despesa_id[]')
        datas_desp = request.form.getlist('despesa_data[]')
        valores_desp = request.form.getlist('despesa_valor[]')
        status_pag = request.form.getlist('despesa_status_pagamento[]')
        forma_pag = request.form.getlist('despesa_forma_pagamento[]')
        pago_por = request.form.getlist('despesa_pago_por[]')
        obs_desp = request.form.getlist('despesa_obs[]')
        for i in range(len(despesa_ids)):
            try:
                valor = float(valores_desp[i].replace(',', '.'))
                data = datetime.strptime(datas_desp[i], '%Y-%m-%d').date()
            except:
                continue
            if despesa_ids[i] and valor:
                db.session.add(DespesaEvento(
                    id_evento=evento.id_evento,
                    id_despesa=int(despesa_ids[i]),
                    data=data,
                    valor=valor,
                    status_pagamento=status_pag[i],
                    forma_pagamento=forma_pag[i],
                    pago_por=pago_por[i],
                    observacoes=obs_desp[i]
                ))

        db.session.commit()
        flash('Evento atualizado com sucesso!', 'success')
        return redirect(url_for('listar_eventos'))

    categorias_receita_dict = {
        c.id_categoria_receita: [{'id_receita': r.id_receita, 'nome': r.nome}
                                 for r in Receita.query.filter_by(id_categoria_receita=c.id_categoria_receita)]
        for c in categorias_receita
    }

    categorias_despesa_dict = {
        c.id_categoria_despesa: [{'id_despesa': d.id_despesa, 'nome': d.nome}
                                 for d in Despesa.query.filter_by(id_categoria_despesa=c.id_categoria_despesa)]
        for c in categorias_despesa
    }

    receitas_salvas = ReceitaEvento.query.filter_by(id_evento=evento.id_evento).all()
    despesas_salvas = DespesaEvento.query.filter_by(id_evento=evento.id_evento).all()

    return render_template(
        'novo_evento.html',
        form=form,
        categorias_receita=categorias_receita,
        categorias_receita_dict=categorias_receita_dict,
        categorias_despesa=categorias_despesa,
        categorias_despesa_dict=categorias_despesa_dict,
        receitas_salvas=receitas_salvas,
        despesas_salvas=despesas_salvas,
        current_date=date.today().isoformat()
    )


@app.route('/eventos/excluir/<int:id>')
def excluir_evento(id):
    if session.get('categoria', '').lower() != 'administrativo':
        flash('Você não tem permissão para excluir eventos.', 'danger')
        return redirect(url_for('listar_eventos'))
    evento = Evento.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    flash('Evento excluído com sucesso!', 'success')
    return redirect(url_for('listar_eventos'))

if __name__ == '__main__':
    app.run(debug=True)