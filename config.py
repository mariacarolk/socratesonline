import os

def get_database_config():
    """
    Retorna configuração do banco PostgreSQL:
    1. Railway PostgreSQL (produção) - via DATABASE_URL automática
    2. PostgreSQL local (desenvolvimento) - via DATABASE_URL no .env
    """
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        # Configuração padrão para desenvolvimento local
        database_url = 'postgresql://postgres:postgres@localhost:5432/socrates_online'
    
    # Fix para Railway - substitui postgres:// por postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    # Configuração para PostgreSQL
    return {
        'SQLALCHEMY_DATABASE_URI': database_url,
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'pool_pre_ping': True,
            'pool_recycle': 300,
            'pool_size': 10,
            'max_overflow': 20,
            'echo': False
        }
    }

class Config:
    # Chave secreta para sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-aqui-mude-em-producao'
    
    # Configurações de upload
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads/comprovantes')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB máximo por arquivo
    
    # Configurações gerais do SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de banco dinâmicas
    db_config = get_database_config()
    SQLALCHEMY_DATABASE_URI = db_config['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_ENGINE_OPTIONS = db_config['SQLALCHEMY_ENGINE_OPTIONS']

class DevelopmentConfig(Config):
    DEBUG = True
    
    # Reconfigurar banco para desenvolvimento
    db_config = get_database_config()
    SQLALCHEMY_DATABASE_URI = db_config['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_ENGINE_OPTIONS = db_config['SQLALCHEMY_ENGINE_OPTIONS'].copy()
    
    # Configurações para desenvolvimento
    SQLALCHEMY_ENGINE_OPTIONS.update({
        'pool_size': 5,
        'max_overflow': 10,
        'echo': True  # Log SQL em desenvolvimento
    })

class ProductionConfig(Config):
    DEBUG = False
    
    # Reconfigurar banco para produção
    db_config = get_database_config()
    SQLALCHEMY_DATABASE_URI = db_config['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_ENGINE_OPTIONS = db_config['SQLALCHEMY_ENGINE_OPTIONS'].copy()
    
    # Configurações otimizadas para produção
    if 'postgresql' in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_ENGINE_OPTIONS.update({
            'pool_size': 20,
            'max_overflow': 40
        })

class RailwayConfig(ProductionConfig):
    """Configuração específica para Railway"""
    
    # Railway fornece PORT via variável de ambiente
    PORT = int(os.environ.get('PORT', 5000))
    
    # Reconfigurar banco para Railway
    db_config = get_database_config()
    SQLALCHEMY_DATABASE_URI = db_config['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_ENGINE_OPTIONS = db_config['SQLALCHEMY_ENGINE_OPTIONS'].copy()
    
    # Configurações específicas para Railway
    if 'postgresql' in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_ENGINE_OPTIONS.update({
            'pool_size': 15,
            'max_overflow': 30,
            'pool_timeout': 20,
            'pool_recycle': 1800  # 30 minutos
        })
