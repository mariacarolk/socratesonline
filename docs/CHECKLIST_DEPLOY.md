# Checklist de Deploy - Railway

## ✅ Pré-Deploy (Local)

### 1. Migrações
- [ ] Testar migrações localmente: `flask db upgrade`
- [ ] Verificar se todas as migrações estão commitadas
- [ ] Confirmar que `flask db current` mostra a última migração

### 2. Dependências
- [ ] `requirements.txt` atualizado
- [ ] Todas as dependências testadas localmente
- [ ] Versões compatíveis com produção

### 3. Configurações
- [ ] `railway.json` configurado com `deploy.py`
- [ ] Variáveis de ambiente documentadas
- [ ] Arquivo `.env.example` atualizado

## ✅ Configuração Railway

### 1. Variáveis de Ambiente
- [ ] `DATABASE_URL` - PostgreSQL URL
- [ ] `SECRET_KEY` - Chave secreta forte
- [ ] `FLASK_ENV=production`
- [ ] `MAIL_SERVER` (se usando email)
- [ ] `MAIL_USERNAME` e `MAIL_PASSWORD` (se necessário)

### 2. Banco de Dados
- [ ] PostgreSQL plugin ativo
- [ ] `DATABASE_URL` conectado automaticamente
- [ ] Conexão testada

## ✅ Deploy

### 1. Push para Railway
- [ ] Código commitado no Git
- [ ] Push para branch principal
- [ ] Railway iniciou build automaticamente

### 2. Monitoramento do Deploy
- [ ] Logs do build sem erros
- [ ] Script `deploy.py` executado com sucesso
- [ ] Migrações aplicadas: `✅ Aplicando migrações do banco de dados - Sucesso`
- [ ] Usuário root criado: `✅ Usuário root criado com sucesso`
- [ ] Gunicorn iniciado sem erros

### 3. Verificação da Aplicação
- [ ] Site carrega corretamente
- [ ] Login funciona
- [ ] Login com `root@socratesonline.com` / `admin123` funciona
- [ ] Menus aparecem corretamente conforme permissões

## ✅ Pós-Deploy

### 1. Testes Funcionais
- [ ] Dashboard carrega para usuário root
- [ ] Cadastros funcionam
- [ ] Marketing dashboard funciona
- [ ] Relatórios geram corretamente

### 2. Configurações Iniciais
- [ ] Alterar senha do usuário root
- [ ] Criar usuários administrativos necessários
- [ ] Configurar parâmetros do sistema
- [ ] Testar envio de emails (se configurado)

### 3. Monitoramento
- [ ] Verificar logs de erro
- [ ] Monitorar performance
- [ ] Configurar alertas (se necessário)

## 🚨 Troubleshooting

### Se o deploy falhar:

1. **Erro de Migração**:
   ```bash
   # No Railway Console
   flask db current
   flask db heads
   flask db upgrade
   ```

2. **Usuário Root não criado**:
   ```bash
   # No Railway Console
   python -c "
   from app import app
   from extensions import db
   from models import Usuario
   from werkzeug.security import generate_password_hash
   
   with app.app_context():
       root = Usuario.query.filter_by(email='root@socratesonline.com').first()
       if not root:
           root = Usuario(
               nome='Administrador Root',
               email='root@socratesonline.com',
               categoria='administrativo',
               senha=generate_password_hash('admin123')
           )
           db.session.add(root)
           db.session.commit()
           print('Usuário root criado!')
       else:
           print('Usuário root já existe')
   "
   ```

3. **Erro de Dependências**:
   - Verificar `requirements.txt`
   - Testar `pip install -r requirements.txt` localmente
   - Verificar logs de build no Railway

4. **Erro de Configuração**:
   - Verificar variáveis de ambiente
   - Testar `DATABASE_URL` manualmente
   - Verificar `railway.json`

## 📋 Comandos Úteis

### Railway CLI
```bash
# Login no Railway
railway login

# Ver logs em tempo real
railway logs

# Conectar ao console
railway shell

# Ver variáveis de ambiente
railway variables
```

### Flask (no Railway Console)
```bash
# Status das migrações
flask db current
flask db heads

# Aplicar migrações
flask db upgrade

# Verificar usuários
python -c "from app import app; from models import Usuario; from extensions import db; 
with app.app_context(): print([u.email for u in Usuario.query.all()])"
```

## 🎯 Sucesso!

Quando tudo estiver funcionando:
- ✅ Site acessível via URL do Railway
- ✅ Login root funcionando
- ✅ Todos os menus visíveis para root
- ✅ Funcionalidades básicas operacionais
- ✅ Banco de dados com migrações aplicadas
