#!/usr/bin/env python3
"""
Script para inicializar o usuário ROOT do Sistema Sócrates Online
Este script pode ser executado independentemente para criar o usuário ROOT
"""

import os
import sys
from datetime import datetime

# Configurar o ambiente
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Função principal para inicializar o usuário ROOT"""
    try:
        from app import app, db
        from models import Usuario, Colaborador, CategoriaColaborador, ColaboradorCategoria
        from werkzeug.security import generate_password_hash
        
        print("🚀 Iniciando configuração do Sistema Sócrates Online...")
        print("=" * 60)
        
        with app.app_context():
            # Verificar se já existe usuário ROOT
            usuario_root = Usuario.query.filter_by(email='root@socratesonline.com').first()
            if usuario_root:
                print("✅ Usuário ROOT já existe!")
                print(f"📧 Email: root@socratesonline.com")
                print(f"👤 Nome: {usuario_root.nome}")
                print(f"🏷️ Categorias: {', '.join([cat.nome for cat in usuario_root.colaborador.categorias])}")
                return
            
            print("🔄 Criando usuário ROOT do sistema...")
            
            # Criar categorias básicas se não existirem
            categorias_basicas = [
                'Administrativo',
                'Operacional', 
                'Promotor de Vendas',
                'Produtor',
                'Motorista',
                'Técnico'
            ]
            
            print("\n📝 Verificando/Criando categorias de colaborador...")
            categorias_criadas = []
            for nome_categoria in categorias_basicas:
                categoria_existente = CategoriaColaborador.query.filter_by(nome=nome_categoria).first()
                if not categoria_existente:
                    nova_categoria = CategoriaColaborador(nome=nome_categoria)
                    db.session.add(nova_categoria)
                    db.session.flush()  # Para obter o ID
                    categorias_criadas.append(nova_categoria)
                    print(f"   ✓ Categoria '{nome_categoria}' criada")
                else:
                    categorias_criadas.append(categoria_existente)
                    print(f"   ✓ Categoria '{nome_categoria}' já existe")
            
            # Verificar se já existe colaborador ROOT
            colaborador_root = Colaborador.query.filter_by(email='root@socratesonline.com').first()
            if not colaborador_root:
                print("\n👤 Criando colaborador ROOT...")
                colaborador_root = Colaborador(
                    nome='ROOT - Administrador do Sistema',
                    telefone='(00) 00000-0000',
                    email='root@socratesonline.com'
                )
                db.session.add(colaborador_root)
                db.session.flush()  # Para obter o ID do colaborador
                print("   ✓ Colaborador ROOT criado")
            else:
                print("\n👤 Colaborador ROOT já existe")
            
            # Verificar e associar todas as categorias ao colaborador ROOT
            print("\n🏷️ Associando categorias ao colaborador ROOT...")
            categorias_associadas = [assoc.categoria for assoc in colaborador_root.categorias_associacao]
            categorias_adicionadas = 0
            
            for categoria in categorias_criadas:
                if categoria not in categorias_associadas:
                    associacao = ColaboradorCategoria(
                        id_colaborador=colaborador_root.id_colaborador,
                        id_categoria_colaborador=categoria.id_categoria_colaborador
                    )
                    db.session.add(associacao)
                    categorias_adicionadas += 1
                    print(f"   ✓ Categoria '{categoria.nome}' associada")
                else:
                    print(f"   ✓ Categoria '{categoria.nome}' já associada")
            
            # Criar usuário ROOT
            print("\n🔐 Criando usuário ROOT...")
            senha_hash = generate_password_hash('Admin@2025')
            usuario_root = Usuario(
                nome='ROOT',
                email='root@socratesonline.com',
                senha_hash=senha_hash,
                id_colaborador=colaborador_root.id_colaborador
            )
            db.session.add(usuario_root)
            
            db.session.commit()
            
            print("\n" + "=" * 60)
            print("✅ USUÁRIO ROOT CRIADO COM SUCESSO!")
            print("=" * 60)
            print(f"📧 Email: root@socratesonline.com")
            print(f"🔒 Senha: Admin@2025")
            print(f"👤 Nome: ROOT")
            print(f"🏷️ Categorias: {', '.join([cat.nome for cat in categorias_criadas])}")
            print(f"📅 Criado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}")
            print("\n💡 INSTRUÇÕES:")
            print("1. Acesse o sistema usando as credenciais acima")
            print("2. O usuário ROOT tem acesso a todas as funcionalidades")
            print("3. Recomenda-se criar outros usuários específicos para cada função")
            print("4. A senha pode ser alterada após o primeiro login")
            print("\n🚀 Sistema pronto para uso!")
            
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Certifique-se de que o ambiente virtual está ativo e as dependências estão instaladas")
        print("   Execute: pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário ROOT: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
