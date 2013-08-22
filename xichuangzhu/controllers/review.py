#-*- coding: UTF-8 -*-
from __future__ import division
import math
import cgi
import markdown2
from flask import render_template, request, redirect, url_for, json, session, abort
from xichuangzhu import app
from xichuangzhu import db
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.work_model import Work
from xichuangzhu.models.review_model import WorkReview
from xichuangzhu.models.review_model import WorkReviewComment
from xichuangzhu.models.review_model import Review
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.comment_model import Comment
from xichuangzhu.models.user_model import User
from xichuangzhu.models.inform_model import Inform
from xichuangzhu.form import ReviewForm, CommentForm
# from xichuangzhu.utils import time_diff, get_comment_replyee_id, rebuild_comment, build_review_inform_title, require_admin, require_login, Pagination
from xichuangzhu.utils import time_diff, require_admin, require_login, Pagination

# page review
#--------------------------------------------------
@app.route('/review/<int:review_id>')
def review(review_id):
    form = CommentForm()

    review = WorkReview.query.get_or_404(review_id)

    # others cannot see draft
    is_me = True if "user_id" in session and session['user_id'] == review.user_id else False
    if not is_me and not review.is_publish: 
        abort(404)
    
    # Click num + 1
    review.click_num += 1 
    db.session.add(review)
    db.session.commit()

    return render_template('review/review.html', review=review, form=form)

# proc - add comment
@app.route('/review/<int:review_id>/comment', methods=['POST'])
@require_login
def comment_review(review_id):
    form = CommentForm(request.form)
    if form.validate():
        comment = WorkReviewComment(content=cgi.escape(form.content.data), review_id=review_id, user_id=session['user_id'])
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('review', review_id=review_id) + "#" + str(comment.id))
    else:
        return redirect(url_for('review', review_id=review_id))

# page - all reviews
#--------------------------------------------------
@app.route('/reviews')
def reviews():
    page = int(request.args.get('page', 1))
    pagination = WorkReview.query.paginate(page, 10)

    # get reviews
    stmt = db.session.query(WorkReview.user_id, db.func.count(WorkReview.user_id).label('reviews_num')).group_by(WorkReview.user_id).subquery()
    hot_reviewers = db.session.query(User).join(stmt, User.id==stmt.c.user_id).order_by(stmt.c.reviews_num)

    return render_template('review/reviews.html', pagination=pagination, hot_reviewers=hot_reviewers)

# page - add review
#--------------------------------------------------
@app.route('/work/<int:work_id>/add_review', methods=['GET', 'POST'])
@require_login
def add_review(work_id):
    work = Work.query.get_or_404(work_id)
    if request.method == 'GET':
        form = ReviewForm()
        return render_template('review/add_review.html', work=work, form=form)
    else:
        form = ReviewForm(request.form)
        if form.validate():
            is_publish = True if 'publish' in request.form else False
            review = WorkReview(title=cgi.escape(form.title.data), content=cgi.escape(form.content.data), user_id=session['user_id'], work_id=work_id, is_publish=is_publish)
            db.session.add(review)
            db.session.commit()
            return redirect(url_for('review', review_id=review.id))
        else:
            return render_template('review/add_review.html', work=work, form=form)

# page - edit review
#--------------------------------------------------
@app.route('/review/<int:review_id>/edit', methods=['GET', 'POST'])
@require_login
def edit_review(review_id):
    review = WorkReview.query.get_or_404(review_id)
    if review.user_id != session['user_id']:
        abort(404)

    if request.method == 'GET':
        form = ReviewForm(title=review.title, content=review.content)
        return render_template('review/edit_review.html', review=review, form=form)
    else:
        form = ReviewForm(request.form)
        if form.validate():
            review.title = cgi.escape(form.title.data)
            review.content = cgi.escape(form.content.data)
            review.is_publish = True if 'publish' in request.form else False
            db.session.add(review)
            db.session.commit()
            return redirect(url_for('review', review_id=review_id))
        else:
            return render_template('review/edit_review.html', review=review, form=form)

# proc delete review
#--------------------------------------------------
@app.route('/review/<int:review_id>/delete')
@require_login
def delete_review(review_id):
    review = WorkReview.query.get_or_404(review_id)
    if review.user_id != session['user_id']:
        abort(404)

    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('index'))