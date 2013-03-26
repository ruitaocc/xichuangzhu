#-*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, json, session

from xichuangzhu import app

import config

from xichuangzhu.models.user_model import User
from xichuangzhu.models.love_work_model import Love_Work
from xichuangzhu.models.review_model import Review

import urllib, urllib2

import smtplib
from email.mime.text import MIMEText

import hashlib

import re

# proc - login by douban's oauth2.0
@app.route('/login/douban')
def auth():
	code = request.args['code']

	# get access token and userID
	url = "https://www.douban.com/service/auth2/token"
	data = {
		'client_id': config.DOUBAN_CLIENT_ID,
		'client_secret': config.DOUBAN_SECRET,
		'redirect_uri': config.DOUBAN_REDIRECT_URI,
		'grant_type': 'authorization_code',
		'code': code
	}
	data = urllib.urlencode(data)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	info = eval(response.read())
	user_id = int(info['douban_user_id'])

	# if user exist
	if User.check_user_exist(user_id):
		# if user unactive
		if not User.check_user_active(user_id):
			return redirect(url_for('verify_email_callback', state='unactive', user_id=user_id))
		else:
			# set session
			session['user_id'] = user_id
			session['user_name'] = User.get_name(user_id)
			session['user_abbr'] = User.get_abbr(user_id)
			return redirect(url_for('index'))
	# if not exist
	else:
		# get user info
		url = "https://api.douban.com/v2/user/" + str(user_id)
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		user_info = eval(response.read().replace('\\', ''))	# remove '\' and convert str to dict

		# add user
		user_id     = int(user_info['id'])
		user_name   = user_info['name']
		abbr   = user_info['uid']
		avatar      = user_info['avatar']
		signature   = user_info['signature']
		desc        = user_info['desc']
		location_id = int(user_info['loc_id'])
		location    = user_info['loc_name']
		User.add_user(user_id, user_name, abbr, avatar, signature, desc, location_id, location)

		# go to the verify email page
		return redirect(url_for('send_verify_email', user_id=user_id))

# page - send verify email
@app.route('/send_verify_email/douban', methods=['GET', 'POST'])
def send_verify_email():
	if request.method == 'GET':
		user_id = int(request.args['user_id'])
		user_name = User.get_name(user_id)
		return render_template('send_verify_email.html', user_id=user_id, user_name=user_name)
	elif request.method == 'POST':
		# email
		t_addr = request.form['email']

		# user info
		user_id = int(request.form['user_id'])
		user_name = User.get_name(user_id)

		# add this email to user
		User.add_email(user_id, t_addr)

		# gene verify url
		verify_code = hashlib.sha1(user_name).hexdigest()
		verify_url = config.SITE_DOMAIN + "verify_email/douban/" + str(user_id) + "/" + verify_code

		# prepare email content
		msgText = '''<html>
			<h1>点击下面的链接，激活你在西窗烛的帐号：</h1>
			<a href='%s'>%s</a>
			</html>''' % (verify_url, verify_url)
		msg = MIMEText(msgText, 'html', 'utf-8')
		msg['From'] = "西窗烛 <" + config.SMTP_FROM + ">"
		msg['To'] = user_name + "<" + t_addr + ">"
		msg['Subject'] = "欢迎来到西窗烛！"

		# send email
		s = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
		s.login(config.SMTP_USER, config.SMTP_PASSWORD)
		s.sendmail(config.SMTP_FROM, t_addr, msg.as_string())

		return redirect(url_for('verify_email_callback', state='send_succ'))

# proc - verify the code and active user
@app.route('/verify_email/douban/<int:user_id>/<verify_code>')
def verify_email(user_id, verify_code):
	user_name = User.get_name(user_id)
	user_abbr = User.get_abbr(user_id)
	if verify_code == hashlib.sha1(user_name).hexdigest():
		User.active_user(user_id)
		session['user_id'] = user_id
		session['user_name'] = user_name
		session['user_abbr'] = user_abbr
		return redirect(url_for('verify_email_callback', state='active_succ'))
	else:
		return redirect(url_for('verify_email_callback', state='active_failed'))

# page - show the state of verify
@app.route('/verify_email_callback/douban/')
def verify_email_callback():
	state = request.args['state']
	user_id = int(request.args['user_id']) if 'user_id' in request.args else 0
	return render_template('verify_email_callback.html', state=state, user_id=user_id)

# proc - logout
@app.route('/logout')
def logout():
	session.pop('user_id', None)
	session.pop('user_name', None)
	return redirect(url_for('index'))

# page - personal page
@app.route('/people/<user_abbr>')
def people(user_abbr):
	people = User.get_people_by_abbr(user_abbr)

	works = Love_Work.get_works_by_user_love(people['UserID'], 3)
	for work in works:
		work['Content'] = re.sub(r'<([^<]+)>', '', work['Content'])
		work['Content'] = work['Content'].replace('%', '')
		work['Content'] = work['Content'].replace('（一）', "")

	reviews = Review.get_reviews_by_user(people['UserID'], 3)

	if "user_id" in session and session['user_id'] == people['UserID']:
		title_name = '我'
	else:
		title_name = people['Name']
	return render_template('people.html', people=people, works=works, reviews=reviews, title_name=title_name)
