from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

from comment_form import CommentForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/flask-sql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Comment(db.Model):
    __tablename__ = 'comment'

    username = db.Column(db.String(12))
    comment = db.Column(db.String(255))
    date = db.Column(db.DATETIME)

    uid = db.Column(db.Integer, primary_key=True)

    pass

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
            db.session.add(Comment(username=form.username.data, comment=form.content.data, date=datetime.now()))

            db.session.commit()
            return redirect(url_for('index'))
        else:
            return redirect(url_for('add'))
    else:
        return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
