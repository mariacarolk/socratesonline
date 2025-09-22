#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script ONE-TIME para limpar alembic_version no Railway
REMOVA este arquivo após usar!
"""
import os
import sys

def fix_railway_migrations():
    """Limpar alembic_version no Railway"""
    # Só executar em produção
    if not os.environ.get('RAILWAY_ENVIRONMENT'):
        print("Este script só deve ser executado no Railway!")
        sys.exit(1)
    
    try:
        from app import app
        from extensions import db
        
        with app.app_context():
            # Limpar alembic_version
            result = db.session.execute(db.text("DELETE FROM alembic_version"))
            db.session.commit()
            print(f"[RAILWAY FIX] Removidos {result.rowcount} registros da alembic_version")
            print("[RAILWAY FIX] Banco pronto para novas migrações!")
            
    except Exception as e:
        print(f"[RAILWAY FIX] Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fix_railway_migrations()
    print("\n[RAILWAY FIX] Script concluído. REMOVA este arquivo após o deploy!")
