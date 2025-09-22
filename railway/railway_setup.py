#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para configurar o Railway para executar migrações automaticamente
"""
import json
import os

def setup_railway():
    """Configurar railway.json para migrações automáticas"""
    
    railway_config = {
        "$schema": "https://railway.app/railway.schema.json",
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "startCommand": "flask db upgrade && python app.py",
            "restartPolicyType": "ON_FAILURE",
            "restartPolicyMaxRetries": 10,
            "healthcheckPath": "/",
            "healthcheckTimeout": 300
        },
        "environments": {
            "production": {
                "deploy": {
                    "startCommand": "flask db upgrade && python app.py"
                }
            }
        }
    }
    
    # Salvar configuração
    with open("railway.json", "w", encoding="utf-8") as f:
        json.dump(railway_config, f, indent=2)
    
    print("✅ railway.json configurado para executar migrações automaticamente")
    
    # Criar Procfile como backup
    procfile_content = """web: flask db upgrade && python app.py"""
    
    with open("Procfile", "w", encoding="utf-8") as f:
        f.write(procfile_content)
    
    print("✅ Procfile criado como backup")
    
    # Criar script de verificação para Railway
    check_script = """#!/usr/bin/env python
# Script executado antes do app no Railway
import os
import subprocess
import sys

print("=" * 60)
print(" RAILWAY DEPLOYMENT - MIGRATIONS CHECK")
print("=" * 60)

# Configurar ambiente
os.environ['FLASK_APP'] = 'app.py'

# Verificar migração atual
try:
    result = subprocess.run(['flask', 'db', 'current'], capture_output=True, text=True)
    print("Current migration:", result.stdout)
except Exception as e:
    print(f"Error checking current migration: {e}")

# Aplicar migrações
print("\\nApplying migrations...")
try:
    result = subprocess.run(['flask', 'db', 'upgrade'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Migrations applied successfully")
        print(result.stdout)
    else:
        print("❌ Migration failed:")
        print(result.stderr)
        sys.exit(1)
except Exception as e:
    print(f"Error applying migrations: {e}")
    sys.exit(1)

print("\\n" + "=" * 60)
print(" MIGRATIONS COMPLETE - STARTING APP")
print("=" * 60)
"""
    
    with open("railway_migrate.py", "w", encoding="utf-8") as f:
        f.write(check_script)
    
    print("✅ railway_migrate.py criado para verificação de migrações")
    
    # Criar arquivo de variáveis de ambiente exemplo
    env_example = """# Variáveis de ambiente para Railway

# Banco de dados (Railway fornece automaticamente)
DATABASE_URL=postgresql://user:pass@host:port/database

# Configurações Flask
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# Email (opcional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@yourdomain.com

# WhatsApp (opcional)
WHATSAPP_API_URL=https://api.whatsapp.com/
WHATSAPP_API_TOKEN=your-token-here
"""
    
    with open(".env.railway.example", "w", encoding="utf-8") as f:
        f.write(env_example)
    
    print("✅ .env.railway.example criado com variáveis necessárias")
    
    print("\n" + "=" * 60)
    print("CONFIGURAÇÃO DO RAILWAY COMPLETA!")
    print("=" * 60)
    print("""
📋 CHECKLIST PARA DEPLOY NO RAILWAY:

1. Commit das mudanças:
   git add .
   git commit -m "feat: railway auto-migration setup"
   
2. Push para o GitHub:
   git push origin main
   
3. No Railway Dashboard:
   - Conecte seu repositório GitHub
   - Configure as variáveis de ambiente
   - DATABASE_URL será fornecida automaticamente
   
4. O Railway executará automaticamente:
   - flask db upgrade (aplicar migrações)
   - python app.py (iniciar aplicação)
   
5. Monitorar logs no Railway para verificar se tudo funcionou
""")

if __name__ == "__main__":
    setup_railway()
