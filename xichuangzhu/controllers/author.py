#-*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, json

from xichuangzhu import app

from xichuangzhu.models.author_model import Author
from xichuangzhu.models.work_model import Work
from xichuangzhu.models.collection_model import Collection
from xichuangzhu.models.dynasty_model import Dynasty

import re

# page all authors
#--------------------------------------------------

@app.route('/author')
def authors():
	dynasties = Dynasty.get_dynasties()
	for dyn in dynasties:
		dyn['authors'] = Author.get_authors_by_dynasty(dyn['DynastyID'])
	hot_authors = Author.get_hot_authors(8)
	return render_template('authors.html', dynasties=dynasties, hot_authors=hot_authors)

# page single author
#--------------------------------------------------

@app.route('/author/<author_abbr>')
def single_author(author_abbr):
	author = Author.get_author_by_abbr(author_abbr)
	collections = Collection.get_collections_by_author(author['AuthorID'])

	works = Work.get_works_by_author(author['AuthorID'])
	for work in works:
		work['Content'] = re.sub(r'<([^<]+)>', '', work['Content'])
		work['Content'] = work['Content'].replace('%', '').replace('/', '')

	# count num of different type work
	# return like this - works_num['shi'] = {'type_name': '诗', 'num': 0}
	work_types = Work.get_types()
	works_num = {}
	for wt in work_types:
		works_num[wt['WorkType']] = {'type_name': wt['TypeName'], 'num': 0}
	for work in works:
		work_type = work['Type']  
		works_num[work_type]['num'] += 1

	return render_template('single_author.html', author=author, collections=collections, works=works, works_num=works_num)

# page add author
#--------------------------------------------------

@app.route('/author/add', methods=['GET', 'POST'])
def add_author():
	if request.method == 'GET':
		dynasties = Dynasty.get_dynasties()
		return render_template('add_author.html', dynasties=dynasties)
	elif request.method == 'POST':
		author       = request.form['author']
		abbr         = request.form['abbr']
		quote        = request.form['quote']
		introduction = request.form['introduction']
		birthYear    = request.form['birthYear']
		deathYear    = request.form['deathYear']
		dynastyID    = int(request.form['dynastyID'])
		Author.add_author(author, abbr, quote, introduction, birthYear, deathYear, dynastyID)
		return redirect(url_for('single_author', author_abbr=abbr))

# page edit author
#--------------------------------------------------

@app.route('/author/edit/<int:authorID>', methods=['GET', 'POST'])
def edit_author(authorID):
	if request.method == 'GET':
		dynasties = Dynasty.get_dynasties()
		author = Author.get_author_by_id(authorID)
		return render_template('edit_author.html', dynasties=dynasties, author=author)
	elif request.method == 'POST':
		author       = request.form['author']
		abbr         = request.form['abbr']
		quote        = request.form['quote']
		introduction = request.form['introduction']
		birthYear    = request.form['birthYear']
		deathYear    = request.form['deathYear']
		dynastyID    = int(request.form['dynastyID'])		
		Author.edit_author(author, abbr, quote, introduction, birthYear, deathYear, dynastyID, authorID)
		return redirect(url_for('single_author', author_abbr=abbr))