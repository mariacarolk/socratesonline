# Deploy no Railway - Sócrates Online

## Configuração Automática de Migrações

### Como funciona

O sistema está configurado para aplicar automaticamente as migrações do banco de dados durante o deploy no Railway através do script `deploy.py`.

### Arquivos de Configuração

#### 1. `railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python deploy.py && gunicorn -w 2 -k gthread -t 120 -b 0.0.0.0:$PORT app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### 2. `deploy.py`
Script que executa antes da aplicação iniciar:
- ✅ Aplica migrações do banco (`flask db upgrade`)
- ✅ Fallback: cria tabelas se migrações falharem (`db.create_all()`)
- ✅ Garante que o usuário root existe
- ✅ Tratamento de erros robusto

### Processo de Deploy

1. **Build**: Railway constrói a aplicação
2. **Deploy**: Executa `python deploy.py`
   - Aplica migrações pendentes
   - Verifica/cria usuário root
   - Registra logs detalhados
3. **Start**: Inicia o Gunicorn com a aplicação Flask

### Logs do Deploy

Durante o deploy, você verá logs como:
```
🌐 Deploy para Railway - Sócrates Online
==================================================
🔄 Aplicando migrações do banco de dados...
✅ Aplicando migrações do banco de dados - Sucesso
👑 Criando usuário root...
✅ Usuário root criado com sucesso
==================================================
✅ Deploy concluído com sucesso!
🚀 Iniciando aplicação...
```

### Variáveis de Ambiente Necessárias

No Railway, configure:
- `DATABASE_URL` - URL do banco PostgreSQL
- `SECRET_KEY` - Chave secreta da aplicação
- `FLASK_ENV` - `production`

### Troubleshooting

#### Se as migrações falharem:
1. O script tentará criar as tabelas diretamente (`db.create_all()`)
2. Logs detalhados mostrarão o erro específico
3. A aplicação pode falhar no start se o banco não estiver configurado

#### Usuário Root:
- Criado automaticamente como `root@socratesonline.com` / `admin123`
- Categoria: `administrativo`
- Acesso total ao sistema

### Comandos Manuais (se necessário)

Se precisar executar migrações manualmente:

```bash
# No Railway Console
flask db upgrade

# Verificar status das migrações
flask db current
flask db heads

# Criar usuário root manualmente (se necessário)
python -c "
from app import app
from extensions import db
from models import Usuario
from werkzeug.security import generate_password_hash

with app.app_context():
    root = Usuario(
        nome='Administrador Root',
        email='root@socratesonline.com',
        categoria='administrativo',
        senha=generate_password_hash('admin123')
    )
    db.session.add(root)
    db.session.commit()
    print('Usuário root criado!')
"
```

### Estrutura de Migrações

As migrações estão em `migrations/versions/` e são aplicadas em ordem cronológica:
- Alembic gerencia o versionamento
- Cada migração tem um ID único
- O sistema mantém controle do estado atual

### Monitoramento

- Railway mostra logs em tempo real
- Erros de migração aparecem no console
- Reinicializações automáticas em caso de falha (até 10 tentativas)

### Backup e Rollback

⚠️ **Importante**: Railway PostgreSQL não tem rollback automático de migrações.
- Sempre teste migrações localmente primeiro
- Considere fazer backup manual antes de deploys grandes
- Use `flask db downgrade` com cuidado em produção
