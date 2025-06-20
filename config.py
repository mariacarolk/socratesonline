import os

class Config:
    # Configurações do banco de dados
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações específicas para SQLite
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'connect_args': {
            'check_same_thread': False,
            'timeout': 30
        }
    }
    
    # Chave secreta para sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-aqui'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
