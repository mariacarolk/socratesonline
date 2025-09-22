import os
import sys

# Definir variável de ambiente para o banco PostgreSQL
os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres@localhost:5432/socrates_online'

# Importar e configurar app Flask
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from extensions import db

def add_columns():
    with app.app_context():
        try:
            # Executar SQL diretamente
            db.engine.execute("ALTER TABLE despesas_evento ADD COLUMN IF NOT EXISTS valor_pago_socrates FLOAT;")
            db.engine.execute("ALTER TABLE despesas_empresa ADD COLUMN IF NOT EXISTS valor_pago_socrates FLOAT;")
            print("✅ Colunas adicionadas com sucesso!")
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    add_columns()



