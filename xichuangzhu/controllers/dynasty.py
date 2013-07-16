#-*- coding: UTF-8 -*-

import markdown2
from flask import render_template, request, redirect, url_for, json, abort
from xichuangzhu import app
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.quote_model import Quote
from xichuangzhu.utils import require_admin

# page single dynasty
#--------------------------------------------------
@app.route('/dynasty/<dynasty_abbr>')
def single_dynasty(dynasty_abbr):
    dynasty = Dynasty.get_dynasty_by_abbr(dynasty_abbr)
    if not dynasty:
        abort(404)

    authors_num = Author.get_authors_num_by_dynasty(dynasty['DynastyID'])
    authors = Author.get_authors_by_dynasty(dynasty['DynastyID'], 5, True)
    for a in authors:
        quote = Quote.get_quote_by_random(a['AuthorID'])
        a['Quote'] = quote['Quote'] if quote else ""
        a['QuoteID'] = quote['QuoteID'] if quote else 0
    
    dynasties = Dynasty.get_dynasties()
    
    return render_template('dynasty/single_dynasty.html', dynasty=dynasty, authors=authors, authors_num=authors_num, dynasties=dynasties)

# page add dynasty
#--------------------------------------------------
@app.route('/dynasty/add', methods=['GET', 'POST'])
@require_admin
def add_dynasty():
    if request.method == 'GET':
        return render_template('dynasty/add_dynasty.html')
    else:
        dynasty = request.form['dynasty']
        abbr = request.form['abbr']
        introduction = request.form['introduction']
        startYear = int(request.form['startYear'])
        endYear = int(request.form['endYear'])
        Dynasty.add_dynasty(dynasty, abbr, introduction, startYear, endYear)
        return redirect(url_for('dynasty/single_dynasty', dynasty_abbr=abbr))

# page edit dynasty
#--------------------------------------------------
@app.route('/dynasty/edit/<int:dynasty_id>', methods=['GET', 'POST'])
@require_admin
def edit_dynasty(dynasty_id):
    if request.method == 'GET':
        dynasty = Dynasty.get_dynasty(dynasty_id)
        return render_template('dynasty/edit_dynasty.html', dynasty=dynasty)
    else:
        dynasty = request.form['dynasty']
        abbr = request.form['abbr']
        introduction = request.form['introduction']
        history = request.form['history']
        startYear = int(request.form['startYear'])
        endYear = int(request.form['endYear'])
        Dynasty.edit_dynasty(dynasty, abbr, introduction, history, startYear, endYear, dynasty_id)
        return redirect(url_for('dynasty/single_dynasty', dynasty_abbr=abbr))