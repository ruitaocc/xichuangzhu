#-*- coding: UTF-8 -*-
from __future__ import division
import math
import cgi
import markdown2
from flask import render_template, request, redirect, url_for, json, session, abort
from xichuangzhu import app
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.work_model import Work
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.review_model import Review
from xichuangzhu.models.comment_model import Comment
from xichuangzhu.models.user_model import User
from xichuangzhu.models.inform_model import Inform
from xichuangzhu.form import ReviewForm, CommentForm
from xichuangzhu.utils import time_diff, get_comment_replyee_id, rebuild_comment, build_review_inform_title, require_admin, require_login, Pagination

# page review
#--------------------------------------------------
@app.route('/review/<int:review_id>')
def review(review_id):
    form = CommentForm()

    # check exist
    review = Review.get_review(review_id)
    if not review:
        abort(404)

    # the others cannot see draft 
    is_me = True if "user_id" in session and session['user_id'] == review['UserID'] else False
    if not is_me and review['IsPublish'] == 0: 
        abort(404)

    # review['Content'] = markdown2.markdown(review['Content'])
    review['Content'] = review['Content'].replace('\n', "<div class='text-gap'></div>")
    review['Time'] = time_diff(review['Time'])
    Review.add_click_num(review_id)
    comments = Comment.get_comments_by_review(review_id)
    for c in comments:
        c['Time'] = time_diff(c['Time'])

    return render_template('review/review.html', review=review, comments=comments, form=form)

# proc - add comment
@app.route('/review/add_comment/<int:review_id>', methods=['POST'])
@require_login
def add_comment_to_review(review_id):
    form = CommentForm(request.form)
    if form.validate():
        comment = cgi.escape(form.comment.data)

        # add comment
        replyer_id = session['user_id']
        replyee_id = get_comment_replyee_id(comment)    # check if @people exist
        if replyee_id != -1:
            comment = rebuild_comment(comment, replyee_id)
        new_comment_id = Comment.add_comment_to_review(review_id, replyer_id, comment)

        Review.add_comment_num(review_id)

        # add inform
        review_user_id = Review.get_review(review_id)['UserID']
        inform_title = build_review_inform_title(replyer_id, review_id)
        # if the review not add by me
        if  replyer_id != review_user_id:
            Inform.add(replyer_id, review_user_id, inform_title, comment)
        # if replyee exist,
        # and the topic not add by me,
        # and not review_user_id, because if so, the inform has already been sended above
        if replyee_id != -1 and replyee_id != replyer_id and replyee_id != review_user_id:
            Inform.add(replyer_id, replyee_id, inform_title, comment)
        return redirect(url_for('review', review_id=review_id) + "#" + str(new_comment_id))
    else:
        return redirect(url_for('review', review_id=review_id))

# page - all reviews
#--------------------------------------------------
@app.route('/reviews')
def reviews():
    # pagination
    per_page = 10
    page = int(request.args['page'] if 'page' in request.args else 1)

    reviews = Review.get_reviews(page, per_page)
    for r in reviews:
        r['Time'] = time_diff(r['Time'])

    reviews_num = Review.get_reviews_num()

    pagination = Pagination(page, per_page, reviews_num)

    reviewers = Review.get_hot_reviewers(8)

    return render_template('review/reviews.html', reviews=reviews, reviewers=reviewers, pagination=pagination)

# page - add review
#--------------------------------------------------
@app.route('/review/add/<int:work_id>', methods=['GET', 'POST'])
@require_login
def add_review(work_id):
    work = Work.get_work(work_id)
    if request.method == 'GET':
        form = ReviewForm()
        return render_template('review/add_review.html', work=work, form=form)
    else:
        form = ReviewForm(request.form)
        if form.validate():
            user_id = session['user_id']
            title = cgi.escape(form.title.data)
            content = cgi.escape(form.content.data)
            is_publish = 1 if 'publish' in request.form else 0
            new_review_id = Review.add_review(work_id, user_id, title, content, is_publish)
            return redirect(url_for('review', review_id=new_review_id))
        else:
            return render_template('review/add_review.html', work=work, form=form)

# page - edit review
#--------------------------------------------------
@app.route('/review/edit/<int:review_id>', methods=['GET', 'POST'])
@require_login
def edit_review(review_id):
    review = Review.get_review(review_id)
    if review['UserID'] != session['user_id']:
        abort(404)

    if request.method == 'GET':
        form = ReviewForm(title=review['Title'], content=review['Content'])
        return render_template('review/edit_review.html', review=review, form=form)
    else:
        form = ReviewForm(request.form)
        if form.validate():
            title = cgi.escape(form.title.data)
            content = cgi.escape(form.content.data)
            is_publish = 1 if 'publish' in request.form else 0
            Review.edit_review(review_id, title, content, is_publish)
            return redirect(url_for('review', review_id=review_id))
        else:
            return render_template('review/edit_review.html', review=review, form=form)

# proc delete review
#--------------------------------------------------
@app.route('/review/delete/<int:review_id>')
@require_login
def delete_review(review_id):
    review = Review.get_review(review_id)
    if review['UserID'] != session['user_id']:
        abort(404)
    Review.delete(review_id)
    return redirect(url_for('index'))