# coding: utf-8
from fabric.api import run, env, cd, prefix
from xichuangzhu import config


def deploy():
    env.host_string = config.HOST_STRING
    with cd('/var/www/xichuangzhu'):
        run('git pull')
        run('bower install')
        with prefix('source venv/bin/activate'):
            run('pip install -r requirements.txt')
        run('sudo supervisorctl restart xcz')


def restart():
    env.host_string = config.HOST_STRING
    run('sudo supervisorctl restart xcz')


def gene_sqlite():
    """生成sqlite文件，并通过邮件发送"""
    env.host_string = config.HOST_STRING
    with cd('/var/www/xichuangzhu'):
        with prefix('source venv/bin/activate'):
            run('python manage.py gene_sqlite')