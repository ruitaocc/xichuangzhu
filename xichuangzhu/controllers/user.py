# coding: utf-8
from __future__ import division
from flask import render_template, request, session
from xichuangzhu import app
from xichuangzhu.models.user import User
from xichuangzhu.models.collect import CollectWork, CollectWorkImage
from xichuangzhu.models.topic import Topic
from xichuangzhu.models.work import Work, WorkImage, WorkReview
from xichuangzhu.utils import require_login, check_is_me


@app.route('/u/<user_abbr>')
def user(user_abbr):
    """用户主页"""
    user = User.query.filter(User.abbr == user_abbr).first_or_404()

    query = user.work_reviews.order_by(WorkReview.create_time.desc())
    if check_is_me(user.id):
        work_reviews = query.limit(3)
        work_reviews_num = query.count()
    else:
        work_reviews = query.filter(WorkReview.is_publish == True).limit(3)
        work_reviews_num = query.filter(WorkReview.is_publish == True).count()

    topics = user.topics.order_by(Topic.create_time.desc()).limit(3)
    topics_num = user.topics.count()

    work_images = user.work_images.order_by(WorkImage.create_time.desc()).limit(16)
    work_images_num = user.work_images.count()

    return render_template('user/user.html', user=user, work_reviews=work_reviews, work_reviews_num=work_reviews_num,
                           topics=topics, topics_num=topics_num, work_images=work_images,
                           work_images_num=work_images_num)


@app.route('/u/<user_abbr>/work_reviews')
def user_work_reviews(user_abbr):
    """用户的作品点评"""
    user = User.query.filter(User.abbr == user_abbr).first_or_404()
    page = int(request.args.get('page', 1))
    query = user.work_reviews.order_by(WorkReview.create_time.desc())
    if check_is_me(user.id):
        pagination = query.paginate(page, 10)
    else:
        pagination = query.filter(WorkReview.is_publish == True).paginate(page, 10)
    return render_template('user/user_work_reviews.html', user=user, pagination=pagination)


@app.route('/u/<user_abbr>/topics')
def user_topics(user_abbr):
    """用户发表的话题"""
    user = User.query.filter(User.abbr == user_abbr).first_or_404()
    page = int(request.args.get('page', 1))
    pagination = user.topics.order_by(Topic.create_time.desc()).paginate(page, 10)
    return render_template('user/user_topics.html', user=user, pagination=pagination)


@app.route('/u/<user_abbr>/work_images')
def user_work_images(user_abbr):
    """用户上传的作品图片"""
    user = User.query.filter(User.abbr == user_abbr).first_or_404()
    page = int(request.args.get('page', 1))
    pagination = user.work_images.order_by(WorkImage.create_time.desc()).paginate(page, 16)
    return render_template('user/user_work_images.html', user=user, pagination=pagination)


@app.route('/my_collects')
@require_login
def my_collects():
    """用户收藏页"""
    user = User.query.get_or_404(session['user_id'])

    collect_works = Work.query.join(CollectWork).filter(CollectWork.user_id == user.id).order_by(
        CollectWork.create_time.desc()).limit(12)
    collect_works_num = user.collect_works.count()

    collect_work_images = WorkImage.query.join(CollectWorkImage).filter(CollectWorkImage.user_id == user.id).order_by(
        CollectWorkImage.create_time.desc()).limit(9)
    collect_work_images_num = user.collect_work_images.count()

    return render_template('user/my_collects.html', collect_works=collect_works, collect_works_num=collect_works_num,
                           collect_work_images=collect_work_images, collect_work_images_num=collect_work_images_num)


@app.route('/my_collect_works')
@require_login
def my_collect_works():
    """用户收藏的文学作品"""
    page = int(request.args.get('page', 1))
    pagination = Work.query.join(CollectWork).filter(CollectWork.user_id == session['user_id']).order_by(
        CollectWork.create_time.desc()).paginate(page, 10)
    return render_template('user/my_collect_works.html', pagination=pagination)


@app.route('/collect_work_images')
@require_login
def my_collect_work_images():
    """用户收藏的图片"""
    page = int(request.args.get('page', 1))
    pagination = WorkImage.query.join(CollectWorkImage).filter(CollectWorkImage.user_id == session['user_id']).order_by(
        CollectWorkImage.create_time.desc()).paginate(page, 12)
    return render_template('user/my_collect_work_images.html', pagination=pagination)