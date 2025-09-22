# SISTEMA DE MIGRAÇÕES - DOCUMENTAÇÃO

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
