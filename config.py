#-*- coding:utf-8 -*-

# site
SITE_DOMAIN = "http://localhost:5000"

# admin id
ADMIN_ID = 

# image upload path
IMAGE_PATH = '/var/www/xcz_uploads/work_imgs/'
IMAGE_URL = '/xcz_uploads/work_imgs/'

# app config
SECRET_KEY = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT" # replace to your secret key
PERMANENT_SESSION_LIFETIME = 3600*24*7
SESSION_COOKIE_NAME = 'xcz_session'

# db config
DB_HOST = "localhost"
DB_USER = ""
DB_PASSWD = ""
DB_NAME = "xichuangzhu"

# smtp config
SMTP_SERVER = ""
SMTP_PORT = 25
SMTP_USER = ""
SMTP_PASSWORD = ""
SMTP_FROM = ""
SMTP_ADMIN = ""

# douban oauth
#DOUBAN_CLIENT_ID = ''
#DOUBAN_SECRET = ''
#DOUBAN_REDIRECT_URI = '%s/login/douban' % SITE_DOMAIN
#DOUBAN_LOGIN_URL = "https://www.douban.com/service/auth2/auth?client_id=%s&redirect_uri=%s&response_type=code" % (DOUBAN_CLIENT_ID, DOUBAN_REDIRECT_URI)
