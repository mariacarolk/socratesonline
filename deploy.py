#!/usr/bin/env python3
"""
Script de deploy para Railway - Aplica migrações automaticamente
"""
import os
import sys
import subprocess
from flask import Flask
from extensions import db
from models import Usuario
from werkzeug.security import generate_password_hash

def run_command(command, description):
    """Executa um comando e trata erros"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Sucesso")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erro")
        print(f"   Error: {e.stderr.strip()}")
        return False

def apply_migrations():
    """Aplica as migrações do banco de dados"""
    print("🚀 Iniciando processo de deploy...")
    
    # Verificar se o Flask-Migrate está disponível
    print("📋 Verificando ambiente...")
    
    # Aplicar migrações
    if not run_command("flask db upgrade", "Aplicando migrações do banco de dados"):
        print("⚠️  Erro ao aplicar migrações. Tentando criar tabelas...")
        # Fallback: criar tabelas se as migrações falharem
        try:
            from app import app
            with app.app_context():
                db.create_all()
                print("✅ Tabelas criadas com sucesso (fallback)")
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            return False
    
    return True

def ensure_root_user():
    """Garante que o usuário root existe"""
    try:
        from app import app
        with app.app_context():
            root_user = Usuario.query.filter_by(email='root@socratesonline.com').first()
            if not root_user:
                print("👑 Criando usuário root...")
                root_user = Usuario(
                    nome='Administrador Root',
                    email='root@socratesonline.com',
                    categoria='administrativo',
                    senha=generate_password_hash('admin123')
                )
                db.session.add(root_user)
                db.session.commit()
                print("✅ Usuário root criado com sucesso")
            else:
                print("✅ Usuário root já existe")
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar/criar usuário root: {e}")
        return False

def main():
    """Função principal do deploy"""
    print("🌐 Deploy para Railway - Sócrates Online")
    print("=" * 50)
    
    # Configurar variáveis de ambiente
    os.environ['FLASK_APP'] = 'app.py'
    
    # Aplicar migrações
    if not apply_migrations():
        print("💥 Falha no deploy - Migrações")
        sys.exit(1)
    
    # Garantir usuário root
    if not ensure_root_user():
        print("⚠️  Aviso: Não foi possível verificar/criar usuário root")
    
    print("=" * 50)
    print("✅ Deploy concluído com sucesso!")
    print("🚀 Iniciando aplicação...")

if __name__ == '__main__':
    main()
