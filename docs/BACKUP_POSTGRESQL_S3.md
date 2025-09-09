# Backup Automático PostgreSQL Railway → S3

Sistema completo de backup automático do banco PostgreSQL do Railway para Amazon S3, com restauração e rotação automática de arquivos.

## 🎯 Visão Geral

Este sistema resolve o problema de backup automático do PostgreSQL hospedado no Railway, oferecendo:

- ✅ **Backup automático diário** via GitHub Actions
- ✅ **Compressão gzip** para economizar espaço
- ✅ **Rotação automática** (remove backups antigos)
- ✅ **Restauração completa** com script dedicado
- ✅ **Logs detalhados** para monitoramento
- ✅ **Execução manual** quando necessário

## 📋 Pré-requisitos

### 1. AWS S3
- Bucket S3 criado
- Usuário IAM com permissões específicas
- Credenciais de acesso (Access Key ID + Secret)

### 2. Railway
- Aplicação PostgreSQL ativa
- DATABASE_URL disponível

### 3. Ferramentas
- Python 3.11+
- PostgreSQL client tools (`pg_dump`, `psql`)
- Dependências: `boto3`, `python-dotenv`

## 🚀 Configuração Rápida

### Passo 1: Configurar AWS S3

1. **Criar bucket S3:**
   ```bash
   # Via AWS CLI (opcional)
   aws s3 mb s3://meu-bucket-backups --region us-east-1
   ```

2. **Criar usuário IAM com política:**
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "s3:PutObject",
           "s3:GetObject", 
           "s3:DeleteObject",
           "s3:ListBucket"
         ],
         "Resource": [
           "arn:aws:s3:::meu-bucket-backups",
           "arn:aws:s3:::meu-bucket-backups/*"
         ]
       }
     ]
   }
   ```

### Passo 2: Configurar Variáveis de Ambiente

1. **Para execução local:**
   ```bash
   # Copiar exemplo
   cp scripts/env.backup.example .env
   
   # Editar com suas configurações
   nano .env
   ```

2. **Para GitHub Actions:**
   
   Configure os seguintes secrets no repositório:
   - `RAILWAY_DATABASE_URL`
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `S3_BACKUP_BUCKET`
   - `S3_BACKUP_REGION`

### Passo 3: Testar Backup Manual

```bash
# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Instalar dependências
pip install boto3 python-dotenv

# Executar backup de teste
python scripts/backup_postgres_s3.py
```

## 📅 Backup Automático

### GitHub Actions (Recomendado)

O backup está configurado para executar **automaticamente todos os dias às 02:00 UTC** (23:00 Brasília).

**Arquivo:** `.github/workflows/backup-database.yml`

**Funcionalidades:**
- ✅ Execução diária automática
- ✅ Execução manual via interface do GitHub
- ✅ Instalação automática de dependências
- ✅ Notificação de falhas
- ✅ Logs completos

**Para executar manualmente:**
1. Acesse GitHub → Actions
2. Selecione "Backup PostgreSQL to S3"
3. Clique "Run workflow"

### Execução Local/Servidor

```bash
# Backup único
python scripts/backup_postgres_s3.py

# Via cron (Linux/Mac)
0 2 * * * cd /path/to/project && python scripts/backup_postgres_s3.py

# Via Task Scheduler (Windows)
# Configure tarefa diária executando o script
```

## 🔄 Restauração de Backup

### Restaurar Backup Mais Recente
```bash
python scripts/restore_postgres_s3.py
```

### Restaurar Backup Específico
```bash
# Listar backups disponíveis primeiro
python scripts/restore_postgres_s3.py --list

# Restaurar backup específico
python scripts/restore_postgres_s3.py socrates-online_backup_20240115_143022.sql.gz
```

### ⚠️ ATENÇÃO - Restauração
- **A restauração SOBRESCREVE completamente o banco atual**
- **Use apenas em emergências ou ambiente de teste**
- **Sempre confirme o backup correto antes de restaurar**

## 📊 Monitoramento

### Verificar Status dos Backups

```bash
# Listar backups no S3
aws s3 ls s3://meu-bucket-backups/socrates-online_backup_ --human-readable

# Verificar logs do GitHub Actions
# Acesse: GitHub → Actions → Backup PostgreSQL to S3
```

### Logs Detalhados

Os scripts geram logs completos incluindo:
- ✅ Timestamp de execução
- ✅ Tamanho do backup
- ✅ Status do upload S3
- ✅ Limpeza de backups antigos
- ✅ Erros detalhados

**Exemplo de log de sucesso:**
```
2024-01-15 14:30:22 - INFO - === INICIANDO BACKUP AUTOMÁTICO ===
2024-01-15 14:30:22 - INFO - Backup configurado para bucket: meu-bucket-backups
2024-01-15 14:30:25 - INFO - Backup criado com sucesso
2024-01-15 14:30:25 - INFO - Backup comprimido: 45.2 MB
2024-01-15 14:30:28 - INFO - Upload para S3 concluído com sucesso
2024-01-15 14:30:30 - INFO - Removendo 2 backups antigos
2024-01-15 14:30:31 - INFO - Total de backups disponíveis: 28
2024-01-15 14:30:31 - INFO - === BACKUP CONCLUÍDO COM SUCESSO ===
```

## ⚙️ Configurações Avançadas

### Personalizar Retenção de Backups

```bash
# Manter backups por 60 dias
export BACKUP_RETENTION_DAYS=60

# Manter apenas 7 dias (semanal)
export BACKUP_RETENTION_DAYS=7
```

### Personalizar Horário do Backup

Edite `.github/workflows/backup-database.yml`:

```yaml
on:
  schedule:
    # Diário às 03:00 UTC ao invés de 02:00
    - cron: '0 3 * * *'
    
    # Ou apenas aos domingos às 02:00 UTC
    - cron: '0 2 * * 0'
```

### Configurar Notificações

Para receber notificações de falha, adicione no workflow:

```yaml
- name: Notificar falha via Slack
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: failure
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## 🛠️ Troubleshooting

### Erro: "pg_dump não encontrado"

**Solução:**
```bash
# Ubuntu/Debian
sudo apt-get install postgresql-client

# macOS
brew install postgresql

# Windows
# Baixar PostgreSQL do site oficial
```

### Erro: "Configurações S3 incompletas"

**Verificar variáveis:**
```bash
echo $AWS_ACCESS_KEY_ID
echo $S3_BACKUP_BUCKET
# Não exiba AWS_SECRET_ACCESS_KEY por segurança
```

### Erro: "Access Denied" no S3

**Verificar permissões IAM:**
- Usuário tem acesso ao bucket?
- Política JSON está correta?
- Credenciais estão válidas?

### Backup muito lento

**Otimizações:**
- Use região S3 próxima ao Railway
- Verifique conexão de rede
- Configure `--jobs` no pg_dump para paralelização

### Restauração falha

**Verificações:**
- Arquivo de backup não corrompido?
- DATABASE_URL correta?
- Banco de destino acessível?
- Permissões de escrita no banco?

## 📈 Custos Estimados

### AWS S3 (us-east-1)

**Assumindo banco de 100MB comprimido:**
- **Armazenamento:** ~$0.50/mês (30 backups × 100MB × $0.023/GB)
- **Uploads:** ~$0.01/mês (30 uploads × $0.0005/1000 requests)
- **Downloads:** $0.09/GB (apenas quando restaurar)

**Total estimado:** ~$0.51/mês

### GitHub Actions

- **2000 minutos grátis/mês** (suficiente para backups diários)
- **Backup leva ~2-3 minutos/dia** = 90 minutos/mês
- **Custo:** $0 (dentro do limite gratuito)

## 🔐 Segurança

### Boas Práticas

1. **Credenciais AWS:**
   - Use usuário IAM dedicado (não root)
   - Rotacione credenciais regularmente
   - Permissões mínimas necessárias

2. **Secrets GitHub:**
   - Nunca commite credenciais no código
   - Use secrets do repositório
   - Revise acessos regularmente

3. **Backup:**
   - Teste restaurações periodicamente
   - Monitore logs de backup
   - Configure alertas de falha

### Criptografia

- **Em trânsito:** HTTPS/TLS automático (AWS)
- **Em repouso:** AES-256 padrão do S3
- **Para maior segurança:** Habilite S3 KMS

## 📚 Estrutura dos Arquivos

```
├── scripts/
│   ├── backup_postgres_s3.py      # Script principal de backup
│   ├── restore_postgres_s3.py     # Script de restauração
│   └── env.backup.example         # Exemplo de configuração
├── .github/workflows/
│   └── backup-database.yml        # GitHub Actions workflow
├── docs/
│   └── BACKUP_POSTGRESQL_S3.md    # Esta documentação
└── requirements.txt               # Dependências atualizadas
```

## 🤝 Suporte

### Logs e Debugging

1. **Ativar logs detalhados:**
   ```python
   logging.getLogger().setLevel(logging.DEBUG)
   ```

2. **Testar conectividade:**
   ```bash
   # Testar Railway
   psql $DATABASE_URL -c "SELECT version();"
   
   # Testar S3
   aws s3 ls s3://meu-bucket-backups
   ```

### Contato

Para problemas específicos:
1. Verifique os logs detalhados
2. Consulte o troubleshooting acima
3. Teste componentes individualmente
4. Documente o erro completo

---

## 📝 Changelog

### v1.0.0 (2024-01-15)
- ✅ Sistema completo de backup PostgreSQL → S3
- ✅ Restauração automática com confirmação
- ✅ GitHub Actions para execução diária
- ✅ Rotação automática de backups antigos
- ✅ Logs detalhados e monitoramento
- ✅ Documentação completa

---

**🎉 Pronto!** Seu sistema de backup automático está configurado e funcionando!
