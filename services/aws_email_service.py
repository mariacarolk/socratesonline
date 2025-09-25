"""
Serviço de envio de emails usando AWS SES
"""
import boto3
import os
from botocore.exceptions import ClientError
from typing import Dict, List, Optional

class AWSEmailService:
    def __init__(self):
        """Inicializa o cliente AWS SES"""
        self.ses_client = boto3.client(
            'ses',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )
        
        # SNS para tópicos (opcional, para notificações)
        self.sns_client = boto3.client(
            'sns',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )
    
    def send_email(
        self, 
        recipient: str, 
        subject: str, 
        html_body: str, 
        text_body: str,
        sender: Optional[str] = None,
        bcc: Optional[List[str]] = None
    ) -> Dict:
        """
        Envia um email usando AWS SES
        
        Args:
            recipient: Email do destinatário
            subject: Assunto do email
            html_body: Corpo do email em HTML
            text_body: Corpo do email em texto simples
            sender: Email do remetente (opcional, usa o padrão se não informado)
            bcc: Lista de emails para cópia oculta (opcional)
            
        Returns:
            Dict com resultado do envio
        """
        if not sender:
            sender = os.environ.get('MAIL_DEFAULT_SENDER', 'contato@socratesonline.com')
        
        try:
            # Configurar destinatários
            destination = {'ToAddresses': [recipient]}
            if bcc:
                destination['BccAddresses'] = bcc
            
            response = self.ses_client.send_email(
                Source=sender,
                Destination=destination,
                Message={
                    'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                    'Body': {
                        'Html': {'Data': html_body, 'Charset': 'UTF-8'},
                        'Text': {'Data': text_body, 'Charset': 'UTF-8'}
                    }
                }
            )
            
            return {
                'success': True,
                'message_id': response['MessageId'],
                'recipient': recipient
            }
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            
            return {
                'success': False,
                'error_code': error_code,
                'error_message': error_message,
                'recipient': recipient
            }
        except Exception as e:
            return {
                'success': False,
                'error_code': 'UNKNOWN_ERROR',
                'error_message': str(e),
                'recipient': recipient
            }
    
    def send_bulk_email(
        self,
        recipients: List[str],
        subject: str,
        html_body: str,
        text_body: str,
        sender: Optional[str] = None,
        bcc: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Envia emails em lote usando AWS SES
        
        Args:
            recipients: Lista de emails dos destinatários
            subject: Assunto do email
            html_body: Corpo do email em HTML
            text_body: Corpo do email em texto simples
            sender: Email do remetente (opcional)
            bcc: Lista de emails para cópia oculta (opcional)
            
        Returns:
            Lista com resultados de cada envio
        """
        results = []
        
        for recipient in recipients:
            result = self.send_email(recipient, subject, html_body, text_body, sender, bcc)
            results.append(result)
        
        return results
    
    def verify_email_identity(self, email: str) -> Dict:
        """
        Verifica uma identidade de email no AWS SES
        
        Args:
            email: Email para verificar
            
        Returns:
            Dict com resultado da verificação
        """
        try:
            response = self.ses_client.verify_email_identity(EmailAddress=email)
            return {
                'success': True,
                'message': f'Verificação enviada para {email}'
            }
        except ClientError as e:
            return {
                'success': False,
                'error': e.response['Error']['Message']
            }
    
    def verify_domain_identity(self, domain: str) -> Dict:
        """
        Verifica uma identidade de domínio no AWS SES
        
        Args:
            domain: Domínio para verificar
            
        Returns:
            Dict com resultado da verificação e token TXT
        """
        try:
            response = self.ses_client.verify_domain_identity(Domain=domain)
            return {
                'success': True,
                'verification_token': response['VerificationToken'],
                'message': f'Adicione este TXT record ao seu DNS: _amazonses.{domain} = {response["VerificationToken"]}'
            }
        except ClientError as e:
            return {
                'success': False,
                'error': e.response['Error']['Message']
            }
    
    def get_send_quota(self) -> Dict:
        """
        Obtém a cota de envio atual
        
        Returns:
            Dict com informações da cota
        """
        try:
            response = self.ses_client.get_send_quota()
            return {
                'success': True,
                'max_24_hour': response['Max24HourSend'],
                'max_send_rate': response['MaxSendRate'],
                'sent_last_24_hours': response['SentLast24Hours']
            }
        except ClientError as e:
            return {
                'success': False,
                'error': e.response['Error']['Message']
            }
    
    def list_verified_identities(self) -> Dict:
        """
        Lista todas as identidades verificadas
        
        Returns:
            Dict com lista de identidades
        """
        try:
            response = self.ses_client.list_verified_email_addresses()
            return {
                'success': True,
                'verified_emails': response['VerifiedEmailAddresses']
            }
        except ClientError as e:
            return {
                'success': False,
                'error': e.response['Error']['Message']
            }

# Instância global do serviço
aws_email_service = AWSEmailService()

