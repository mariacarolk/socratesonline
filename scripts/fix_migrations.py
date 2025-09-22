"""
Script para corrigir problemas de migração de forma definitiva
"""
import os
import sys
import shutil
from datetime import datetime
import subprocess
import psycopg2
from psycopg2 import sql
import json

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def backup_migrations():
    """Fazer backup da pasta de migrações atual"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backups/migrations_backup_{timestamp}"
    
    if os.path.exists("migrations"):
        print(f"📦 Fazendo backup das migrações em {backup_dir}")
        shutil.copytree("migrations", backup_dir)
        print("✅ Backup criado com sucesso")
    return backup_dir

def get_database_url():
    """Obter URL do banco de dados"""
    database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/socrates_online')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    return database_url

def clean_alembic_version():
    """Limpar a tabela alembic_version do banco"""
    try:
        database_url = get_database_url()
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
            # Backup da versão atual
            cur.execute("SELECT version_num FROM alembic_version")
            current_version = cur.fetchone()
            if current_version:
                print(f"📝 Versão atual no banco: {current_version[0]}")
            
            # Limpar a tabela
            cur.execute("DELETE FROM alembic_version")
            conn.commit()
            print("✅ Tabela alembic_version limpa")
        else:
            print("ℹ️ Tabela alembic_version não existe")
        
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Erro ao limpar alembic_version: {e}")
        return False

def export_current_schema():
    """Exportar o schema atual do banco de dados"""
    try:
        database_url = get_database_url()
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        
        # Obter lista de todas as tabelas
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            AND table_name != 'alembic_version'
            ORDER BY table_name;
        """)
        tables = cur.fetchall()
        
        schema_info = {}
        for (table_name,) in tables:
            # Obter colunas da tabela
            cur.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position;
            """, (table_name,))
            
            columns = cur.fetchall()
            
            # Obter constraints
            cur.execute("""
                SELECT constraint_name, constraint_type
                FROM information_schema.table_constraints
                WHERE table_name = %s;
            """, (table_name,))
            
            constraints = cur.fetchall()
            
            schema_info[table_name] = {
                'columns': columns,
                'constraints': constraints
            }
        
        cur.close()
        conn.close()
        
        # Salvar schema em arquivo JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        schema_file = f"backups/schema_backup_{timestamp}.json"
        os.makedirs("backups", exist_ok=True)
        
        with open(schema_file, 'w', encoding='utf-8') as f:
            json.dump(schema_info, f, indent=2, default=str)
        
        print(f"✅ Schema exportado para {schema_file}")
        return schema_info
    except Exception as e:
        print(f"❌ Erro ao exportar schema: {e}")
        return None

def reset_migrations():
    """Resetar completamente as migrações"""
    print("\n🔧 INICIANDO RESET DE MIGRAÇÕES\n")
    
    # 1. Fazer backup
    backup_dir = backup_migrations()
    
    # 2. Exportar schema atual
    schema = export_current_schema()
    
    # 3. Limpar versão do Alembic no banco
    clean_alembic_version()
    
    # 4. Remover pasta migrations/versions
    versions_dir = "migrations/versions"
    if os.path.exists(versions_dir):
        print(f"🗑️ Removendo {versions_dir}")
        shutil.rmtree(versions_dir)
        os.makedirs(versions_dir)
        # Criar arquivo __init__.py vazio
        with open(os.path.join(versions_dir, '__init__.py'), 'w') as f:
            pass
        print("✅ Diretório versions limpo")
    
    # 5. Criar migração inicial
    print("\n📝 Criando migração inicial...")
    os.environ['FLASK_APP'] = 'app.py'
    
    try:
        # Criar migração inicial com todo o schema atual
        result = subprocess.run(
            ['flask', 'db', 'migrate', '-m', 'Initial migration - full schema reset'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Migração inicial criada com sucesso")
            print(result.stdout)
        else:
            print(f"⚠️ Aviso ao criar migração: {result.stderr}")
    except Exception as e:
        print(f"❌ Erro ao criar migração: {e}")
    
    # 6. Aplicar migração
    print("\n🚀 Aplicando migração inicial...")
    try:
        result = subprocess.run(
            ['flask', 'db', 'upgrade'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Migração aplicada com sucesso")
            print(result.stdout)
        else:
            print(f"❌ Erro ao aplicar migração: {result.stderr}")
    except Exception as e:
        print(f"❌ Erro ao aplicar migração: {e}")
    
    print("\n✨ RESET COMPLETO!")
    print(f"📁 Backup salvo em: {backup_dir}")
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("CORREÇÃO DEFINITIVA DE MIGRAÇÕES")
    print("=" * 50)
    
    response = input("\n⚠️ Este script vai resetar as migrações. Continuar? (s/n): ")
    if response.lower() == 's':
        reset_migrations()
        
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Verifique se tudo está funcionando localmente")
        print("2. Use o script scripts/deploy_migrations.py para deploy")
        print("3. Para novas alterações, use scripts/safe_migrate.py")
    else:
        print("❌ Operação cancelada")
