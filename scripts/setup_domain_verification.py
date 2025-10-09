#!/usr/bin/env python3
"""
Script para auxiliar na configuração de verificação de domínio no AWS SES
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from services.aws_email_service import aws_email_service

def setup_domain_verification():
    """Guia para configurar verificação de domínio"""
    print("🌐 CONFIGURAÇÃO DE VERIFICAÇÃO DE DOMÍNIO")
    print("=" * 60)
    
    domain = input("Digite seu domínio (ex: socratesonline.com): ").strip()
    
    if not domain:
        print("❌ Domínio obrigatório!")
        return
    
    print(f"\n🔍 Iniciando verificação para: {domain}")
    
    # Verificar domínio no AWS SES
    result = aws_email_service.verify_domain_identity(domain)
    
    if not result['success']:
        print(f"❌ Erro ao iniciar verificação: {result['error']}")
        return
    
    token = result['verification_token']
    
    print(f"\n✅ Verificação iniciada!")
    print(f"🔑 Token de verificação: {token}")
    
    print(f"\n📋 CONFIGURAÇÕES DNS NECESSÁRIAS:")
    print("=" * 40)
    
    # 1. Verificação SES
    print("1️⃣ VERIFICAÇÃO AWS SES:")
    print(f"   Tipo: TXT")
    print(f"   Nome: _amazonses.{domain}")
    print(f"   Valor: {token}")
    print(f"   TTL: 300")
    
    # 2. SPF
    print(f"\n2️⃣ REGISTRO SPF:")
    print(f"   Tipo: TXT")
    print(f"   Nome: {domain}")
    print(f"   Valor: \"v=spf1 include:amazonses.com ~all\"")
    print(f"   TTL: 300")
    
    # 3. DMARC
    print(f"\n3️⃣ REGISTRO DMARC:")
    print(f"   Tipo: TXT")
    print(f"   Nome: _dmarc.{domain}")
    print(f"   Valor: \"v=DMARC1; p=quarantine; rua=mailto:dmarc@{domain}\"")
    print(f"   TTL: 300")
    
    print(f"\n4️⃣ REGISTROS DKIM:")
    print("   ⚠️ Após a verificação do domínio ser aprovada:")
    print("   1. Acesse AWS SES Console")
    print(f"   2. Clique no domínio {domain}")
    print("   3. DKIM → Edit → Enable DKIM signing")
    print("   4. Copie os 3 registros CNAME gerados")
    print("   5. Adicione-os ao seu DNS")
    
    print(f"\n🔧 INSTRUÇÕES REGISTRO.BR:")
    print("=" * 35)
    print("1. Acesse: https://registro.br/")
    print("2. Login → Meus domínios")
    print(f"3. Clique em '{domain}'")
    print("4. DNS → Editar zona DNS")
    print("5. Adicione os registros acima")
    print("6. Salve as alterações")
    
    print(f"\n⏱️ TEMPO DE PROPAGAÇÃO:")
    print("• DNS: 5 minutos a 24 horas")
    print("• Verificação AWS: até 72 horas")
    
    print(f"\n🧪 VERIFICAR PROPAGAÇÃO:")
    print(f"nslookup -type=TXT _amazonses.{domain}")
    print(f"nslookup -type=TXT {domain}")
    
    print(f"\n📞 PRÓXIMOS PASSOS:")
    print("1. Configure os registros DNS")
    print("2. Aguarde a propagação")
    print("3. Execute: python scripts/test_aws_email.py")
    print("4. Configure DKIM após verificação aprovada")

def check_dns_propagation():
    """Verifica se os registros DNS propagaram"""
    domain = input("\nDigite o domínio para verificar: ").strip()
    
    if not domain:
        return
        
    print(f"\n🔍 Verificando propagação DNS para: {domain}")
    
    try:
        import subprocess
        
        # Verificar registro SES
        print("\n1️⃣ Verificando registro _amazonses...")
        try:
            result = subprocess.run(['nslookup', '-type=TXT', f'_amazonses.{domain}'], 
                                 capture_output=True, text=True, timeout=10)
            if 'text =' in result.stdout.lower():
                print("   ✅ Registro _amazonses encontrado")
            else:
                print("   ❌ Registro _amazonses não encontrado ainda")
        except Exception as e:
            print(f"   ⚠️ Erro ao verificar: {str(e)}")
        
        # Verificar SPF
        print("\n2️⃣ Verificando registro SPF...")
        try:
            result = subprocess.run(['nslookup', '-type=TXT', domain], 
                                 capture_output=True, text=True, timeout=10)
            if 'v=spf1' in result.stdout.lower():
                print("   ✅ Registro SPF encontrado")
            else:
                print("   ❌ Registro SPF não encontrado ainda")
        except Exception as e:
            print(f"   ⚠️ Erro ao verificar: {str(e)}")
            
        # Verificar DMARC
        print("\n3️⃣ Verificando registro DMARC...")
        try:
            result = subprocess.run(['nslookup', '-type=TXT', f'_dmarc.{domain}'], 
                                 capture_output=True, text=True, timeout=10)
            if 'v=dmarc1' in result.stdout.lower():
                print("   ✅ Registro DMARC encontrado")
            else:
                print("   ❌ Registro DMARC não encontrado ainda")
        except Exception as e:
            print(f"   ⚠️ Erro ao verificar: {str(e)}")
            
    except ImportError:
        print("⚠️ nslookup não disponível. Verifique manualmente:")
        print(f"nslookup -type=TXT _amazonses.{domain}")
        print(f"nslookup -type=TXT {domain}")
        print(f"nslookup -type=TXT _dmarc.{domain}")

def main():
    """Menu principal"""
    print("🛠️ ASSISTENTE DE CONFIGURAÇÃO DNS")
    print("=" * 50)
    
    while True:
        print("\nEscolha uma opção:")
        print("1. Configurar verificação de domínio")
        print("2. Verificar propagação DNS")
        print("3. Sair")
        
        choice = input("\nOpção (1-3): ").strip()
        
        if choice == '1':
            setup_domain_verification()
        elif choice == '2':
            check_dns_propagation()
        elif choice == '3':
            print("\n👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main()














