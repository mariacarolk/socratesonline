#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SOLUÇÃO COMPLETA PARA PROBLEMAS DE MIGRAÇÃO
"""
import os
import sys
import subprocess
import shutil
from datetime import datetime

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def create_migration_solution():
    """Criar solução completa para migrações"""
    
    print_section("SOLUÇÃO DEFINITIVA PARA MIGRAÇÕES")
    
    # 1. Criar script SQL
    sql_fix = """-- Execute este script no seu cliente PostgreSQL (pgAdmin, DBeaver, etc)
-- Database: socrates_online

-- Passo 1: Limpar versão antiga do Alembic
DELETE FROM alembic_version;

-- Passo 2: Verificar
SELECT * FROM alembic_version;
-- Deve retornar 0 registros

-- Se a tabela não existir, crie:
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);"""
    
    with open("FIX_DATABASE.sql", "w", encoding="utf-8") as f:
        f.write(sql_fix)
    
    print("\n✅ Arquivo FIX_DATABASE.sql criado!")
    
    # 2. Criar novo env.py sem caracteres especiais
    env_content = """import logging
from logging.config import fileConfig
import os

from flask import current_app
from alembic import context

config = context.config
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

def get_engine():
    try:
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        return current_app.extensions['migrate'].db.engine

def get_engine_url():
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        print(f"[INFO] Using DATABASE_URL: {database_url[:30]}...")
        return database_url.replace('%', '%%')
    
    print("[INFO] Using Flask config")
    try:
        return get_engine().url.render_as_string(hide_password=False).replace('%', '%%')
    except AttributeError:
        return str(get_engine().url).replace('%', '%%')

config.set_main_option('sqlalchemy.url', get_engine_url())
target_db = current_app.extensions['migrate'].db

def get_metadata():
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=get_metadata(), literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = get_engine()
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **conf_args
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()"""
    
    # Atualizar env.py
    env_path = "migrations/env.py"
    if os.path.exists(env_path):
        # Backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"backups/env_backup_{timestamp}.py"
        os.makedirs("backups", exist_ok=True)
        shutil.copy(env_path, backup_path)
        
        # Escrever novo conteúdo
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(env_content)
        print(f"✅ Arquivo env.py atualizado (backup em {backup_path})")
    
    # 3. Criar script batch para Windows
    batch_script = """@echo off
echo ====================================
echo  CORRECAO DE MIGRACOES - PASSO A PASSO
echo ====================================
echo.
echo PASSO 1: Execute o arquivo FIX_DATABASE.sql no PostgreSQL
echo         (Use pgAdmin, DBeaver ou outro cliente)
echo.
pause
echo.
echo PASSO 2: Criando migracao inicial...
call venv\\Scripts\\activate.bat
set FLASK_APP=app.py
flask db migrate -m "Initial complete database schema"
echo.
echo PASSO 3: Aplicando migracao...
flask db upgrade
echo.
echo PASSO 4: Verificando status...
flask db current
echo.
echo ====================================
echo  PROCESSO COMPLETO!
echo ====================================
pause"""
    
    with open("fix_migrations.bat", "w") as f:
        f.write(batch_script)
    print("✅ Arquivo fix_migrations.bat criado!")
    
    # 4. Instruções finais
    print_section("INSTRUÇÕES PARA CORRIGIR AS MIGRAÇÕES")
    
    print("""
📋 SIGA ESTES PASSOS:

1️⃣ LIMPAR O BANCO (PostgreSQL):
   - Abra o pgAdmin ou DBeaver
   - Conecte ao banco 'socrates_online'
   - Execute o arquivo: FIX_DATABASE.sql
   
2️⃣ CRIAR NOVA MIGRAÇÃO (Terminal):
   Execute os comandos:
   
   flask db migrate -m "Initial complete database schema"
   flask db upgrade
   flask db current
   
   OU simplesmente execute: fix_migrations.bat

3️⃣ VERIFICAR:
   - Teste o sistema localmente
   - Verifique se todas as tabelas existem
   
4️⃣ PARA O RAILWAY:
   - Faça commit das novas migrações
   - git add migrations/
   - git commit -m "fix: reset migrations with complete schema"
   - git push origin main
""")
    
    # 5. Criar arquivo de documentação
    doc_content = """# SISTEMA DE MIGRAÇÕES - DOCUMENTAÇÃO

## Como funcionam as migrações

As migrações são gerenciadas pelo Flask-Migrate (Alembic) e permitem versionamento do schema do banco.

## Comandos principais

### Para criar uma nova migração (após alterar models.py):
```bash
flask db migrate -m "Descrição da mudança"
```

### Para aplicar migrações:
```bash
flask db upgrade
```

### Para reverter última migração:
```bash
flask db downgrade
```

### Para ver status atual:
```bash
flask db current
flask db heads
```

## Processo para novas alterações

1. Altere o arquivo models.py
2. Execute: `python scripts/safe_migrate.py`
3. Teste localmente
4. Faça commit e push

## Deploy no Railway

O Railway executa automaticamente `flask db upgrade` no deploy.

## Resolução de problemas comuns

### Erro: "Can't locate revision"
- Execute FIX_DATABASE.sql no PostgreSQL
- Delete a pasta migrations/versions
- Execute flask db migrate

### Erro: "Target database is not up to date"
- Execute: flask db upgrade

### Erro: "Multiple head revisions"
- Execute: flask db merge -m "merge heads"
- Depois: flask db upgrade
"""
    
    with open("MIGRATIONS_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(doc_content)
    print("✅ Arquivo MIGRATIONS_GUIDE.md criado!")
    
    return True

if __name__ == "__main__":
    create_migration_solution()
    
    print("\n" + "🎯" * 30)
    print("\n✨ SOLUÇÃO CRIADA COM SUCESSO!")
    print("\nAgora siga as instruções acima para resolver o problema definitivamente.")
    print("\n" + "🎯" * 30)
