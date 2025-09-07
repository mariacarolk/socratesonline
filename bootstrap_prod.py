#!/usr/bin/env python3
"""
Bootstrap de produção: cria as tabelas diretamente no PostgreSQL usando SQLAlchemy,
sem rodar Alembic. Útil quando há problemas nas cadeias de migração e não há
necessidade de migrar dados existentes.
"""
import sys
from sqlalchemy import inspect

try:
    from app import app
    from extensions import db
except Exception as e:
    print(f"❌ Falha ao carregar app/db: {e}")
    sys.exit(1)


def main() -> int:
    with app.app_context():
        try:
            engine = db.engine
            inspector = inspect(engine)
            existing_tables = set(inspector.get_table_names())
        except Exception as e:
            print(f"❌ Erro ao inspecionar banco: {e}")
            return 1

        print(f"🔎 Tabelas existentes: {sorted(existing_tables)}")

        try:
            # Cria quaisquer tabelas que ainda não existam
            db.create_all()
            print("✅ Tabelas criadas/garantidas com sucesso (create_all)")
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())


