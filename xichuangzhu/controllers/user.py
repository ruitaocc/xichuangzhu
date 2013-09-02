#-*- coding: UTF-8 -*-
from __future__ import division
import urllib, urllib2
import smtplib
from email.mime.text import MIMEText
import hashlib
import math
from flask import render_template, request, redirect, url_for, json, session
from xichuangzhu import app, db, config
from xichuangzhu.models.user_model import User
from xichuangzhu.models.collect_model import CollectWork, CollectWorkImage
from xichuangzhu.models.topic_model import Topic
from xichuangzhu.models.work_model import Work, WorkImage, WorkReview
from xichuangzhu.utils import require_login, check_is_me
from xichuangzhu.form import EmailForm

# page - user personal space
#--------------------------------------------------
@app.route('/u/<user_abbr>')
def user(user_abbr):
    user = User.query.filter(User.abbr==user_abbr).first_or_404()

    query = user.reviews.order_by(WorkReview.create_time.desc())
    if check_is_me(user.id):
        work_reviews = query.limit(3)
        work_reviews_num =query.count()
    else:
        work_reviews = query.filter(WorkReview.is_publish==True).limit(3)
        work_reviews_num = query.filter(WorkReview.is_publish==True).count()

    topics = user.topics.order_by(Topic.create_time.desc()).limit(3)
    topics_num = user.topics.count()

    work_images = user.work_images.order_by(WorkImage.create_time.desc()).limit(9)
    work_images_num = user.work_images.count()

    return render_template('user/user.html', user=user, work_reviews=work_reviews, work_reviews_num=work_reviews_num, topics=topics, topics_num=topics_num, work_images=work_images, work_images_num=work_images_num)

# page - user reviews
#--------------------------------------------------
@app.route('/u/<user_abbr>/reviews')
def user_reviews(user_abbr):
    user = User.query.filter(User.abbr==user_abbr).first_or_404()

    page = int(request.args.get('page', 1))
    query = user.reviews.order_by(WorkReview.create_time.desc())
    if check_is_me(user.id):
        pagination = query.paginate(page, 10)
    else:
        pagination = query.filter(WorkReview.is_publish==True).paginate(page, 10)

    return render_template('user/user_reviews.html', user=user, pagination=pagination)

# page - user topics
#--------------------------------------------------
@app.route('/u/<user_abbr>/topics')
def user_topics(user_abbr):
    user = User.query.filter(User.abbr==user_abbr).first_or_404()

    page = int(request.args.get('page', 1))
    pagination = user.topics.order_by(Topic.create_time.desc()).paginate(page, 10)

    return render_template('user/user_topics.html', user=user, pagination=pagination)

# page - user work images
#--------------------------------------------------
@app.route('/u/<user_abbr>/work_images')
def user_work_images(user_abbr):
    user = User.query.filter(User.abbr==user_abbr).first_or_404()

    page = int(request.args.get('page', 1))
    pagination = user.work_images.order_by(WorkImage.create_time.desc()).paginate(page, 10)

    return render_template('user/user_work_images.html', user=user, pagination=pagination)

# page - user collects
#--------------------------------------------------
@app.route('/my_collects')
@require_login
def my_collects():
    user = User.query.get_or_404(session['user_id'])

    collect_works = Work.query.join(CollectWork).filter(CollectWork.user_id==user.id).order_by(CollectWork.create_time.desc()).limit(6)
    collect_works_num = user.collect_works.count()

    collect_work_images = WorkImage.query.join(CollectWorkImage).filter(CollectWorkImage.user_id==user.id).order_by(CollectWorkImage.create_time.desc()).limit(9)
    collect_work_images_num = user.collect_work_images.count()

    return render_template('/user/my_collects.html', collect_works=collect_works, collect_works_num=collect_works_num, collect_work_images=collect_work_images, collect_work_images_num=collect_work_images_num)

# page - user's collect works
#--------------------------------------------------
@app.route('/my_collect_works')
@require_login
def my_collect_works():
    page = int(request.args.get('page', 1))
    pagination = Work.query.join(CollectWork).filter(CollectWork.user_id==session['user_id']).order_by(CollectWork.create_time.desc()).paginate(page, 10)
    return render_template('user/my_collect_works.html', pagination=pagination)

# page - user's collect work images
#--------------------------------------------------
@app.route('/collect_work_images')
@require_login
def my_collect_work_images():
    page = int(request.args.get('page', 1))
    pagination = WorkImage.query.join(CollectWorkImage).filter(CollectWorkImage.user_id==session['user_id']).order_by(CollectWorkImage.create_time.desc()).paginate(page, 12)
    return render_template('user/my_collect_work_images.html', pagination=pagination)