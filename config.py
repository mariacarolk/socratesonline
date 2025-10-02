import os
import locale

# Set locale to UTF-8 to handle encoding issues
try:
    locale.setlocale(locale.LC_ALL, 'C.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except locale.Error:
        pass  # Use system default if UTF-8 locales are not available

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'sua-chave-secreta-aqui-mude-em-producao')
    
    # Uploads
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads/comprovantes')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Banco de dados
    database_url = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@localhost:5432/socrates_online_dev?client_encoding=utf8'
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    # Adicionar client_encoding=utf8 se não estiver presente
    if 'client_encoding' not in database_url:
        separator = '&' if '?' in database_url else '?'
        database_url += f'{separator}client_encoding=utf8'
    
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'client_encoding': 'utf8',
            'options': '-c client_encoding=utf8'
        }
    }
    
    # Configurações de E-mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@socratesonline.com')
    
    # Configurações de WhatsApp (API)
    WHATSAPP_API_URL = os.environ.get('WHATSAPP_API_URL')
    WHATSAPP_API_TOKEN = os.environ.get('WHATSAPP_API_TOKEN')
    
    # Configurações AWS
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
    MAIL_SERVICE = os.environ.get('MAIL_SERVICE', 'smtp')  # 'smtp' ou 'aws_ses'
    
    # SNS Topics (opcional)
    AWS_SNS_EMAIL_TOPIC_ARN = os.environ.get('AWS_SNS_EMAIL_TOPIC_ARN')