# 🎪 Exemplo Prático - Configuração WhatsApp para sua Empresa

## 📝 Dados de Exemplo (Substitua pelos seus)

Vamos supor que sua empresa de circo tenha os seguintes dados:

- **Nome**: Circo Estrela Mágica
- **WhatsApp**: (11) 98765-4321
- **E-mail**: contato@circoestrelamagica.com.br
- **Phone Number ID**: 123456789012345 (obtido no Meta Developer)
- **Access Token**: EAABsbCS1234567890abcdefghijklmnopqrstuvwxyz...

## ⚙️ Configuração no arquivo `.env`

```env
# Configurações básicas do sistema
DATABASE_URL=sqlite:///socrates_online.db
SECRET_KEY=sua-chave-secreta-super-segura-mude-em-producao-123456789

# Configurações de WhatsApp - SEUS DADOS REAIS
WHATSAPP_API_URL=https://graph.facebook.com/v18.0/123456789012345/messages
WHATSAPP_API_TOKEN=EAABsbCS1234567890abcdefghijklmnopqrstuvwxyz...

# Dados da sua empresa
EMPRESA_WHATSAPP=5511987654321
EMPRESA_NOME=Circo Estrela Mágica
EMPRESA_CONTATO=contato@circoestrelamagica.com.br

# Configurações de E-mail (opcional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=contato@circoestrelamagica.com.br
MAIL_PASSWORD=sua-senha-do-app-gmail
MAIL_DEFAULT_SENDER=contato@circoestrelamagica.com.br
```

## 📱 Como Obter as Credenciais do WhatsApp

### 1. Acesse o Meta Developer Console
```
https://developers.facebook.com/
```

### 2. Crie um App Business
- Clique em "Criar App"
- Escolha "Business" como tipo
- Nome: "Circo Estrela Mágica - WhatsApp"

### 3. Adicione WhatsApp Business API
- No painel do app, clique em "Adicionar produto"
- Selecione "WhatsApp Business API"

### 4. Configure o Número
- Vá em WhatsApp > Primeiros passos
- Adicione seu número: +55 11 98765-4321
- Verifique o número via SMS/chamada

### 5. Obtenha as Credenciais
- **Phone Number ID**: Copie em WhatsApp > API Setup
  ```
  Exemplo: 123456789012345
  ```
- **Access Token**: Gere um token permanente
  ```
  Exemplo: EAABsbCS1234567890abcdefghijklmnopqrstuvwxyz...
  ```

## 🧪 Teste a Configuração

### 1. Teste Manual via Postman/cURL

```bash
curl -X POST \
  https://graph.facebook.com/v18.0/123456789012345/messages \
  -H 'Authorization: Bearer EAABsbCS1234567890abcdefghijklmnopqrstuvwxyz...' \
  -H 'Content-Type: application/json' \
  -d '{
    "messaging_product": "whatsapp",
    "to": "5511987654321",
    "type": "text",
    "text": {
      "body": "Teste do WhatsApp - Circo Estrela Mágica! 🎪"
    }
  }'
```

### 2. Teste no Sistema
1. Cadastre uma escola com WhatsApp
2. Agende uma visita
3. Verifique se a mensagem foi enviada
4. Confira os logs em "Administrativo > Logs"

## 📋 Mensagem que será Enviada

Com a configuração acima, a mensagem será:

```
🎪 *Circo Estrela Mágica*

Olá, Escola Municipal São João!

Temos o prazer de informar que foi agendada uma visita do nosso circo em sua escola.

📅 *Data da Visita:* 15/12/2024 às 14:30
👤 *Promotor Responsável:* João Silva
📍 *Escola:* Escola Municipal São João - São Paulo/SP

Nossa equipe entrará em contato para alinhar todos os detalhes do espetáculo.

Para mais informações:
📧 contato@circoestrelamagica.com.br
📱 (11) 98765-4321

Aguardamos vocês para um espetáculo inesquecível! 🎭✨

_Mensagem enviada automaticamente pelo sistema Circo Estrela Mágica_
```

## ⚠️ Pontos Importantes

### Formato do Número
- **Seu número da empresa**: `5511987654321` (sem formatação)
- **Números das escolas**: Sistema formata automaticamente
- **Sempre usar código do país**: 55 para Brasil

### Token de Acesso
- **Use token PERMANENTE**, não temporário
- **Nunca compartilhe** o token
- **Renove periodicamente** por segurança

### Custos
- **Meta WhatsApp Business API**: ~R$ 0,30 por conversa iniciada
- **Primeiro mês**: Geralmente gratuito para testes
- **Monitore uso**: Para controlar custos

## 🚀 Próximos Passos

1. **Configure webhook** (opcional) para receber status de entrega
2. **Crie templates** personalizados no Meta Business Manager
3. **Configure alertas** para monitorar falhas de envio
4. **Treine equipe** para usar o sistema

## 🆘 Problemas Comuns

### "Invalid access token"
- Verifique se o token não expirou
- Gere um novo token permanente

### "Phone number not registered"
- Confirme se seu número foi verificado no Meta
- Aguarde até 24h após verificação

### "Rate limit exceeded"
- Meta limita mensagens por minuto
- Aguarde alguns minutos e tente novamente

---

**💡 Dica**: Comece com um número de teste e poucos contatos antes de usar em produção!

**🎪 Sistema Sócrates Online**  
*Configuração personalizada para sua empresa*
