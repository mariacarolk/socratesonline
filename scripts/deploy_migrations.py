"""
Script para fazer deploy seguro das migrações para o Railway
"""
import os
import sys
import subprocess
import json
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_deployment_package():
    """Criar pacote de deployment com todas as migrações"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("\n🚀 PREPARANDO DEPLOY PARA O RAILWAY\n")
    
    # 1. Verificar se existem migrações não commitadas
    result = subprocess.run(['git', 'status', '--porcelain', 'migrations/'], 
                          capture_output=True, text=True)
    
    if result.stdout:
        print("⚠️ Existem migrações não commitadas:")
        print(result.stdout)
        response = input("\n Deseja adicionar ao git? (s/n): ")
        if response.lower() == 's':
            subprocess.run(['git', 'add', 'migrations/'])
            commit_msg = f"feat: migrations update - {timestamp}"
            subprocess.run(['git', 'commit', '-m', commit_msg])
            print(f"✅ Migrações commitadas: {commit_msg}")
    
    # 2. Criar arquivo de instruções para o Railway
    instructions = {
        "timestamp": timestamp,
        "instructions": [
            "1. Fazer backup do banco de produção",
            "2. Executar: flask db upgrade",
            "3. Verificar se todas as tabelas foram criadas/atualizadas",
            "4. Testar funcionalidades principais"
        ],
        "commands": {
            "backup": "pg_dump $DATABASE_URL > backup_before_migration.sql",
            "migrate": "flask db upgrade",
            "verify": "flask db current"
        }
    }
    
    with open('DEPLOY_INSTRUCTIONS.json', 'w') as f:
        json.dump(instructions, f, indent=2)
    
    print("\n✅ Instruções de deploy criadas em DEPLOY_INSTRUCTIONS.json")
    
    # 3. Criar script de migração automática para Railway
    railway_script = """#!/bin/bash
# Script de migração automática para Railway

echo "🚀 Iniciando migração no Railway..."

# Exportar variáveis
export FLASK_APP=app.py

# Verificar migração atual
echo "📝 Migração atual:"
flask db current

# Aplicar novas migrações
echo "⬆️ Aplicando migrações..."
flask db upgrade

# Verificar nova versão
echo "✅ Nova versão:"
flask db current

echo "✨ Migração concluída!"
"""
    
    with open('railway_migrate.sh', 'w') as f:
        f.write(railway_script)
    
    print("✅ Script railway_migrate.sh criado")
    
    # 4. Atualizar railway.json se necessário
    if os.path.exists('railway.json'):
        with open('railway.json', 'r') as f:
            railway_config = json.load(f)
        
        # Adicionar comando de migração ao deploy
        if 'deploy' not in railway_config:
            railway_config['deploy'] = {}
        
        railway_config['deploy']['startCommand'] = "flask db upgrade && python app.py"
        
        with open('railway.json', 'w') as f:
            json.dump(railway_config, f, indent=2)
        
        print("✅ railway.json atualizado com comando de migração")
    
    print("\n📋 CHECKLIST PARA DEPLOY:")
    print("1. ✅ Migrações preparadas")
    print("2. ⏳ Fazer push para o GitHub: git push origin main")
    print("3. ⏳ Railway vai executar automaticamente as migrações")
    print("4. ⏳ Verificar logs no Railway Dashboard")
    
    return True

def check_production_compatibility():
    """Verificar compatibilidade com produção"""
    print("\n🔍 Verificando compatibilidade com produção...")
    
    # Verificar se todas as migrações são reversíveis
    migrations_dir = "migrations/versions"
    if os.path.exists(migrations_dir):
        migration_files = [f for f in os.listdir(migrations_dir) if f.endswith('.py') and f != '__init__.py']
        
        for migration_file in migration_files:
            file_path = os.path.join(migrations_dir, migration_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                if 'def downgrade():' not in content:
                    print(f"⚠️ Migração {migration_file} não tem função downgrade")
                elif 'pass' in content.split('def downgrade():')[1].split('def')[0]:
                    print(f"⚠️ Migração {migration_file} tem downgrade vazio")
    
    print("✅ Verificação concluída")

if __name__ == "__main__":
    print("=" * 50)
    print("DEPLOY DE MIGRAÇÕES PARA O RAILWAY")
    print("=" * 50)
    
    check_production_compatibility()
    
    response = input("\n Preparar deploy? (s/n): ")
    if response.lower() == 's':
        create_deployment_package()
        
        print("\n🎉 DEPLOY PREPARADO!")
        print("\n Comandos para executar:")
        print("   1. git push origin main")
        print("   2. Acompanhar logs no Railway Dashboard")
    else:
        print("❌ Deploy cancelado")
