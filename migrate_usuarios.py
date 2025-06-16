#!/usr/bin/env python3
"""
Script de migração: Transferir usuários para usar CategoriaColaborador
"""

from app import app, db
from models import Usuario, CategoriaColaborador, Colaborador, ColaboradorCategoria
from sqlalchemy import text

def migrar_usuarios():
    with app.app_context():
        print("🔄 Iniciando migração de usuários...")
        
        # 1. Verificar se existem dados para migrar
        usuarios_raw = db.session.execute(text("SELECT * FROM usuario")).fetchall()
        if not usuarios_raw:
            print("❌ Nenhum usuário encontrado para migrar")
            return
        
        print(f"📊 Encontrados {len(usuarios_raw)} usuários para migrar")
        
        # 2. Garantir que as categorias básicas existam em CategoriaColaborador
        categorias_basicas = ['Administrativo', 'Produtor', 'Coreógrafo']
        for nome_categoria in categorias_basicas:
            categoria_existente = CategoriaColaborador.query.filter_by(nome=nome_categoria).first()
            if not categoria_existente:
                nova_categoria = CategoriaColaborador(nome=nome_categoria)
                db.session.add(nova_categoria)
                print(f"✅ Categoria '{nome_categoria}' criada em CategoriaColaborador")
        
        db.session.commit()
        
        # 3. Para cada usuário, criar um colaborador correspondente
        usuarios_migrados = 0
        categoria_admin = CategoriaColaborador.query.filter_by(nome='Administrativo').first()
        
        for usuario_raw in usuarios_raw:
            try:
                # Verificar se já existe um colaborador para este usuário
                colaborador_existente = Colaborador.query.filter_by(nome=usuario_raw.nome).first()
                
                if not colaborador_existente:
                    # Criar novo colaborador
                    novo_colaborador = Colaborador(nome=usuario_raw.nome)
                    db.session.add(novo_colaborador)
                    db.session.flush()  # Para obter o ID
                    
                    # Associar categoria administrativa por padrão
                    if categoria_admin:
                        colaborador_categoria = ColaboradorCategoria(
                            id_colaborador=novo_colaborador.id_colaborador,
                            id_categoria_colaborador=categoria_admin.id_categoria_colaborador
                        )
                        db.session.add(colaborador_categoria)
                    
                    colaborador = novo_colaborador
                    print(f"✅ Colaborador criado para usuário: {usuario_raw.nome}")
                else:
                    colaborador = colaborador_existente
                    print(f"🔄 Usando colaborador existente: {usuario_raw.nome}")
                
                # Atualizar usuário com referência ao colaborador
                db.session.execute(
                    text("UPDATE usuario SET id_colaborador = :colaborador_id WHERE id = :usuario_id"),
                    {"colaborador_id": colaborador.id_colaborador, "usuario_id": usuario_raw.id}
                )
                
                usuarios_migrados += 1
                
            except Exception as e:
                print(f"❌ Erro ao migrar usuário {usuario_raw.nome}: {str(e)}")
                db.session.rollback()
                continue
        
        print(f"\n✅ Migração concluída! {usuarios_migrados} usuários migrados")
        db.session.commit()

if __name__ == "__main__":
    migrar_usuarios() 