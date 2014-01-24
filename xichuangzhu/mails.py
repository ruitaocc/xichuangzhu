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
    msg.html = "<h3>点击<a href='%s'>这里</a>，激活你在西窗烛的帐号。</h3>" % url
    mail.send(msg)