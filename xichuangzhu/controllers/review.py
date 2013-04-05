#-*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, json, session

from xichuangzhu import app

from xichuangzhu.models.author_model import Author
from xichuangzhu.models.work_model import Work
from xichuangzhu.models.collection_model import Collection
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.review_model import Review
from xichuangzhu.models.comment_model import Comment
from xichuangzhu.models.user_model import User
from xichuangzhu.models.inform_model import Inform

import markdown2

from xichuangzhu.utils import time_diff, get_comment_replyee_id, rebuild_comment, build_review_inform_title

# page single review
#--------------------------------------------------

# view
@app.route('/review/<int:review_id>')
def single_review(review_id):
	Review.add_click_num(review_id)
	review = Review.get_review(review_id)
	review['Content'] = markdown2.markdown(review['Content'])
	review['Time'] = time_diff(review['Time'])
	comments = Comment.get_comments_by_review(review_id)
	for c in comments:
		c['Time'] = time_diff(c['Time'])
	return render_template('single_review.html', review=review, comments=comments)

# proc - add comment
@app.route('/review/add_comment/<int:review_id>', methods=['POST'])
def add_comment_to_review(review_id):
	replyer_id = session['user_id']

	# add comment
	comment = request.form['comment']	
	replyee_id = get_comment_replyee_id(comment)	# check if @people exist
	if replyee_id != -1:
		comment = rebuild_comment(comment, replyee_id)
	Comment.add_comment_to_review(review_id, replyer_id, comment)

	# plus comment num
	Review.add_comment_num(review_id)

	# inform
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
	
	return redirect(url_for('single_review', review_id=review_id))

# page all reviews
#--------------------------------------------------

# view
@app.route('/reviews')
def reviews():
	reviews = Review.get_hot_reviews()
	for r in reviews:
		r['Time'] = time_diff(r['Time'])
	reviewers = Review.get_hot_reviewers(8)
	return render_template('reviews.html', reviews=reviews, reviewers=reviewers)

# page add review
#--------------------------------------------------

@app.route('/review/add/<int:work_id>', methods=['GET', 'POST'])
def add_review(work_id):
	if request.method == 'GET':
		work = Work.get_work(work_id)
		return render_template('add_review.html', work=work)
	elif request.method == 'POST':
		user_id = int(request.form['user_id'])
		title = request.form['title']
		content = request.form['content']
		new_review_id = Review.add_review(work_id, user_id, title, content)
		return redirect(url_for('single_review', review_id=new_review_id))

# page edit review
#--------------------------------------------------
@app.route('/review/edit/<int:review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
	if request.method == 'GET':
		review = Review.get_review(review_id)
		return render_template('edit_review.html', review=review)
	elif request.method == 'POST':
		title = request.form['title']
		content = request.form['content']
		Review.edit_review(review_id, title, content)
		return redirect(url_for('single_review', review_id=review_id))