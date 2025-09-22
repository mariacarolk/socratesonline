"""
Script para forçar reset completo das migrações
"""
import os
import shutil
from datetime import datetime

def force_reset():
    print("=== FORÇANDO RESET DAS MIGRAÇÕES ===\n")
    
    # 1. Fazer backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Backup do diretório migrations
    if os.path.exists("migrations"):
        backup_dir = f"backups/migrations_full_{timestamp}"
        os.makedirs("backups", exist_ok=True)
        shutil.copytree("migrations", backup_dir)
        print(f"✅ Backup completo salvo em: {backup_dir}")
    
    # 2. Remover completamente o diretório migrations
    if os.path.exists("migrations"):
        shutil.rmtree("migrations")
        print("✅ Diretório migrations removido")
    
    # 3. Criar script SQL para limpar alembic_version
    sql_script = """
-- Script para limpar a tabela alembic_version
-- Execute este comando no PostgreSQL

DELETE FROM alembic_version;

-- Ou se preferir dropar e recriar a tabela:
-- DROP TABLE IF EXISTS alembic_version;
"""
    
    with open("scripts/clean_alembic.sql", "w") as f:
        f.write(sql_script)
    
    print("\n✅ Reset preparado!")
    print("\n📋 PRÓXIMOS PASSOS:\n")
    print("1. Execute no PostgreSQL (psql ou pgAdmin):")
    print("   DELETE FROM alembic_version;")
    print("\n2. Inicialize as migrações novamente:")
    print("   flask db init")
    print("\n3. Crie a migração inicial:")
    print("   flask db migrate -m 'Initial migration - complete schema'")
    print("\n4. Aplique a migração:")
    print("   flask db upgrade")
    print("\n5. Verifique o status:")
    print("   flask db current")
    
    return True

if __name__ == "__main__":
    force_reset()
