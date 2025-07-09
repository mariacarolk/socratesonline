#!/bin/bash

# SCRIPT DE BACKUP AUTOMÁTICO - SOCRATES ONLINE
# Arquivo: /home/socrates/socrates_online/deploy/backup.sh

# Configurações
APP_DIR="/home/socrates/socrates_online"
BACKUP_DIR="/home/socrates/backups"
DB_NAME="socrates_db"
DB_USER="socrates_user"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função de log
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

# Criar diretório de backup se não existir
mkdir -p $BACKUP_DIR

log "Iniciando backup do Socrates Online..."

# 1. Backup do banco de dados PostgreSQL
log "Fazendo backup do banco de dados..."
pg_dump -U $DB_USER -h localhost $DB_NAME > $BACKUP_DIR/database_${DATE}.sql

if [ $? -eq 0 ]; then
    log "Backup do banco de dados criado: database_${DATE}.sql"
else
    error "Falha no backup do banco de dados"
    exit 1
fi

# 2. Backup dos arquivos de upload
log "Fazendo backup dos arquivos de upload..."
if [ -d "$APP_DIR/uploads" ]; then
    tar -czf $BACKUP_DIR/uploads_${DATE}.tar.gz -C $APP_DIR uploads/
    if [ $? -eq 0 ]; then
        log "Backup dos uploads criado: uploads_${DATE}.tar.gz"
    else
        error "Falha no backup dos uploads"
    fi
else
    warning "Diretório de uploads não encontrado"
fi

# 3. Backup da configuração
log "Fazendo backup das configurações..."
tar -czf $BACKUP_DIR/config_${DATE}.tar.gz -C $APP_DIR \
    --exclude="venv" \
    --exclude="__pycache__" \
    --exclude="*.pyc" \
    --exclude=".git" \
    --exclude="logs" \
    --exclude="instance/database.db" \
    .

if [ $? -eq 0 ]; then
    log "Backup das configurações criado: config_${DATE}.tar.gz"
else
    error "Falha no backup das configurações"
fi

# 4. Backup dos logs (últimos 7 dias)
log "Fazendo backup dos logs..."
if [ -d "$APP_DIR/logs" ]; then
    find $APP_DIR/logs -name "*.log" -mtime -7 -exec tar -czf $BACKUP_DIR/logs_${DATE}.tar.gz {} +
    if [ $? -eq 0 ]; then
        log "Backup dos logs criado: logs_${DATE}.tar.gz"
    else
        warning "Nenhum log recente encontrado ou falha no backup"
    fi
else
    warning "Diretório de logs não encontrado"
fi

# 5. Criar arquivo de informações do sistema
log "Criando arquivo de informações do sistema..."
{
    echo "BACKUP INFORMATION - $(date)"
    echo "=================================="
    echo "Server: $(hostname)"
    echo "Date: $(date)"
    echo "App Version: $(cd $APP_DIR && git rev-parse HEAD 2>/dev/null || echo 'N/A')"
    echo "App Branch: $(cd $APP_DIR && git branch --show-current 2>/dev/null || echo 'N/A')"
    echo "Python Version: $(python3 --version)"
    echo "Nginx Status: $(systemctl is-active nginx)"
    echo "Supervisor Status: $(systemctl is-active supervisor)"
    echo "Disk Usage:"
    df -h
    echo ""
    echo "Memory Usage:"
    free -h
    echo ""
    echo "System Load:"
    uptime
} > $BACKUP_DIR/system_info_${DATE}.txt

# 6. Limpeza de backups antigos
log "Limpando backups antigos (mais de $RETENTION_DAYS dias)..."
find $BACKUP_DIR -name "*.sql" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "*.txt" -mtime +$RETENTION_DAYS -delete

if [ $? -eq 0 ]; then
    log "Limpeza de backups antigos concluída"
else
    warning "Problemas na limpeza de backups antigos"
fi

# 7. Verificar espaço em disco
DISK_USAGE=$(df $BACKUP_DIR | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    warning "Uso de disco alto: ${DISK_USAGE}%"
    # Enviar alerta por email (opcional)
    # echo "Disk usage is at ${DISK_USAGE}%" | mail -s "High Disk Usage Alert" admin@seudominio.com.br
fi

# 8. Calcular tamanho total dos backups
TOTAL_SIZE=$(du -sh $BACKUP_DIR | cut -f1)
log "Tamanho total dos backups: $TOTAL_SIZE"

# 9. Verificar integridade do backup do banco
log "Verificando integridade do backup do banco..."
if pg_restore --list $BACKUP_DIR/database_${DATE}.sql > /dev/null 2>&1; then
    log "Backup do banco está íntegro"
else
    # Tentar como SQL plain text
    if head -n 10 $BACKUP_DIR/database_${DATE}.sql | grep -q "PostgreSQL database dump"; then
        log "Backup do banco (SQL) está íntegro"
    else
        error "Backup do banco pode estar corrompido"
    fi
fi

log "Backup concluído com sucesso!"
log "Arquivos criados:"
ls -la $BACKUP_DIR/*${DATE}*

# 10. Opcional: Upload para cloud storage (uncomment se usar)
# log "Enviando backup para cloud storage..."
# aws s3 cp $BACKUP_DIR/ s3://seu-bucket-backup/socrates/$(date +%Y/%m/%d)/ --recursive --exclude="*" --include="*${DATE}*"

exit 0 