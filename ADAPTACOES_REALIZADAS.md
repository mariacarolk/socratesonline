# Adaptações para Railway e Local - Sócrates Online

## ✅ Adaptações Realizadas

### 1. **Configuração PostgreSQL Otimizada** (`config.py`)
- ✅ PostgreSQL obrigatório para todos os ambientes
- ✅ Fix automático para URLs do Railway (`postgres://` → `postgresql://`)
- ✅ Configurações otimizadas para cada ambiente:
  - **Railway**: Pool reduzido (15/30) com timeout adequado
  - **Produção**: Pool grande (20/40) para alta carga
  - **Desenvolvimento**: Pool pequeno (5/10) com logs SQL ativados

### 2. **Detecção Automática de Ambiente** (`app.py`)
- ✅ Detecta Railway via variável `RAILWAY_ENVIRONMENT`
- ✅ Porta dinâmica usando `PORT` (Railway) ou 5000 (local)
- ✅ Host configurado para `0.0.0.0` (necessário para Railway)
- ✅ Debug automático apenas em desenvolvimento

### 3. **Arquivos de Deploy**
- ✅ **`Procfile`**: Comandos para iniciar app e executar migrações
- ✅ **`railway.json`**: Configurações específicas do Railway
- ✅ **`requirements.txt`**: Versões fixas + `psycopg2-binary` + `gunicorn`

### 4. **Estrutura de Projeto**
- ✅ **`env.example`**: Template de variáveis de ambiente
- ✅ **`.gitignore`**: Ignora arquivos sensíveis e temporários
- ✅ **`.gitkeep`**: Mantém pasta de uploads no Git
- ✅ **`RAILWAY_DEPLOYMENT.md`**: Guia completo de deploy

## 🔧 Como Funciona

### **Desenvolvimento Local**
1. **PostgreSQL obrigatório**: Define `DATABASE_URL` no `.env` ou usa padrão
2. **Configuração padrão**: `postgresql://postgres:postgres@localhost:5432/socrates_online`
3. **Debug**: Ativado automaticamente com `FLASK_ENV=development`

### **Railway (Produção)**
1. **Detecção**: Via variável `RAILWAY_ENVIRONMENT` (automática)
2. **Banco**: PostgreSQL fornecido pelo Railway
3. **Migrações**: Executadas automaticamente no deploy
4. **Porta**: Dinâmica via variável `PORT`

## 🚀 Para Usar

### **Desenvolvimento Local**
```bash
# 1. Instalar e configurar PostgreSQL local
# 2. Copiar variáveis de ambiente
cp env.example .env

# 3. Configurar .env
FLASK_ENV=development
SECRET_KEY=sua-chave-local
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/socrates_online

# 4. Executar migrações e app
flask db upgrade
python app.py
```

### **Deploy no Railway**
1. Conectar repositório ao Railway
2. Adicionar PostgreSQL no dashboard
3. Configurar variáveis:
   - `SECRET_KEY`: Chave única para produção
   - `FLASK_ENV`: production
4. Deploy automático!

## 📊 Configurações por Ambiente

| Ambiente | Banco | Pool Size | Debug | Porta | Logs SQL |
|----------|-------|-----------|-------|-------|----------|
| **Desenvolvimento** | PostgreSQL | 5/10 | ✅ | 5000 | ✅ |
| **Railway** | PostgreSQL | 15/30 | ❌ | Dinâmica | ❌ |
| **Produção** | PostgreSQL | 20/40 | ❌ | 5000 | ❌ |

## ✨ Vantagens da Adaptação

1. **PostgreSQL Consistente**: Mesmo banco em todos os ambientes
2. **Deploy Simples**: Railway detecta tudo automaticamente
3. **Configuração Padrão**: PostgreSQL local configurado automaticamente
4. **Migrações Automáticas**: Banco sempre atualizado no deploy
5. **Configuração Otimizada**: Cada ambiente com settings ideais
6. **Compatibilidade Total**: Mesmo comportamento local e produção

## 🔍 Configuração Corrigida

**Problema identificado**: Sistema estava usando SQLite como fallback desnecessário.

**Solução aplicada**: 
- ✅ PostgreSQL obrigatório para todos os ambientes
- ✅ Configuração padrão: `postgresql://postgres:postgres@localhost:5432/socrates_online`
- ✅ Sem fallback SQLite - mantém consistência com ambiente original

**Agora o sistema usa PostgreSQL como esperado!**
