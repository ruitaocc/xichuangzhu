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
from xichuangzhu.utils import content_clean, time_diff, require_login
from xichuangzhu.form import EmailForm


# page - user personal space
#--------------------------------------------------
@app.route('/u/<user_abbr>')
def user(user_abbr):
    user = User.get_user_by_abbr(user_abbr)
    is_me = True if "user_id" in session and session['user_id'] == user['UserID'] else False

    # works
    works = Collect.get_works_by_user(user['UserID'], 1, 3)
    for work in works:
        work['Content'] = content_clean(work['Content'])
    works_num = Collect.get_works_num_by_user(user['UserID'])

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

    return render_template('user/user.html', user=user, works=works, works_num=works_num, reviews=reviews, reviews_num=reviews_num, topics=topics, topics_num=topics_num)

# page - user's collect works
#--------------------------------------------------
@app.route('/u/<user_abbr>/collect/works')
def user_collect_works(user_abbr):
    user = User.get_user_by_abbr(user_abbr)
    user_name = '我' if "user_id" in session and session['user_id'] == user['UserID'] else user['Name']

    # pagination
    num_per_page = 10
    page = int(request.args['page'] if 'page' in request.args else 1)

    works = Collect.get_works_by_user(user['UserID'], page, num_per_page)
    for work in works:
        work['Content'] = content_clean(work['Content'])

    works_num = Collect.get_works_num_by_user(user['UserID'])

    # page paras
    total_page = int(math.ceil(works_num / num_per_page))
    pre_page = (page - 1) if page > 1 else 1
    if total_page == 0:
        next_page = 1
    elif page < total_page:
        next_page = page + 1
    else:
        next_page = total_page

    return render_template('user/user_collect_works.html', user=user, works=works, works_num=works_num, user_name=user_name, page=page, total_page=total_page, pre_page=pre_page, next_page=next_page)

# page - user reviews
#--------------------------------------------------
@app.route('/u/<user_abbr>/reviews')
def user_reviews(user_abbr):
    user = User.get_user_by_abbr(user_abbr)
    is_me = True if "user_id" in session and session['user_id'] == user['UserID'] else False
    user_name = '我' if is_me else user['Name']

    # pagination
    num_per_page = 10
    page = int(request.args['page'] if 'page' in request.args else 1)

    reviews = Review.get_reviews_by_user(user['UserID'], page, num_per_page, is_me)
    for r in reviews:
        r['Time'] = time_diff(r['Time'])
        
    reviews_num = Review.get_reviews_num_by_user(user['UserID'], is_me)

    # page paras
    total_page = int(math.ceil(reviews_num / num_per_page))
    pre_page = (page - 1) if page > 1 else 1
    if total_page == 0:
        next_page = 1
    elif page < total_page:
        next_page = page + 1
    else:
        next_page = total_page

    return render_template('user/user_reviews.html', user=user, reviews=reviews, reviews_num=reviews_num, user_name=user_name, page=page, total_page=total_page, pre_page=pre_page, next_page=next_page)

# page - user topics
#--------------------------------------------------
@app.route('/u/<user_abbr>/topics')
def user_topics(user_abbr):
    user = User.get_user_by_abbr(user_abbr)
    user_name = '我' if "user_id" in session and session['user_id'] == user['UserID'] else user['Name']

    # pagination
    num_per_page = 10
    page = int(request.args['page'] if 'page' in request.args else 1)

    topics = Topic.get_topics_by_user(user['UserID'], page, num_per_page)
    for t in topics:
        t['Time'] = time_diff(t['Time'])

    topics_num = Topic.get_topics_num_by_user(user['UserID'])

    # page paras
    total_page = int(math.ceil(topics_num / num_per_page))
    pre_page = (page - 1) if page > 1 else 1
    if total_page == 0:
        next_page = 1
    elif page < total_page:
        next_page = page + 1
    else:
        next_page = total_page

    return render_template('user/user_topics.html', user=user, topics=topics, topics_num=topics_num, user_name=user_name, page=page, total_page=total_page, pre_page=pre_page, next_page=next_page)

# page - informs
#--------------------------------------------------
@app.route('/informs')
@require_login
def informs():  
    # pagination
    num_per_page = 10
    page = int(request.args['page'] if 'page' in request.args else 1)
    
    informs = Inform.get_informs(session['user_id'], page, num_per_page)
    for i in informs:
        i['Time'] = time_diff(i['Time'])

    # page paras
    informs_num = Inform.get_informs_num(session['user_id'])
    #return str(informs_num)
    total_page = int(math.ceil(informs_num / num_per_page))
    pre_page   = (page - 1) if page > 1 else 1
    if total_page == 0:
        next_page = 1
    elif page < total_page:
        next_page = page + 1
    else:
        next_page = total_page

    new_informs_num = Inform.get_new_informs_num(session['user_id'])
    Inform.update_check_inform_time(session['user_id'])
    return render_template('user/informs.html', informs=informs, new_informs_num=new_informs_num, page=page, total_page=total_page, pre_page=pre_page, next_page=next_page)