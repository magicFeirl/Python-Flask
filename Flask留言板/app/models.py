from datetime import datetime


from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    time = db.Column(db.DATETIME, default=datetime.utcnow)
    title = db.Column(db.String(12), index=True, default='无标题')
    message = db.Column(db.String(255))
    is_topic = db.Column(db.Boolean, default=False) # 是否为置顶评论

    def __repr__(self):
        return f'<Comment {self.title}>'

    def topic_this(self):
        self.is_topic = True


# 日志表
# 这里不能使用继承
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    time = db.Column(db.DATETIME, default=datetime.utcnow)
    title = db.Column(db.String(12), index=True, default='无标题')
    message = db.Column(db.String(255))

    def __repr__(self):
        return f'<Log {self.title}>'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(12), index=True, unique=True)
    pwd_hash = db.Column(db.String(128))

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd_hash, pwd)

    def set_pwd(self, pwd):
        self.pwd_hash = generate_password_hash(pwd)

    def __repr__(self):
        return f'<User {self.username}>'
