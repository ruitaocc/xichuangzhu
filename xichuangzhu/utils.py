# coding: utf-8
import datetime
import uuid
from functools import wraps
from flask import session, abort, g
import config


# count the time diff by timedelta, return a user-friendly format
def time_diff(time):
    """Friendly time gap"""
    now = datetime.datetime.now()
    delta = now - time
    if delta.days > 365:
        return '%d年前' % (delta.days / 365)
    if delta.days > 30:
        return '%d个月前' % (delta.days / 30)
    if delta.days > 0:
        return '%d天前' % delta.days
    if delta.seconds > 3600:
        return '%d小时前' % (delta.seconds / 3600)
    if delta.seconds > 60:
        return '%d分钟前' % (delta.seconds / 60)
    return '刚刚'


def check_is_me(user_id):
    return True if "user_id" in session and session['user_id'] == user_id else False


# Check if is Administrator
def require_admin(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if not (g.user_id and g.user_id == config.ADMIN_ID):
            return abort(404)
        return func(*args, **kwargs)
    return decorator


# Check if login
def require_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not g.user_id:
            return abort(404)
        return func(*args, **kwargs)

    return decorated_function


def random_filename():
    """生成伪随机文件名"""
    return str(uuid.uuid4())