#-*- coding: UTF-8 -*-

import datetime, time
import re

from flask import url_for

from xichuangzhu.models.user_model import User
from xichuangzhu.models.topic_model import Topic
from xichuangzhu.models.review_model import Review

# count the time diff by timedelta, return a user-friendly format
# dt must be format as 2013-4-1 14:25:10
def time_diff(dt):
	dt = datetime.datetime.strptime(str(dt), "%Y-%m-%d %H:%M:%S")
	today = datetime.datetime.today()
	s = int((today - dt).total_seconds())

	# if day_diff > 365, use year
	if s/3600/24 >= 365:
		return str(s/3600/24/365) + " 年前"
	# elif day_diff > 30, use month
	elif s/3600/24 >= 30:
		return str(s/3600/24/30) + " 个月前"
	# elif hour_diff > 24, use day
	elif s/3600 >= 24:
		return str(s/3600/24) + " 天前"
	# elif minite_diff > 60, use hour
	elif s/60 > 60:
		return str(s/3600) + " 小时前"
	# elif second_diff > 60, use minite
	elif s > 60:
		return str(s/60) + " 分钟前"
	# else use "just now"
	else:
		return "刚刚"

# clean work content for displayment
def content_clean(content):
	c = re.sub(r'<([^<]+)>', '', content)
	c = c.replace('%', '')
	c  = c.replace('（一）', "")
	return c

def get_comment_replyee_id(comment):
	replyee_id = -1
	header = comment.split(' ')[0]
	if header.find('@') == 0:
		if User.check_exist_by_name(header.lstrip('@')):
			replyee_name = header.lstrip('@')
			replyee_id = User.get_id_by_name(replyee_name)
	return replyee_id

# inject <a> tag to @user in the comment
def rebuild_comment(comment, replyee_id):
	replyee_name = User.get_name_by_id(replyee_id)
	replyee_abbr = User.get_abbr_by_id(replyee_id)
	comment = "@" + "<a href=" + url_for('people', user_abbr=replyee_abbr + ">" + replyee_name + "</a>") + "&nbsp;&nbsp;" + comment.split(' ')[1]
	return comment

def build_topic_inform_title(replyer_id, topic_id):
	replyer = User.get_user_by_id(replyer_id)
	topic = Topic.get_topic(topic_id)
	inform_title = "<a href=" + url_for('people', user_abbr=replyer['Abbr']) + ">" + replyer['Name'] + "</a>&nbsp;&nbsp;在话题&nbsp;&nbsp;" + "<a href=" + url_for('single_topic', topic_id=topic_id) + ">" + topic['Title'] + "</a>" + "&nbsp;&nbsp;中回复了你"
	return inform_title

def build_review_inform_title(replyer_id, review_id):
	replyer = User.get_user_by_id(replyer_id)
	review = Review.get_review(review_id)
	inform_title = "<a href=" + url_for('people', user_abbr=replyer['Abbr']) + ">" + replyer['Name'] + "</a>&nbsp;&nbsp;在评论&nbsp;&nbsp;" + "<a href=" + url_for('single_review', review_id=review_id) + ">" + review['Title'] + "</a>" + "&nbsp;&nbsp;中回复了你"
	return inform_title