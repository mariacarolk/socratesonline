#!/usr/bin/env python
"""
Script para corrigir problemas de migração no Railway
Especificamente para resolver o erro KeyError: 'dae112c6d426'
"""
import os
import subprocess
import sys
from sqlalchemy import create_engine, text

print("=" * 60)
print(" RAILWAY MIGRATION FIX")
print("=" * 60)

# Configurar ambiente
os.environ['FLASK_APP'] = 'app.py'

def get_database_url():
    """Obter URL do banco de dados"""
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    return database_url

def fix_alembic_version():
    """Corrigir a tabela alembic_version se necessário"""
    try:
        database_url = get_database_url()
        if not database_url:
            print("❌ DATABASE_URL não encontrada")
            return False
            
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Verificar se a tabela alembic_version existe
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'alembic_version'
                );
            """))
            
            table_exists = result.scalar()
            
            if table_exists:
                # Verificar a versão atual
                result = conn.execute(text("SELECT version_num FROM alembic_version;"))
                current_version = result.scalar()
                print(f"Versão atual no banco: {current_version}")
                
                # Se a versão for a problemática, corrigir
                if current_version == 'dae112c6d426':
                    print("🔧 Corrigindo versão problemática...")
                    conn.execute(text("UPDATE alembic_version SET version_num = 'fix_missing_indexes_railway';"))
                    conn.commit()
                    print("✅ Versão corrigida para 'fix_missing_indexes_railway'")
                    return True
                elif current_version in ['initial', 'fix_missing_indexes_railway', '4769126cc9d9', '8fcd83687262']:
                    print("✅ Versão válida encontrada")
                    return True
                else:
                    print(f"⚠️ Versão desconhecida: {current_version}")
                    # Resetar para a versão inicial segura
                    conn.execute(text("UPDATE alembic_version SET version_num = 'initial';"))
                    conn.commit()
                    print("✅ Resetado para versão inicial")
                    return True
            else:
                print("ℹ️ Tabela alembic_version não existe - será criada na primeira migração")
                return True
                
    except Exception as e:
        print(f"❌ Erro ao verificar/corrigir alembic_version: {e}")
        return False

def run_migrations():
    """Executar migrações"""
    print("\n🔄 Aplicando migrações...")
    try:
        # Primeiro, tentar stamp para garantir que estamos na versão correta
        result = subprocess.run(['flask', 'db', 'stamp', 'head'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Stamp realizado com sucesso")
        else:
            print(f"⚠️ Aviso no stamp: {result.stderr}")
        
        # Agora aplicar as migrações
        result = subprocess.run(['flask', 'db', 'upgrade'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Migrações aplicadas com sucesso")
            print(result.stdout)
            return True
        else:
            print("❌ Falha nas migrações:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar migrações: {e}")
        return False

def main():
    """Função principal"""
    print("🔍 Verificando e corrigindo problemas de migração...")
    
    # Primeiro, tentar corrigir a tabela alembic_version
    if not fix_alembic_version():
        print("❌ Falha ao corrigir alembic_version")
        sys.exit(1)
    
    # Executar migrações
    if not run_migrations():
        print("❌ Falha ao executar migrações")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print(" ✅ CORREÇÃO DE MIGRAÇÃO CONCLUÍDA")
    print("=" * 60)

if __name__ == "__main__":
    main()
