#-*- coding: UTF-8 -*-

from __future__ import division
import re
import math
import markdown2
from flask import render_template, request, redirect, url_for, json, session, abort
from xichuangzhu import app
from xichuangzhu.models.work_model import Work
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.review_model import Review
from xichuangzhu.models.collect_model import Collect
from xichuangzhu.models.widget_model import Widget
from xichuangzhu.models.product_model import Product
from xichuangzhu.models.tag_model import Tag
from xichuangzhu.utils import time_diff, content_clean, check_admin, check_login

# page - single work
#--------------------------------------------------

# view (public)
@app.route('/work/<int:work_id>')
def single_work(work_id):
	work = Work.get_work(work_id)
	if not work:
		abort(404)

	# add comment, split ci, gene paragraph
	work['Content'] = re.sub(r'<([^<^b]+)>', r"<sup title='\1'></sup>", work['Content'])
	work['Content'] = work['Content'].replace('%', "&nbsp;&nbsp;")
	work['Content'] = markdown2.markdown(work['Content'])

	# check if is collected
	if 'user_id' in session:
		is_collected = Collect.check(session['user_id'], work_id)
		tags = Collect.get_tags(session['user_id'], work_id) if is_collected else ""
		my_tags = Tag.get_user_tags(session['user_id'], 20)
		popular_tags = Tag.get_work_tags(work_id, 20)
	else:
		is_collected = False
		tags = ""
		my_tags = []
		popular_tags = []

	reviews = Review.get_reviews_by_work(work_id)
	for r in reviews:
		r['Time'] = time_diff(r['Time'])

	product = Product.get_product_by_random()

	other_works = Work.get_other_works_by_author(work['AuthorID'], work_id, 5)
	for ow in other_works:
		ow['Content'] = content_clean(ow['Content'])

	collectors = Collect.get_users_by_work(work_id, 4)

	return render_template('work/single_work.html', work=work, tags=tags, my_tags=my_tags, popular_tags=popular_tags, reviews=reviews, is_collected=is_collected, product=product, other_works=other_works, collectors=collectors)

# proc - add & edit collected work (login)
@app.route('/work/collect/<int:work_id>', methods=['POST'])
def collect_work(work_id):
	check_login()

	tags = request.form['tags'].split(' ')

	# remove the empty & repeat item
	new_tags = []
	for t in tags:
		if t != '':
			new_tags.append(t)
	new_tags = list(set(new_tags))

	# collect work
	is_collected = Collect.check(session['user_id'], work_id)
	if is_collected:
		Collect.edit(session['user_id'], work_id, ' '.join(new_tags) + ' ')
	else:	# edit tags
		Collect.add(session['user_id'], work_id, ' '.join(new_tags) + ' ')

	# update user tags & work tags
	for t in new_tags:
		Tag.add_tag(t)
		Tag.add_user_tag(session['user_id'], t)
		Tag.add_work_tag(work_id, t)

	return redirect(url_for('single_work', work_id=work_id))

# proc - discollect work (login)
@app.route('/work/discollect/<int:work_id>')
def discollect_work(work_id):
	check_login()

	Collect.remove(session['user_id'], work_id)
	return redirect(url_for('single_work', work_id=work_id))

# page - all works
#--------------------------------------------------

# view (public)
@app.route('/works')
def works():
	num_per_page = 10

	work_type = request.args['type'] if 'type' in request.args else 'all'
	dynasty_abbr = request.args['dynasty'] if 'dynasty' in request.args else 'all'
	page = int(request.args['page'] if 'page' in request.args else 1)

	works = Work.get_works(work_type, dynasty_abbr, page, num_per_page)
	for work in works:
		work['Content'] = content_clean(work['Content'])

	works_num = Work.get_works_num(work_type, dynasty_abbr)

	# page paras
	total_page = int(math.ceil(works_num / num_per_page))
	pre_page = (page - 1) if page > 1 else 1
	if total_page == 0:
		next_page = 1
	elif page < total_page:
		next_page = page + 1
	else:
		next_page = total_page

	work_types = Work.get_types()

	dynasties = Dynasty.get_dynasties()

	return render_template('work/works.html', works=works, works_num=works_num, work_types=work_types, dynasties=dynasties, page=page, total_page=total_page, pre_page=pre_page, next_page=next_page, work_type=work_type, dynasty_abbr=dynasty_abbr)

# page - works by tag
#--------------------------------------------------

# view (public)
@app.route('/tag/<tag>')
def works_by_tag(tag):
	num_per_page = 10

	page = int(request.args['page'] if 'page' in request.args else 1)

	works = Work.get_works_by_tag(tag, page, num_per_page)
	for work in works:
		work['Content'] = content_clean(work['Content'])

	works_num = Work.get_works_num_by_tag(tag)

	# page paras
	total_page = int(math.ceil(works_num / num_per_page))
	pre_page = (page - 1) if page > 1 else 1
	if total_page == 0:
		next_page = 1
		total_page = 1
	elif page < total_page:
		next_page = page + 1
	else:
		next_page = total_page

	return render_template('work/works_by_tag.html', works=works, tag=tag, page=page, total_page=total_page, pre_page=pre_page, next_page=next_page)

# page - add work
#--------------------------------------------------

# view (admin)
@app.route('/work/add', methods=['GET', 'POST'])
def add_work():
	check_admin()

	if request.method == 'GET':
		work_types = Work.get_types()
		return render_template('work/add_work.html', work_types=work_types)
	elif request.method == 'POST':
		title = request.form['title']
		content = request.form['content']
		foreword = request.form['foreword']
		intro = request.form['introduction']
		authorID = int(request.form['authorID'])
		dynastyID = int(Dynasty.get_dynastyID_by_author(authorID))
		work_type = request.form['type']
		type_name = Work.get_type_name(work_type)
		
		new_work_id = Work.add_work(title, content, foreword, intro, authorID, dynastyID, work_type, type_name)
		return redirect(url_for('single_work', work_id=new_work_id))

# page - edit work
#--------------------------------------------------

# view (admin)
@app.route('/work/edit/<int:work_id>', methods=['GET', 'POST'])
def edit_work(work_id):
	check_admin()

	if request.method == 'GET':
		work = Work.get_work(work_id)
		work_types = Work.get_types()
		return render_template('work/edit_work.html', work=work, work_types=work_types)
	elif request.method == 'POST':
		title = request.form['title']
		content = request.form['content']
		foreword = request.form['foreword']
		intro = request.form['introduction']
		author_id = int(request.form['authorID'])
		dynasty_id = int(Dynasty.get_dynastyID_by_author(author_id))
		work_type = request.form['type']
		type_name = Work.get_type_name(work_type)

		Work.edit_work(title, content, foreword, intro ,author_id, dynasty_id, work_type, type_name, work_id)
		return redirect(url_for('single_work', work_id=work_id))

# json - search authors in page add & edit work (admin)
#--------------------------------------------------

@app.route('/work/search_authors', methods=['POST'])
def get_authors_by_name():
	check_admin()

	name = request.form['author']
	authors = Author.get_authors_by_name(name)
	return json.dumps(authors)