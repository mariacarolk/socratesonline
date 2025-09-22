
-- Script para limpar a tabela alembic_version
-- Execute este comando no PostgreSQL

DELETE FROM alembic_version;

-- Ou se preferir dropar e recriar a tabela:
-- DROP TABLE IF EXISTS alembic_version;
