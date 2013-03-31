import sys
sys.path.append('/var/www')
import config

from flask import Flask, g
app = Flask(__name__)
app.config.update(SECRET_KEY=config.SECRET_KEY)

# inject douban_login_url into template context
@app.context_processor
def inject_user():
	return dict(douban_login_url=config.DOUBAN_LOGIN_URL, admin_id = config.ADMIN_ID)

# send log msg using smtp
if not app.debug:
	import logging
	# from logging import Formatter
	from logging.handlers import SMTPHandler
	credentials = (config.SMTP_USER, config.SMTP_PASSWORD)
	mail_handler = SMTPHandler((config.SMTP_SERVER, config.SMTP_PORT), config.SMTP_FROM, config.SMTP_ADMIN, 'xcz-log', credentials)
	mail_handler.setLevel(logging.ERROR)
	# mail_handler.setFormatter(Formatter('''
	# 	Message Type: %(levelname)s
	# 	'''))
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

# convert python's encoding to utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import controllers