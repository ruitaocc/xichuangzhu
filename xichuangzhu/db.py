#-*- coding: UTF-8 -*-

import MySQLdb
import MySQLdb.cursors
from flask import g
from xichuangzhu import app
import config

# create db connection
@app.before_request
def before_request():
	g.conn = MySQLdb.connect(host=config.DB_HOST, user=config.DB_USER, passwd=config.DB_PASSWD, db=config.DB_NAME, use_unicode=True, charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)
	g.cursor = g.conn.cursor()

# close connection
@app.teardown_request
def teardown_request(exception):
	g.conn.close()