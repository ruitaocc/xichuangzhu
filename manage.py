# coding: utf-8
from flask.ext.script import Manager
from fabric.api import run as fabrun, env
from xichuangzhu import app
from xichuangzhu.models import db

manager = Manager(app)


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
def test():
    pass


if __name__ == "__main__":
    manager.run()