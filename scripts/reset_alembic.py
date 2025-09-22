"""
Script para resetar completamente as migrações usando SQLAlchemy
"""
import os
import sys
import shutil
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configura variável de ambiente
os.environ['FLASK_APP'] = 'app.py'

from app import app
from extensions import db

def reset_alembic():
    """Resetar as migrações"""
    with app.app_context():
        try:
            # Tentar limpar a tabela alembic_version
            result = db.session.execute(db.text("SELECT * FROM alembic_version"))
            current_version = result.fetchone()
            if current_version:
                print(f"Versão atual no banco: {current_version[0]}")
                
            # Limpar a tabela
            db.session.execute(db.text("DELETE FROM alembic_version"))
            db.session.commit()
            print("Tabela alembic_version limpa com sucesso!")
            
        except Exception as e:
            print(f"Erro ao limpar alembic_version: {e}")
            # Se a tabela não existir, não é problema
            if "does not exist" not in str(e):
                db.session.rollback()
        
        # Limpar diretório versions
        versions_dir = "migrations/versions"
        if os.path.exists(versions_dir):
            # Fazer backup primeiro
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = f"backups/versions_backup_{timestamp}"
            os.makedirs("backups", exist_ok=True)
            
            if os.listdir(versions_dir):  # Se não estiver vazio
                shutil.copytree(versions_dir, backup_dir)
                print(f"Backup das versões antigas salvo em: {backup_dir}")
            
            # Limpar o diretório
            for file in os.listdir(versions_dir):
                if file != '__init__.py':
                    os.remove(os.path.join(versions_dir, file))
            print("Diretório versions limpo!")
        
        print("\nMigrações resetadas com sucesso!")
        print("\nPróximos comandos:")
        print("1. flask db migrate -m 'Initial migration'")
        print("2. flask db upgrade")

if __name__ == "__main__":
    reset_alembic()
