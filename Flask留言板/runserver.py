from app import app, db
from app.models import Comment, User, Log


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, app=app, comment=Comment, user=User, log=Log)

def commit_log(message, title):
    l = Log(message=message, title=title)
    db.session.add(l)
    db.session.commit()


if __name__ == '__main__':

    app.run(debug=True)
