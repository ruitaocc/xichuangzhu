#-*- coding: UTF-8 -*-

# convert python's encoding to utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# load config
sys.path.append('/var/www')
import config

# app
from flask import Flask, g, session
app = Flask(__name__)
app.config.update(
	SECRET_KEY = config.SECRET_KEY,
	SESSION_COOKIE_NAME = config.SESSION_COOKIE_NAME,
	PERMANENT_SESSION_LIFETIME = config.PERMANENT_SESSION_LIFETIME)

from xichuangzhu.models.inform_model import Inform

# inject vars into template context
@app.context_processor
def inject_vars():
	return dict(
		douban_login_url = config.DOUBAN_LOGIN_URL,	# douban oauth url
		admin_id = config.ADMIN_ID,	# admin id
		informs_num = Inform.get_new_informs_num(session['user_id']) if 'user_id' in session else 0)	# new informs num

# send log msg using smtp
if not app.debug:
	import logging
	from logging.handlers import SMTPHandler
	credentials = (config.SMTP_USER, config.SMTP_PASSWORD)
	mail_handler = SMTPHandler((config.SMTP_SERVER, config.SMTP_PORT), config.SMTP_FROM, config.SMTP_ADMIN, 'xcz-log', credentials)
	mail_handler.setLevel(logging.ERROR)
	app.logger.addHandler(mail_handler)

# mysql
import MySQLdb
import MySQLdb.cursors

@app.before_request
def before_request():
	g.conn = MySQLdb.connect(host=config.DB_HOST, user=config.DB_USER, passwd=config.DB_PASSWD, db=config.DB_NAME, use_unicode=True, charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)
	g.cursor = g.conn.cursor()

@app.teardown_request
def teardown_request(exception):
	g.conn.close()

import controllers