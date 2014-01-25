from flask.ext.script import Manager
from xichuangzhu import app
from xichuangzhu.models import db

manager = Manager(app)


@manager.command
def run():
    app.run(debug=True)


@manager.command
def syncdb():
    db.create_all()


@manager.command
def test():
    pass


if __name__ == "__main__":
    manager.run()