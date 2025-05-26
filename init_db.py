from app import app
from extensions import db
from models import (
    Usuario, CategoriaUsuario,
    Circo, CategoriaDespesa, Despesa,
    CategoriaReceita, Receita,
    CategoriaColaborador, Colaborador,
    CategoriaFornecedor, Fornecedor,
    Evento, DespesaEvento, ReceitaEvento,
    Elenco, ElencoEvento, EquipeEvento, FornecedorEvento
)
import os

with app.app_context():
    if os.getenv("FLASK_ENV") == "development":
        db.create_all()

        # Criar categorias de usuário padrão se estiver vazio
        if CategoriaUsuario.query.count() == 0:
            for nome in ["Produtor", "Coreógrafo", "Administrativo"]:
                db.session.add(CategoriaUsuario(nome=nome))
            db.session.commit()

        print("Banco de dados local inicializado.")
    else:
        print("Init DB só permitido em modo de desenvolvimento.")
