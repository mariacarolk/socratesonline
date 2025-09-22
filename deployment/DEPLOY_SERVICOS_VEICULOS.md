# 🚀 DEPLOY DE SERVIÇOS DE VEÍCULOS PARA PRODUÇÃO

## 📋 Problema Identificado

O sistema de migrações do projeto tem um **ciclo de dependências** que impede a criação de novas migrações via Alembic. Isso acontece quando diferentes migrações referenciam umas às outras de forma circular.

## ✅ Solução para Produção

Para aplicar as tabelas de serviços de veículos em **produção**, use uma das opções abaixo:

### 🔧 Opção 1: Script SQL Direto (RECOMENDADO)

Execute o arquivo `CRIAR_TABELAS_SERVICOS_POSTGRES.sql` diretamente no banco de produção:

```bash
# No servidor de produção, conecte ao PostgreSQL e execute:
psql -U [usuario] -d [banco_producao] -f CRIAR_TABELAS_SERVICOS_POSTGRES.sql
```

### 🔧 Opção 2: Aplicação Manual via Cliente PostgreSQL

1. **Faça backup do banco de produção**
2. **Conecte ao banco** via pgAdmin, DBeaver ou psql
3. **Execute o script** `CRIAR_TABELAS_SERVICOS_POSTGRES.sql`
4. **Verifique as tabelas** criadas

### 🔧 Opção 3: Migração Manual (AVANÇADO)

Se você preferir resolver o ciclo de migrações:

1. **Faça backup completo**
2. **Delete todas as migrações** da pasta `migrations/versions/`
3. **Recrie o sistema de migrações**:
   ```bash
   flask db init
   flask db migrate -m "initial migration"
   flask db upgrade
   ```
4. **Aplique a migração de serviços**

## 📊 Tabelas que Serão Criadas

### 🚨 multa_veiculo
- **Campos**: id_multa, id_veiculo, numero_ait, data_infracao, data_vencimento, data_pagamento, valor_original, valor_pago, local_infracao, tipo_infracao, orgao_autuador, status, observacoes
- **Índices**: por veículo, data de infração, status
- **Constraints**: FK para veículo, valores positivos, status válidos

### 📄 ipva_veiculo  
- **Campos**: id_ipva, id_veiculo, ano_exercicio, data_vencimento, data_pagamento, valor_ipva, valor_taxa_detran, valor_multa_juros, valor_total, valor_pago, numero_documento, status, observacoes
- **Índices**: por veículo, ano de exercício, status
- **Constraints**: FK para veículo, unicidade por veículo/ano, valores positivos

### ✅ licenciamento_veiculo
- **Campos**: id_licenciamento, id_veiculo, ano_exercicio, data_vencimento, data_pagamento, valor_licenciamento, valor_taxa_detran, valor_multa_juros, valor_total, valor_pago, numero_documento, status, observacoes  
- **Índices**: por veículo, ano de exercício, status
- **Constraints**: FK para veículo, unicidade por veículo/ano, valores positivos

### 🔧 manutencao_veiculo
- **Campos**: id_manutencao, id_veiculo, data_servico, tipo_manutencao, descricao, fornecedor_servico, km_veiculo, valor_servico, valor_pecas, valor_total, data_proxima_revisao, km_proxima_revisao, garantia_dias, observacoes
- **Índices**: por veículo, data de serviço, tipo de manutenção  
- **Constraints**: FK para veículo, valores positivos, tipos válidos

## 🔒 Considerações de Segurança

1. ✅ **Backup obrigatório** antes da aplicação
2. ✅ **Teste em ambiente de staging** primeiro
3. ✅ **Aplicação em horário de baixo tráfego**
4. ✅ **Verificação pós-deploy** das funcionalidades

## 🎯 Verificação Pós-Deploy

Após aplicar as tabelas, verifique se tudo funcionou:

```sql
-- Verificar se as tabelas foram criadas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('multa_veiculo', 'ipva_veiculo', 'licenciamento_veiculo', 'manutencao_veiculo');

-- Verificar integridade referencial
SELECT conname, confrelid::regclass, af.attname AS fcol, confkey, conrelid::regclass, a.attname AS col
FROM pg_attribute af, pg_attribute a,
(SELECT conname, conrelid, confrelid,conkey[i] AS conkey, confkey[i] AS confkey
 FROM (SELECT conname, conrelid, confrelid, conkey, confkey,
              generate_series(1,array_upper(conkey,1)) AS i
       FROM pg_constraint WHERE contype = 'f') ss) ss2
WHERE af.attnum = confkey AND af.attrelid = confrelid AND
      a.attnum = conkey AND a.attrelid = conrelid AND
      af.attrelid::regclass::text LIKE '%veiculo%';
```

## ✅ Status Pós-Deploy

Depois que as tabelas forem criadas em produção:

- ✅ **Sistema de modais** funcionará 100%
- ✅ **CRUD completo** para todos os serviços
- ✅ **Logs de auditoria** funcionando
- ✅ **Interface responsiva** ativa
- ✅ **Validações** de negócio operando

## 🎉 Funcionalidades Ativas Pós-Deploy

1. **🚨 Gestão de Multas** - Cadastro, edição, exclusão via modal
2. **📄 Controle de IPVA** - Gestão anual de impostos
3. **✅ Licenciamento** - Controle de documentação veicular  
4. **🔧 Manutenções** - Histórico completo de serviços

---

**⚠️ IMPORTANTE**: Execute sempre em ambiente controlado e com backup!
