"""
Script para limpar a tabela alembic_version do PostgreSQL
"""
import os
import psycopg2
from psycopg2 import sql

def clean_alembic():
    """Limpar a tabela alembic_version"""
    try:
        # Conectar ao banco
        database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/socrates_online')
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        print(f"Conectando ao banco: {database_url[:50]}...")
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        
        # Verificar se a tabela existe
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'alembic_version'
            );
        """)
        exists = cur.fetchone()[0]
        
        if exists:
            # Ver versão atual
            try:
                cur.execute("SELECT version_num FROM alembic_version")
                current = cur.fetchone()
                if current:
                    print(f"Versão atual no banco: {current[0]}")
            except:
                pass
            
            # Limpar a tabela
            cur.execute("DELETE FROM alembic_version")
            conn.commit()
            print("Tabela alembic_version limpa com sucesso!")
        else:
            print("Tabela alembic_version não existe")
        
        # Fechar conexão
        cur.close()
        conn.close()
        
        print("\nPróximo passo: flask db migrate -m 'Initial migration'")
        return True
        
    except Exception as e:
        print(f"Erro: {e}")
        return False

if __name__ == "__main__":
    clean_alembic()
