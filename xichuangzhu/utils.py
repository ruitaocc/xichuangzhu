#-*- coding: UTF-8 -*-

import datetime, time
import re

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