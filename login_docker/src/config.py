"""Flask app configuration."""
from os import environ, path
from dotenv import load_dotenv

from authomatic.providers import oauth2

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    '''Set Flask configuration.'''

    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get('SECRET_KEY')

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Assets
    LESS_BIN = environ.get('LESS_BIN')
    ASSETS_DEBUG = environ.get('ASSETS_DEBUG')
    LESS_RUN_IN_DEBUG = environ.get('LESS_RUN_IN_DEBUG')

    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    COMPRESSOR_DEBUG = environ.get('COMPRESSOR_DEBUG')


class MailerConfig:
    ''' Set mailer config.'''

    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USE_SSL = environ.get('MAIL_USE_SSL')
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    SENDER = environ.get('SENDER')


class SocialConfig:
    ''' Set social media config.'''

    SECRET_KEY = environ.get('SECRET_KEY')
    CONFIG = {
        'fb': {
            'class_': oauth2.Facebook,
            'consumer_key': environ.get('FB_CONSUMER_KEY'),
            'consumer_secret': environ.get('FB_CONSUMER_SECRET'),
            'scope': ['email']
        },
        'google' : {
            'class_': 'authomatic.providers.oauth2.Google',
            'consumer_key': environ.get('G_CONSUMER_KEY'),
            'consumer_secret': environ.get('G_CONSUMER_SECRET'),
            'scope': [
                'https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email'
            ]
        }
    }
