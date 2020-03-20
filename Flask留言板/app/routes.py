from datetime import datetime

from flask import render_template, url_for, redirect
from flask_login import login_user

from app import app, db, login_manager
from .forms import CommentForm, LoginForm, LogForm
from .models import Comment, User, Log


@app.route('/')
@app.route('/index')
def index():
    cards = Comment.query.order_by(Comment.is_topic.desc()). \
    order_by(Comment.id.desc()).all()

    return render_template('index.html', title='首页', cards=cards)


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

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    form = CommentForm()
    if form.validate_on_submit():
        message = form.message.data
        # 这里标题数据库有默认值，但是''不为None，所以还得写个判断
        title = form.title.data if form.title.data != '' else '无标题'
        is_topic = form.topic_this.data

        print(title, '#', sep='')

        c = Comment(message=message, title=title, is_topic=is_topic, \
        time=datetime.now(tz=app.config['TIMEZONE']))
        db.session.add(c)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('comment.html', title='留言', form=form)


@app.route('/log', methods=['GET', 'POST'])
def log():
    cards = Log.query.order_by(Log.id.desc()).all()

    return render_template('index.html', title='日志', cards=cards)

