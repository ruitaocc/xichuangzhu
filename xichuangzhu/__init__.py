#-*- coding: UTF-8 -*-
import sys

sys.path.append('/var/www/flaskconfig/xichuangzhu')
import config
from flask import Flask, request, url_for, session, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

# convert python's encoding to utf8
reload(sys)
sys.setdefaultencoding('utf8')

# app
app = Flask(__name__)
app.config.from_object(config)

# Debug toolbar
if app.debug:
    toolbar = DebugToolbarExtension(app)

# SQLAlchemy
db = SQLAlchemy(app)

# inject vars into template context
@app.context_processor
def inject_vars():
    return dict(
        douban_login_url=config.DOUBAN_LOGIN_URL,
        admin_id=config.ADMIN_ID,
    )


# url generator for pagination
def url_for_other_page(page):
    view_args = request.view_args.copy()
    args = request.args.copy()
    args['page'] = page
    view_args.update(args)
    return url_for(request.endpoint, **view_args)


app.jinja_env.globals['url_for_other_page'] = url_for_other_page


# before every request
@app.before_request
def before_request():
    g.user_id = session['user_id'] if 'user_id' in session else None


import log
import controllers
import models