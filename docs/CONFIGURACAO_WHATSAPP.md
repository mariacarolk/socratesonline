# 📱 Configuração do WhatsApp Business API - Sócrates Online

Este guia completo mostra como configurar o envio automático de WhatsApp para escolas no sistema Sócrates Online.

## 🎯 Funcionalidades Implementadas

- ✅ Envio automático de mensagens para escolas quando visitas são agendadas
- ✅ Mensagens personalizadas com dados da empresa
- ✅ Logs de envio no sistema
- ✅ Formatação automática de números brasileiros
- ✅ Tratamento de erros e timeouts
- ✅ Interface para envio em lote

## 🚀 Como Configurar (Passo a Passo)

### 1. Obter Credenciais do WhatsApp Business API

#### Opção A: Meta (Facebook) - Recomendado
1. Acesse: https://developers.facebook.com/
2. Crie uma conta Business se não tiver
3. Crie um novo App do tipo "Business"
4. Adicione o produto "WhatsApp Business API"
5. Configure seu número de telefone
6. Obtenha as credenciais:
   - **Phone Number ID**: Encontrado em WhatsApp > API Setup
   - **Access Token**: Token de acesso permanente

#### Opção B: Provedores Terceirizados
- Twilio
- Chat-API
- WhatsApp Business Solution Providers

### 2. Configurar Variáveis de Ambiente

Crie/edite o arquivo `.env` na raiz do projeto:

```env
# Configurações de WhatsApp API - Meta (Facebook)
WHATSAPP_API_URL=https://graph.facebook.com/v18.0/SEU_PHONE_NUMBER_ID/messages
WHATSAPP_API_TOKEN=SEU_TOKEN_DE_ACESSO_PERMANENTE

# Dados da sua empresa
EMPRESA_WHATSAPP=5511987654321
EMPRESA_NOME=Circo Mágico
EMPRESA_CONTATO=marketing@circomagico.com
```

### 3. Exemplo com Dados Reais

```env
# EXEMPLO REAL (substitua pelos seus dados):
WHATSAPP_API_URL=https://graph.facebook.com/v18.0/123456789012345/messages
WHATSAPP_API_TOKEN=EAABsbCS1234567890abcdef...
EMPRESA_WHATSAPP=5511987654321
EMPRESA_NOME=Circo dos Sonhos
EMPRESA_CONTATO=contato@circodosSonhos.com
```

### 4. Formato das Credenciais

#### WHATSAPP_API_URL
- **Formato**: `https://graph.facebook.com/v18.0/[PHONE_NUMBER_ID]/messages`
- **Onde encontrar**: Meta Developer Console > WhatsApp > API Setup > Phone Number ID

#### WHATSAPP_API_TOKEN  
- **Formato**: Token longo (ex: `EAABsbCS1234567890abcdef...`)
- **Onde encontrar**: Meta Developer Console > WhatsApp > API Setup > Access Token
- **Importante**: Use token permanente, não temporário

#### EMPRESA_WHATSAPP
- **Formato**: Número brasileiro com código do país (ex: `5511987654321`)
- **Sem formatação**: Apenas números, sem parênteses, espaços ou traços

## 📋 Mensagem Padrão Enviada

```
🎪 *Circo dos Sonhos*

Olá, Escola Municipal João Silva!

Temos o prazer de informar que foi agendada uma visita do nosso circo em sua escola.

📅 *Data da Visita:* 15/12/2024 às 14:30
👤 *Promotor Responsável:* Maria Santos
📍 *Escola:* Escola Municipal João Silva - São Paulo/SP

Nossa equipe entrará em contato para alinhar todos os detalhes do espetáculo.

Para mais informações:
📧 contato@circodosSonhos.com
📱 (11) 98765-4321

Aguardamos vocês para um espetáculo inesquecível! 🎭✨

_Mensagem enviada automaticamente pelo sistema Circo dos Sonhos_
```

## 🔧 Como Usar no Sistema

### 1. Envio Automático
- O WhatsApp é enviado automaticamente quando uma visita é agendada
- Apenas se a escola tiver WhatsApp cadastrado
- Logs são registrados automaticamente

### 2. Envio Manual em Lote
1. Acesse: **Marketing > Dashboard Marketing**
2. Clique em **"Enviar Comunicações"**
3. Selecione **"WhatsApp"**
4. Sistema enviará para todas as escolas pendentes

### 3. Verificar Logs
1. Acesse: **Administrativo > Logs do Sistema**
2. Procure por ações do tipo **"Envio WhatsApp"**
3. Veja detalhes dos envios realizados

## 🛠️ Resolução de Problemas

### Erro: "WhatsApp API não configurada"
**Solução**: Verifique se as variáveis `WHATSAPP_API_URL` e `WHATSAPP_API_TOKEN` estão no arquivo `.env`

### Erro: "Erro da API: 401"
**Solução**: Token de acesso inválido ou expirado. Gere um novo token permanente.

### Erro: "Erro da API: 400"
**Solução**: 
- Verifique o Phone Number ID na URL
- Confirme se o número está no formato internacional
- Verifique se o número de destino é válido

### Erro: "Erro de conexão"
**Solução**: 
- Verifique sua conexão com a internet
- Confirme se a URL da API está correta
- Teste com uma ferramenta como Postman

### Números não estão sendo formatados corretamente
**Solução**: O sistema formata automaticamente números brasileiros:
- `11987654321` → `5511987654321`
- `987654321` → `5511987654321`
- Números já com 55 são mantidos

## 💰 Custos Estimados

### Meta (Facebook) WhatsApp Business API
- **Conversas iniciadas pelo business**: ~R$ 0,30 por conversa
- **Conversas iniciadas pelo usuário**: Gratuitas nas primeiras 24h
- **Template messages**: Necessárias para iniciar conversas

### Provedores Terceirizados
- **Twilio**: ~R$ 0,25-0,50 por mensagem
- **Chat-API**: ~R$ 0,15-0,30 por mensagem
- Preços variam conforme volume

## 🔒 Segurança e Boas Práticas

1. **Nunca compartilhe** seu Access Token
2. **Use HTTPS** sempre nas URLs da API
3. **Configure webhook** para receber status de entrega
4. **Respeite limites** de rate limiting da API
5. **Monitore logs** para detectar problemas

## 📞 Suporte

Se precisar de ajuda:

1. **Documentação oficial**: https://developers.facebook.com/docs/whatsapp
2. **Comunidade**: Facebook Developer Community
3. **Suporte técnico**: Através do Meta Business Help Center

## ✅ Checklist de Configuração

- [ ] Conta Meta Developer criada
- [ ] App Business criado
- [ ] WhatsApp Business API adicionado
- [ ] Número de telefone configurado
- [ ] Phone Number ID obtido
- [ ] Access Token permanente gerado
- [ ] Variáveis no `.env` configuradas
- [ ] Sistema testado com número real
- [ ] Logs verificados no sistema

---

**🎪 Sistema Sócrates Online - Gestão de Eventos Circenses**  
*Documentação atualizada em: Dezembro 2024*
