#-*- coding: UTF-8 -*-

from __future__ import division

import math

import cgi

import markdown2

from flask import render_template, request, redirect, url_for, json, session, abort

from xichuangzhu import app

from xichuangzhu.models.author_model import Author
from xichuangzhu.models.work_model import Work
from xichuangzhu.models.collection_model import Collection
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.review_model import Review
from xichuangzhu.models.comment_model import Comment
from xichuangzhu.models.user_model import User
from xichuangzhu.models.inform_model import Inform

from xichuangzhu.form import ReviewForm, CommentForm

from xichuangzhu.utils import time_diff, get_comment_replyee_id, rebuild_comment, build_review_inform_title, check_private, check_login

# page single review
#--------------------------------------------------

# view (public)
@app.route('/review/<int:review_id>')
def single_review(review_id):
	form = CommentForm()

	# check exist
	review = Review.get_review(review_id)
	if not review:
		abort(404)

	review['Content'] = markdown2.markdown(review['Content'])
	review['Time'] = time_diff(review['Time'])
	Review.add_click_num(review_id)
	comments = Comment.get_comments_by_review(review_id)
	for c in comments:
		c['Time'] = time_diff(c['Time'])

	return render_template('single_review.html', review=review, comments=comments, form=form)

# proc - add comment (login)
@app.route('/review/add_comment/<int:review_id>', methods=['POST'])
def add_comment_to_review(review_id):
	check_login()

	form = CommentForm(request.form)
	if form.validate():
		comment = cgi.escape(form.comment.data)

		# add comment
		replyer_id = session['user_id']
		replyee_id = get_comment_replyee_id(comment)	# check if @people exist
		if replyee_id != -1:
			comment = rebuild_comment(comment, replyee_id)
		new_comment_id = Comment.add_comment_to_review(review_id, replyer_id, comment)

		# plus comment num by 1
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
		return redirect(url_for('single_review', review_id=review_id) + "#" + str(new_comment_id))

	return redirect(url_for('single_review', review_id=review_id))

# page all reviews
#--------------------------------------------------

# view (public)
@app.route('/reviews')
def reviews():
	# pagination
	num_per_page = 10
	page = int(request.args['page'] if 'page' in request.args else 1)

	reviews = Review.get_reviews(page, num_per_page)
	for r in reviews:
		r['Time'] = time_diff(r['Time'])

	# page paras
	reviews_num = Review.get_reviews_num()
	total_page = int(math.ceil(reviews_num / num_per_page))
	pre_page = (page - 1) if page > 1 else 1
	if total_page == 0:
		next_page = 1
	elif page < total_page:
		next_page = page + 1
	else:
		next_page = total_page

	reviewers = Review.get_hot_reviewers(8)
	return render_template('reviews.html', reviews=reviews, reviewers=reviewers, page=page, total_page=total_page, pre_page=pre_page, next_page=next_page)

# page add review
#--------------------------------------------------

# view (login)
@app.route('/review/add/<int:work_id>', methods=['GET', 'POST'])
def add_review(work_id):
	check_login()
	form = ReviewForm(request.form)
	work = Work.get_work(work_id)
	if request.method == 'POST' and form.validate():
		user_id = session['user_id']
		title = cgi.escape(form.title.data)
		content = cgi.escape(form.content.data)
		new_review_id = Review.add_review(work_id, user_id, title, content)
		return redirect(url_for('single_review', review_id=new_review_id))
	return render_template('add_review.html', work=work, form=form)

# page edit review
#--------------------------------------------------

# view (private)
@app.route('/review/edit/<int:review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
	review = Review.get_review(review_id)
	check_private(review['UserID'])
	form = ReviewForm(title=review['Title'], content=review['Content'])

	if request.method == 'POST':
		form = ReviewForm(request.form)
		if form.validate():
			title = cgi.escape(form.title.data)
			content = cgi.escape(form.content.data)
			Review.edit_review(review_id, title, content)
			return redirect(url_for('single_review', review_id=review_id))

	return render_template('edit_review.html', review=review, form=form)
