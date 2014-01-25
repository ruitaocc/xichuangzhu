# coding: utf-8
import hashlib
from flask import render_template, url_for
from flask_mail import Message, Mail
from . import config

mail = Mail()


def signup_mail(user):
    """Send signup email"""
    token = hashlib.sha1(user.name).hexdigest()
    url = config.SITE_DOMAIN + url_for('.activate', user_id=user.id, token=token)
    msg = Message("欢迎来到西窗烛", recipients=[user.email])
    msg.html = render_template('email/signup.html', url=url)
    mail.send(msg)