#!/usr/bin/env python3
'''
Script pré-deploy: Verificações antes do deploy
'''

import os
import sys
import subprocess

def verificar_mapeamento_atualizado():
    '''Verifica se o mapeamento está atualizado'''
    print("📋 Verificando atualização do mapeamento...")
    
    try:
        result = subprocess.run([sys.executable, 'scripts/atualizar_mapeamento.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Mapeamento verificado e atualizado!")
            return True
        else:
            print("❌ Erro na verificação do mapeamento:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("🚀 VERIFICAÇÕES PRÉ-DEPLOY - SÓCRATES ONLINE")
    print("=" * 50)
    
    checks = [
        ("Mapeamento do sistema", verificar_mapeamento_atualizado),
    ]
    
    sucesso = True
    
    for nome, funcao in checks:
        print(f"\n🔍 {nome}...")
        if not funcao():
            sucesso = False
    
    print("\n" + "=" * 50)
    if sucesso:
        print("✅ TODAS AS VERIFICAÇÕES PASSARAM!")
        print("🚀 Sistema pronto para deploy!")
    else:
        print("❌ ALGUMAS VERIFICAÇÕES FALHARAM!")
        print("🛑 Corrija os problemas antes do deploy!")
    
    return 0 if sucesso else 1

if __name__ == "__main__":
    exit(main())
