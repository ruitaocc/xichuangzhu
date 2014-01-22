# coding: utf-8
from __future__ import division
from flask import render_template, request, redirect, url_for, json, Blueprint, abort, g
from ..models import db, Work, WorkType, WorkTag, WorkImage, WorkReview, Tag, Dynasty, Author, \
    User, CollectWork, CollectWorkImage, WorkReviewComment
from ..utils import check_is_me
from ..permissions import user_permission, admin_permission, WorkImageOwnerPermission, \
    WorkReviewOwnerPermission
from ..forms import WorkImageForm, WorkReviewCommentForm, WorkReviewForm, WorkForm
from ..utils import random_filename
from ..uploadsets import workimages

bp = Blueprint('work', __name__)


@bp.route('/<int:work_id>')
def view(work_id):
    """文学作品"""
    work = Work.query.get_or_404(work_id)
    query = work.reviews.filter(WorkReview.is_publish == True)
    reviews = query.limit(4)
    reviews_num = query.count()
    images = work.images.limit(16)
    other_works = Work.query.filter(Work.author_id == work.author_id).filter(
        Work.id != work_id).limit(5)
    collectors = User.query.join(CollectWork).join(Work).filter(Work.id == work_id).limit(4)
    return render_template('work/work.html', work=work, reviews=reviews, reviews_num=reviews_num,
                           images=images, collectors=collectors, other_works=other_works)


@bp.route('/<int:work_id>/collect', methods=['GET'])
@user_permission
def collect(work_id):
    """收藏作品"""
    collect = CollectWork(user_id=g.user.id, work_id=work_id)
    db.session.add(collect)
    db.session.commit()
    return redirect(url_for('.view', work_id=work_id))


@bp.route('/<int:work_id>/discollect')
@user_permission
def discollect(work_id):
    """取消收藏文学作品"""
    db.session.query(CollectWork).filter(CollectWork.user_id == g.user.id).filter(
        CollectWork.work_id == work_id).delete()
    db.session.commit()
    return redirect(url_for('.view', work_id=work_id))


@bp.route('/', defaults={'page': 1})
@bp.route('/page/<int:page>')
def works(page):
    """全部文学作品"""
    work_type = request.args.get('type', 'all')
    dynasty_abbr = request.args.get('dynasty', 'all')
    works = Work.query
    if work_type != 'all':
        works = works.filter(Work.type.has(WorkType.en == work_type))
    if dynasty_abbr != 'all':
        works = works.filter(Work.author.has(Author.dynasty.has(Dynasty.abbr == dynasty_abbr)))
    paginator = works.paginate(page, 10)
    work_types = WorkType.query
    dynasties = Dynasty.query.order_by(Dynasty.start_year.asc())
    return render_template('work/works.html', paginator=paginator, work_type=work_type,
                           dynasty_abbr=dynasty_abbr, work_types=work_types, dynasties=dynasties)


@bp.route('/tags')
def tags():
    """作品标签页"""
    tags = Tag.query
    return render_template('work/tags.html', tags=tags)


@bp.route('/tag/<int:tag_id>', defaults={'page': 1})
@bp.route('/tag/<int:tag_id>/page/<int:page>')
def tag(tag_id, page):
    """作品标签"""
    tag = Tag.query.get_or_404(tag_id)
    paginator = Work.query.filter(Work.tags.any(WorkTag.tag_id == tag_id)).paginate(page, 12)
    return render_template('work/tag.html', tag=tag, paginator=paginator)


@bp.route('/add', methods=['GET', 'POST'])
@admin_permission
def add():
    """添加作品"""
    form = WorkForm(author_id=request.args.get('author_id', None))
    form.author_id.choices = [(a.id, '〔%s〕%s' % (a.dynasty.name, a.name)) for a in Author.query]
    form.type_id.choices = [(t.id, t.cn) for t in WorkType.query]
    if form.validate_on_submit():
        work = Work(**form.data)
        db.session.add(work)
        db.session.commit()
        return redirect(url_for('.view', work_id=work.id))
    return render_template('work/add.html', form=form)


@bp.route('/<int:work_id>/edit', methods=['GET', 'POST'])
@admin_permission
def edit(work_id):
    """编辑作品"""
    work = Work.query.get_or_404(work_id)
    form = WorkForm(obj=work)
    form.author_id.choices = [(a.id, '〔%s〕%s' % (a.dynasty.name, a.name)) for a in Author.query]
    form.type_id.choices = [(t.id, t.cn) for t in WorkType.query]
    if form.validate_on_submit():
        form.populate_obj(work)
        db.session.add(work)
        db.session.commit()
        return redirect(url_for('.view', work_id=work_id))
    return render_template('work/edit.html', work=work, form=form)


@bp.route('/<int:work_id>/reviews', defaults={'page': 1})
@bp.route('/<int:work_id>/reviews/page/<int:page>')
def reviews(work_id, page):
    """作品点评"""
    work = Work.query.get_or_404(work_id)
    paginator = work.reviews.filter(WorkReview.is_publish == True).order_by(
        WorkReview.create_time.desc()).paginate(page, 10)
    return render_template('work/reviews.html', work=work, paginator=paginator)


@bp.route('/<int:work_id>/images', defaults={'page': 1})
@bp.route('/<int:work_id>/images/page/<int:page>')
def images(work_id, page):
    """作品图片"""
    work = Work.query.get_or_404(work_id)
    paginator = work.images.order_by(WorkImage.create_time.desc()).paginate(page, 16)
    return render_template('work/images.html', work=work, paginator=paginator)


@bp.route('/search_authors', methods=['POST'])
@admin_permission
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
    return render_template('work/image.html', work_image=work_image)


@bp.route('/<int:work_id>/add_image', methods=['GET', 'POST'])
@user_permission
def add_image(work_id):
    """添加作品图片"""
    work = Work.query.get_or_404(work_id)
    form = WorkImageForm()
    if form.validate_on_submit():
        # Save image
        filename = workimages.save(request.files['image'], name=random_filename() + ".")
        work_image = WorkImage(work_id=work_id, user_id=g.user.id, filename=filename)
        db.session.add(work_image)
        db.session.commit()
        return redirect(url_for('.image', work_image_id=work_image.id))
    return render_template('work/add_image.html', work=work, form=form)


@bp.route('/image/<int:work_image_id>/edit', methods=['GET', 'POST'])
@user_permission
def edit_image(work_image_id):
    """编辑作品图片"""
    work_image = WorkImage.query.get_or_404(work_image_id)
    permission = WorkImageOwnerPermission(work_image_id)
    if not permission.check():
        return permission.deny()
    form = WorkImageForm()
    if form.validate_on_submit():
        filename = workimages.save(request.files['image'], name=random_filename() + ".")
        work_image.filename = filename
        db.session.add(work_image)
        db.session.commit()
        return redirect(url_for('.image', work_image_id=work_image_id))
    return render_template('work/edit_image.html', work_image=work_image, form=form)


@bp.route('/image/<int:work_image_id>/delete', methods=['GET'])
@user_permission
def delete_image(work_image_id):
    """删除作品图片"""
    work_image = WorkImage.query.get_or_404(work_image_id)
    permission = WorkImageOwnerPermission(work_image_id)
    if not permission.check():
        return permission.deny()
    db.session.delete(work_image)
    db.session.commit()
    return redirect(url_for('.view', work_id=work_image.work_id))


@bp.route('/image/<int:work_image_id>/collect', methods=['GET'])
@user_permission
def collect_image(work_image_id):
    """收藏作品图片"""
    collect = CollectWorkImage(user_id=g.user.id, work_image_id=work_image_id)
    db.session.add(collect)
    db.session.commit()
    return redirect(url_for('.image', work_image_id=work_image_id))


@bp.route('/image/<int:work_image_id>/discollect')
@user_permission
def discollect_image(work_image_id):
    """取消收藏作品图片"""
    db.session.query(CollectWorkImage).filter(CollectWorkImage.user_id == g.user.id).filter(
        CollectWorkImage.work_image_id == work_image_id).delete()
    db.session.commit()
    return redirect(url_for('.image', work_image_id=work_image_id))


@bp.route('/all_images', defaults={'page': 1})
@bp.route('/all_images/page/<int:page>')
def all_images(page):
    """所有作品图片"""
    paginator = WorkImage.query.paginate(page, 12)
    return render_template('work/all_images.html', paginator=paginator)


@bp.route('/review/<int:review_id>', methods=['GET', 'POST'])
def review(review_id):
    """作品点评"""
    form = WorkReviewCommentForm()
    review = WorkReview.query.get_or_404(review_id)
    # others cannot see draft
    if not review.is_publish and not check_is_me(review.user_id):
        abort(404)
    review.click_num += 1
    db.session.add(review)
    db.session.commit()
    if form.validate_on_submit():
        comment = WorkReviewComment(review_id=review_id, user_id=g.user.id, **form.data)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.review', review_id=review_id) + "#" + str(comment.id))
    return render_template('work/review.html', review=review, form=form)


@bp.route('/all_reviews', defaults={'page': 1})
@bp.route('/all_reviews/page/<int:page>')
def all_reviews(page):
    """最新作品点评"""
    paginator = WorkReview.query.filter(WorkReview.is_publish == True).order_by(
        WorkReview.create_time.desc()).paginate(page, 10)
    stmt = db.session.query(WorkReview.user_id, db.func.count(WorkReview.user_id).label(
        'reviews_num')).group_by(WorkReview.user_id).subquery()
    hot_reviewers = db.session.query(User).join(stmt, User.id == stmt.c.user_id).order_by(
        stmt.c.reviews_num)
    return render_template('work/all_reviews.html', paginator=paginator,
                           hot_reviewers=hot_reviewers)


@bp.route('/<int:work_id>/add_review', methods=['GET', 'POST'])
@user_permission
def add_review(work_id):
    """添加作品点评"""
    work = Work.query.get_or_404(work_id)
    form = WorkReviewForm()
    if form.validate_on_submit():
        is_publish = True if 'publish' in request.form else False
        review = WorkReview(user_id=g.user.id, work_id=work_id, is_publish=is_publish,
                            **form.data)
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('.review', review_id=review.id))
    return render_template('work/add_review.html', work=work, form=form)


@bp.route('/review/<int:review_id>/edit', methods=['GET', 'POST'])
@user_permission
def edit_review(review_id):
    """编辑作品点评"""
    review = WorkReview.query.get_or_404(review_id)
    permission = WorkReviewOwnerPermission(review_id)
    if not permission.check():
        return permission.deny()
    form = WorkReviewForm(obj=review)
    if form.validate_on_submit():
        form.populate_obj(review)
        review.is_publish = True if 'publish' in request.form else False
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('.review', review_id=review_id))
    return render_template('work/edit_review.html', review=review, form=form)


@bp.route('/review/<int:review_id>/delete')
@user_permission
def delete_review(review_id):
    """删除作品点评"""
    review = WorkReview.query.get_or_404(review_id)
    permission = WorkReviewOwnerPermission(review_id)
    if not permission.check():
        return permission.deny()
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('.view', work_id=review.work_id))