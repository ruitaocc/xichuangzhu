#-*- coding: UTF-8 -*-

from __future__ import division

from flask import render_template, request, redirect, url_for, json, session

from xichuangzhu import app

from xichuangzhu.models.work_model import Work
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.collection_model import Collection
from xichuangzhu.models.review_model import Review
from xichuangzhu.models.love_model import Love
from xichuangzhu.models.widget_model import Widget

import markdown2

import re

import math

# page - single work
#--------------------------------------------------

# view
@app.route('/work/<int:work_id>')
def single_work(work_id):
	work = Work.get_work(work_id)

	# 1 - add comment
	work['Content'] = re.sub(r'<([^<^b]+)>', r"<sup title='\1'></sup>", work['Content'])

	# 2 - split ci
	work['Content'] = work['Content'].replace('%', "&nbsp;&nbsp;")

	# 3 - gene paragraph
	work['Content'] = markdown2.markdown(work['Content'])

	reviews = Review.get_reviews_by_work(work_id)
	widgets = Widget.get_widgets('work', work_id)

	# check is loved
	if 'user_id' in session:
		is_loved = Love.check_love(session['user_id'], work_id)
	else:
		is_loved = False
	return render_template('single_work.html', work=work, reviews=reviews, widgets=widgets, is_loved=is_loved)

# proc - love work
#--------------------------------------------------
@app.route('/work/love/<int:work_id>')
def love_work(work_id):
	Love.add_love(session['user_id'], work_id)
	return redirect(url_for('single_work', work_id=work_id))

# proc - unlove work
#--------------------------------------------------
@app.route('/work/unlove/<int:work_id>')
def unlove_work(work_id):
	Love.remove_love(session['user_id'], work_id)
	return redirect(url_for('single_work', work_id=work_id))

# page - all works
#--------------------------------------------------

# view
@app.route('/works')
def works():
	num_per_page = 10

	work_type  = request.args['type'] if 'type' in request.args else 'all'
	dynasty_abbr = request.args['dynasty'] if 'dynasty' in request.args else 'all'
	page       = int(request.args['page'] if 'page' in request.args else 1)

	works = Work.get_works(work_type, dynasty_abbr, page, num_per_page)
	for work in works:
		work['Content'] = re.sub(r'<([^<]+)>', '', work['Content'])
		work['Content'] = work['Content'].replace('%', '')

	works_num  = Work.get_works_num(work_type, dynasty_abbr)

	# page paras
	total_page = int(math.ceil(works_num / num_per_page))
	pre_page   = (page - 1) if page > 1 else 1
	if total_page == 0:
		next_page = 1
	elif page < total_page:
		next_page = page + 1
	else:
		next_page = total_page

	work_types = Work.get_types()
	dynasties = Dynasty.get_dynasties()
	return render_template('works.html', works=works, works_num=works_num, work_types=work_types, dynasties=dynasties, page=page,total_page=total_page, pre_page=pre_page, next_page=next_page, work_type=work_type, dynasty_abbr=dynasty_abbr)

# page - add work
#--------------------------------------------------

@app.route('/work/add', methods=['GET', 'POST'])
def add_work():
	if request.method == 'GET':
		work_types = Work.get_types()
		return render_template('add_work.html', work_types=work_types)
	elif request.method == 'POST':
		title        = request.form['title']
		content      = request.form['content']
		foreword     = request.form['foreword']
		intro        = request.form['introduction']
		authorID     = int(request.form['authorID'])
		dynastyID    = int(Dynasty.get_dynastyID_by_author(authorID))
		collectionID = int(request.form['collectionID'])
		work_type    = request.form['type']
		type_name    = Work.get_type_name(work_type)
		
		new_work_id = Work.add_work(title, content, foreword, intro, authorID, dynastyID, collectionID, work_type, type_name)
		return redirect(url_for('single_work', work_id=new_work_id))

# page - edit work
#--------------------------------------------------

@app.route('/work/edit/<int:work_id>', methods=['GET', 'POST'])
def edit_work(work_id):
	if request.method == 'GET':
		work = Work.get_work(work_id)
		work_types = Work.get_types()
		return render_template('edit_work.html', work=work, work_types=work_types)
	elif request.method == 'POST':
		title        = request.form['title']
		content      = request.form['content']
		foreword     = request.form['foreword']
		intro        = request.form['introduction']
		authorID     = int(request.form['authorID'])
		dynastyID    = int(Dynasty.get_dynastyID_by_author(authorID))
		collectionID = int(request.form['collectionID'])
		work_type    = request.form['type']
		type_name    = Work.get_type_name(work_type)

		Work.edit_work(title, content, foreword, intro ,authorID, dynastyID, collectionID, work_type, type_name, work_id)
		return redirect(url_for('single_work', work_id=work_id))

# proc - delete work
#--------------------------------------------------

# @app.route('/work/delete/<int:workID>', methods=['GET'])
# def delete_work(workID):
# 	Work.delete_work(workID)
# 	return redirect(url_for('index'))

# helper - search authors and their collections in page add work
#--------------------------------------------------

@app.route('/work/search_authors', methods=['POST'])
def get_authors_by_name():
	name = request.form['author']
	authors = Author.get_authors_by_name(name)
	for author in authors:
		author['Collections'] = Collection.get_collections_by_author(author['AuthorID'])
	return json.dumps(authors)

# helper - search the author's collections in page edit work
#--------------------------------------------------
@app.route('/work/search_collections', methods=['POST'])
def get_collections_by_author():
	authorID = int(request.form['authorID'])
	collections = Collection.get_collections_by_author(authorID)
	return json.dumps(collections)
