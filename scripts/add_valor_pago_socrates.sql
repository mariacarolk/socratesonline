-- Script para adicionar campo valor_pago_socrates nas tabelas de despesas
-- Execute este script no PostgreSQL para adicionar o novo campo

-- Adicionar coluna valor_pago_socrates na tabela despesas_evento
ALTER TABLE despesas_evento ADD COLUMN IF NOT EXISTS valor_pago_socrates FLOAT;

-- Adicionar coluna valor_pago_socrates na tabela despesas_empresa  
ALTER TABLE despesas_empresa ADD COLUMN IF NOT EXISTS valor_pago_socrates FLOAT;

-- Comentários para documentação
COMMENT ON COLUMN despesas_evento.valor_pago_socrates IS 'Valor pago pelo Sócrates Online para esta despesa';
COMMENT ON COLUMN despesas_empresa.valor_pago_socrates IS 'Valor pago pelo Sócrates Online para esta despesa';



