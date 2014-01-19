# coding: utf-8
import datetime
import re
import markdown2
from flask import session
from models import CollectWork, CollectWorkImage


def timesince(value):
    """Friendly time gap"""
    now = datetime.datetime.now()
    delta = now - value
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


def clean_work(content):
    """截取作品内容时，去除其中一些不需要的元素"""
    c = re.sub(r'<([^<]+)>', '', content)
    c = c.replace('%', '')
    c = c.replace('（一）', "")
    c = c.replace('(一)', "")
    return c


def markdown_work(content):
    """将作品内容格式化为HTML标签
    Add comment -> Split ci -> Generate paragraph
    """
    c = re.sub(r'<([^<^b]+)>', r"<sup title='\1'></sup>", content)
    c = c.replace('%', "&nbsp;&nbsp;")
    c = markdown2.markdown(c)
    return c


def format_year(year):
    """将数字表示的年转换成中文"""
    return str(year).replace('-', '前') + "年"


def format_text(text):
    """将文本中的换行符替换为div"""
    return text.replace('\n', "<div class='text-gap'></div>")


def is_work_collected(work):
    """判断当前用户是否收藏此作品，如果未登录，则返回False"""
    if 'user_id' not in session:
        return False
    return CollectWork.query.filter(CollectWork.work_id == work.id).filter(
        CollectWork.user_id == session['user_id']).count() > 0


def is_work_image_collected(work_image):
    """判断当前用户是否收藏此作品图片，如果未登录，则返回False"""
    if 'user_id' not in session:
        return False
    return CollectWorkImage.query.filter(CollectWorkImage.user_id == session['user_id']).filter(
        CollectWorkImage.work_image_id == work_image.id).count() > 0