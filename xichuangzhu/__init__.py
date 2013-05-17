#-*- coding: UTF-8 -*-

import sys
sys.path.append('/var/www')
import config
from flask import Flask, session
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

import db
import log
import controllers
