#-*- coding: UTF-8 -*-
import re
from flask import render_template, request, redirect, url_for, json, abort, session
from xichuangzhu import app
import config
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.work_model import Work
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.quote_model import Quote
from xichuangzhu.utils import content_clean, require_admin

# page all authors
#--------------------------------------------------
@app.route('/authors')
def authors():
    dynasties = Dynasty.get_dynasties()
    for d in dynasties:
        d['authors'] = Author.get_authors_by_dynasty(d['DynastyID'], 30, False)
        for a in d['authors']:
            quote = Quote.get_quote_by_random(a['AuthorID'])
            a['Quote'] = quote['Quote'] if quote else ""
            a['QuoteID'] = quote['QuoteID'] if quote else 0
            a['QuotesNum'] = Quote.get_quotes_num_by_author(a['AuthorID'])

    hot_authors = Author.get_hot_authors(8)
    for a in hot_authors:
        quote = Quote.get_quote_by_random(a['AuthorID'])
        a['Quote'] = quote['Quote'] if quote else ""
        a['QuoteID'] = quote['QuoteID'] if quote else 0

    return render_template('author/authors.html', dynasties=dynasties, hot_authors=hot_authors)

# page single author
#--------------------------------------------------
@app.route('/author/<author_abbr>')
def single_author(author_abbr):
    author = Author.get_author_by_abbr(author_abbr)
    if not author:
        abort(404)
    
    # if 'q' in form.args, then display it,
    # otherwise, display a random quote
    if 'q' in request.args:
        q_id = int(request.args['q'])
        quote = Quote.get_quote_by_id(q_id)
    else:
        quote = Quote.get_quote_by_random(author['AuthorID'])
    
    quotes_num = Quote.get_quotes_num_by_author(author['AuthorID'])

    works = Work.get_works_by_author(author['AuthorID'])
    for work in works:
        work['Content'] = content_clean(work['Content'])

    # count num of different type work.
    # return like this - works_num['shi'] = {'type_name': '诗', 'num': 0}.
    work_types = Work.get_types()
    works_num = {}
    for wt in work_types:
        works_num[wt['WorkType']] = {'type_name': wt['TypeName'], 'num': 0}
    for work in works:
        work_type = work['Type']  
        works_num[work_type]['num'] += 1

    return render_template('author/single_author.html', author=author, quote=quote, quotes_num=quotes_num, works=works, works_num=works_num)

# page add author
#--------------------------------------------------
@app.route('/author/add', methods=['GET', 'POST'])
@require_admin
def add_author():
    if request.method == 'GET':
        dynasties = Dynasty.get_dynasties()
        return render_template('author/add_author.html', dynasties=dynasties)
    else:
        author = request.form['author']
        abbr = request.form['abbr']
        introduction = request.form['introduction']
        birthYear = request.form['birthYear']
        deathYear = request.form['deathYear']
        dynastyID = int(request.form['dynastyID'])
        Author.add_author(author, abbr, introduction, birthYear, deathYear, dynastyID)
        return redirect(url_for('author/single_author', author_abbr=abbr))

# page edit author
#--------------------------------------------------
@app.route('/author/edit/<int:authorID>', methods=['GET', 'POST'])
@require_admin
def edit_author(authorID):
    if request.method == 'GET':
        dynasties = Dynasty.get_dynasties()
        author = Author.get_author_by_id(authorID)
        return render_template('author/edit_author.html', dynasties=dynasties, author=author)
    else:
        author = request.form['author']
        abbr = request.form['abbr']
        introduction = request.form['introduction']
        birthYear = request.form['birthYear']
        deathYear = request.form['deathYear']
        dynastyID = int(request.form['dynastyID'])      
        Author.edit_author(author, abbr, introduction, birthYear, deathYear, dynastyID, authorID)
        return redirect(url_for('author/single_author', author_abbr=abbr))

# page - admin quotes
#--------------------------------------------------
@app.route('/quote/admin/<int:author_id>')
@require_admin
def admin_quotes(author_id):
    author = Author.get_author_by_id(author_id)
    quotes = Quote.get_quotes_by_author(author_id)
    return render_template('author/admin_quotes.html', quotes=quotes, author=author)

# proc - add quote
@app.route('/quote/add/<int:author_id>', methods=['POST'])
@require_admin
def add_quote(author_id):
    quote = request.form['quote']
    work_id = int(request.form['work-id'])
    work_title = Work.get_work(work_id)['Title'] 
    Quote.add(author_id, quote, work_id, work_title)
    return redirect(url_for('author/admin_quotes', author_id=author_id))

# proc - delete quote
@app.route('/quote/delete/<int:quote_id>')
@require_admin
def delete_quote(quote_id):
    author_id = int(request.args['author_id'])
    Quote.delete(quote_id)
    return redirect(url_for('author/admin_quotes', author_id=author_id))

# page edit quote
#--------------------------------------------------
@app.route('/quote/edit/<int:quote_id>', methods=['GET', 'POST'])
@require_admin
def edit_quote(quote_id):   
    if request.method == 'GET':
        quote = Quote.get_quote_by_id(quote_id)
        return render_template('author/edit_quote.html', quote=quote)
    else:
        quote = request.form['quote']
        work_id = int(request.form['work-id'])
        work = Work.get_work(work_id)
        Quote.edit(quote_id, work['AuthorID'], quote, work['WorkID'], work['Title'])
        return redirect(url_for('author/admin_quotes', author_id=work['AuthorID']))