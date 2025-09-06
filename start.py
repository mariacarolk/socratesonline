#!/usr/bin/env python3
"""
Script de inicialização para Railway
Garante que as migrações sejam executadas com a configuração correta
"""
import os
import sys
import subprocess
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

def run_command(cmd, description):
    """Executa um comando e trata erros"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} concluído com sucesso")
        if result.stdout:
            print(f"📋 Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}")
        print(f"📋 Error: {e.stderr}")
        return False

def main():
    """Função principal de inicialização"""
    print("🚀 Iniciando aplicação Sócrates Online no Railway...")
    
    # Debug completo das variáveis de ambiente
    print("🔍 DEBUG - Variáveis de ambiente relevantes:")
    env_vars = ['DATABASE_URL', 'RAILWAY_ENVIRONMENT', 'PORT', 'FLASK_ENV', 'FLASK_APP']
    for var in env_vars:
        value = os.getenv(var, 'NÃO DEFINIDA')
        if var == 'DATABASE_URL' and value != 'NÃO DEFINIDA':
            print(f"   {var}: {value[:50]}...")
        else:
            print(f"   {var}: {value}")
    
    # Verificar se DATABASE_URL está definida
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ ERROR: DATABASE_URL não está definida!")
        print("🔍 Listando todas as variáveis de ambiente que contêm 'postgres' ou 'railway':")
        for key, value in os.environ.items():
            if 'postgres' in key.lower() or 'railway' in key.lower() or 'database' in key.lower():
                print(f"   {key}: {value[:50]}...")
        sys.exit(1)
    
    # Verificar se é localhost (problema)
    if 'localhost' in database_url or '127.0.0.1' in database_url:
        print("⚠️  ERRO CRÍTICO: DATABASE_URL aponta para localhost!")
        print("🔍 Isso indica que o Railway não configurou o PostgreSQL corretamente.")
        print("🔧 Tentando encontrar variável alternativa...")
        
        # Procurar por outras variáveis que possam conter a URL do banco
        possible_vars = []
        for key, value in os.environ.items():
            if ('postgres' in value.lower() or 'railway' in value.lower()) and 'localhost' not in value:
                possible_vars.append((key, value))
        
        if possible_vars:
            print("🔍 Variáveis alternativas encontradas:")
            for key, value in possible_vars:
                print(f"   {key}: {value[:50]}...")
            
            # Usar a primeira variável encontrada
            alt_key, alt_value = possible_vars[0]
            print(f"🔧 Usando {alt_key} como DATABASE_URL")
            database_url = alt_value
            os.environ['DATABASE_URL'] = database_url
        else:
            print("❌ Nenhuma variável alternativa encontrada!")
            sys.exit(1)
    
    print(f"🔗 DATABASE_URL final: {database_url[:50]}...")
    
    # Definir FLASK_APP se não estiver definida
    if not os.getenv('FLASK_APP'):
        os.environ['FLASK_APP'] = 'app.py'
        print("📝 FLASK_APP definida como app.py")
    
    # Executar migrações (env.py agora força DATABASE_URL)
    if not run_command("flask db upgrade", "Executando migrações do banco"):
        print("❌ Falha nas migrações - parando aplicação")
        sys.exit(1)
    
    # Iniciar aplicação
    print("🎯 Iniciando aplicação Flask...")
    try:
        # Importar e executar a aplicação
        from app import app
        port = int(os.environ.get('PORT', 5000))
        print(f"🌐 Aplicação iniciando na porta {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
