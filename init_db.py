from app import app
from extensions import db
from models import (
    Usuario,
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
        print("Banco de dados PostgreSQL inicializado.")
    else:
        print("Init DB só permitido em modo de desenvolvimento.")
