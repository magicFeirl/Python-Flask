from wtforms import Form, StringField, TextField
from wtforms.validators import Length, DataRequired


class CommentForm(Form):
    content = TextField('content', [Length(0, 255), DataRequired()])
    username = StringField('title', [Length(3, 12), DataRequired()])
