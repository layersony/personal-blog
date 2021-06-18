import os
import secrets

secret =secrets.token_urlsafe(32)

class Config:
  SECRET_KEY = secret
  MAIL_SERVER = 'smtp.googlemail.com'
  MAIL_PORT = 587
  MAIL_USE_TLS = True
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  UPLOADED_PHOTOS_DEST = 'app/static/photos'

class ProdConfig(Config):
  pass

class DevConfig(Config):
  SQLALCHEMY_DATABASE_URI = ''
  DEBUG = True

config_options = {
  'development':DevConfig,
  'production':ProdConfig
}