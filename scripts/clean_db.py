#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para limpar a tabela alembic_version
"""
import psycopg2
from psycopg2 import sql

def clean_alembic_table():
    """Limpar tabela alembic_version"""
    try:
        # Conexão usando parâmetros separados (evita problemas de encoding)
        conn = psycopg2.connect(
            host="localhost",
            database="socrates_online",
            user="postgres",
            password="postgres",
            port=5432
        )
        
        cur = conn.cursor()
        
        # Verificar se tabela existe
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_name = 'alembic_version'
            );
        """)
        
        exists = cur.fetchone()[0]
        
        if exists:
            # Tentar obter versão atual
            try:
                cur.execute("SELECT version_num FROM alembic_version")
                version = cur.fetchone()
                if version:
                    print(f"Versao atual: {version[0]}")
            except:
                pass
            
            # Limpar tabela
            cur.execute("DELETE FROM alembic_version")
            conn.commit()
            print("Tabela alembic_version limpa com sucesso!")
        else:
            print("Tabela alembic_version nao existe")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Erro: {e}")
        return False

if __name__ == "__main__":
    clean_alembic_table()
