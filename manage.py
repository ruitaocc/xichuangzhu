# coding: utf-8
import os
import re
from werkzeug.security import gen_salt
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from fabric.api import run as fabrun, env
from xichuangzhu import create_app
from xichuangzhu.models import db, Work, Author, Dynasty, Quote
from xichuangzhu.utils import s2t

app = create_app()
manager = Manager(app)

# 添加migrate命令
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
def sqlite(tr=False):
    """生成SQLite3数据库文件"""
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import Column, Integer, String, Enum, Text

    if tr:
        db_file_path = "/tmp/xcz_tr.db"
    else:
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

    class _Version(Base):
        __tablename__ = 'version'

        version = Column(String(20), primary_key=True)

    class _Work(Base):
        __tablename__ = 'works'

        id = Column(Integer, primary_key=True)
        title = Column(String(50))
        full_title = Column(String(50))
        show_order = Column(Integer)
        author = Column(String(50))
        author_id = Column(Integer)
        dynasty = Column(String(10))
        kind = Column(Enum('shi', 'ci', 'qu', 'fu', 'wen'))
        kind_cn = Column(String(20))
        foreword = Column(Text)
        content = Column(Text)
        intro = Column(Text)
        layout = Column(String(10))
        updated_at = Column(String(30))

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
        updated_at = Column(String(30))

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
        updated_at = Column(String(30))

    Base.metadata.create_all(engine)

    with app.app_context():
        # 设置version
        version = _Version(version=gen_salt(20))
        session.add(version)

        # 转存作品
        works = Work.query.filter(Work.highlight).order_by(db.func.random())
        for index, work in enumerate(works):
            # 优先使用mobile版title和content
            work_title = work.mobile_title or work.title
            if work.title_suffix and '-' not in work.title:
                work_full_title = "%s-%s" % (work_title, work.title_suffix)
            else:
                work_full_title = work_title
            work_content = work.mobile_content or work.content

            # 处理content，去掉注释，将%转换为空格
            work_content = re.sub(r'<([^<]+)>', '', work_content)
            work_content = work_content.replace('%', "    ")
            work_content = work_content.replace('\r\n\r\n', '\n')

            # 处理评析
            work_intro = work.intro.replace('\r\n\r\n', '\n')
            _work = _Work(id=work.id, show_order=index, title=work_title,
                          full_title=work_full_title,
                          author_id=work.author_id, author=work.author.name,
                          dynasty=work.author.dynasty.name,
                          kind=work.type.en, kind_cn=work.type.cn, foreword=work.foreword,
                          content=work_content, intro=work_intro, layout=work.layout,
                          updated_at=work.updated_at.strftime('%Y-%m-%d %H:%M:%S'))
            if tr:
                _s2t_work(_work)
            session.add(_work)

        # 转存文学家
        for author in Author.query.filter(Author.works.any(Work.highlight)).order_by(
                Author.birth_year.asc()):
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
                              death_year=death_year,
                              updated_at=author.updated_at.strftime('%Y-%m-%d %H:%M:%S'))
            if tr:
                _s2t_author(_author)
            session.add(_author)

        # 转存朝代
        for dynasty in Dynasty.query.filter(
                Dynasty.authors.any(Author.works.any(Work.highlight))):
            _dynasty = _Dynasty(id=dynasty.id, name=dynasty.name, intro=dynasty.intro,
                                start_year=dynasty.start_year, end_year=dynasty.end_year)
            if tr:
                _s2t_dynasty(_dynasty)
            session.add(_dynasty)

        # 转存摘录
        for quote in Quote.query.filter(Quote.work.has(Work.highlight)):
            _quote = _Quote(id=quote.id, quote=quote.quote, author_id=quote.author_id,
                            author=quote.author.name, work_id=quote.work_id, work=quote.work.title,
                            updated_at=quote.updated_at.strftime('%Y-%m-%d %H:%M:%S'))
            if tr:
                _s2t_quote(_quote)
            session.add(_quote)

        session.commit()

        # 将数据库文件以邮件的形式发送
        from flask_mail import Message
        from xichuangzhu.mails import mail

        config = app.config
        msg = Message("SQLite File", recipients=[config.get('MAIL_ADMIN_ADDR')])
        with open(db_file_path, 'rb') as f:
            msg.attach("xcz.db", "application/octet-stream", f.read())
        mail.send(msg)


@manager.command
def generate_like_db():
    """生成xcz_user.db"""
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import Column, Integer, String, Enum, Text

    db_file_path = "/tmp/xcz_user.db"

    if os.path.isfile(db_file_path):
        os.remove(db_file_path)

    engine = create_engine('sqlite:///%s' % db_file_path)
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
    session = Session()
    session._model_changes = {}

    class _Like(Base):
        __tablename__ = 'likes'

        id = Column(Integer, primary_key=True)
        work_id = Column(Integer)
        show_order = Column(Integer, default=0)
        created_at = Column(String(30))

        def __repr__(self):
            return '<Like %s>' % self.work_id

    Base.metadata.create_all(engine)


def _s2t_work(work):
    work.title = s2t(work.title)
    work.full_title = s2t(work.full_title)
    work.author = s2t(work.author)
    work.dynasty = s2t(work.dynasty)
    work.intro = s2t(work.intro)
    work.content = s2t(work.content)
    work.foreword = s2t(work.foreword)


def _s2t_dynasty(dynasty):
    dynasty.name = s2t(dynasty.name)
    dynasty.intro = s2t(dynasty.intro)


def _s2t_quote(quote):
    quote.quote = s2t(quote.quote)
    quote.author = s2t(quote.author)
    quote.work = s2t(quote.work)


def _s2t_author(author):
    author.name = s2t(author.name)
    author.intro = s2t(author.intro)
    author.dynasty = s2t(author.dynasty)


if __name__ == "__main__":
    manager.run()