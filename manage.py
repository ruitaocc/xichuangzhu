# coding: utf-8
import os
import re
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from fabric.api import run as fabrun, env
from xichuangzhu import app, config
from xichuangzhu.models import db, Work, Author, Dynasty, Quote

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
    from sqlalchemy import Column, Integer, String, Enum, Text

    db_file_path = "/tmp/xcz.db"

    if os.path.isfile(db_file_path):
        os.remove(db_file_path)

    engine = create_engine('sqlite:///%s' % db_file_path)
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
    session = Session()
    # 如果没有这一行，会报：
    # AttributeError: 'Session' object has no attribute '_model_changes'
    # 具体见：
    # http://stackoverflow.com/questions/20201809/sqlalchemy-flask-attributeerror-session-object
    # -has-no-attribute-model-chan
    session._model_changes = {}

    class _Work(Base):
        __tablename__ = 'works'

        id = Column(Integer, primary_key=True)
        title = Column(String(50))
        author = Column(String(50))
        author_id = Column(Integer)
        dynasty = Column(String(10))
        kind = Column(Enum('shi', 'ci', 'qu', 'fu', 'wen'))
        kind_cn = Column(String(20))
        foreword = Column(Text)
        content = Column(Text)
        intro = Column(Text)
        layout = Column(String(10))

        def __repr__(self):
            return '<Work %s>' % self.title

    class _Author(Base):
        __tablename__ = 'authors'

        id = Column(Integer, primary_key=True)
        name = Column(String(50))
        intro = Column(Text)
        dynasty = Column(String(10))
        birth_year = Column(String(20))
        death_year = Column(String(20))

    class _Dynasty(Base):
        __tablename__ = 'dynasties'

        id = Column(Integer, primary_key=True)
        name = Column(String(10))
        intro = Column(db.Text)
        start_year = Column(Integer)
        end_year = Column(Integer)

    class _Quote(Base):
        __tablename__ = 'quotes'

        id = Column(Integer, primary_key=True)
        quote = Column(db.Text)
        author_id = Column(Integer)
        author = Column(String(10))
        work_id = Column(Integer)
        work = Column(String(50))

    Base.metadata.create_all(engine)

    # 转存作品
    for work in Work.query.filter(Work.highlight == True):
        # 去掉注释，将%转换为空格
        work_title = work.mobile_title or work.title
        work_content = work.mobile_content or work.content
        work_content = re.sub(r'<([^<]+)>', '', work_content)
        work_content = work_content.replace('%', "    ")
        work_content = work_content.replace('\r\n\r\n', '\n')
        _work = _Work(id=work.id, title=work_title, author_id=work.author_id,
                      author=work.author.name, dynasty=work.author.dynasty.name,
                      kind=work.type.en, kind_cn=work.type.cn, foreword=work.foreword,
                      content=work_content, intro=work.intro, layout=work.layout)
        session.add(_work)

    # 转存文学家
    for author in Author.query.filter(Author.works.any(Work.highlight)):
        # 处理birth_year
        birth_year = author.birth_year
        if birth_year and '?' not in birth_year:
            birth_year += "年"
        if '-' in birth_year:
            birth_year = birth_year.replace('-', '前')

        # 处理death_year
        death_year = author.death_year
        if death_year and '?' not in death_year:
            death_year += "年"
        if '-' in death_year:
            death_year = death_year.replace('-', '前')

        _author = _Author(id=author.id, name=author.name, intro=author.intro,
                          dynasty=author.dynasty.name, birth_year=birth_year,
                          death_year=death_year)
        session.add(_author)

    # 转存朝代
    for dynasty in Dynasty.query.filter(
            Dynasty.authors.any(Author.works.any(Work.highlight == True))):
        _dynasty = _Dynasty(id=dynasty.id, name=dynasty.name, intro=dynasty.intro,
                            start_year=dynasty.start_year, end_year=dynasty.end_year)
        session.add(_dynasty)

    # 转存摘录
    for q in Quote.query.filter(Quote.work.has(Work.highlight == True)):
        _quote = _Quote(id=q.id, quote=q.quote, author_id=q.author_id, author=q.author.name,
                        work_id=q.work_id, work=q.work.title)
        session.add(_quote)

    session.commit()

    # 将数据库文件以邮件的形式发送
    from flask_mail import Message
    from xichuangzhu.mails import mail

    msg = Message("SQLite File", recipients=[config.MAIL_ADMIN_ADDR])
    with open(db_file_path, 'rb') as f:
        msg.attach("xcz.db", "application/octet-stream", f.read())
    mail.send(msg)


@manager.command
def test():
    pass


if __name__ == "__main__":
    manager.run()