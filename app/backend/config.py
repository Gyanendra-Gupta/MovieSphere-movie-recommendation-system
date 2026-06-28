import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', '7d8f9e0a1b2c3d4e5f6g7h8i9j0k1l2m')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'm2l1k0j9i8h7g6f5e4d3c2b1a0e9f8d7')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    
    # Database selection logic
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///moviesphere.db'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False