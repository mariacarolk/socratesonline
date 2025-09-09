#!/usr/bin/env python3
"""
Script de Restauração PostgreSQL do S3
======================================

Este script restaura um backup do PostgreSQL armazenado no S3.

ATENÇÃO: Este script irá SOBRESCREVER o banco de dados atual!
Use apenas em situações de emergência ou para restaurar em ambiente de teste.

Uso:
    python scripts/restore_postgres_s3.py [backup_key]
    
    Se backup_key não for especificado, será usado o backup mais recente.

Exemplo:
    python scripts/restore_postgres_s3.py socrates-online_backup_20240115_143022.sql.gz
"""

import os
import sys
import subprocess
import boto3
import gzip
import logging
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional, List

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PostgreSQLRestoreS3:
    def __init__(self):
        """Inicializa o sistema de restauração."""
        
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
        
        self.backup_prefix = os.getenv('BACKUP_PREFIX', 'socrates-online')
        
        # Cliente S3
        self.s3_client = boto3.client(
            's3',
            region_name=self.s3_region,
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key
        )
        
        logger.info(f"Restauração configurada para bucket: {self.s3_bucket}")

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

    def list_available_backups(self) -> List[dict]:
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

    def download_backup(self, backup_key: str) -> str:
        """Baixa o backup do S3 para arquivo temporário."""
        try:
            logger.info(f"Baixando backup: {backup_key}")
            
            # Criar arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix='.sql.gz') as temp_file:
                temp_path = temp_file.name
            
            # Download do S3
            self.s3_client.download_file(self.s3_bucket, backup_key, temp_path)
            
            backup_size = os.path.getsize(temp_path)
            logger.info(f"Backup baixado: {backup_size / 1024 / 1024:.2f} MB")
            
            return temp_path
            
        except Exception as e:
            logger.error(f"Erro no download do backup: {e}")
            raise

    def decompress_backup(self, compressed_path: str) -> str:
        """Descomprime o arquivo de backup."""
        try:
            logger.info("Descomprimindo backup...")
            
            # Criar arquivo descomprimido
            decompressed_path = compressed_path.replace('.gz', '')
            
            with gzip.open(compressed_path, 'rb') as f_in:
                with open(decompressed_path, 'wb') as f_out:
                    f_out.writelines(f_in)
            
            decompressed_size = os.path.getsize(decompressed_path)
            logger.info(f"Backup descomprimido: {decompressed_size / 1024 / 1024:.2f} MB")
            
            return decompressed_path
            
        except Exception as e:
            logger.error(f"Erro na descompressão: {e}")
            raise

    def restore_database(self, sql_file_path: str) -> bool:
        """Restaura o banco de dados usando psql."""
        db_config = self.parse_database_url()
        
        try:
            logger.info("Iniciando restauração do banco de dados...")
            logger.warning("ATENÇÃO: O banco atual será SOBRESCRITO!")
            
            # Comando psql para restauração
            cmd = [
                'psql',
                f"--host={db_config['host']}",
                f"--port={db_config['port']}",
                f"--username={db_config['username']}",
                f"--dbname={db_config['database']}",
                '--quiet',
                f"--file={sql_file_path}"
            ]
            
            # Configurar variável de ambiente para senha
            env = os.environ.copy()
            env['PGPASSWORD'] = db_config['password']
            
            logger.info(f"Executando: psql para {db_config['database']}")
            
            # Executar psql
            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
                timeout=3600  # 60 minutos timeout
            )
            
            if result.returncode != 0:
                logger.error(f"Erro no psql: {result.stderr}")
                return False
            
            logger.info("Restauração concluída com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro na restauração: {e}")
            return False

    def run_restore(self, backup_key: Optional[str] = None) -> bool:
        """Executa o processo completo de restauração."""
        temp_files = []
        
        try:
            logger.info("=== INICIANDO RESTAURAÇÃO DO BACKUP ===")
            logger.info(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 1. Listar backups disponíveis
            backups = self.list_available_backups()
            
            if not backups:
                logger.error("Nenhum backup encontrado no S3")
                return False
            
            # 2. Determinar qual backup usar
            if backup_key:
                # Verificar se o backup especificado existe
                backup_exists = any(b['key'] == backup_key for b in backups)
                if not backup_exists:
                    logger.error(f"Backup especificado não encontrado: {backup_key}")
                    logger.info("Backups disponíveis:")
                    for backup in backups[:5]:  # Mostrar apenas os 5 mais recentes
                        logger.info(f"  - {backup['key']} ({backup['size_mb']:.2f} MB)")
                    return False
                
                selected_backup = backup_key
            else:
                # Usar o backup mais recente
                selected_backup = backups[0]['key']
                logger.info(f"Usando backup mais recente: {selected_backup}")
            
            # 3. Baixar backup do S3
            compressed_path = self.download_backup(selected_backup)
            temp_files.append(compressed_path)
            
            # 4. Descomprimir backup
            sql_path = self.decompress_backup(compressed_path)
            temp_files.append(sql_path)
            
            # 5. Confirmar restauração (apenas em modo interativo)
            if sys.stdin.isatty():
                confirmation = input(f"\nATENÇÃO: Isso irá SOBRESCREVER o banco atual!\n"
                                   f"Backup: {selected_backup}\n"
                                   f"Deseja continuar? (digite 'CONFIRMAR' para prosseguir): ")
                
                if confirmation != 'CONFIRMAR':
                    logger.info("Restauração cancelada pelo usuário")
                    return False
            
            # 6. Executar restauração
            success = self.restore_database(sql_path)
            
            if success:
                logger.info("=== RESTAURAÇÃO CONCLUÍDA COM SUCESSO ===")
                logger.info(f"Banco restaurado a partir de: {selected_backup}")
            else:
                logger.error("=== RESTAURAÇÃO FALHOU ===")
            
            return success
            
        except Exception as e:
            logger.error(f"Erro na restauração: {e}")
            logger.error("=== RESTAURAÇÃO FALHOU ===")
            return False
            
        finally:
            # Limpar arquivos temporários
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    logger.info(f"Arquivo temporário removido: {temp_file}")


def main():
    """Função principal."""
    try:
        # Verificar se psql está disponível
        result = subprocess.run(['psql', '--version'], capture_output=True)
        if result.returncode != 0:
            logger.error("psql não encontrado. Instale PostgreSQL client tools.")
            sys.exit(1)
        
        # Obter backup_key dos argumentos
        backup_key = sys.argv[1] if len(sys.argv) > 1 else None
        
        # Executar restauração
        restore_system = PostgreSQLRestoreS3()
        success = restore_system.run_restore(backup_key)
        
        sys.exit(0 if success else 1)
        
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
