#-*- coding: UTF-8 -*-
import markdown2
from flask import render_template, request, redirect, url_for, json, abort
from xichuangzhu import app
from xichuangzhu import db
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.quote_model import Quote
from xichuangzhu.utils import require_admin

# page dynasty
#--------------------------------------------------
@app.route('/dynasty/<dynasty_abbr>')
def dynasty(dynasty_abbr):
    dynasty = Dynasty.query.filter(Dynasty.abbr==dynasty_abbr).one()
    if not dynasty:
        abort(404)

    authors = Author.query.filter(Author.dynasty_id==dynasty.id).order_by(db.func.rand()).limit(5)
    authors_num = Author.query.filter(Author.dynasty_id==dynasty.id).count()

    dynasties = Dynasty.query.order_by(Dynasty.start_year)
    
    return render_template('dynasty/dynasty.html', dynasty=dynasty, authors=authors, authors_num=authors_num, dynasties=dynasties)

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
        return redirect(url_for('dynasty/dynasty', dynasty_abbr=abbr))

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
        return redirect(url_for('dynasty/dynasty', dynasty_abbr=abbr))