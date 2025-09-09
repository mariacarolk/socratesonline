#!/usr/bin/env python3
"""
Script de Backup Automático PostgreSQL Railway → S3
==================================================

Este script realiza backup do banco PostgreSQL do Railway e envia para S3.

Configuração necessária:
- Variáveis de ambiente para Railway DB
- Credenciais AWS S3
- pg_dump instalado (ou usar via Docker)

Uso:
    python scripts/backup_postgres_s3.py
"""

import os
import sys
import subprocess
import boto3
import gzip
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List
import tempfile

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PostgreSQLBackupS3:
    def __init__(self):
        """Inicializa o sistema de backup com configurações do ambiente."""
        
        # Configurações do Railway PostgreSQL
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL não encontrada nas variáveis de ambiente")
        
        # Configurações S3
        self.s3_bucket = os.getenv('S3_BACKUP_BUCKET')
        self.s3_region = os.getenv('S3_BACKUP_REGION', 'us-east-1')
        self.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        
        if not all([self.s3_bucket, self.aws_access_key, self.aws_secret_key]):
            raise ValueError("Configurações S3 incompletas. Verifique as variáveis de ambiente.")
        
        # Configurações de backup
        self.backup_retention_days = int(os.getenv('BACKUP_RETENTION_DAYS', '30'))
        self.backup_prefix = os.getenv('BACKUP_PREFIX', 'socrates-online')
        
        # Cliente S3
        self.s3_client = boto3.client(
            's3',
            region_name=self.s3_region,
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key
        )
        
        logger.info(f"Backup configurado para bucket: {self.s3_bucket}")
        logger.info(f"Retenção: {self.backup_retention_days} dias")

    def parse_database_url(self) -> dict:
        """Extrai componentes da DATABASE_URL do Railway."""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(self.database_url)
            
            return {
                'host': parsed.hostname,
                'port': parsed.port or 5432,
                'database': parsed.path.lstrip('/'),
                'username': parsed.username,
                'password': parsed.password
            }
        except Exception as e:
            logger.error(f"Erro ao parsear DATABASE_URL: {e}")
            raise

    def create_backup(self) -> str:
        """Cria backup do PostgreSQL usando pg_dump."""
        db_config = self.parse_database_url()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"{self.backup_prefix}_backup_{timestamp}.sql"
        
        logger.info("Iniciando backup do PostgreSQL...")
        
        # Criar arquivo temporário para o backup
        with tempfile.NamedTemporaryFile(mode='w+b', delete=False, suffix='.sql') as temp_file:
            temp_path = temp_file.name
        
        try:
            # Comando pg_dump com compatibilidade máxima
            cmd = [
                'pg_dump',
                f"--host={db_config['host']}",
                f"--port={db_config['port']}",
                f"--username={db_config['username']}",
                f"--dbname={db_config['database']}",
                '--clean',
                '--no-owner',
                '--no-privileges',
                '--format=plain',
                '--inserts',  # Usar INSERT statements (mais compatível)
                '--column-inserts',  # INSERT com nomes de colunas
                f"--file={temp_path}"
            ]
            
            # Configurar variável de ambiente para senha e compatibilidade
            env = os.environ.copy()
            env['PGPASSWORD'] = db_config['password']
            env['PGOPTIONS'] = '--client-min-messages=warning'  # Reduzir warnings
            
            logger.info(f"Executando: pg_dump para {db_config['database']}")
            
            # Estratégia de fallback para compatibilidade de versão
            attempts = [
                (cmd, "Tentativa 1: Backup completo"),
                (cmd + ['--data-only'], "Tentativa 2: Apenas dados (fallback)"),
                (cmd + ['--schema-only'], "Tentativa 3: Apenas estrutura (fallback)")
            ]
            
            result = None
            for attempt_cmd, description in attempts:
                logger.info(description)
                result = subprocess.run(
                    attempt_cmd,
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=1800  # 30 minutos timeout
                )
                
                if result.returncode == 0:
                    logger.info("Backup executado com sucesso!")
                    break
                elif "server version mismatch" in result.stderr:
                    logger.warning(f"Erro de versão: {result.stderr.split('detail:')[1] if 'detail:' in result.stderr else 'incompatibilidade detectada'}")
                    continue
                else:
                    # Outro tipo de erro, parar tentativas
                    break
            
            if result.returncode != 0:
                logger.error(f"Erro no pg_dump: {result.stderr}")
                raise subprocess.CalledProcessError(result.returncode, cmd, result.stderr)
            
            logger.info("Backup criado com sucesso")
            
            # Comprimir o arquivo
            compressed_path = f"{temp_path}.gz"
            with open(temp_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    f_out.writelines(f_in)
            
            # Remover arquivo não comprimido
            os.unlink(temp_path)
            
            backup_size = os.path.getsize(compressed_path)
            logger.info(f"Backup comprimido: {backup_size / 1024 / 1024:.2f} MB")
            
            return compressed_path, f"{backup_filename}.gz"
            
        except Exception as e:
            # Limpar arquivo temporário em caso de erro
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise e

    def upload_to_s3(self, local_path: str, s3_key: str) -> bool:
        """Faz upload do backup para S3."""
        try:
            logger.info(f"Enviando backup para S3: s3://{self.s3_bucket}/{s3_key}")
            
            # Upload com metadata
            extra_args = {
                'Metadata': {
                    'backup-date': datetime.now().isoformat(),
                    'database': 'socrates-online',
                    'source': 'railway-postgresql'
                },
                'StorageClass': 'STANDARD_IA'  # Classe de armazenamento mais barata
            }
            
            self.s3_client.upload_file(
                local_path, 
                self.s3_bucket, 
                s3_key,
                ExtraArgs=extra_args
            )
            
            logger.info("Upload para S3 concluído com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro no upload para S3: {e}")
            return False

    def cleanup_old_backups(self):
        """Remove backups antigos do S3 baseado na política de retenção."""
        try:
            logger.info("Limpando backups antigos...")
            
            # Listar objetos no bucket
            response = self.s3_client.list_objects_v2(
                Bucket=self.s3_bucket,
                Prefix=f"{self.backup_prefix}_backup_"
            )
            
            if 'Contents' not in response:
                logger.info("Nenhum backup encontrado para limpeza")
                return
            
            # Calcular data limite
            cutoff_date = datetime.now() - timedelta(days=self.backup_retention_days)
            
            objects_to_delete = []
            for obj in response['Contents']:
                if obj['LastModified'].replace(tzinfo=None) < cutoff_date:
                    objects_to_delete.append({'Key': obj['Key']})
            
            # Deletar objetos antigos
            if objects_to_delete:
                logger.info(f"Removendo {len(objects_to_delete)} backups antigos")
                
                self.s3_client.delete_objects(
                    Bucket=self.s3_bucket,
                    Delete={'Objects': objects_to_delete}
                )
                
                for obj in objects_to_delete:
                    logger.info(f"Removido: {obj['Key']}")
            else:
                logger.info("Nenhum backup antigo para remover")
                
        except Exception as e:
            logger.error(f"Erro na limpeza de backups antigos: {e}")

    def list_backups(self) -> List[dict]:
        """Lista todos os backups disponíveis no S3."""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.s3_bucket,
                Prefix=f"{self.backup_prefix}_backup_"
            )
            
            if 'Contents' not in response:
                return []
            
            backups = []
            for obj in response['Contents']:
                backups.append({
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'],
                    'size_mb': obj['Size'] / 1024 / 1024
                })
            
            # Ordenar por data (mais recente primeiro)
            backups.sort(key=lambda x: x['last_modified'], reverse=True)
            
            return backups
            
        except Exception as e:
            logger.error(f"Erro ao listar backups: {e}")
            return []

    def run_backup(self) -> bool:
        """Executa o processo completo de backup."""
        try:
            logger.info("=== INICIANDO BACKUP AUTOMÁTICO ===")
            logger.info(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 1. Criar backup
            local_path, s3_key = self.create_backup()
            
            try:
                # 2. Upload para S3
                success = self.upload_to_s3(local_path, s3_key)
                
                if success:
                    # 3. Limpar backups antigos
                    self.cleanup_old_backups()
                    
                    # 4. Listar backups disponíveis
                    backups = self.list_backups()
                    logger.info(f"Total de backups disponíveis: {len(backups)}")
                    
                    if backups:
                        latest = backups[0]
                        logger.info(f"Backup mais recente: {latest['key']} ({latest['size_mb']:.2f} MB)")
                    
                    logger.info("=== BACKUP CONCLUÍDO COM SUCESSO ===")
                    return True
                else:
                    logger.error("=== BACKUP FALHOU NO UPLOAD ===")
                    return False
                    
            finally:
                # Sempre limpar arquivo local
                if os.path.exists(local_path):
                    os.unlink(local_path)
                    logger.info("Arquivo local temporário removido")
                    
        except Exception as e:
            logger.error(f"Erro no backup: {e}")
            logger.error("=== BACKUP FALHOU ===")
            return False


def main():
    """Função principal."""
    try:
        # Verificar se pg_dump está disponível
        result = subprocess.run(['pg_dump', '--version'], capture_output=True)
        if result.returncode != 0:
            logger.error("pg_dump não encontrado. Instale PostgreSQL client tools.")
            sys.exit(1)
        
        # Executar backup
        backup_system = PostgreSQLBackupS3()
        success = backup_system.run_backup()
        
        sys.exit(0 if success else 1)
        
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
