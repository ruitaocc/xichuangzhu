#-*- coding: UTF-8 -*-
import re
from flask import render_template, request, redirect, url_for, json, abort, session
from xichuangzhu import app
from xichuangzhu import db
import config
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.author_model import AuthorQuote
from xichuangzhu.models.work_model import Work
from xichuangzhu.models.collect_work import CollectWork
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.quote_model import Quote
from xichuangzhu.utils import content_clean, require_admin

# page all authors
#--------------------------------------------------
@app.route('/authors')
def authors():
    dynasties = Dynasty.query.options(db.subqueryload(Dynasty.authors)).order_by(Dynasty.start_year)

    # get the authors who's works are latest collected by user
    stmt = db.session.query(Author.id, CollectWork.create_time).join(Work).join(CollectWork).group_by(Author.id).having(db.func.max(CollectWork.create_time)).subquery()
    hot_authors = Author.query.join(stmt, Author.id==stmt.c.id).order_by(stmt.c.create_time).limit(8)

    return render_template('author/authors.html', dynasties=dynasties, hot_authors=hot_authors)

# page author
#--------------------------------------------------
@app.route('/author/<author_abbr>')
def author(author_abbr):
    author = Author.query.options(db.subqueryload(Author.works)).filter(Author.abbr==author_abbr).one()
    if not author:
        abort(404)
    
    if 'q' in request.args:
        quote = AuthorQuote.get(int(request.args['q']))
    else:
        quote = author.random_quote

    work_types_num = db.session.query(Work.type, Work.type_name, db.func.count(Work.type_name).label('type_num')).filter(Work.author_id==author.id).group_by(Work.type_name)

    return render_template('author/author.html', author=author, quote=quote, work_types_num=work_types_num)

# page add author
#--------------------------------------------------
@app.route('/author/add', methods=['GET', 'POST'])
@require_admin
def add_author():
    if request.method == 'GET':
        dynasties = Dynasty.query.order_by(Dynasty.start_year)
        return render_template('author/add_author.html', dynasties=dynasties)
    else:
        author = Author(name=request.form['name'], abbr=request.form['abbr'], intro=request.form['intro'], birth_year=request.form['birth_year'], death_year=request.form['death_year'], dynasty_id=int(request.form['dynasty_id']))
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('author', author_abbr=author.abbr))

# page edit author
#--------------------------------------------------
@app.route('/author/<int:author_id>/edit', methods=['GET', 'POST'])
@require_admin
def edit_author(author_id):
    if request.method == 'GET':
        dynasties = Dynasty.query.order_by(Dynasty.start_year)
        author = Author.query.get(author_id)
        return render_template('author/edit_author.html', dynasties=dynasties, author=author)
    else:
        author = Author.query.get(author_id)
        author.name = request.form['name']
        author.abbr = request.form['abbr']
        author.intro = request.form['intro']
        author.birth_year = request.form['birth_year']
        author.death_year = request.form['death_year']
        author.dynasty_id = int(request.form['dynasty_id'])
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('author', author_abbr=author.abbr))

# page - admin quotes
#--------------------------------------------------
@app.route('/author/<int:author_id>/admin_quote')
@require_admin
def admin_quotes(author_id):
    author = Author.query.options(db.subqueryload(Author.quotes)).get(author_id)
    return render_template('author/admin_quotes.html', author=author)

# proc - add quote
@app.route('/author/<int:author_id>/add_quote', methods=['POST'])
@require_admin
def add_quote(author_id):
    quote = AuthorQuote(quote=request.form['quote'], author_id=author_id, work_id=int(request.form['work_id']))
    db.session.add(quote)
    db.session.commit()
    return redirect(url_for('admin_quotes', author_id=author_id))

# proc - delete quote
@app.route('/quote/<int:quote_id>/delete')
@require_admin
def delete_quote(quote_id):
    quote = AuthorQuote.query.get(quote_id)
    db.session.delete(quote)
    db.session.commit()
    return redirect(url_for('admin_quotes', author_id=quote.author_id))

# page edit quote
#--------------------------------------------------
@app.route('/quote/<int:quote_id>/edit', methods=['GET', 'POST'])
@require_admin
def edit_quote(quote_id):   
    if request.method == 'GET':
        quote = AuthorQuote.query.get(quote_id)
        return render_template('author/edit_quote.html', quote=quote)
    else:
        quote = AuthorQuote.query.get(quote_id)
        quote.quote = request.form['quote']
        quote.work_id = int(request.form['work_id'])
        db.session.add(quote)
        db.session.commit()
        return redirect(url_for('admin_quotes', author_id=quote.work.author_id))