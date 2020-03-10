from datetime import datetime

from flask import render_template, request, redirect, url_for, flash

from .model import Comment
from .comment_form import CommentForm
from app import app, db, timezone


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
