# 🚀 Guia Rápido: Configurar Emails AWS SES

## ⚡ Configuração em 5 Passos

### 1. **Credenciais AWS**
```bash
# Crie usuário IAM com política AmazonSESFullAccess
# Copie Access Key ID e Secret Access Key
```

### 2. **Configurar .env**
```env
MAIL_SERVICE=aws_ses
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/xxxxx
AWS_REGION=us-east-1
MAIL_DEFAULT_SENDER=contato@socratesonline.com
```

### 3. **Verificar Domínio**
```bash
# Execute o script auxiliar:
python scripts/setup_domain_verification.py

# Ou manualmente no AWS Console:
# SES → Verified identities → Create identity → Domain
```

### 4. **Configurar DNS**
```dns
# Registro.br → Seus domínios → DNS
# Adicione os registros TXT fornecidos pelo AWS
```

### 5. **Testar**
```bash
python scripts/test_aws_email.py
```

## 🎛️ Como Usar no Dashboard

1. **Acesse:** `http://127.0.0.1:5000/marketing/dashboard_escolas`
2. **Clique:** "Enviar E-mails Pendentes"
3. **Sistema detecta automaticamente:** AWS SES ou SMTP

## 🔧 Troubleshooting Rápido

### ❌ "Credentials not configured"
```bash
# Verifique .env
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY
```

### ❌ "Email address not verified" 
```bash
# Conta em sandbox mode
# Adicione emails de teste no SES Console
# OU solicite production access
```

### ❌ DNS não propaga
```bash
# Aguarde até 24h
nslookup -type=TXT _amazonses.socratesonline.com
```

## 📊 Custos
- **62.000 emails/mês:** GRÁTIS (via EC2)
- **Após:** $0.10/1.000 emails
- **Estimativa:** ~$1-2/mês para uso típico

## 🎯 Status do Sistema
- ✅ **Serviço AWS criado:** `services/aws_email_service.py`
- ✅ **Função atualizada:** `enviar_email_marketing()`
- ✅ **Config automático:** Detecta `MAIL_SERVICE=aws_ses`
- ✅ **Scripts de teste:** Disponíveis em `scripts/`
- ✅ **Compatibilidade:** Funciona com SMTP existente

**🔗 Links Úteis:**
- [AWS SES Console](https://console.aws.amazon.com/ses/)
- [Registro.br DNS](https://registro.br/)
- [Documentação Completa](./AWS_EMAIL_CONFIGURATION.md)


