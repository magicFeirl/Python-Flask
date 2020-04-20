from datetime import datetime

from flask import render_template, url_for, redirect, request
from flask_login import login_user, logout_user, login_required

from app import app, db, login_manager
from .forms import CommentForm, LoginForm, LogForm
from .models import Comment, User, Log, Reply


def get_comment_by_id(id):
    return Comment.query.get_or_404(id)

@app.route('/')
@app.route('/index')
def index():
    cards = Comment.query.order_by(Comment.is_topic.desc()). \
    order_by(Comment.id.desc()).all()

    # replys = Comment.query.replys.all()

    return render_template('index.html', title='留言板', \
    cards=cards, rep=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_pwd(pwd):
            return redirect(url_for('login'))
        else:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))

    return render_template('login.html', title='登录', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/reply', methods=['POST'])
def reply():
    data_id = request.form.get('data_id')
    text = request.form.get('text')

    if len(text) > 0 and len(text) <= 255:

        c = get_comment_by_id(data_id)
        r = Reply(message=text, \
        time=datetime.now(tz=app.config['TIMEZONE']), comment=c)

        db.session.add(r)
        db.session.commit()

    return {'status': '200'}

@app.route('/topic', methods=['POST'])
@login_required
def topic():
    c = get_comment_by_id(request.form.get('data_id'))
    c.is_topic = not c.is_topic
    db.session.add(c)
    db.session.commit()

    return {'status': '200'}

@app.route('/delete', methods=['POST'])
@login_required
def delete():
    c = get_comment_by_id(request.form.get('data_id'))
    reps = c.replys.all()
    for rep in reps:
        db.session.delete(rep)
    db.session.delete(c)

    db.session.commit()
    return {'status': '200'}

@app.route('/hide', methods=['POST'])
@login_required
def hide():
    c = get_comment_by_id(request.form.get('data_id'))
    c.hide_this()
    db.session.add(c)
    db.session.commit()

    return {'status': '200'}

@app.route('/delete_reply', methods=['POST'])
@login_required
def delete_reply():
    r = Reply.query.get_or_404(request.form.get('data_id'))
    db.session.delete(r)

    db.session.commit()
    return {'status': '200'}

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    form = CommentForm()
    if form.validate_on_submit():
        message = form.message.data
        # 这里标题数据库有默认值，但是''不为None，所以还得写个判断
        title = form.title.data if form.title.data != '' else '无标题'
        is_topic = form.topic_this.data

        c = Comment(message=message, title=title, is_topic=is_topic, \
        time=datetime.now(tz=app.config['TIMEZONE']))
        db.session.add(c)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('comment.html', title='留言', form=form)


@app.route('/log', methods=['GET', 'POST'])
def log():
    cards = Log.query.order_by(Log.id.desc()).all()

    return render_template('index.html', title='日志', cards=cards, \
    rep=False)


