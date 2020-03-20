import os
from datetime import datetime

import pytz

basedir = os.path.abspath(os.path.dirname(__file__))

def get_prefix():
    import sys

    prefix = 'sqlite:///'
    if not sys.platform.startswith('win'):
        prefix += '/'

    return prefix

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
    'You will never guess this.'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        get_prefix() + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TIMEZONE = pytz.timezone('Asia/Shanghai')
