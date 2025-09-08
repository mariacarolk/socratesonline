# CONFIGURAÇÃO DE WHATSAPP - EXEMPLO PARA SUA EMPRESA
# 
# Este arquivo mostra como configurar o WhatsApp Business API
# para enviar mensagens automáticas para as escolas

import os
import requests
from datetime import datetime
from flask import current_app

class WhatsAppService:
    """Serviço para envio de mensagens via WhatsApp Business API"""
    
    def __init__(self):
        # Configurações da API do WhatsApp Business (Meta)
        self.api_url = os.environ.get('WHATSAPP_API_URL')
        self.access_token = os.environ.get('WHATSAPP_API_TOKEN')
        self.empresa_numero = os.environ.get('EMPRESA_WHATSAPP', '5511999887766')
        self.empresa_nome = os.environ.get('EMPRESA_NOME', 'Sócrates Online')
        
    def enviar_mensagem(self, numero_destino, mensagem):
        """
        Envia mensagem via WhatsApp Business API
        
        Args:
            numero_destino (str): Número do WhatsApp no formato internacional (5511999887766)
            mensagem (str): Texto da mensagem
            
        Returns:
            dict: Resultado do envio
        """
        if not self.api_url or not self.access_token:
            return {
                'success': False,
                'error': 'WhatsApp API não configurada. Configure WHATSAPP_API_URL e WHATSAPP_API_TOKEN'
            }
        
        # Limpar o número (remover caracteres especiais)
        numero_limpo = ''.join(filter(str.isdigit, numero_destino))
        
        # Garantir formato internacional
        if not numero_limpo.startswith('55'):
            numero_limpo = '55' + numero_limpo
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'messaging_product': 'whatsapp',
            'to': numero_limpo,
            'type': 'text',
            'text': {
                'body': mensagem
            }
        }
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message_id': response.json().get('messages', [{}])[0].get('id'),
                    'numero_enviado': numero_limpo
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro da API: {response.status_code} - {response.text}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Erro ao enviar mensagem: {str(e)}'
            }
    
    def criar_mensagem_visita_escola(self, escola_nome, data_visita, promotor_nome, contato_empresa=None):
        """
        Cria mensagem padrão para visita à escola
        
        Args:
            escola_nome (str): Nome da escola
            data_visita (datetime): Data e hora da visita
            promotor_nome (str): Nome do promotor responsável
            contato_empresa (str): Contato da empresa (opcional)
            
        Returns:
            str: Mensagem formatada
        """
        contato = contato_empresa or os.environ.get('EMPRESA_CONTATO', 'contato@socratesonline.com')
        
        mensagem = f"""🎪 *{self.empresa_nome}*

Olá, {escola_nome}!

Temos o prazer de informar que foi agendada uma visita do nosso circo em sua escola.

📅 *Data da Visita:* {data_visita.strftime('%d/%m/%Y às %H:%M')}
👤 *Promotor Responsável:* {promotor_nome}

Nossa equipe entrará em contato para alinhar todos os detalhes do espetáculo.

Para mais informações:
📧 {contato}
📱 {self.empresa_numero}

Aguardamos vocês para um espetáculo inesquecível! 🎭✨"""
        
        return mensagem
    
    def criar_mensagem_lembrete(self, escola_nome, data_visita, promotor_nome):
        """
        Cria mensagem de lembrete da visita
        """
        mensagem = f"""🔔 *Lembrete - {self.empresa_nome}*

Olá, {escola_nome}!

Este é um lembrete de que nossa visita está agendada para:

📅 *{data_visita.strftime('%d/%m/%Y às %H:%M')}*
👤 *Promotor:* {promotor_nome}

Estamos ansiosos para apresentar nosso espetáculo! 🎪

Qualquer dúvida, entre em contato conosco.

Até breve! 🎭"""
        
        return mensagem

# EXEMPLO DE USO:
# 
# # 1. Configure as variáveis de ambiente no seu .env:
# WHATSAPP_API_URL=https://graph.facebook.com/v18.0/123456789012345/messages
# WHATSAPP_API_TOKEN=EAABsbCS1234567890abcdef...
# EMPRESA_WHATSAPP=5511987654321
# EMPRESA_NOME=Circo Mágico
# EMPRESA_CONTATO=marketing@circomagico.com
#
# # 2. No seu código:
# whatsapp = WhatsAppService()
# resultado = whatsapp.enviar_mensagem('11987654321', 'Olá! Teste do WhatsApp')
#
# if resultado['success']:
#     print(f"Mensagem enviada! ID: {resultado['message_id']}")
# else:
#     print(f"Erro: {resultado['error']}")

# COMO OBTER AS CREDENCIAIS:
#
# 1. Acesse: https://developers.facebook.com/
# 2. Crie um App do tipo "Business"
# 3. Adicione o produto "WhatsApp Business API"
# 4. Configure o número de telefone
# 5. Obtenha o Phone Number ID e o Access Token
# 6. Configure o webhook (opcional para receber mensagens)
#
# FORMATO DAS VARIÁVEIS:
# WHATSAPP_API_URL: https://graph.facebook.com/v18.0/[PHONE_NUMBER_ID]/messages
# WHATSAPP_API_TOKEN: Token de acesso permanente do Facebook
# EMPRESA_WHATSAPP: Número da empresa no formato internacional (5511987654321)
