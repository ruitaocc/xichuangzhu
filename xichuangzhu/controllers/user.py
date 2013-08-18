#-*- coding: UTF-8 -*-
from __future__ import division
import urllib, urllib2
import smtplib
from email.mime.text import MIMEText
import hashlib
import math
from flask import render_template, request, redirect, url_for, json, session
from xichuangzhu import app
import config
from xichuangzhu.models.user_model import User
from xichuangzhu.models.collect_model import Collect
from xichuangzhu.models.review_model import Review
from xichuangzhu.models.inform_model import Inform
from xichuangzhu.models.topic_model import Topic
from xichuangzhu.models.work_model import Work
from xichuangzhu.utils import content_clean, time_diff, require_login, Pagination
from xichuangzhu.form import EmailForm

# page - user personal space
#--------------------------------------------------
@app.route('/u/<user_abbr>')
def user(user_abbr):
    user = User.get_user_by_abbr(user_abbr)
    is_me = True if "user_id" in session and session['user_id'] == user['UserID'] else False

    # reivews
    reviews = Review.get_reviews_by_user(user['UserID'], 1, 3, is_me)
    for r in reviews:
        r['Time'] = time_diff(r['Time'])
    reviews_num = Review.get_reviews_num_by_user(user['UserID'], is_me)

    # topics
    topics = Topic.get_topics_by_user(user['UserID'], 1, 3)
    for t in topics:
        t['Time'] = time_diff(t['Time'])
    topics_num = Topic.get_topics_num_by_user(user['UserID'])

    # handwritings
    work_images = Work.get_images_by_user(user['UserID'], 9)
    work_images_num = Work.get_images_num_by_user(user['UserID'])

    return render_template('user/user.html', user=user, reviews=reviews, reviews_num=reviews_num, topics=topics, topics_num=topics_num, work_images=work_images, work_images_num=work_images_num)

# page - user reviews
#--------------------------------------------------
@app.route('/u/<user_abbr>/reviews')
def user_reviews(user_abbr):
    user = User.get_user_by_abbr(user_abbr)
    is_me = True if "user_id" in session and session['user_id'] == user['UserID'] else False
    user_name = '我' if is_me else user['Name']

    page = int(request.args['page'] if 'page' in request.args else 1)
    per_page = 10

    reviews = Review.get_reviews_by_user(user['UserID'], page, per_page, is_me)
    for r in reviews:
        r['Time'] = time_diff(r['Time'])

    reviews_num = Review.get_reviews_num_by_user(user['UserID'], is_me)

    pagination = Pagination(page, per_page, reviews_num)

    return render_template('user/user_reviews.html', user=user, reviews=reviews, reviews_num=reviews_num, user_name=user_name, pagination=pagination)

# page - user topics
#--------------------------------------------------
@app.route('/u/<user_abbr>/topics')
def user_topics(user_abbr):
    user = User.get_user_by_abbr(user_abbr)
    user_name = '我' if "user_id" in session and session['user_id'] == user['UserID'] else user['Name']

    page = int(request.args['page'] if 'page' in request.args else 1)
    per_page = 10

    topics = Topic.get_topics_by_user(user['UserID'], page, per_page)
    for t in topics:
        t['Time'] = time_diff(t['Time'])

    topics_num = Topic.get_topics_num_by_user(user['UserID'])

    pagination = Pagination(page, per_page, topics_num)

    return render_template('user/user_topics.html', user=user, topics=topics, topics_num=topics_num, user_name=user_name, pagination=pagination)

# page - informs
#--------------------------------------------------
@app.route('/informs')
@require_login
def informs():  
    per_page = 10
    page = int(request.args['page'] if 'page' in request.args else 1)
    
    informs = Inform.get_informs(session['user_id'], page, per_page)
    for i in informs:
        i['Time'] = time_diff(i['Time'])

    informs_num = Inform.get_informs_num(session['user_id'])
    new_informs_num = Inform.get_new_informs_num(session['user_id'])

    pagination = Pagination(page, per_page, informs_num)
    
    Inform.update_check_inform_time(session['user_id'])

    return render_template('user/informs.html', informs=informs, new_informs_num=new_informs_num, pagination=pagination)

# page - user collects
#--------------------------------------------------
@app.route('/collects')
@require_login
def collects():
    collect_works = Collect.get_works_by_user(session['user_id'], 1, 6)
    for w in collect_works:
        w['Content'] = content_clean(w['Content'])
    collect_works_num = Collect.get_works_num_by_user(session['user_id'])
    return render_template('/user/collects.html', collect_works=collect_works, collect_works_num=collect_works_num)

# page - user's collect works
#--------------------------------------------------
@app.route('/collect_works')
@require_login
def collect_works():
    # pagination
    per_page = 10
    page = int(request.args['page'] if 'page' in request.args else 1)

    collect_works = Collect.get_works_by_user(session['user_id'], page, per_page)
    for w in collect_works:
        w['Content'] = content_clean(w['Content'])

    collect_works_num = Collect.get_works_num_by_user(session['user_id'])

    pagination = Pagination(page, per_page, collect_works_num)

    return render_template('user/collect_works.html', collect_works=collect_works, collect_works_num=collect_works_num, pagination=pagination)