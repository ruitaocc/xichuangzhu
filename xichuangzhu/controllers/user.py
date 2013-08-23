#-*- coding: UTF-8 -*-
from __future__ import division
import urllib, urllib2
import smtplib
from email.mime.text import MIMEText
import hashlib
import math
from flask import render_template, request, redirect, url_for, json, session
from xichuangzhu import app
from xichuangzhu import db
import config
from xichuangzhu.models.user_model import User
from xichuangzhu.models.collect_model import Collect
from xichuangzhu.models.collect import CollectWork, CollectWorkImage
from xichuangzhu.models.review_model import Review
from xichuangzhu.models.review_model import WorkReview
from xichuangzhu.models.work_image import WorkImage
from xichuangzhu.models.inform_model import Inform
from xichuangzhu.models.topic_model import Topic
from xichuangzhu.models.work_model import Work
from xichuangzhu.utils import require_login, Pagination
from xichuangzhu.form import EmailForm

def check_is_me(user_id):
    return True if "user_id" in session and session['user_id'] == user_id else False

# page - user personal space
#--------------------------------------------------
@app.route('/u/<user_abbr>')
def user(user_abbr):
    user = User.query.filter(User.abbr==user_abbr).first_or_404()

    query = WorkReview.query.filter(WorkReview.user_id==user.id).order_by(WorkReview.create_time)
    if check_is_me(user.id):
        work_reviews = query.limit(3)
        work_reviews_num =query.count()
    else:
        work_reviews = query.filter(WorkReview.is_publish==True).limit(3)
        work_reviews_num = query.filter(WorkReview.is_publish==True).count()

    topics = Topic.query.filter(Topic.user_id==user.id).order_by(Topic.create_time).limit(3)
    topics_num = Topic.query.filter(Topic.user_id==user.id).count()

    work_images = WorkImage.query.filter(WorkImage.user_id==user.id).order_by(WorkImage.create_time).limit(9)
    work_images_num = WorkImage.query.filter(WorkImage.user_id==user.id).count()

    return render_template('user/user.html', user=user, work_reviews=work_reviews, work_reviews_num=work_reviews_num, topics=topics, topics_num=topics_num, work_images=work_images, work_images_num=work_images_num)

# page - user reviews
#--------------------------------------------------
@app.route('/u/<user_abbr>/reviews')
def user_reviews(user_abbr):
    user = User.query.filter(User.abbr==user_abbr).first_or_404()

    page = int(request.args.get('page', 1))
    query = WorkReview.query.filter(WorkReview.user_id==user.id).order_by(WorkReview.create_time)
    if check_is_me(user.id):
        pagination = query.paginate(page, 10)
    else:
        pagination = query.filter(WorkReview.is_publish==True).paginate(page, 10)

    return render_template('user/reviews.html', user=user, pagination=pagination)

# page - user topics
#--------------------------------------------------
@app.route('/u/<user_abbr>/topics')
def user_topics(user_abbr):
    user = User.query.filter(User.abbr==user_abbr).first_or_404()

    page = int(request.args.get('page', 1))
    pagination = Topic.query.filter(Topic.user_id==user.id).order_by(Topic.create_time).paginate(page, 10)

    return render_template('user/topics.html', user=user, pagination=pagination)

# page - user work images
#--------------------------------------------------
@app.route('/u/<user_abbr>/work_images')
def user_work_images(user_abbr):
    user = User.query.filter(User.abbr==user_abbr).first_or_404()

    page = int(request.args.get('page', 1))
    pagination = WorkImage.query.filter(WorkImage.user_id==user.id).order_by(WorkImage.create_time).paginate(page, 10)

    return render_template('user/work_images.html', user=user, pagination=pagination)

# page - user collects
#--------------------------------------------------
@app.route('/collects')
@require_login
def collects():
    query = Work.query.join(CollectWork).filter(CollectWork.user_id==session['user_id']).order_by(CollectWork.create_time)
    collect_works = query.limit(6)
    collect_works_num = query.count()

    query = WorkImage.query.join(CollectWorkImage).filter(CollectWorkImage.user_id==session['user_id']).order_by(CollectWorkImage.create_time)
    collect_work_images = query.limit(9)
    collect_work_images_num = query.count()

    return render_template('/user/collects.html', collect_works=collect_works, collect_works_num=collect_works_num, collect_work_images=collect_work_images, collect_work_images_num=collect_work_images_num)

# page - user's collect works
#--------------------------------------------------
@app.route('/collect_works')
@require_login
def collect_works():
    page = int(request.args.get('page', 1))
    pagination = Work.query.join(CollectWork).filter(CollectWork.user_id==session['user_id']).order_by(CollectWork.create_time).paginate(page, 10)
    return render_template('user/collect_works.html', pagination=pagination)

# page - user's collect work images
#--------------------------------------------------
@app.route('/collect_work_images')
@require_login
def collect_work_images():
    page = int(request.args.get('page', 1))
    pagination = WorkImage.query.join(CollectWorkImage).filter(CollectWorkImage.user_id==session['user_id']).order_by(CollectWorkImage.create_time).paginate(page, 12)
    return render_template('user/collect_work_images.html', pagination=pagination)