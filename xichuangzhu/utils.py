# coding: utf-8
import datetime
import uuid
from functools import wraps
from flask import session, abort, g
import config

# count the time diff by timedelta, return a user-friendly format
# dt must be format as 2013-4-1 14:25:10
def time_diff(dt):
    dt = datetime.datetime.strptime(str(dt), "%Y-%m-%d %H:%M:%S")
    today = datetime.datetime.today()
    s = int((today - dt).total_seconds())

    # day_diff > 365, use year
    if s/3600/24 >= 365:
        return str(s/3600/24/365) + " 年前"
    elif s/3600/24 >= 30:   # day_diff > 30, use month
        return str(s/3600/24/30) + " 个月前"
    elif s/3600 >= 24:  # hour_diff > 24, use day
        return str(s/3600/24) + " 天前"
    elif s/60 > 60: # minite_diff > 60, use hour
        return str(s/3600) + " 小时前"
    elif s > 60:    # second_diff > 60, use minite
        return str(s/60) + " 分钟前"
    else:   # use "just now"
        return "刚刚"

def check_is_me(user_id):
    return True if "user_id" in session and session['user_id'] == user_id else False

# Check if is Administrator
def require_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not (g.user_id and g.user_id == config.ADMIN_ID):
            return abort(404)
        return func(*args, **kwargs)
    return decorated_function

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