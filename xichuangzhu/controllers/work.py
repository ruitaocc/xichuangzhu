# coding: utf-8
from __future__ import division
import os
import uuid
import cgi
from flask import render_template, request, redirect, url_for, json, session, Blueprint, abort
from xichuangzhu import config
from ..models import db, Work, WorkType, WorkTag, WorkImage, WorkReview, Tag, Dynasty, Author, User, CollectWork,\
    CollectWorkImage, WorkReviewComment
from ..utils import require_login, require_admin
from ..forms import WorkImageForm, CommentForm, WorkReviewForm

bp = Blueprint('work', __name__)


@bp.route('/<int:work_id>')
def view(work_id):
    """文学作品"""
    work = Work.query.get_or_404(work_id)

    if 'user_id' in session:
        is_collected = CollectWork.query.filter(CollectWork.work_id == work_id).filter(
            CollectWork.user_id == session['user_id']).count() > 0
    else:
        is_collected = False

    reviews = work.reviews.order_by(WorkReview.create_time.desc()).filter(WorkReview.is_publish == True).limit(4)
    reviews_num = work.reviews.filter(WorkReview.is_publish == True).count()

    images = work.images.order_by(WorkImage.create_time).limit(16)
    images_num = work.images.count()

    other_works = Work.query.filter(Work.author_id == work.author_id).filter(Work.id != work_id).limit(5)

    collectors = User.query.join(CollectWork).join(Work).filter(Work.id == work_id).limit(4)

    return render_template('work/work.html', work=work, reviews=reviews, reviews_num=reviews_num, images=images,
                           images_num=images_num, collectors=collectors, is_collected=is_collected,
                           other_works=other_works)


@bp.route('/<int:work_id>/collect', methods=['GET'])
@require_login
def collect(work_id):
    """收藏作品"""
    collect = CollectWork(user_id=session['user_id'], work_id=work_id)
    db.session.add(collect)
    db.session.commit()
    return redirect(url_for('.view', work_id=work_id))


@bp.route('/<int:work_id>/discollect')
@require_login
def discollect(work_id):
    """取消收藏文学作品"""
    db.session.query(CollectWork).filter(CollectWork.user_id == session['user_id']).filter(
        CollectWork.work_id == work_id).delete()
    db.session.commit()
    return redirect(url_for('.view', work_id=work_id))


@bp.route('/')
def works():
    """全部文学作品"""
    work_type = request.args.get('type', 'all')
    dynasty_abbr = request.args.get('dynasty', 'all')
    page = int(float(request.args.get('page', 1)))
    works = Work.query
    if work_type != 'all':
        works = works.filter(Work.type.has(WorkType.en == work_type))
    if dynasty_abbr != 'all':
        works = works.filter(Work.author.has(Author.dynasty.has(Dynasty.abbr == dynasty_abbr)))
    paginator = works.paginate(page, 10)
    work_types = WorkType.query
    dynasties = Dynasty.query.order_by(Dynasty.start_year)
    return render_template('work/works.html', paginator=paginator, work_type=work_type, dynasty_abbr=dynasty_abbr,
                           work_types=work_types, dynasties=dynasties)


@bp.route('/tags')
def tags():
    """作品标签页"""
    tags = Tag.query
    return render_template('work/tags.html', tags=tags)


@bp.route('/tag/<int:tag_id>')
def tag(tag_id):
    """作品标签"""
    tag = Tag.query.get_or_404(tag_id)
    page = int(request.args.get('page', 1))
    paginator = Work.query.filter(Work.tags.any(WorkTag.tag_id == tag_id)).paginate(page, 12)
    return render_template('work/tag.html', tag=tag, paginator=paginator)


@bp.route('/add', methods=['GET', 'POST'])
@require_admin
def add():
    """添加作品"""
    if request.method == 'GET':
        if 'author_id' in request.args:
            author = Author.query.get_or_404(request.args['author_id'])
        else:
            author = None
        work_types = WorkType.query
        return render_template('work/add.html', work_types=work_types, author=author)
    work = Work(title=request.form['title'], content=request.form['content'], foreword=request.form['foreword'],
                intro=request.form['intro'], author_id=int(request.form['author_id']),
                type_id=request.form['type_id'])
    db.session.add(work)
    db.session.commit()
    return redirect(url_for('.view', work_id=work.id))


@bp.route('/<int:work_id>/edit', methods=['GET', 'POST'])
@require_admin
def edit(work_id):
    """编辑作品"""
    work = Work.query.get_or_404(work_id)
    if request.method == 'GET':
        work_types = WorkType.query
        return render_template('work/edit.html', work=work, work_types=work_types)
    else:
        work.title = request.form['title']
        work.content = request.form['content']
        work.foreword = request.form['foreword']
        work.intro = request.form['intro']
        work.author_id = int(request.form['author_id'])
        work.type_id = request.form['type_id']
        db.session.add(work)
        db.session.commit()
        return redirect(url_for('.view', work_id=work_id))


@bp.route('/<int:work_id>/reviews')
def reviews(work_id):
    """作品点评"""
    work = Work.query.get_or_404(work_id)
    page = int(request.args.get('page', 1))
    paginator = work.reviews.filter(WorkReview.is_publish == True).order_by(WorkReview.create_time.desc()).paginate(
        page, 10)
    return render_template('work/reviews.html', work=work, paginator=paginator)


@bp.route('/<int:work_id>/images', methods=['GET'])
def images(work_id):
    """作品图片"""
    work = Work.query.get_or_404(work_id)
    page = int(request.args.get('page', 1))
    paginator = work.images.order_by(WorkImage.create_time.desc()).paginate(page, 16)
    return render_template('work/images.html', work=work, paginator=paginator)


@bp.route('/search_authors', methods=['POST'])
@require_admin
def search_authors():
    """根据关键字返回json格式的作者信息"""
    author_name = request.form.get('author_name', '')
    authors = Author.query.filter(Author.name.like('%%%s%%' % author_name))
    dict_authors = []
    for a in authors:
        dict_authors.append({'id': a.id, 'dynasty': a.dynasty.name, 'name': a.name})
    return json.dumps(dict_authors)


@bp.route('/image/<int:work_image_id>', methods=['GET'])
def image(work_image_id):
    """作品的单个相关图片"""
    work_image = WorkImage.query.get_or_404(work_image_id)
    if 'user_id' in session:
        is_collected = CollectWorkImage.query.filter(CollectWorkImage.user_id == session['user_id']).filter(
            CollectWorkImage.work_image_id == work_image_id).count() > 0
    else:
        is_collected = False
    return render_template('work/image.html', work_image=work_image, is_collected=is_collected)


@bp.route('/image/<int:work_image_id>/delete', methods=['GET'])
@require_login
def delete_image(work_image_id):
    """删除作品的相关图片"""
    work_image = WorkImage.query.get_or_404(work_image_id)
    if work_image.user_id != session['user_id']:
        abort(404)
        # delete image file
    if os.path.isfile(config.IMAGE_PATH + work_image.filename):
        os.remove(config.IMAGE_PATH + work_image.filename)
    db.session.delete(work_image)
    db.session.commit()
    return redirect(url_for('.view', work_id=work_image.work_id))


@bp.route('/image/<int:work_image_id>/collect', methods=['GET'])
@require_login
def collect_image(work_image_id):
    """收藏作品图片"""
    collect = CollectWorkImage(user_id=session['user_id'], work_image_id=work_image_id)
    db.session.add(collect)
    db.session.commit()
    return redirect(url_for('.image', work_image_id=work_image_id))


@bp.route('/image/<int:work_image_id>/discollect', methods=['GET'])
@require_login
def discollect_image(work_image_id):
    """取消收藏作品图片"""
    db.session.query(CollectWorkImage).filter(CollectWorkImage.user_id == session['user_id']).filter(
        CollectWorkImage.work_image_id == work_image_id).delete()
    db.session.commit()
    return redirect(url_for('.image', work_image_id=work_image_id))


@bp.route('/all_images', methods=['GET'])
def all_images():
    """所有作品图片"""
    page = int(request.args.get('page', 1))
    paginator = WorkImage.query.paginate(page, 12)
    return render_template('work/all_images.html', paginator=paginator)


@bp.route('/<int:work_id>/add_image', methods=['GET', 'POST'])
@require_login
def add_image(work_id):
    """为作品添加相关图片"""
    work = Work.query.get_or_404(work_id)
    form = WorkImageForm()
    if form.validate_on_submit():
        # Save image
        image = request.files['image']
        image_filename = str(uuid.uuid1()) + '.' + image.filename.split('.')[-1]
        image.save(config.IMAGE_PATH + image_filename)

        work_image = WorkImage(work_id=work_id, user_id=session['user_id'], url=config.IMAGE_URL + image_filename,
                               filename=image_filename)
        db.session.add(work_image)
        db.session.commit()
        return redirect(url_for('.image', work_image_id=work_image.id))
    return render_template('work/add_image.html', work=work, form=form)


@bp.route('/image/<int:work_image_id>/edit', methods=['GET', 'POST'])
@require_login
def edit_image(work_image_id):
    """编辑作品图片"""
    work_image = WorkImage.query.get_or_404(work_image_id)
    form = WorkImageForm()
    if form.validate_on_submit():
        # Delete old image
        if os.path.isfile(config.IMAGE_PATH + work_image.filename):
            os.remove(config.IMAGE_PATH + work_image.filename)

        # Save new image
        image = request.files['image']
        image_filename = str(uuid.uuid1()) + '.' + image.filename.split('.')[-1]
        image.save(config.IMAGE_PATH + image_filename)

        # update image info
        work_image.url = config.IMAGE_URL + image_filename
        work_image.filename = image_filename
        db.session.add(work_image)
        db.session.commit()
        return redirect(url_for('.image', work_image_id=work_image_id))
    return render_template('work/edit_image.html', work_image=work_image, form=form)


@bp.route('/review/<int:review_id>', methods=['GET', 'POST'])
def review(review_id):
    """作品点评"""
    form = CommentForm()
    review = WorkReview.query.get_or_404(review_id)
    # others cannot see draft
    is_me = True if "user_id" in session and session['user_id'] == review.user_id else False
    if not is_me and not review.is_publish:
        abort(404)
    review.click_num += 1
    db.session.add(review)
    db.session.commit()
    if form.validate_on_submit():
        comment = WorkReviewComment(content=cgi.escape(form.content.data), review_id=review_id,
                                    user_id=session['user_id'])
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.review', review_id=review_id) + "#" + str(comment.id))
    return render_template('work/review.html', review=review, form=form)


@bp.route('/all_reviews')
def all_reviews():
    """最新作品点评"""
    page = int(request.args.get('page', 1))
    paginator = WorkReview.query.filter(WorkReview.is_publish == True).order_by(
        WorkReview.create_time.desc()).paginate(page, 10)
    stmt = db.session.query(WorkReview.user_id, db.func.count(WorkReview.user_id).label('reviews_num')).group_by(
        WorkReview.user_id).subquery()
    hot_reviewers = db.session.query(User).join(stmt, User.id == stmt.c.user_id).order_by(stmt.c.reviews_num)
    return render_template('work/all_reviews.html', paginator=paginator, hot_reviewers=hot_reviewers)


@bp.route('/<int:work_id>/add_review', methods=['GET', 'POST'])
@require_login
def add_review(work_id):
    """添加作品点评"""
    work = Work.query.get_or_404(work_id)
    form = WorkReviewForm()
    if form.validate_on_submit():
        is_publish = True if 'publish' in request.form else False
        review = WorkReview(title=cgi.escape(form.title.data), content=cgi.escape(form.content.data),
                            user_id=session['user_id'], work_id=work_id, is_publish=is_publish)
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('.review', review_id=review.id))
    return render_template('work/add_review.html', work=work, form=form)


@bp.route('/review/<int:review_id>/edit', methods=['GET', 'POST'])
@require_login
def edit_review(review_id):
    """编辑作品点评"""
    review = WorkReview.query.get_or_404(review_id)
    if review.user_id != session['user_id']:
        abort(404)
    form = WorkReviewForm(obj=review)
    if form.validate_on_submit():
        review.title = cgi.escape(form.title.data)
        review.content = cgi.escape(form.content.data)
        review.is_publish = True if 'publish' in request.form else False
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('.review', review_id=review_id))
    return render_template('work/edit_review.html', review=review, form=form)


@bp.route('/review/<int:review_id>/delete')
@require_login
def delete_review(review_id):
    """删除作品点评"""
    review = WorkReview.query.get_or_404(review_id)
    if review.user_id != session['user_id']:
        abort(404)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('.view', work_id=review.work_id))