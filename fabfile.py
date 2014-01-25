from fabric.api import run, env, cd, prefix
from xichuangzhu import config


def deploy():
    env.host_string = config.HOST_STRING
    with cd('/var/www/xichuangzhu'):
        with prefix('source venv/bin/activate'):
            run('pip install -r requirements.txt')
        run('git pull')
        run('supervisorctl restart xcz')