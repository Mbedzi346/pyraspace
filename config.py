import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'abcde'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:speedbird@localhost/marketline'
    SQLALCHEMY_TRACK_MODIFICATIONS = False