# coding: utf-8
import datetime
import uuid
from oss.oss_api import OssAPI
from flask import session, g
from . import config, roles
from .models import User


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
    """判断此user是否为当前在线的user"""
    return g.user and g.user.id == user_id


def signin_user(user, permenent):
    """Sign in user"""
    session.permanent = permenent
    session['user_id'] = user.id


def signout_user():
    """Sign out user"""
    session.pop('user_id', None)


def get_current_user():
    """获取当前user，同时进行session有效性的检测"""
    if not 'user_id' in session:
        return None
    user = User.query.filter(User.id == session['user_id']).first()
    if not user:
        signout_user()
        return None
    return user


def get_current_user_role():
    """获取当前用户的角色，若无有效用户，则返回VisitorRole"""
    if not g.user:
        return roles.VisitorRole
    return g.user.role


def random_filename():
    """生成伪随机文件名"""
    return str(uuid.uuid4())


def save_to_oss(filename, uploadset):
    """将文件保存到OSS上，若保存失败，则抛出IO异常"""
    oss = OssAPI(config.OSS_HOST, config.OSS_KEY, config.OSS_SECRET)
    res = oss.put_object_from_file("xichuangzhu", filename, uploadset.config.destination + '/' + filename)
    status = res.status
    if status != 200:
        raise IOError
