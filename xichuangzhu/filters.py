# coding: utf-8
import datetime
import re
import markdown2


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
    return year.replace('-', '前') + "年"