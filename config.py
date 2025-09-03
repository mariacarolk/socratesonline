import os

class Config:
    # Configurações do banco de dados PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@localhost:5432/socrates_online'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações otimizadas para PostgreSQL
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20,
        'echo': False
    }
    
    # Chave secreta para sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-aqui'
    
    # Configurações de upload
    UPLOAD_FOLDER = 'uploads/comprovantes'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo por arquivo

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@localhost:5432/socrates_online_dev'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 5,
        'max_overflow': 10,
        'echo': True  # Log SQL em desenvolvimento
    }

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 20,
        'max_overflow': 40,
        'echo': False
    }
