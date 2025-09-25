#!/usr/bin/env python3
"""
Script para testar configuração de email AWS SES
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from services.aws_email_service import aws_email_service

def test_aws_credentials():
    """Testa se as credenciais AWS estão configuradas"""
    print("🔐 Testando credenciais AWS...")
    
    required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION']
    missing = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Variáveis de ambiente faltando: {', '.join(missing)}")
        return False
    
    print("✅ Credenciais AWS configuradas")
    return True

def test_send_quota():
    """Testa se consegue acessar informações da cota SES"""
    print("\n📊 Verificando cota de envio...")
    
    try:
        quota = aws_email_service.get_send_quota()
        
        if quota['success']:
            print(f"✅ Cota atual:")
            print(f"   • Máximo 24h: {quota['max_24_hour']} emails")
            print(f"   • Taxa máxima: {quota['max_send_rate']} emails/segundo")
            print(f"   • Enviados hoje: {quota['sent_last_24_hours']}")
            print(f"   • Restam hoje: {quota['max_24_hour'] - quota['sent_last_24_hours']}")
            return True
        else:
            print(f"❌ Erro ao acessar cota: {quota['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Exceção ao verificar cota: {str(e)}")
        return False

def test_verified_identities():
    """Lista identidades verificadas"""
    print("\n📧 Verificando identidades...")
    
    try:
        identities = aws_email_service.list_verified_identities()
        
        if identities['success']:
            verified = identities['verified_emails']
            if verified:
                print(f"✅ Identidades verificadas ({len(verified)}):")
                for email in verified:
                    print(f"   • {email}")
            else:
                print("⚠️  Nenhuma identidade verificada ainda")
                print("   Configure pelo menos um email no AWS SES Console")
            return True
        else:
            print(f"❌ Erro ao listar identidades: {identities['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Exceção ao listar identidades: {str(e)}")
        return False

def test_send_email(recipient=None):
    """Testa envio de email"""
    if not recipient:
        recipient = input("\n📮 Digite um email para teste (ou Enter para pular): ").strip()
        
    if not recipient:
        print("⏭️ Pulando teste de envio")
        return True
        
    print(f"\n📤 Testando envio para: {recipient}")
    
    try:
        resultado = aws_email_service.send_email(
            recipient=recipient,
            subject="🧪 Teste AWS SES - Sócrates Online",
            html_body="""
            <h1>Teste de Configuração AWS SES</h1>
            <p>Se você está lendo este email, a configuração do AWS SES está funcionando corretamente!</p>
            <p><strong>Sistema:</strong> Sócrates Online</p>
            <p><strong>Serviço:</strong> Amazon SES</p>
            <hr>
            <small>Este é um email de teste automático.</small>
            """,
            text_body="""
Teste de Configuração AWS SES

Se você está lendo este email, a configuração do AWS SES está funcionando corretamente!

Sistema: Sócrates Online
Serviço: Amazon SES

---
Este é um email de teste automático.
            """
        )
        
        if resultado['success']:
            print(f"✅ Email enviado com sucesso!")
            print(f"   • Message ID: {resultado['message_id']}")
            print(f"   • Destinatário: {resultado['recipient']}")
            return True
        else:
            print(f"❌ Falha no envio:")
            print(f"   • Código: {resultado['error_code']}")
            print(f"   • Mensagem: {resultado['error_message']}")
            
            # Dicas baseadas no erro
            if 'not verified' in resultado['error_message'].lower():
                print("\n💡 Dica: Email não verificado.")
                print("   1. Acesse AWS SES Console")
                print("   2. Verified identities → Create identity")
                print("   3. Adicione o email ou domínio")
                
            elif 'sandbox' in resultado['error_message'].lower():
                print("\n💡 Dica: Conta em modo Sandbox.")
                print("   1. Só pode enviar para emails verificados")
                print("   2. Request production access no SES Console")
                
            return False
            
    except Exception as e:
        print(f"❌ Exceção no envio: {str(e)}")
        return False

def main():
    """Função principal de teste"""
    print("🧪 TESTE DE CONFIGURAÇÃO AWS SES")
    print("=" * 50)
    
    success_count = 0
    total_tests = 4
    
    # Teste 1: Credenciais
    if test_aws_credentials():
        success_count += 1
    
    # Teste 2: Cota
    if test_send_quota():
        success_count += 1
    
    # Teste 3: Identidades
    if test_verified_identities():
        success_count += 1
    
    # Teste 4: Envio (opcional)
    if test_send_email():
        success_count += 1
    
    # Resultado final
    print("\n" + "=" * 50)
    print(f"📊 RESULTADO: {success_count}/{total_tests} testes passaram")
    
    if success_count == total_tests:
        print("🎉 Configuração AWS SES está funcionando perfeitamente!")
        print("\n🚀 Próximos passos:")
        print("   1. Configure DNS (SPF, DKIM, DMARC)")
        print("   2. Solicite acesso de produção (se em sandbox)")
        print("   3. Configure MAIL_SERVICE=aws_ses no .env")
    elif success_count >= 2:
        print("⚠️  Configuração parcial. Verifique os erros acima.")
    else:
        print("❌ Configuração com problemas. Verifique:")
        print("   1. Credenciais AWS corretas")
        print("   2. Permissões SES no IAM")
        print("   3. Região AWS correta")

if __name__ == "__main__":
    main()


