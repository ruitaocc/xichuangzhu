from fabric.api import run, env, cd
from xichuangzhu import config


def deploy():
    env.host_string = config.HOST_STRING
    with cd('/var/www/xichuangzhu'):
        run('git pull')
        run('supervisorctl restart xcz')