#!/usr/bin/env python3
"""
Teste de Conexão com PostgreSQL Railway
=======================================

Script para testar se a DATABASE_URL está configurada corretamente.
Útil para verificar antes de configurar o backup.

Uso:
    python scripts/test_connection.py
"""

import os
import sys
from urllib.parse import urlparse

def test_database_connection():
    """Testa a conexão com o banco PostgreSQL."""
    
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL não encontrada nas variáveis de ambiente")
        print("💡 Configure a variável DATABASE_URL com a URL do Railway")
        return False
    
    print("🔍 Testando conexão com PostgreSQL...")
    print(f"📋 URL configurada: {database_url[:50]}...")
    
    # Parse da URL para mostrar detalhes
    try:
        parsed = urlparse(database_url)
        print(f"🏠 Host: {parsed.hostname}")
        print(f"🔌 Porta: {parsed.port}")
        print(f"💾 Database: {parsed.path.lstrip('/')}")
        print(f"👤 Usuário: {parsed.username}")
        print()
    except Exception as e:
        print(f"⚠️ Erro ao analisar URL: {e}")
        return False
    
    # Testar conexão usando psycopg2
    try:
        import psycopg2
        
        print("🔄 Tentando conectar...")
        
        # Conectar ao banco
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Executar query simples
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        # Verificar número de tabelas
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        table_count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        print("✅ CONEXÃO ESTABELECIDA COM SUCESSO!")
        print(f"🐘 PostgreSQL: {version.split(' ')[1]}")
        print(f"📊 Tabelas encontradas: {table_count}")
        print()
        print("🎉 A URL está correta e o banco está acessível!")
        
        return True
        
    except ImportError:
        print("⚠️ psycopg2 não instalado. Instalando...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
            print("✅ psycopg2 instalado. Execute o script novamente.")
        except:
            print("❌ Erro ao instalar psycopg2")
            print("💡 Execute: pip install psycopg2-binary")
        return False
        
    except Exception as e:
        print(f"❌ ERRO DE CONEXÃO: {e}")
        print()
        print("🔍 Possíveis causas:")
        print("   • URL incorreta ou expirada")
        print("   • Banco PostgreSQL não está rodando")
        print("   • Credenciais inválidas")
        print("   • Problemas de rede/firewall")
        print()
        print("💡 Verifique:")
        print("   • Se você está usando a URL PRIVADA do Railway")
        print("   • Se o serviço PostgreSQL está ativo no Railway")
        print("   • Se a URL não expirou (regenerar se necessário)")
        
        return False

def main():
    """Função principal."""
    print("=" * 60)
    print("🧪 TESTE DE CONEXÃO POSTGRESQL RAILWAY")
    print("=" * 60)
    print()
    
    success = test_database_connection()
    
    print()
    print("=" * 60)
    
    if success:
        print("🎯 RESULTADO: Conexão OK - Pronto para backup!")
    else:
        print("🚨 RESULTADO: Conexão falhou - Verifique configuração")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
