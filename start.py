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
    
    # Verificar se DATABASE_URL está definida
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ ERROR: DATABASE_URL não está definida!")
        sys.exit(1)
    
    print(f"🔗 DATABASE_URL configurada: {database_url[:50]}...")
    
    # Definir FLASK_APP se não estiver definida
    if not os.getenv('FLASK_APP'):
        os.environ['FLASK_APP'] = 'app.py'
        print("📝 FLASK_APP definida como app.py")
    
    # Executar migrações
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
