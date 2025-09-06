#!/usr/bin/env python3
"""
Script de debug específico para Railway
Analisa todas as variáveis de ambiente e configurações
"""
import os
import sys

def debug_railway_environment():
    """Debug completo do ambiente Railway"""
    print("=" * 60)
    print("🔍 RAILWAY DEBUG - ANÁLISE COMPLETA DO AMBIENTE")
    print("=" * 60)
    
    # 1. Verificar indicadores do Railway
    print("\n1️⃣ INDICADORES DO RAILWAY:")
    railway_indicators = [
        'RAILWAY_ENVIRONMENT', 'RAILWAY_PROJECT_ID', 'RAILWAY_SERVICE_ID',
        'RAILWAY_DEPLOYMENT_ID', 'RAILWAY_PUBLIC_DOMAIN', 'PORT'
    ]
    
    is_railway = False
    for indicator in railway_indicators:
        value = os.getenv(indicator, 'NÃO DEFINIDA')
        print(f"   {indicator}: {value}")
        if value != 'NÃO DEFINIDA':
            is_railway = True
    
    print(f"\n🎯 DETECTADO COMO RAILWAY: {'SIM' if is_railway else 'NÃO'}")
    
    # 2. Analisar todas as variáveis relacionadas ao banco
    print("\n2️⃣ VARIÁVEIS DE BANCO DE DADOS:")
    database_vars = []
    
    for key, value in os.environ.items():
        key_lower = key.lower()
        value_lower = value.lower() if isinstance(value, str) else ''
        
        # Procurar variáveis que podem conter URLs de banco
        if any(term in key_lower for term in ['database', 'postgres', 'db', 'sql']):
            database_vars.append((key, value))
        elif any(term in value_lower for term in ['postgres', 'railway', 'database']) and value_lower.startswith(('postgres', 'postgresql')):
            database_vars.append((key, value))
    
    if database_vars:
        print("   Variáveis encontradas:")
        for key, value in database_vars:
            is_localhost = 'localhost' in value or '127.0.0.1' in value
            status = "❌ LOCALHOST" if is_localhost else "✅ REMOTO"
            print(f"   {key}: {value[:50]}... [{status}]")
    else:
        print("   ❌ NENHUMA VARIÁVEL DE BANCO ENCONTRADA!")
    
    # 3. Verificar configuração atual do Flask
    print("\n3️⃣ CONFIGURAÇÃO ATUAL:")
    try:
        # Tentar importar e verificar a configuração
        sys.path.insert(0, '.')
        from app import app
        
        with app.app_context():
            db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'NÃO DEFINIDA')
            is_localhost = 'localhost' in db_uri or '127.0.0.1' in db_uri
            status = "❌ LOCALHOST" if is_localhost else "✅ REMOTO"
            print(f"   SQLALCHEMY_DATABASE_URI: {db_uri[:50]}... [{status}]")
            
    except Exception as e:
        print(f"   ❌ ERRO AO CARREGAR CONFIG: {e}")
    
    # 4. Recomendações
    print("\n4️⃣ RECOMENDAÇÕES:")
    
    if not is_railway:
        print("   ⚠️  Não foi detectado ambiente Railway")
        print("   🔧 Verifique se o deploy foi feito corretamente")
    
    valid_db_vars = [var for var in database_vars if 'localhost' not in var[1] and '127.0.0.1' not in var[1]]
    
    if not valid_db_vars:
        print("   ❌ NENHUMA VARIÁVEL DE BANCO REMOTO ENCONTRADA!")
        print("   🔧 AÇÃO NECESSÁRIA: Adicionar PostgreSQL ao projeto Railway")
        print("   📋 Passos:")
        print("      1. Acesse o dashboard do Railway")
        print("      2. Clique em '+ New' no projeto")
        print("      3. Selecione 'Database' → 'Add PostgreSQL'")
        print("      4. Aguarde a criação do banco")
        print("      5. Faça novo deploy")
    else:
        print("   ✅ Variáveis de banco remoto encontradas:")
        for key, value in valid_db_vars:
            print(f"      {key}: {value[:50]}...")
        
        print(f"\n   🔧 SUGESTÃO: Usar {valid_db_vars[0][0]} como DATABASE_URL")
    
    print("\n" + "=" * 60)
    return database_vars, is_railway

if __name__ == '__main__':
    debug_railway_environment()
