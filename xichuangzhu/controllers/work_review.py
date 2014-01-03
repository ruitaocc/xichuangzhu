# coding: utf-8
from __future__ import division
import cgi
from flask import render_template, request, redirect, url_for, session, abort
from xichuangzhu import app, db
from xichuangzhu.models.work import Work, WorkReview, WorkReviewComment
from xichuangzhu.models.user import User
from xichuangzhu.form import ReviewForm, CommentForm
from xichuangzhu.utils import require_login


@app.route('/work_review/<int:review_id>')
def work_review(review_id):
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
    return render_template('work_review/work_review.html', review=review, form=form)


@app.route('/work_review/<int:review_id>/comment', methods=['POST'])
@require_login
def comment_work_review(review_id):
    """评论作品点评"""
    form = CommentForm(request.form)
    if form.validate_on_submit():
        comment = WorkReviewComment(content=cgi.escape(form.content.data), review_id=review_id,
                                    user_id=session['user_id'])
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('work_review', review_id=review_id) + "#" + str(comment.id))
    return redirect(url_for('work_review', review_id=review_id))


@app.route('/all_work_reviews')
def all_work_reviews():
    """作品的所有点评"""
    page = int(request.args.get('page', 1))
    pagination = WorkReview.query.filter(WorkReview.is_publish == True).order_by(
        WorkReview.create_time.desc()).paginate(page, 10)
    stmt = db.session.query(WorkReview.user_id, db.func.count(WorkReview.user_id).label('reviews_num')).group_by(
        WorkReview.user_id).subquery()
    hot_reviewers = db.session.query(User).join(stmt, User.id == stmt.c.user_id).order_by(stmt.c.reviews_num)
    return render_template('work_review/all_work_reviews.html', pagination=pagination, hot_reviewers=hot_reviewers)


@app.route('/work/<int:work_id>/add_review', methods=['GET', 'POST'])
@require_login
def add_work_review(work_id):
    """为作品添加点评"""
    work = Work.query.get_or_404(work_id)
    form = ReviewForm()
    if form.validate_on_submit():
        is_publish = True if 'publish' in request.form else False
        review = WorkReview(title=cgi.escape(form.title.data), content=cgi.escape(form.content.data),
                            user_id=session['user_id'], work_id=work_id, is_publish=is_publish)
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('work_review', review_id=review.id))
    return render_template('work_review/add_work_review.html', work=work, form=form)


@app.route('/work_review/<int:review_id>/edit', methods=['GET', 'POST'])
@require_login
def edit_work_review(review_id):
    """编辑作品点评"""
    review = WorkReview.query.get_or_404(review_id)
    if review.user_id != session['user_id']:
        abort(404)
    form = ReviewForm(obj=review)
    if form.validate_on_submit():
        review.title = cgi.escape(form.title.data)
        review.content = cgi.escape(form.content.data)
        review.is_publish = True if 'publish' in request.form else False
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('work_review', review_id=review_id))
    return render_template('work_review/edit_work_review.html', review=review, form=form)


@app.route('/review/<int:review_id>/delete')
@require_login
def delete_work_review(review_id):
    """删除作品点评"""
    review = WorkReview.query.get_or_404(review_id)
    if review.user_id != session['user_id']:
        abort(404)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('index'))