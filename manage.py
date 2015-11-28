# coding: utf-8
import os
import re
import glob2
import requests
from lxml import html
from werkzeug.security import gen_salt
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from fabric.api import run as fabrun, env
from application import create_app
from application.models import db, Work, Author, Dynasty, Quote, Collection, CollectionKind, CollectionWork
from application.utils.helpers import s2t

# Used by app debug & livereload
PORT = 5000

app = create_app()
manager = Manager(app)

# 添加migrate命令
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    """启动app"""
    app.run(debug=True, port=PORT)


@manager.command
def build():
    """Use FIS to compile assets."""
    os.system('gulp')
    os.chdir('application')
    os.system('fis release -d ../output -opmD')


@manager.command
def live():
    """Run livereload server"""
    from livereload import Server

    server = Server(app)

    map(server.watch, glob2.glob("application/pages/**/*.*"))  # pages
    map(server.watch, glob2.glob("application/macros/**/*.html"))  # macros
    map(server.watch, glob2.glob("application/static/**/*.*"))  # public assets

    server.serve(port=PORT)


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
        db_file = "xcz_tr.db"
    else:
        db_file = "/xcz.db"
    db_file_path = "/tmp/%s" % db_file

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
        baidu_wiki = Column(String(200))
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
        first_char = Column(String(10))
        intro = Column(Text)
        works_count = Column(Integer)
        dynasty = Column(String(10))
        birth_year = Column(String(20))
        death_year = Column(String(20))
        updated_at = Column(String(30))
        baidu_wiki = Column(String(200))

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
        quote = Column(Text)
        author_id = Column(Integer)
        author = Column(String(10))
        work_id = Column(Integer)
        work = Column(String(50))
        updated_at = Column(String(30))

    class _Collection(Base):
        __tablename__ = 'collections'

        id = Column(Integer, primary_key=True)
        show_order = Column(Integer)
        name = Column(String(200))
        full_name = Column(String(200))
        abbr = Column(String(50))
        desc = Column(Text())
        cover = Column(String(200))
        link = Column(String(300))
        kind_id = Column(Integer)
        kind = Column(String(100))

    class _CollectionKind(Base):
        __tablename__ = 'collection_kinds'

        id = Column(Integer, primary_key=True)
        show_order = Column(Integer)
        name = Column(String(100))

    class _CollectionWork(Base):
        __tablename__ = 'collection_works'

        id = Column(Integer, primary_key=True)
        show_order = Column(Integer)

        work_id = Column(Integer)
        work_title = Column(String(100))
        work_full_title = Column(String(50))
        work_author = Column(String(50))
        work_dynasty = Column(String(10))
        work_content = Column(Text)

        collection_id = Column(Integer)
        collection = Column(String(100))

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
            if work.title_suffix and '·' not in work.title:
                work_full_title = "%s · %s" % (work_title, work.title_suffix)
            else:
                work_full_title = work_title

            work_content = _get_work_content(work)

            # 处理评析
            work_intro = work.intro.replace('\r\n\r\n', '\n')
            _work = _Work(id=work.id, show_order=index, title=work_title,
                          full_title=work_full_title, baidu_wiki=work.baidu_wiki,
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
                              death_year=death_year, baidu_wiki=author.baidu_wiki,
                              updated_at=author.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                              works_count=author.works.filter(Work.highlight).count(),
                              first_char=_get_first_char(author.name))
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
            _quote = _Quote(id=quote.id, quote=quote.quote, author_id=quote.work.author_id,
                            author=quote.work.author.name, work_id=quote.work_id, work=quote.work.title,
                            updated_at=quote.updated_at.strftime('%Y-%m-%d %H:%M:%S'))
            if tr:
                _s2t_quote(_quote)
            session.add(_quote)

        # 转存集合类型
        for collection_kind in CollectionKind.query:
            _collection_kind = _CollectionKind(id=collection_kind.id, show_order=collection_kind.order,
                                               name=collection_kind.name)
            session.add(_collection_kind)

        # 转存集合
        for collection in Collection.query:
            _collection = _Collection(id=collection.id, show_order=collection.order,
                                      name=collection.name, full_name=collection.full_name,
                                      abbr=collection.abbr, desc=collection.desc,
                                      cover=collection.cover, link=collection.link,
                                      kind=collection.kind.name, kind_id=collection.kind_id)
            session.add(_collection)

        # 转存集合作品
        for collection_work in CollectionWork.query:
            _collection_work = _CollectionWork(id=collection_work.id, show_order=collection_work.order,
                                               work_id=collection_work.work_id, work_title=collection_work.work.title,
                                               work_full_title=collection_work.work.full_title,
                                               work_author=collection_work.work.author.name,
                                               work_dynasty=collection_work.work.author.dynasty.name,
                                               work_content=_get_work_content(collection_work.work),
                                               collection_id=collection_work.collection_id,
                                               collection=collection_work.collection.name)
            session.add(_collection_work)

        session.commit()

        # 将数据库文件以邮件的形式发送
        from flask_mail import Message
        from application.utils.mails import mail

        config = app.config
        msg = Message("SQLite File", recipients=[config.get('MAIL_ADMIN_ADDR')])
        with open(db_file_path, 'rb') as f:
            msg.attach(db_file, "application/octet-stream", f.read())
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


@manager.command
def convert_title():
    with app.app_context():
        for work in Work.query:
            work.title = work.title.replace('-', ' · ')
            db.session.add(work)
        db.session.commit()


@manager.command
def detect_whitespace():
    with app.app_context():
        for work in Work.query:
            if ' ' in work.content:
                index = work.content.index(' ')
                print("work %d - %d - %s" % (work.id, index, work.content[index + 1]))
        for quote in Quote.query:
            if ' ' in quote.quote:
                index = quote.quote.index(' ')
                print("quote %d - %d - %s" % (quote.id, index, quote.quote[index + 1]))


@manager.command
def detect_illegal_punctuation():
    with app.app_context():
        for work in Work.query:
            for letter in ',()?-:':
                if letter in work.content:
                    print("work %d %s" % (work.id, letter))
        for quote in Quote.query:
            for letter in ',()?-:':
                if letter in quote.quote:
                    print("work %d %s" % (quote.id, letter))


@manager.command
def find_works_wiki():
    with app.app_context():
        for work in Work.query:
            if work.baidu_wiki:
                continue

            title = work.title
            if work.title_suffix:
                title += '' + work.title_suffix
            print(title)

            r = requests.get('http://baike.baidu.com/search?word=%s&pn=0&rn=0&enc=utf8' % title)
            tree = html.fromstring(r.text)
            results = tree.cssselect('.search-list dd a')
            if len(results) > 0:
                work.baidu_wiki = results[0].get('href')
                print(work.baidu_wiki)
                db.session.add(work)
                db.session.commit()


@manager.command
def find_authors_wiki():
    with app.app_context():
        for author in Author.query:
            if author.baidu_wiki:
                continue
            print(author.name)

            r = requests.get('http://baike.baidu.com/search?word=%s&pn=0&rn=0&enc=utf8' % author.name)
            tree = html.fromstring(r.text)
            results = tree.cssselect('.search-list dd a')
            if len(results) > 0:
                author.baidu_wiki = results[0].get('href')
                print(author.baidu_wiki)
                db.session.add(author)
                db.session.commit()


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


def _get_work_content(work):
    work_content = work.mobile_content or work.content
    work_content = re.sub(r'<([^<]+)>', '', work_content)
    work_content = work_content.replace('%', "    ")
    work_content = work_content.replace('\r\n\r\n', '\n')
    return work_content


def _get_first_char(text):
    from pypinyin import lazy_pinyin

    return lazy_pinyin(text)[0][0].upper()


if __name__ == "__main__":
    manager.run()
