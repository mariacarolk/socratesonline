# 🚀 GUIA COMPLETO DE DEPLOY - SOCRATES ONLINE

## 📋 PRÉ-REQUISITOS

- Servidor Ubuntu 20.04+ (recomendado DigitalOcean, AWS, ou VPS)
- Domínio registrado (ex: seudominio.com.br)
- Conhecimento básico de terminal Linux

## 🏗️ PASSO 1: PREPARAR O SERVIDOR

### 1.1 - Conectar ao servidor via SSH
```bash
ssh root@SEU_IP_SERVIDOR
```

### 1.2 - Atualizar sistema
```bash
apt update && apt upgrade -y
```

### 1.3 - Criar usuário para a aplicação
```bash
adduser socrates
usermod -aG sudo socrates
su - socrates
```

## 🐍 PASSO 2: INSTALAR DEPENDÊNCIAS

### 2.1 - Python e ferramentas essenciais
```bash
sudo apt install python3 python3-pip python3-venv nginx supervisor git -y
```

### 2.2 - Instalar PostgreSQL (recomendado para produção)
```bash
sudo apt install postgresql postgresql-contrib -y
```

## 💾 PASSO 3: CONFIGURAR BANCO DE DADOS

### 3.1 - Configurar PostgreSQL
```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE socrates_db;
CREATE USER socrates_user WITH PASSWORD 'senha_super_segura_aqui';
GRANT ALL PRIVILEGES ON DATABASE socrates_db TO socrates_user;
\q
```

## 📁 PASSO 4: PREPARAR A APLICAÇÃO

### 4.1 - Clonar o repositório
```bash
cd /home/socrates
git clone https://github.com/SEU_USUARIO/socrates_online.git
cd socrates_online
```

### 4.2 - Criar ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4.3 - Instalar dependências Python
```bash
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

## ⚙️ PASSO 5: CONFIGURAR VARIÁVEIS DE AMBIENTE

### 5.1 - Criar arquivo de ambiente
```bash
nano .env
```

### 5.2 - Configurar variáveis (ver arquivo .env)

## 🗄️ PASSO 6: MIGRAR BANCO DE DADOS

```bash
export FLASK_APP=app.py
flask db upgrade
```

## 🌐 PASSO 7: CONFIGURAR NGINX

### 7.1 - Configurar Nginx (ver arquivo nginx.conf)
### 7.2 - Ativar configuração

```bash
sudo ln -s /home/socrates/socrates_online/deploy/nginx.conf /etc/nginx/sites-available/socrates
sudo ln -s /etc/nginx/sites-available/socrates /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

## 🔧 PASSO 8: CONFIGURAR GUNICORN

### 8.1 - Criar configuração do Gunicorn (ver arquivo gunicorn.conf.py)
### 8.2 - Configurar Supervisor (ver arquivo supervisor.conf)

```bash
sudo cp deploy/supervisor.conf /etc/supervisor/conf.d/socrates.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start socrates
```

## 🔒 PASSO 9: CONFIGURAR SSL (HTTPS)

### 9.1 - Instalar Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 9.2 - Obter certificado SSL
```bash
sudo certbot --nginx -d seudominio.com.br
```

## 🔄 PASSO 10: CONFIGURAR BACKUP

### 10.1 - Criar script de backup (ver arquivo backup.sh)
### 10.2 - Configurar cron para backup diário

```bash
crontab -e
# Adicionar linha:
0 2 * * * /home/socrates/socrates_online/deploy/backup.sh
```

## 📊 PASSO 11: CONFIGURAR MONITORAMENTO

### 11.1 - Instalar htop e configurar logs
```bash
sudo apt install htop -y
```

### 11.2 - Configurar logrotate (ver arquivo logrotate.conf)

## 🎯 COMANDOS ÚTEIS

### Verificar status da aplicação
```bash
sudo supervisorctl status socrates
```

### Reiniciar aplicação
```bash
sudo supervisorctl restart socrates
```

### Ver logs da aplicação
```bash
sudo tail -f /home/socrates/socrates_online/logs/gunicorn.log
```

### Atualizar aplicação
```bash
cd /home/socrates/socrates_online
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
sudo supervisorctl restart socrates
```

## 🛡️ SEGURANÇA

1. **Firewall**: Configure UFW para permitir apenas portas necessárias
2. **SSH**: Configure autenticação por chave
3. **Backup**: Automatize backups diários
4. **Updates**: Configure atualizações automáticas de segurança
5. **Monitoring**: Configure alertas de monitoramento

## 📋 CHECKLIST FINAL

- [ ] Servidor configurado e atualizado
- [ ] Python, Nginx, PostgreSQL instalados
- [ ] Banco de dados criado e configurado
- [ ] Aplicação rodando com Gunicorn
- [ ] Nginx configurado como proxy reverso
- [ ] SSL/HTTPS configurado
- [ ] Domínio apontando para o servidor
- [ ] Backup automático configurado
- [ ] Logs configurados
- [ ] Firewall configurado
- [ ] Monitoramento ativo

## 🆘 TROUBLESHOOTING

### Aplicação não inicia
```bash
sudo supervisorctl tail socrates stderr
```

### Problemas de permissão
```bash
sudo chown -R socrates:socrates /home/socrates/socrates_online
sudo chmod -R 755 /home/socrates/socrates_online
```

### Nginx não consegue conectar
```bash
sudo nginx -t
sudo systemctl status nginx
```

### Problemas de banco
```bash
sudo -u postgres psql -d socrates_db
```

## 💰 ESTIMATIVA DE CUSTOS (MENSAL)

- **VPS DigitalOcean**: $20-40/mês
- **Domínio**: $10-15/ano
- **SSL**: Gratuito (Let's Encrypt)
- **Backup**: $5-10/mês
- **Total**: ~$25-50/mês

## 🎉 CONCLUSÃO

Após seguir todos estes passos, sua aplicação Socrates Online estará rodando em produção de forma segura e escalável! 