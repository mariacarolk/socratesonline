# Deploy no Railway - Sócrates Online

Este guia explica como fazer o deploy da aplicação Sócrates Online no Railway.

## Pré-requisitos

1. Conta no [Railway](https://railway.app/)
2. Repositório Git com o código (GitHub, GitLab, etc.)
3. **PostgreSQL instalado localmente** para desenvolvimento

## Passos para Deploy

### 1. Preparar o Projeto Localmente

1. **Copie o arquivo de exemplo de variáveis:**
   ```bash
   cp env.example .env
   ```

2. **Configure as variáveis no `.env` para desenvolvimento local:**
   ```env
   FLASK_ENV=development
   FLASK_APP=app.py
   SECRET_KEY=sua-chave-secreta-super-secreta-aqui
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/socrates_online
   ```
   
   **⚠️ Importante**: Certifique-se de que o PostgreSQL está instalado e rodando localmente com:
   - Usuário: `postgres`
   - Senha: `postgres` 
   - Banco: `socrates_online` (será criado automaticamente pelas migrações)

### 2. Deploy no Railway

1. **Acesse [Railway](https://railway.app/) e faça login**

2. **Crie um novo projeto:**
   - Clique em "New Project"
   - Selecione "Deploy from GitHub repo"
   - Escolha seu repositório

3. **Adicione PostgreSQL:**
   - No dashboard do projeto, clique em "+ New"
   - Selecione "Database" → "Add PostgreSQL"
   - O Railway criará automaticamente a variável `DATABASE_URL`

4. **Configure as variáveis de ambiente:**
   - Clique no serviço da aplicação
   - Vá para a aba "Variables"
   - Adicione as seguintes variáveis:

   ```
   FLASK_ENV=production
   SECRET_KEY=uma-chave-super-secreta-para-producao-aqui
   UPLOAD_FOLDER=uploads/comprovantes
   ```

   > **Importante:** Gere uma SECRET_KEY única e segura para produção!

5. **Deploy automático:**
   - O Railway detectará automaticamente os arquivos `railway.json` e `requirements.txt`
   - O deploy iniciará automaticamente
   - As migrações do banco serão executadas durante o startup via `flask db upgrade && python app.py`

### 3. Verificar o Deploy

1. **Acesse a aplicação:**
   - O Railway fornecerá uma URL pública
   - Acesse a URL para verificar se está funcionando

2. **Verificar logs:**
   - No dashboard do Railway, clique em "View Logs"
   - Verifique se não há erros

## Configurações Automáticas

O sistema foi configurado para detectar automaticamente se está rodando no Railway:

- **Detecção automática:** Usa a variável `RAILWAY_ENVIRONMENT`
- **Configuração de banco:** PostgreSQL obrigatório (Railway ou local)
- **Porta dinâmica:** Usa a variável `PORT` fornecida pelo Railway
- **Migrações:** Executadas automaticamente no deploy

## Desenvolvimento Local

Para desenvolvimento local, você **DEVE** usar PostgreSQL:

1. **Instalar PostgreSQL:**
   - Windows: [Download PostgreSQL](https://www.postgresql.org/download/windows/)
   - Configurar usuário `postgres` com senha `postgres`

2. **Configurar no `.env`:**
   ```env
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/socrates_online
   ```

3. **Criar banco (opcional - migrações criam automaticamente):**
   ```sql
   CREATE DATABASE socrates_online;
   ```

## Estrutura de Arquivos Criados/Modificados

```
├── railway.json            # Configurações do Railway (substituiu Procfile)
├── env.example             # Exemplo de variáveis de ambiente
├── requirements.txt        # Dependências atualizadas com versões específicas
├── config.py              # Configurações adaptadas para PostgreSQL
├── app.py                 # Configuração de porta dinâmica e detecção Railway
└── RAILWAY_DEPLOYMENT.md  # Este guia
```

## Troubleshooting

### Problema: Erro de conexão PostgreSQL durante build
**Erro:** `connection to server at "localhost" port 5432 failed`

**Solução:** Este erro ocorre quando as migrações tentam executar durante a fase de build, antes do banco estar disponível.

- ✅ **Corrigido:** Migrações agora executam durante o startup, não no build
- ✅ **Configuração:** `railway.json` configurado com `"startCommand": "flask db upgrade && python app.py"`
- ✅ **Requirements:** Adicionado `psycopg2-binary` com versão específica

### Problema: Aplicação não inicia
- Verifique os logs no Railway
- Confirme se todas as variáveis de ambiente estão configuradas
- Verifique se o PostgreSQL está conectado
- Certifique-se de que `DATABASE_URL` foi criada automaticamente pelo Railway

### Problema: Erro de migração
- As migrações são executadas automaticamente durante o startup
- Se houver problemas, verifique os logs do deploy
- Certifique-se de que o banco PostgreSQL está disponível

### Problema: Upload de arquivos
- O Railway tem sistema de arquivos efêmero
- Para produção, considere usar serviços externos como AWS S3

## Monitoramento

- Use os logs do Railway para monitorar a aplicação
- Configure alertas se necessário
- O Railway fornece métricas básicas de uso

## Backup

- Configure backups regulares do PostgreSQL
- O Railway oferece opções de backup para bancos de dados

---

Para mais informações sobre o Railway, consulte a [documentação oficial](https://docs.railway.app/).
