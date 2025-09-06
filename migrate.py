#!/usr/bin/env python3
"""
Script específico para migrações no Railway
Força a configuração correta do DATABASE_URL antes de executar migrações
"""
import os
import sys
import subprocess
from dotenv import load_dotenv

def main():
    """Executa migrações com configuração forçada"""
    print("🔧 Iniciando migrações Sócrates Online...")
    
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Verificar DATABASE_URL
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ ERROR: DATABASE_URL não encontrada!")
        sys.exit(1)
    
    print(f"🔗 DATABASE_URL: {database_url[:50]}...")
    
    # Verificar se é localhost (problema)
    if 'localhost' in database_url or '127.0.0.1' in database_url:
        print("⚠️  WARNING: DATABASE_URL aponta para localhost!")
        print("🔍 Isso indica que a configuração Railway não está sendo carregada.")
        sys.exit(1)
    
    # Definir variáveis de ambiente necessárias
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['SQLALCHEMY_DATABASE_URI'] = database_url
    
    # Forçar configuração PostgreSQL
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
        os.environ['DATABASE_URL'] = database_url
        os.environ['SQLALCHEMY_DATABASE_URI'] = database_url
    
    print("📝 Variáveis de ambiente configuradas:")
    print(f"   FLASK_APP: {os.environ.get('FLASK_APP')}")
    print(f"   DATABASE_URL: {database_url[:50]}...")
    
    try:
        # Executar migrações
        print("🔄 Executando: flask db upgrade")
        result = subprocess.run(
            ['flask', 'db', 'upgrade'], 
            check=True, 
            capture_output=True, 
            text=True,
            env=os.environ.copy()
        )
        print("✅ Migrações executadas com sucesso!")
        if result.stdout:
            print(f"📋 Output: {result.stdout}")
        return True
        
    except subprocess.CalledProcessError as e:
        print("❌ Erro nas migrações:")
        print(f"📋 Error: {e.stderr}")
        print(f"📋 Output: {e.stdout}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
