#!/bin/bash

# CONFIGURAÇÃO DE FIREWALL - SOCRATES ONLINE
# Arquivo: /home/socrates/socrates_online/deploy/firewall-setup.sh

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

log "Configurando firewall UFW para Socrates Online..."

# Verificar se UFW está instalado
if ! command -v ufw &> /dev/null; then
    log "Instalando UFW..."
    sudo apt update
    sudo apt install ufw -y
fi

# Reset UFW para configuração limpa
log "Resetando configurações do UFW..."
sudo ufw --force reset

# Definir políticas padrão
log "Definindo políticas padrão..."
sudo ufw default deny incoming
sudo ufw default allow outgoing

# SSH (CRÍTICO - sempre permitir primeiro)
log "Permitindo SSH (porta 22)..."
sudo ufw allow ssh
sudo ufw allow 22

# HTTP e HTTPS
log "Permitindo HTTP (porta 80)..."
sudo ufw allow 80

log "Permitindo HTTPS (porta 443)..."
sudo ufw allow 443

# PostgreSQL (apenas localhost se necessário)
log "Configurando acesso ao PostgreSQL..."
sudo ufw allow from 127.0.0.1 to any port 5432

# Gunicorn (apenas localhost)
log "Configurando acesso ao Gunicorn..."
sudo ufw allow from 127.0.0.1 to any port 5000

# Opcional: Permitir ping (ICMP)
log "Permitindo ping (ICMP)..."
sudo ufw allow in on any to any proto icmp

# Opcional: Se usar servidor de email local
# sudo ufw allow 25   # SMTP
# sudo ufw allow 587  # SMTP TLS
# sudo ufw allow 993  # IMAP SSL
# sudo ufw allow 995  # POP3 SSL

# Opcional: Se usar Redis
# sudo ufw allow from 127.0.0.1 to any port 6379

# Opcional: Se usar monitoramento
# sudo ufw allow 9090  # Prometheus
# sudo ufw allow 3000  # Grafana

# Configurações de rate limiting para SSH
log "Configurando rate limiting para SSH..."
sudo ufw limit ssh

# Configurações de rate limiting para HTTP/HTTPS
log "Configurando rate limiting para HTTP/HTTPS..."
sudo ufw limit 80
sudo ufw limit 443

# Regras específicas para bloqueio de IPs maliciosos (opcional)
log "Configurando regras de segurança adicionais..."

# Bloquear tentativas de acesso a portas comuns de ataque
sudo ufw deny 23    # Telnet
sudo ufw deny 135   # RPC
sudo ufw deny 139   # NetBIOS
sudo ufw deny 445   # SMB
sudo ufw deny 1433  # SQL Server
sudo ufw deny 3389  # RDP

# Permitir apenas conexões estabelecidas e relacionadas
sudo ufw allow in on any to any state established,related

# Log das tentativas de conexão
log "Habilitando logs do UFW..."
sudo ufw logging on

# Ativar UFW
log "Ativando UFW..."
sudo ufw --force enable

# Mostrar status
log "Status atual do firewall:"
sudo ufw status verbose

# Criar script para monitorar tentativas de acesso
log "Criando script de monitoramento..."
cat > /home/socrates/monitor-firewall.sh << 'EOF'
#!/bin/bash
# Monitor de tentativas de acesso bloqueadas

LOG_FILE="/var/log/ufw.log"
REPORT_FILE="/home/socrates/firewall-report.txt"

echo "RELATÓRIO DE SEGURANÇA - $(date)" > $REPORT_FILE
echo "======================================" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# IPs mais bloqueados nas últimas 24h
echo "TOP 10 IPs BLOQUEADOS (últimas 24h):" >> $REPORT_FILE
if [ -f "$LOG_FILE" ]; then
    grep "$(date --date='1 day ago' '+%b %d')" $LOG_FILE | \
    grep "BLOCK" | \
    awk '{print $13}' | \
    sort | uniq -c | sort -nr | head -10 >> $REPORT_FILE
else
    echo "Log do UFW não encontrado" >> $REPORT_FILE
fi

echo "" >> $REPORT_FILE

# Estatísticas gerais
echo "ESTATÍSTICAS GERAIS:" >> $REPORT_FILE
if [ -f "$LOG_FILE" ]; then
    TOTAL_BLOCKS=$(grep "BLOCK" $LOG_FILE | wc -l)
    echo "Total de bloqueios: $TOTAL_BLOCKS" >> $REPORT_FILE
    
    TODAY_BLOCKS=$(grep "$(date '+%b %d')" $LOG_FILE | grep "BLOCK" | wc -l)
    echo "Bloqueios hoje: $TODAY_BLOCKS" >> $REPORT_FILE
else
    echo "Estatísticas não disponíveis" >> $REPORT_FILE
fi

echo "" >> $REPORT_FILE
echo "Status do UFW:" >> $REPORT_FILE
ufw status >> $REPORT_FILE

# Enviar por email se configurado
# mail -s "Relatório de Segurança Diário" admin@seudominio.com.br < $REPORT_FILE
EOF

chmod +x /home/socrates/monitor-firewall.sh

# Configurar cron para relatórios diários
log "Configurando relatórios automáticos..."
(crontab -l 2>/dev/null; echo "0 6 * * * /home/socrates/monitor-firewall.sh") | crontab -

# Configurações adicionais de segurança do sistema
log "Aplicando configurações adicionais de segurança..."

# Fail2ban para proteção contra ataques de força bruta
if ! command -v fail2ban-server &> /dev/null; then
    log "Instalando Fail2ban..."
    sudo apt install fail2ban -y
    
    # Configurar Fail2ban para SSH e Nginx
    sudo tee /etc/fail2ban/jail.local > /dev/null <<EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log

[nginx-noscript]
enabled = true
port = http,https
filter = nginx-noscript
logpath = /var/log/nginx/access.log
maxretry = 6

[nginx-badbots]
enabled = true
port = http,https
filter = nginx-badbots
logpath = /var/log/nginx/access.log
maxretry = 2

[nginx-noproxy]
enabled = true
port = http,https
filter = nginx-noproxy
logpath = /var/log/nginx/access.log
maxretry = 2
EOF

    sudo systemctl enable fail2ban
    sudo systemctl start fail2ban
    log "Fail2ban configurado e iniciado"
fi

log "Configuração de firewall concluída!"
log "IMPORTANTE: Verifique se consegue acessar via SSH antes de desconectar!"

# Salvar configuração para backup
sudo ufw status numbered > /home/socrates/ufw-backup.txt

log "Backup das regras UFW salvo em: /home/socrates/ufw-backup.txt"

exit 0 