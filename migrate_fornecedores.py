#!/usr/bin/env python3
"""
Script para migrar dados de fornecedores existentes
Adiciona campos cidade e estado aos fornecedores que não possuem
"""

from app import app, db
from models import Fornecedor

def migrar_fornecedores():
    """Migra fornecedores existentes adicionando campos vazios para cidade e estado"""
    with app.app_context():
        try:
            # Buscar fornecedores que não têm cidade ou estado
            fornecedores_sem_localizacao = Fornecedor.query.filter(
                (Fornecedor.cidade.is_(None)) | (Fornecedor.estado.is_(None))
            ).all()
            
            print(f"Encontrados {len(fornecedores_sem_localizacao)} fornecedores sem localização completa")
            
            # Atualizar fornecedores
            for fornecedor in fornecedores_sem_localizacao:
                if not fornecedor.cidade:
                    fornecedor.cidade = ""
                if not fornecedor.estado:
                    fornecedor.estado = ""
                    
                print(f"Atualizado: {fornecedor.nome}")
            
            # Salvar mudanças
            db.session.commit()
            print("Migração concluída com sucesso!")
            
            # Mostrar estatísticas
            total_fornecedores = Fornecedor.query.count()
            fornecedores_com_localizacao = Fornecedor.query.filter(
                (Fornecedor.cidade != "") & (Fornecedor.estado != "")
            ).count()
            
            print(f"\nEstatísticas:")
            print(f"Total de fornecedores: {total_fornecedores}")
            print(f"Com localização completa: {fornecedores_com_localizacao}")
            print(f"Sem localização: {total_fornecedores - fornecedores_com_localizacao}")
            
        except Exception as e:
            print(f"Erro durante a migração: {e}")
            db.session.rollback()

if __name__ == "__main__":
    migrar_fornecedores() 