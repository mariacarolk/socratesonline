
import os
from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from forms import LoginForm, RegisterForm
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

if __name__ == '__main__':
    app.run(debug=True)
