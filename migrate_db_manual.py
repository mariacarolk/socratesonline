#!/usr/bin/env python3
"""
Script de migração manual do banco de dados
"""

import sqlite3
import os

def migrar_banco():
    db_path = 'instance/database.db'
    
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("🔄 Iniciando migração manual do banco...")
        
        # 1. Adicionar coluna id_colaborador na tabela usuario (se não existir)
        try:
            cursor.execute("ALTER TABLE usuario ADD COLUMN id_colaborador INTEGER")
            print("✅ Coluna id_colaborador adicionada à tabela usuario")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("⚠️  Coluna id_colaborador já existe")
            else:
                raise
        
        # 2. Verificar se existem usuários para migrar
        cursor.execute("SELECT id, nome FROM usuario WHERE id_colaborador IS NULL")
        usuarios = cursor.fetchall()
        
        if not usuarios:
            print("✅ Nenhum usuário precisa ser migrado")
            return
        
        print(f"📊 Encontrados {len(usuarios)} usuários para migrar")
        
        # 3. Para cada usuário, encontrar ou criar colaborador correspondente
        for usuario_id, usuario_nome in usuarios:
            # Verificar se já existe colaborador com esse nome
            cursor.execute("SELECT id_colaborador FROM colaborador WHERE nome = ?", (usuario_nome,))
            colaborador = cursor.fetchone()
            
            if colaborador:
                colaborador_id = colaborador[0]
                print(f"🔄 Usando colaborador existente: {usuario_nome}")
            else:
                # Criar novo colaborador
                cursor.execute("INSERT INTO colaborador (nome) VALUES (?)", (usuario_nome,))
                colaborador_id = cursor.lastrowid
                print(f"✅ Colaborador criado: {usuario_nome}")
                
                # Associar categoria administrativa por padrão
                cursor.execute("SELECT id_categoria_colaborador FROM categoria_colaborador WHERE nome = 'Administrativo'")
                categoria_admin = cursor.fetchone()
                
                if categoria_admin:
                    cursor.execute(
                        "INSERT INTO colaborador_categoria (id_colaborador, id_categoria_colaborador) VALUES (?, ?)",
                        (colaborador_id, categoria_admin[0])
                    )
                    print(f"✅ Categoria Administrativo associada ao colaborador {usuario_nome}")
            
            # Atualizar usuário com referência ao colaborador
            cursor.execute("UPDATE usuario SET id_colaborador = ? WHERE id = ?", (colaborador_id, usuario_id))
            print(f"✅ Usuário {usuario_nome} vinculado ao colaborador")
        
        # 4. Remover coluna categoria_id (se existir)
        try:
            # SQLite não suporta DROP COLUMN diretamente, então vamos ignorar por enquanto
            print("⚠️  Coluna categoria_id mantida (SQLite não suporta DROP COLUMN)")
        except:
            pass
        
        conn.commit()
        print(f"\n✅ Migração concluída! {len(usuarios)} usuários migrados")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Erro na migração: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrar_banco() 