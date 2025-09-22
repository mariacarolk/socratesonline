"""
Script para criar e aplicar migrações de forma segura
Automatiza o processo e evita problemas comuns
"""
import os
import sys
import subprocess
import json
from datetime import datetime
import psycopg2

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_database_url():
    """Obter URL do banco de dados"""
    database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/socrates_online')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    return database_url

def check_migration_status():
    """Verificar status atual das migrações"""
    print("\n📊 Verificando status das migrações...")
    
    os.environ['FLASK_APP'] = 'app.py'
    
    # Verificar head atual
    result = subprocess.run(['flask', 'db', 'heads'], capture_output=True, text=True)
    if result.stdout:
        print(f"📍 Head(s) atual(is): {result.stdout}")
    
    # Verificar versão no banco
    result = subprocess.run(['flask', 'db', 'current'], capture_output=True, text=True)
    if result.stdout:
        print(f"💾 Versão no banco: {result.stdout}")
    
    return True

def backup_database_state():
    """Fazer backup do estado atual do banco"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        database_url = get_database_url()
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        
        # Obter contagem de registros importantes
        tables_to_check = [
            'usuario', 'evento', 'despesas_evento', 'receitas_evento',
            'colaborador', 'fornecedor', 'veiculo'
        ]
        
        backup_info = {
            'timestamp': timestamp,
            'tables': {}
        }
        
        for table in tables_to_check:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                count = cur.fetchone()[0]
                backup_info['tables'][table] = count
            except:
                pass
        
        cur.close()
        conn.close()
        
        # Salvar informações do backup
        backup_file = f"backups/db_state_{timestamp}.json"
        os.makedirs("backups", exist_ok=True)
        
        with open(backup_file, 'w') as f:
            json.dump(backup_info, f, indent=2)
        
        print(f"✅ Estado do banco salvo em {backup_file}")
        return backup_info
    except Exception as e:
        print(f"⚠️ Erro ao fazer backup: {e}")
        return None

def create_migration(description):
    """Criar nova migração com validação"""
    print(f"\n📝 Criando migração: {description}")
    
    os.environ['FLASK_APP'] = 'app.py'
    
    # Verificar se há mudanças para migrar
    result = subprocess.run(
        ['flask', 'db', 'migrate', '-m', description, '--compare-type'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Migração criada com sucesso!")
        print(result.stdout)
        
        # Buscar o arquivo de migração criado
        migrations_dir = "migrations/versions"
        latest_migration = max(
            [f for f in os.listdir(migrations_dir) if f.endswith('.py') and f != '__init__.py'],
            key=lambda f: os.path.getctime(os.path.join(migrations_dir, f))
        )
        
        print(f"📄 Arquivo criado: {latest_migration}")
        
        # Verificar se tem downgrade implementado
        file_path = os.path.join(migrations_dir, latest_migration)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'pass' in content.split('def downgrade():')[1].split('\n')[0]:
                print("⚠️ ATENÇÃO: Função downgrade está vazia!")
                print("   Considere implementar o downgrade para reversibilidade")
        
        return True
    else:
        if "No changes" in result.stdout:
            print("ℹ️ Nenhuma mudança detectada nos models")
        else:
            print(f"❌ Erro ao criar migração: {result.stderr}")
        return False

def apply_migration():
    """Aplicar migrações pendentes"""
    print("\n⬆️ Aplicando migrações...")
    
    os.environ['FLASK_APP'] = 'app.py'
    
    result = subprocess.run(
        ['flask', 'db', 'upgrade'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Migrações aplicadas com sucesso!")
        print(result.stdout)
        return True
    else:
        print(f"❌ Erro ao aplicar migrações: {result.stderr}")
        return False

def validate_migration():
    """Validar que a migração foi aplicada corretamente"""
    print("\n🔍 Validando migração...")
    
    try:
        # Importar models e verificar se o banco está sincronizado
        from app import app
        from models import db
        
        with app.app_context():
            # Tentar fazer uma query simples
            db.session.execute('SELECT 1')
            db.session.commit()
            print("✅ Banco de dados está respondendo")
        
        # Verificar se head = current
        result_head = subprocess.run(['flask', 'db', 'heads'], capture_output=True, text=True)
        result_current = subprocess.run(['flask', 'db', 'current'], capture_output=True, text=True)
        
        # Limpar outputs
        head = result_head.stdout.strip().replace('\n', '')
        current = result_current.stdout.strip().replace('\n', '')
        
        if head in current or current in head:
            print("✅ Banco está sincronizado com as migrações")
            return True
        else:
            print("⚠️ Banco pode estar dessincronizado")
            print(f"   Head: {head}")
            print(f"   Current: {current}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na validação: {e}")
        return False

def auto_migrate():
    """Processo automatizado completo de migração"""
    print("\n🤖 MIGRAÇÃO AUTOMÁTICA\n")
    
    # 1. Verificar status
    check_migration_status()
    
    # 2. Fazer backup
    backup_database_state()
    
    # 3. Solicitar descrição da mudança
    print("\n" + "=" * 50)
    description = input("📝 Descreva a mudança (ex: 'Adicionar campo telefone em colaborador'): ")
    
    if not description:
        print("❌ Descrição é obrigatória")
        return False
    
    # 4. Criar migração
    if create_migration(description):
        # 5. Perguntar se quer aplicar
        response = input("\n Aplicar migração agora? (s/n): ")
        if response.lower() == 's':
            # 6. Aplicar migração
            if apply_migration():
                # 7. Validar
                validate_migration()
                
                print("\n✨ MIGRAÇÃO COMPLETA!")
                print("\n📋 PRÓXIMOS PASSOS:")
                print("1. Teste as funcionalidades afetadas")
                print("2. Se tudo OK, faça commit das migrações")
                print("3. Use scripts/deploy_migrations.py para deploy")
                
                return True
    
    return False

def rollback_migration():
    """Reverter última migração"""
    print("\n⬇️ REVERTENDO MIGRAÇÃO\n")
    
    response = input("⚠️ Tem certeza que deseja reverter a última migração? (s/n): ")
    if response.lower() != 's':
        print("❌ Operação cancelada")
        return False
    
    os.environ['FLASK_APP'] = 'app.py'
    
    # Fazer backup antes
    backup_database_state()
    
    # Reverter
    result = subprocess.run(
        ['flask', 'db', 'downgrade'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Migração revertida!")
        print(result.stdout)
        check_migration_status()
        return True
    else:
        print(f"❌ Erro ao reverter: {result.stderr}")
        return False

def main():
    print("=" * 50)
    print("GERENCIADOR SEGURO DE MIGRAÇÕES")
    print("=" * 50)
    
    options = {
        '1': ('Criar e aplicar nova migração', auto_migrate),
        '2': ('Apenas criar migração', lambda: create_migration(input("Descrição: "))),
        '3': ('Aplicar migrações pendentes', apply_migration),
        '4': ('Verificar status', check_migration_status),
        '5': ('Reverter última migração', rollback_migration),
        '6': ('Validar sincronização', validate_migration)
    }
    
    print("\nOpções:")
    for key, (desc, _) in options.items():
        print(f"  {key}. {desc}")
    
    choice = input("\n Escolha uma opção (1-6): ")
    
    if choice in options:
        _, func = options[choice]
        func()
    else:
        print("❌ Opção inválida")

if __name__ == "__main__":
    main()
