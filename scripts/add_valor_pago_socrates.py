#!/usr/bin/env python3
"""
Script para adicionar campo valor_pago_socrates nas tabelas de despesas
"""

import os
import sys
import psycopg2
from urllib.parse import urlparse

def add_valor_pago_socrates_columns():
    """Adiciona as colunas valor_pago_socrates nas tabelas de despesas"""
    
    # Obter URL de conexão do ambiente
    database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/socrates_online')
    
    try:
        # Conectar ao banco
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # SQL para adicionar as colunas
        sql_commands = [
            "ALTER TABLE despesas_evento ADD COLUMN IF NOT EXISTS valor_pago_socrates FLOAT;",
            "ALTER TABLE despesas_empresa ADD COLUMN IF NOT EXISTS valor_pago_socrates FLOAT;"
        ]
        
        for sql in sql_commands:
            print(f"Executando: {sql}")
            cursor.execute(sql)
        
        # Confirmar transação
        conn.commit()
        print("✅ Colunas valor_pago_socrates adicionadas com sucesso!")
        
        # Fechar conexões
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao adicionar colunas: {e}")
        return False

if __name__ == "__main__":
    success = add_valor_pago_socrates_columns()
    sys.exit(0 if success else 1)
