from fabric.api import run, env, cd

env.host_string = "root@173.208.227.86"

def start():
    with cd('/var/www/xichuangzhu'):
        run('git pull')
        run('gunicorn -c gunicorn.conf xichuangzhu:app -D')

def restart():
    with cd('/var/www/xichuangzhu'):
        run('kill -HUP `cat /tmp/xichuangzhu.pid`')

def deploy():
    with cd('/var/www/xichuangzhu'):
        run('git pull')
        run('kill -HUP `cat /tmp/xichuangzhu.pid`')

def ldeploy():
    with cd('/var/www/xichuangzhu'):
        run('git pull')

def backup():
    pass