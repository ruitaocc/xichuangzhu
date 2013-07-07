#-*- coding: UTF-8 -*-

import sys
sys.path.append('/var/www/flaskconfig/xichuangzhu')
import MySQLdb
import MySQLdb.cursors
import config
from flask import Flask, session, g
from xichuangzhu.models.inform_model import Inform

# convert python's encoding to utf8
reload(sys)
sys.setdefaultencoding('utf8')

# app
app = Flask(__name__)
app.config.update(
	SECRET_KEY = config.SECRET_KEY,
	SESSION_COOKIE_NAME = config.SESSION_COOKIE_NAME,
	PERMANENT_SESSION_LIFETIME = config.PERMANENT_SESSION_LIFETIME)

# inject vars into template context
@app.context_processor
def inject_vars():
	return dict(
		douban_login_url = config.DOUBAN_LOGIN_URL,	# douban oauth url
		admin_id = config.ADMIN_ID,	# admin id
		informs_num = Inform.get_new_informs_num(session['user_id']) if 'user_id' in session else 0)	# new informs num

# bafore every request
@app.before_request
def before_request():
    g.user_id =  session['user_id'] if 'user_id' in session else None
    g.conn = MySQLdb.connect(host=config.DB_HOST, user=config.DB_USER, passwd=config.DB_PASSWD, db=config.DB_NAME, use_unicode=True, charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)
    g.cursor = g.conn.cursor()

# after every request
@app.teardown_request
def teardown_request(exception):
    g.conn.close()

import log
import controllers
