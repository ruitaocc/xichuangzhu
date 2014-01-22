# coding: utf-8
import sys
from flask import Flask, request, url_for, session, g, render_template
from flask_wtf.csrf import CsrfProtect
from flask.ext.uploads import configure_uploads
from flask_debugtoolbar import DebugToolbarExtension
from . import config
from .utils import get_current_user, get_current_role

# convert python's encoding to utf8
reload(sys)
sys.setdefaultencoding('utf8')


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # CSRF protect
    CsrfProtect(app)

    if app.debug:
        DebugToolbarExtension(app)

    register_db(app)
    register_routes(app)
    register_jinja(app)
    register_error_handle(app)
    register_logger(app)
    register_uploadsets(app)

    # before every request
    @app.before_request
    def before_request():
        g.user_id = session['user_id'] if 'user_id' in session else None
        g.current_user = get_current_user()
        g.current_role = get_current_role()

    return app


def register_jinja(app):
    from . import filters

    app.jinja_env.filters['timesince'] = filters.timesince
    app.jinja_env.filters['clean_work'] = filters.clean_work
    app.jinja_env.filters['markdown_work'] = filters.markdown_work
    app.jinja_env.filters['format_year'] = filters.format_year
    app.jinja_env.filters['format_text'] = filters.format_text
    app.jinja_env.filters['is_work_collected'] = filters.is_work_collected
    app.jinja_env.filters['is_work_image_collected'] = filters.is_work_image_collected

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
        args = request.args.copy().to_dict()
        args['page'] = page
        view_args.update(args)
        return url_for(request.endpoint, **view_args)

    app.jinja_env.globals['url_for_other_page'] = url_for_other_page


def register_logger(app):
    """Send error log to admin by smtp"""
    if not app.debug:
        import logging
        from logging.handlers import SMTPHandler
        credentials = (config.SMTP_USER, config.SMTP_PASSWORD)
        mail_handler = SMTPHandler((config.SMTP_SERVER, config.SMTP_PORT), config.SMTP_FROM, config.SMTP_ADMIN, 'xcz-log',
                                   credentials)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


def register_db(app):
    from .models import db
    db.init_app(app)


def register_routes(app):
    from .controllers import account, admin, author, dynasty, topic, site, user, work

    app.register_blueprint(site.bp, url_prefix='')
    app.register_blueprint(account.bp, url_prefix='/account')
    app.register_blueprint(admin.bp, url_prefix='/admin')
    app.register_blueprint(topic.bp, url_prefix='/topic')
    app.register_blueprint(dynasty.bp, url_prefix='/dynasty')
    app.register_blueprint(author.bp, url_prefix='/author')
    app.register_blueprint(work.bp, url_prefix='/work')
    app.register_blueprint(user.bp, url_prefix='/user')


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

app = create_app()