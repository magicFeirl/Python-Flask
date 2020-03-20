from flask_wtf import FlaskForm
from wtforms import TextAreaField, TextField, SubmitField
from wtforms import BooleanField, PasswordField

from wtforms.validators import DataRequired, Length

class CommentForm(FlaskForm):
    message = TextAreaField(validators=[DataRequired(), Length(1, 255)])
    title = TextField(validators=[Length(0, 12)])
    topic_this = BooleanField('置顶该条')

    submit = SubmitField('发送')

class LogForm(FlaskForm):
    message = TextAreaField(validators=[DataRequired(), Length(1, 255)])
    title = TextField(validators=[Length(0, 12)])

    submit = SubmitField('发送日志')

class LoginForm(FlaskForm):
    username = TextField('用户名', validators=[DataRequired(), Length(1, 12)])
    password = PasswordField('密码', validators=[DataRequired()])
    remember = BooleanField('记住我')

    submit = SubmitField('登录')
