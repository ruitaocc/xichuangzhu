# coding: utf-8

# set False in production
DEBUG = True

# site domain
SITE_DOMAIN = "http://localhost:5000"
IMAGE_SERVER_URL = "http://localhost"

# image upload path
UPLOADS_DEFAULT_DEST = "/Library/WebServer/Documents/xcz_uploads"
UPLOADS_DEFAULT_URL = "%s/xcz_uploads/" % IMAGE_SERVER_URL

# app config
SECRET_KEY = ""
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 7
SESSION_COOKIE_NAME = 'xcz_session'

# db config
DB_HOST = ""
DB_USER = ""
DB_PASSWORD = ""
DB_NAME = "xcz"
SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/%s" % (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

# smtp config
SMTP_SERVER = ""
SMTP_PORT = 25
SMTP_USER = ""
SMTP_PASSWORD = ""
SMTP_FROM = ""
SMTP_ADMIN = ""

# Flask debug toolbar
DEBUG_TB_INTERCEPT_REDIRECTS = False

# douban oauth2 config
DOUBAN_CLIENT_ID = '0cf909cba46ce67526eb1d62ed46b35f'
DOUBAN_SECRET = '4c87a8ef33e6c6be'
DOUBAN_REDIRECT_URI = '%s/account/signin' % SITE_DOMAIN
DOUBAN_LOGIN_URL = "https://www.douban.com/service/auth2/auth?client_id=%s&redirect_uri=%s&response_type=code" % (
    DOUBAN_CLIENT_ID, DOUBAN_REDIRECT_URI)