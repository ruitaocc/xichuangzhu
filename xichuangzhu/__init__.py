# coding: utf-8
import os
import sys

# 将project目录加入sys.path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.insert(0, project_path)

from flask import Flask, request, url_for, g, render_template, flash
from jinja2 import Markup
from flask_wtf.csrf import CsrfProtect
from flask.ext.uploads import configure_uploads
from flask_debugtoolbar import DebugToolbarExtension
from .utils import get_current_user, signout_user
from config import load_config

# convert python's encoding to utf8
reload(sys)
sys.setdefaultencoding('utf8')

csrf = CsrfProtect()


def create_app():
    app = Flask(__name__)
    config = load_config()
    app.config.from_object(config)

    # CSRF protect
    csrf.init_app(app)

    if app.debug:
        pass
        # DebugToolbarExtension(app)
    else:
        from .sentry import sentry

        sentry.init_app(app, dsn=app.config.get('SENTRY_DSN'))

    from .mails import mail

    mail.init_app(app)

    register_db(app)
    register_routes(app)
    register_jinja(app)
    register_error_handle(app)
    register_logger(app)
    register_uploadsets(app)

    # before every request
    @app.before_request
    def before_request():
        g.user = get_current_user()
        if g.user:
            if g.user.is_new:
                flash('请登录邮箱激活账户。')
                signout_user()
            if g.user.is_banned:
                flash('账户已被禁用，请联系管理员。')
                signout_user()

    return app


def register_jinja(app):
    from . import filters, permissions

    app.jinja_env.filters.update({
        'clean_work': filters.clean_work,
        'timesince': filters.timesince,
        'markdown_work': filters.markdown_work,
        'markdown': filters.markdown,
        'format_year': filters.format_year,
        'format_text': filters.format_text,
        'is_work_collected': filters.is_work_collected,
        'is_work_image_collected': filters.is_work_image_collected
    })

    # url generator for pagination
    def url_for_other_page(page):
        view_args = request.view_args.copy()
        args = request.args.copy().to_dict()
        args['page'] = page
        view_args.update(args)
        return url_for(request.endpoint, **view_args)

    def set_url_param(**params):
        """Set param in url"""
        view_args = request.view_args.copy()
        args = request.args.copy().to_dict()
        combined_args = dict(view_args.items() + args.items())
        if params:
            combined_args.update(params)
        return url_for(request.endpoint, **combined_args)

    def static(filename):
        """生成静态资源url"""
        return url_for('static', filename=filename)

    def js(path):
        """生成script标签"""
        return Markup("<script type='text/javascript' src='%s'></script>" % static(path))

    def css(path):
        """生成link标签"""
        return Markup("<link rel='stylesheet' href='%s'></script>" % static(path))

    app.jinja_env.globals.update({
        'url_for_other_page': url_for_other_page,
        'set_url_param': set_url_param,
        'static': static,
        'js': js,
        'css': css,
        'permissions': permissions
    })


def register_logger(app):
    """Send error log to admin by smtp"""
    pass


def register_db(app):
    from .models import db

    db.init_app(app)


def register_routes(app):
    from .controllers import account, admin, author, dynasty, topic, site, user, work, api

    app.register_blueprint(site.bp, url_prefix='')
    app.register_blueprint(account.bp, url_prefix='/account')
    app.register_blueprint(admin.bp, url_prefix='/admin')
    app.register_blueprint(topic.bp, url_prefix='/topic')
    app.register_blueprint(dynasty.bp, url_prefix='/dynasty')
    app.register_blueprint(author.bp, url_prefix='/author')
    app.register_blueprint(work.bp, url_prefix='/work')
    app.register_blueprint(user.bp, url_prefix='/user')
    app.register_blueprint(api.bp, url_prefix='/api')


def register_error_handle(app):
    @app.errorhandler(403)
    def page_403(error):
        return render_template('site/403.html'), 403

    @app.errorhandler(404)
    def page_404(error):
        return render_template('site/404.html'), 404

    @app.errorhandler(500)
    def page_500(error):
        return render_template('site/500.html'), 500


def register_uploadsets(app):
    from .uploadsets import workimages

    configure_uploads(app, (workimages))
