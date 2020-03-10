import os
import pytz

from app import app

timezone = pytz.timezone('Asia/Shanghai')

def get_prefix():
    import sys

    prefix = r'sqlite:///'

    if not sys.platform.startswith('win'):
        prefix += r'/'

    return prefix

class Config():
    app_path = os.path.join(app.root_path, 'comment.db')

    app.config['SQLALCHEMY_DATABASE_URI'] = get_prefix() + app_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
