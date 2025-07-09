#!/bin/bash

# SCRIPT AUTOMÁTICO DE DEPLOY - SOCRATES ONLINE
# Execute como: bash complete-deploy-script.sh

set -e  # Parar em caso de erro

# Configurações (EDITE ESTAS VARIÁVEIS)
DOMAIN="seudominio.com.br"
DB_NAME="socrates_db"
DB_USER="socrates_user"
DB_PASSWORD="sua_senha_super_segura_aqui_123"
APP_USER="socrates"
ADMIN_EMAIL="admin@seudominio.com.br"

# Diretórios
APP_DIR="/home/$APP_USER/socrates_online"
VENV_DIR="$APP_DIR/venv"
LOG_DIR="$APP_DIR/logs"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"; }
error() { echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"; }
warning() { echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"; }
info() { echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"; }

# Verificar se está rodando como root
if [[ $EUID -eq 0 ]]; then
   error "Este script não deve ser executado como root"
   exit 1
fi

echo -e "${BLUE}"
echo "========================================"
echo "    DEPLOY AUTOMÁTICO SOCRATES ONLINE"
echo "========================================"
echo -e "${NC}"

# Confirmação
read -p "Deseja continuar com o deploy? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    log "Deploy cancelado pelo usuário"
    exit 1
fi

# PASSO 1: Atualizar sistema
log "PASSO 1: Atualizando o sistema..."
sudo apt update && sudo apt upgrade -y

# PASSO 2: Instalar dependências
log "PASSO 2: Instalando dependências do sistema..."
sudo apt install -y python3 python3-pip python3-venv nginx supervisor git \
    postgresql postgresql-contrib ufw fail2ban htop curl wget unzip \
    certbot python3-certbot-nginx logrotate

# PASSO 3: Configurar PostgreSQL
log "PASSO 3: Configurando PostgreSQL..."
sudo -u postgres psql << EOF
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
\q
EOF

# PASSO 4: Criar diretórios
log "PASSO 4: Criando estrutura de diretórios..."
mkdir -p $LOG_DIR
mkdir -p $APP_DIR/uploads/comprovantes
mkdir -p /home/$APP_USER/backups

# PASSO 5: Configurar Python
log "PASSO 5: Configurando ambiente Python..."
cd $APP_DIR
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install flask flask-sqlalchemy flask-wtf python-dotenv werkzeug openpyxl \
    reportlab flask-login alembic gunicorn psycopg2-binary

# PASSO 6: Configurar .env
log "PASSO 6: Configurando variáveis de ambiente..."
cat > $APP_DIR/.env << EOF
FLASK_ENV=production
FLASK_APP=app.py
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost/$DB_NAME
UPLOAD_FOLDER=$APP_DIR/uploads/comprovantes
MAX_CONTENT_LENGTH=16777216
DOMAIN_NAME=$DOMAIN
LOG_FILE=$LOG_DIR/app.log
EOF

# PASSO 7: Migrar banco
log "PASSO 7: Migrando banco de dados..."
export FLASK_APP=app.py
flask db upgrade

# PASSO 8: Configurar Nginx
log "PASSO 8: Configurando Nginx..."
cat > /tmp/nginx_socrates.conf << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;

    root $APP_DIR;
    client_max_body_size 20M;

    location /static {
        alias $APP_DIR/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /uploads {
        alias $APP_DIR/uploads;
        try_files \$uri @app;
    }

    location / {
        try_files \$uri @app;
    }

    location @app {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    access_log /var/log/nginx/socrates_access.log;
    error_log /var/log/nginx/socrates_error.log;
}
EOF

sudo cp /tmp/nginx_socrates.conf /etc/nginx/sites-available/socrates
sudo ln -sf /etc/nginx/sites-available/socrates /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

if sudo nginx -t; then
    log "Nginx configurado com sucesso"
    sudo systemctl reload nginx
else
    error "Erro na configuração do Nginx"
    exit 1
fi

# PASSO 9: Configurar Supervisor
log "PASSO 9: Configurando Supervisor..."
sudo tee /etc/supervisor/conf.d/socrates.conf > /dev/null << EOF
[program:socrates]
command=$VENV_DIR/bin/gunicorn -w 3 -b 127.0.0.1:5000 app:app
directory=$APP_DIR
user=$APP_USER
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=$LOG_DIR/supervisor.log
environment=PATH="$VENV_DIR/bin"
EOF

sudo supervisorctl reread
sudo supervisorctl update

# PASSO 10: Configurar SSL
log "PASSO 10: Configurando SSL..."
if sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email $ADMIN_EMAIL; then
    log "SSL configurado com sucesso"
else
    warning "Falha na configuração SSL"
fi

# PASSO 11: Configurar Firewall
log "PASSO 11: Configurando firewall..."
sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

# PASSO 12: Configurar backup
log "PASSO 12: Configurando backup..."
cat > $APP_DIR/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/socrates/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup do banco
pg_dump -U socrates_user -h localhost socrates_db > $BACKUP_DIR/db_${DATE}.sql

# Backup dos uploads
tar -czf $BACKUP_DIR/uploads_${DATE}.tar.gz -C /home/socrates/socrates_online uploads/

# Limpeza (manter 30 dias)
find $BACKUP_DIR -type f -mtime +30 -delete
EOF

chmod +x $APP_DIR/backup.sh
(crontab -l 2>/dev/null; echo "0 2 * * * $APP_DIR/backup.sh") | crontab -

# PASSO 13: Ajustar permissões
log "PASSO 13: Ajustando permissões..."
sudo chown -R $APP_USER:$APP_USER $APP_DIR
sudo chmod -R 755 $APP_DIR
sudo chmod 600 $APP_DIR/.env

# PASSO 14: Iniciar aplicação
log "PASSO 14: Iniciando aplicação..."
sudo supervisorctl start socrates
sleep 5

# PASSO 15: Verificações finais
log "PASSO 15: Verificando status..."

if systemctl is-active --quiet nginx; then
    log "✓ Nginx rodando"
else
    error "✗ Nginx parado"
fi

if sudo supervisorctl status socrates | grep -q RUNNING; then
    log "✓ Aplicação rodando"
else
    error "✗ Aplicação parada"
fi

if curl -s http://localhost:5000 | grep -q "Socrates\|Login\|html"; then
    log "✓ Aplicação respondendo"
else
    warning "✗ Aplicação não responde"
fi

echo -e "${GREEN}"
echo "========================================"
echo "    DEPLOY CONCLUÍDO!"
echo "========================================"
echo -e "${NC}"

info "Informações importantes:"
echo "• URL: https://$DOMAIN"
echo "• Banco: $DB_NAME"
echo "• Usuário: $DB_USER"
echo "• Logs: $LOG_DIR"

info "Comandos úteis:"
echo "• Status: sudo supervisorctl status socrates"
echo "• Reiniciar: sudo supervisorctl restart socrates"
echo "• Logs: sudo tail -f $LOG_DIR/supervisor.log"

warning "Próximos passos:"
echo "1. Configure DNS do domínio"
echo "2. Teste a aplicação"
echo "3. Crie usuário administrador"

log "Deploy finalizado!"
exit 0 