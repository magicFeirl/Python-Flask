import os
import sys
from datetime import datetime


import pytz
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

from comment_form import CommentForm


app = Flask(__name__)

prefix = r'sqlite:///'

app_path = os.path.join(app.root_path, 'comment.db')

if not sys.platform.startswith('win'):
    prefix += r'/'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + app_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

timezone = pytz.timezone('Asia/Shanghai')


class Comment(db.Model):
    __tablename__ = 'comment'

    username = db.Column(db.String(12))
    comment = db.Column(db.String(255))
    date = db.Column(db.DATETIME)

    uid = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'<{self.username}(uid:{self.uid})\'s comment.>'


@app.route('/')
def index():
    forms = Comment.query.order_by(Comment.uid.desc()).all()
    return render_template('index.html', forms=forms)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        form = CommentForm(request.form)
        if form.validate():

            # 由于数据库的原因（懒）导致这个地方的form name仍然为usernam，但事实上input框已经改为title了
            db.session.add(Comment(username=form.username.data, \
            comment=form.content.data, date=datetime.now(tz=timezone)))

            db.session.commit()
            return redirect(url_for('index'))
        else:
            return redirect(url_for('add'))
    else:
        return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
