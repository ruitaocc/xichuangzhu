import sys
sys.path.append('/var/www')
import config

from flask import Flask, g
app = Flask(__name__)
app.config.update(DEBUG=config.DEBUG, SECRET_KEY=config.SECRET_KEY)

# inject douban_login_url into template context
@app.context_processor
def inject_user():
	return dict(douban_login_url=config.DOUBAN_LOGIN_URL)

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