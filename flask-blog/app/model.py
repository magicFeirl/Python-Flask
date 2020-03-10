from app import db

class Comment(db.Model):
    __tablename__ = 'comment'

    username = db.Column(db.String(12))
    comment = db.Column(db.String(255))
    date = db.Column(db.DATETIME)

    uid = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'<{self.username}(uid:{self.uid})\'s comment.>'
