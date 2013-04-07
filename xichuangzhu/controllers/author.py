#-*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, json, abort

from xichuangzhu import app

from xichuangzhu.models.author_model import Author
from xichuangzhu.models.work_model import Work
from xichuangzhu.models.collection_model import Collection
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.quote_model import Quote

import re

from xichuangzhu.utils import content_clean

# page all authors
#--------------------------------------------------

@app.route('/author')
def authors():
	dynasties = Dynasty.get_dynasties()
	for dyn in dynasties:
		dyn['authors'] = Author.get_authors_by_dynasty(dyn['DynastyID'])
		for a in dyn['authors']:
			quote = Quote.get_quote_by_random(a['AuthorID'])
			a['Quote'] = quote['Quote'] if quote else ""
			a['QuotesNum'] = Quote.get_quotes_num_by_author(a['AuthorID'])

	hot_authors = Author.get_hot_authors(8)
	for a in hot_authors:
		quote = Quote.get_quote_by_random(a['AuthorID'])
		a['Quote'] = quote['Quote'] if quote else ""

	return render_template('authors.html', dynasties=dynasties, hot_authors=hot_authors)

# page single author
#--------------------------------------------------

@app.route('/author/<author_abbr>')
def single_author(author_abbr):
	author = Author.get_author_by_abbr(author_abbr)

	if not author:
		abort(404)
	
	quote = Quote.get_quote_by_random(author['AuthorID'])
	quotes_num = Quote.get_quotes_num_by_author(author['AuthorID'])

	collections = Collection.get_collections_by_author(author['AuthorID'])

	works = Work.get_works_by_author(author['AuthorID'])
	for work in works:
		work['Content'] = content_clean(work['Content'])

	# count num of different type work
	# return like this - works_num['shi'] = {'type_name': '诗', 'num': 0}
	work_types = Work.get_types()
	works_num = {}
	for wt in work_types:
		works_num[wt['WorkType']] = {'type_name': wt['TypeName'], 'num': 0}
	for work in works:
		work_type = work['Type']  
		works_num[work_type]['num'] += 1

	return render_template('single_author.html', author=author, quote=quote, quotes_num=quotes_num, collections=collections, works=works, works_num=works_num)

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
		introduction = request.form['introduction']
		birthYear    = request.form['birthYear']
		deathYear    = request.form['deathYear']
		dynastyID    = int(request.form['dynastyID'])
		Author.add_author(author, abbr, introduction, birthYear, deathYear, dynastyID)
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
		introduction = request.form['introduction']
		birthYear    = request.form['birthYear']
		deathYear    = request.form['deathYear']
		dynastyID    = int(request.form['dynastyID'])		
		Author.edit_author(author, abbr, introduction, birthYear, deathYear, dynastyID, authorID)
		return redirect(url_for('single_author', author_abbr=abbr))

# page admin quotes
#--------------------------------------------------

# view
@app.route('/quote/admin/<int:author_id>')
def admin_quotes(author_id):
	author = Author.get_author_by_id(author_id)
	quotes = Quote.get_quotes_by_author(author_id)
	return render_template('admin_quotes.html', quotes=quotes, author=author)

# proc - add quote
@app.route('/quote/add/<int:author_id>', methods=['POST'])
def add_quote(author_id):
	quote      = request.form['quote']
	work_id    = int(request.form['work-id'])
	work_title = Work.get_work(work_id)['Title'] 
	Quote.add(author_id, quote, work_id, work_title)
	return redirect(url_for('admin_quotes', author_id=author_id))

# proc - delete quote
@app.route('/quote/delete/<int:quote_id>')
def delete_quote(quote_id):
	author_id = int(request.args['author_id'])
	Quote.delete(quote_id)
	return redirect(url_for('admin_quotes', author_id=author_id))

# page edit quote
#--------------------------------------------------
@app.route('/quote/edit/<int:quote_id>', methods=['GET', 'POST'])
def edit_quote(quote_id):
	if request.method == 'GET':
		quote = Quote.get_quote_by_id(quote_id)
		return render_template('edit_quote.html', quote=quote)
	elif request.method == 'POST':
		quote   = request.form['quote']
		work_id = int(request.form['work-id'])
		work    = Work.get_work(work_id)
		Quote.edit(quote_id, work['AuthorID'], quote, work['WorkID'], work['Title'])
		return redirect(url_for('admin_quotes', author_id=work['AuthorID']))