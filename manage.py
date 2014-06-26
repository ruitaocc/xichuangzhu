# coding: utf-8
import os
import sqlite3
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from fabric.api import run as fabrun, env
from xichuangzhu import app
from xichuangzhu.models import db, Work

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    """启动app"""
    app.run(debug=True)


@manager.command
def syncdb():
    """根据model创建数据库tables"""
    db.create_all()


@manager.command
def backdb():
    """将数据库中的表结构和数据提取为sql文件"""
    env.host_string = "localhost"
    fabrun("mysqldump -uroot -p xcz > /var/www/xichuangzhu/xcz.sql")


@manager.command
def gene_sqlite():
    """生成SQLite3数据库文件"""
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker

    db_filename = "xcz.db"
    if os.path.isfile(db_filename):
        os.remove(db_filename)

    engine = create_engine('sqlite:///xcz.db')
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
    session = Session()
    # 如果没有这一行，会报：
    # AttributeError: 'Session' object has no attribute '_model_changes'
    # 具体见：
    # http://stackoverflow.com/questions/20201809/sqlalchemy-flask-attributeerror-session-object-has-no-attribute-model-chan
    session._model_changes = {}

    class _Work(Base):
        __tablename__ = 'works'

        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(50))
        author = db.Column(db.String(50))
        kind = db.Column(db.Enum('shi', 'ci', 'qu', 'fu', 'wen'))
        foreword = db.Column(db.Text())
        content = db.Column(db.Text())
        intro = db.Column(db.Text())
        layout = db.Column(db.String(10))

        def __repr__(self):
            return '<Work %s>' % self.title

    Base.metadata.create_all(engine)

    for work in Work.query:
        _work = _Work(title=work.title, author=work.author.name, kind=work.type.en,
                      foreword=work.foreword, content=work.content, intro=work.intro,
                      layout=work.layout)
        session.add(_work)
    session.commit()


@manager.command
def test():
    pass


if __name__ == "__main__":
    manager.run()