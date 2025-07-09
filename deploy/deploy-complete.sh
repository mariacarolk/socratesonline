#!/bin/bash

# SCRIPT AUTOMÁTICO DE DEPLOY - SOCRATES ONLINE
# Arquivo: /home/socrates/socrates_online/deploy/deploy-complete.sh
# Execute como: bash deploy-complete.sh

set -e  # Parar em caso de erro

# Configurações
DOMAIN="seudominio.com.br"
DB_NAME="socrates_db"
DB_USER="socrates_user"
DB_PASSWORD="senha_super_segura_aqui"
APP_USER="socrates"
APP_DIR="/home/$APP_USER/socrates_online"
VENV_DIR="$APP_DIR/venv"
LOG_DIR="$APP_DIR/logs"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

info() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# Verificar se está rodando como root
if [[ $EUID -eq 0 ]]; then
   error "Este script não deve ser executado como root"
   exit 1
fi

# Banner
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

# PASSO 2: Instalar dependências do sistema
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
ALTER USER $DB_USER CREATEDB;
\q
EOF

# PASSO 4: Criar diretórios necessários
log "PASSO 4: Criando estrutura de diretórios..."
mkdir -p $LOG_DIR
mkdir -p $APP_DIR/uploads/comprovantes
mkdir -p /home/$APP_USER/backups

# PASSO 5: Configurar ambiente Python
log "PASSO 5: Configurando ambiente Python..."
cd $APP_DIR
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# Instalar dependências Python
pip install --upgrade pip
pip install -r deploy/requirements-production.txt

# PASSO 6: Configurar variáveis de ambiente
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

# PASSO 7: Migrar banco de dados
log "PASSO 7: Migrando banco de dados..."
export FLASK_APP=app.py
flask db upgrade

# PASSO 8: Configurar Nginx
log "PASSO 8: Configurando Nginx..."
# Substituir domínio no arquivo de configuração
sed "s/seudominio.com.br/$DOMAIN/g" deploy/nginx.conf > /tmp/nginx_socrates.conf
sudo cp /tmp/nginx_socrates.conf /etc/nginx/sites-available/socrates

# Ativar site
sudo ln -sf /etc/nginx/sites-available/socrates /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Testar configuração do Nginx
if sudo nginx -t; then
    log "Configuração do Nginx OK"
    sudo systemctl reload nginx
else
    error "Erro na configuração do Nginx"
    exit 1
fi

# PASSO 9: Configurar Supervisor
log "PASSO 9: Configurando Supervisor..."
sudo cp deploy/supervisor.conf /etc/supervisor/conf.d/socrates.conf
sudo supervisorctl reread
sudo supervisorctl update

# PASSO 10: Configurar SSL com Let's Encrypt
log "PASSO 10: Configurando SSL..."
if sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN; then
    log "SSL configurado com sucesso"
else
    warning "Falha na configuração SSL. Configure manualmente depois."
fi

# PASSO 11: Configurar firewall
log "PASSO 11: Configurando firewall..."
bash deploy/firewall-setup.sh

# PASSO 12: Configurar backup automático
log "PASSO 12: Configurando backup automático..."
chmod +x deploy/backup.sh

# Adicionar ao cron
(crontab -l 2>/dev/null; echo "0 2 * * * $APP_DIR/deploy/backup.sh") | crontab -

# PASSO 13: Configurar logrotate
log "PASSO 13: Configurando rotação de logs..."
sudo tee /etc/logrotate.d/socrates > /dev/null << EOF
$LOG_DIR/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 $APP_USER $APP_USER
    postrotate
        sudo supervisorctl restart socrates
    endscript
}

/var/log/nginx/socrates_*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        sudo systemctl reload nginx
    endscript
}
EOF

# PASSO 14: Ajustar permissões
log "PASSO 14: Ajustando permissões..."
sudo chown -R $APP_USER:$APP_USER $APP_DIR
sudo chmod -R 755 $APP_DIR
sudo chmod 700 $APP_DIR/.env
sudo chmod +x $APP_DIR/deploy/*.sh

# PASSO 15: Iniciar aplicação
log "PASSO 15: Iniciando aplicação..."
sudo supervisorctl start socrates

# Aguardar inicialização
sleep 10

# PASSO 16: Verificar status dos serviços
log "PASSO 16: Verificando status dos serviços..."

# Verificar Nginx
if systemctl is-active --quiet nginx; then
    log "✓ Nginx está rodando"
else
    error "✗ Nginx não está rodando"
fi

# Verificar Supervisor
if systemctl is-active --quiet supervisor; then
    log "✓ Supervisor está rodando"
else
    error "✗ Supervisor não está rodando"
fi

# Verificar aplicação
if sudo supervisorctl status socrates | grep -q RUNNING; then
    log "✓ Aplicação Socrates está rodando"
else
    error "✗ Aplicação Socrates não está rodando"
fi

# Verificar PostgreSQL
if systemctl is-active --quiet postgresql; then
    log "✓ PostgreSQL está rodando"
else
    error "✗ PostgreSQL não está rodando"
fi

# Verificar UFW
if sudo ufw status | grep -q "Status: active"; then
    log "✓ Firewall UFW está ativo"
else
    warning "✗ Firewall UFW não está ativo"
fi

# PASSO 17: Teste de conectividade
log "PASSO 17: Testando conectividade..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 | grep -q "200\|302"; then
    log "✓ Aplicação responde localmente"
else
    warning "✗ Aplicação não responde localmente"
fi

# PASSO 18: Criar script de monitoramento
log "PASSO 18: Criando script de monitoramento..."
cat > /home/$APP_USER/monitor-health.sh << 'EOF'
#!/bin/bash
# Monitor de saúde da aplicação

LOG_FILE="/home/socrates/health-check.log"
APP_URL="http://localhost:5000"

check_service() {
    local service=$1
    if systemctl is-active --quiet $service; then
        echo "[$(date)] ✓ $service OK" >> $LOG_FILE
        return 0
    else
        echo "[$(date)] ✗ $service FAILED" >> $LOG_FILE
        return 1
    fi
}

# Verificar serviços essenciais
check_service nginx
check_service postgresql
check_service supervisor

# Verificar aplicação
if curl -s -f $APP_URL > /dev/null; then
    echo "[$(date)] ✓ Application OK" >> $LOG_FILE
else
    echo "[$(date)] ✗ Application FAILED" >> $LOG_FILE
    # Tentar reiniciar aplicação
    sudo supervisorctl restart socrates
    echo "[$(date)] Application restarted" >> $LOG_FILE
fi

# Verificar espaço em disco
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 85 ]; then
    echo "[$(date)] ⚠ High disk usage: ${DISK_USAGE}%" >> $LOG_FILE
fi

# Manter apenas últimas 1000 linhas do log
tail -n 1000 $LOG_FILE > ${LOG_FILE}.tmp && mv ${LOG_FILE}.tmp $LOG_FILE
EOF

chmod +x /home/$APP_USER/monitor-health.sh

# Adicionar monitoramento ao cron (a cada 5 minutos)
(crontab -l 2>/dev/null; echo "*/5 * * * * /home/$APP_USER/monitor-health.sh") | crontab -

# PASSO 19: Informações finais
log "PASSO 19: Deploy concluído!"

echo -e "${GREEN}"
echo "========================================"
echo "    DEPLOY CONCLUÍDO COM SUCESSO!"
echo "========================================"
echo -e "${NC}"

info "Informações importantes:"
echo "• URL da aplicação: https://$DOMAIN"
echo "• Usuário do sistema: $APP_USER"
echo "• Diretório da aplicação: $APP_DIR"
echo "• Banco de dados: $DB_NAME"
echo "• Logs da aplicação: $LOG_DIR"
echo "• Backups: /home/$APP_USER/backups"

info "Comandos úteis:"
echo "• Status da aplicação: sudo supervisorctl status socrates"
echo "• Reiniciar aplicação: sudo supervisorctl restart socrates"
echo "• Ver logs: sudo tail -f $LOG_DIR/supervisor.log"
echo "• Status do Nginx: sudo systemctl status nginx"
echo "• Status do firewall: sudo ufw status"

info "Próximos passos:"
echo "1. Configure o DNS do domínio para apontar para este servidor"
echo "2. Teste a aplicação em https://$DOMAIN"
echo "3. Configure notificações de monitoramento por email"
echo "4. Execute o primeiro backup: $APP_DIR/deploy/backup.sh"
echo "5. Configure usuário administrativo inicial na aplicação"

warning "IMPORTANTE:"
echo "• Mantenha a senha do banco de dados segura"
echo "• Configure backups off-site"
echo "• Monitore os logs regularmente"
echo "• Mantenha o sistema atualizado"

log "Deploy finalizado às $(date)"
exit 0 