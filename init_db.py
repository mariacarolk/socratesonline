
from app import app
from extensions import db
from models import Usuario, CategoriaUsuario
import os

with app.app_context():
    if os.getenv("FLASK_ENV") == "development":
        db.create_all()
        if CategoriaUsuario.query.count() == 0:
            for nome in ["Produtor", "Coreógrafo", "Administrativo"]:
                db.session.add(CategoriaUsuario(nome=nome))
            db.session.commit()
        print("Banco de dados local inicializado.")
    else:
        print("Init DB só permitido em modo de desenvolvimento.")
