#!/usr/bin/env python3
"""
Script de Backup Manual - Execução Única
========================================

Script simplificado para executar backup único do PostgreSQL Railway para S3.
Útil para testes, backups pontuais ou execução em servidores.

Uso:
    python scripts/backup_manual.py

Este script:
- Executa um backup único
- Mostra progresso detalhado
- Lista backups disponíveis após conclusão
- Ideal para testes e verificações
"""

import sys
import os

# Adicionar o diretório raiz ao path para importar o módulo principal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from scripts.backup_postgres_s3 import PostgreSQLBackupS3, logger
except ImportError as e:
    print(f"Erro ao importar módulo de backup: {e}")
    print("Certifique-se de que o arquivo backup_postgres_s3.py existe e está correto.")
    sys.exit(1)

def main():
    """Executa backup manual com interface amigável."""
    
    print("=" * 60)
    print("🚀 BACKUP MANUAL POSTGRESQL → S3")
    print("=" * 60)
    print()
    
    try:
        # Inicializar sistema de backup
        print("📋 Inicializando sistema de backup...")
        backup_system = PostgreSQLBackupS3()
        
        print(f"✅ Bucket S3: {backup_system.s3_bucket}")
        print(f"✅ Retenção: {backup_system.backup_retention_days} dias")
        print()
        
        # Listar backups existentes
        print("📂 Verificando backups existentes...")
        existing_backups = backup_system.list_backups()
        
        if existing_backups:
            print(f"   Encontrados {len(existing_backups)} backups:")
            for i, backup in enumerate(existing_backups[:3], 1):
                print(f"   {i}. {backup['key']} ({backup['size_mb']:.1f} MB)")
            
            if len(existing_backups) > 3:
                print(f"   ... e mais {len(existing_backups) - 3} backups")
        else:
            print("   Nenhum backup encontrado (primeiro backup)")
        
        print()
        
        # Confirmar execução
        response = input("🤔 Deseja executar o backup agora? (s/N): ").strip().lower()
        
        if response not in ['s', 'sim', 'y', 'yes']:
            print("❌ Backup cancelado pelo usuário.")
            return
        
        print()
        print("🔄 Executando backup...")
        print("-" * 40)
        
        # Executar backup
        success = backup_system.run_backup()
        
        print("-" * 40)
        
        if success:
            print("✅ BACKUP CONCLUÍDO COM SUCESSO!")
            
            # Mostrar estatísticas finais
            final_backups = backup_system.list_backups()
            if final_backups:
                latest = final_backups[0]
                print(f"📦 Último backup: {latest['key']}")
                print(f"📏 Tamanho: {latest['size_mb']:.2f} MB")
                print(f"🕒 Data: {latest['last_modified'].strftime('%d/%m/%Y %H:%M:%S')}")
            
            print(f"📊 Total de backups: {len(final_backups)}")
            
        else:
            print("❌ BACKUP FALHOU!")
            print("📋 Verifique os logs acima para detalhes do erro.")
            
    except KeyboardInterrupt:
        print("\n⚠️ Backup interrompido pelo usuário.")
        
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        print(f"💥 Erro fatal: {e}")
        
    finally:
        print()
        print("=" * 60)
        print("🏁 Backup manual finalizado.")
        print("=" * 60)

if __name__ == "__main__":
    main()
