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
    dynasty = Dynasty.query.filter(Dynasty.abbr==dynasty_abbr).first_or_404()
    dynasties = Dynasty.query.order_by(Dynasty.start_year)
    authors = Author.query.filter(Author.dynasty_id==dynasty.id).order_by(db.func.rand()).limit(5)
    authors_num = Author.query.filter(Author.dynasty_id==dynasty.id).count()
    return render_template('dynasty/dynasty.html', dynasty=dynasty, authors=authors, authors_num=authors_num, dynasties=dynasties)

# page add dynasty
#--------------------------------------------------
@app.route('/dynasty/add', methods=['GET', 'POST'])
@require_admin
def add_dynasty():
    if request.method == 'GET':
        return render_template('dynasty/add_dynasty.html')
    else:
        dynasty = Dynasty(name=request.form['name'], abbr=request.form['abbr'], intro=request.form['intro'], start_year=int(request.form['start_year']), end_year=int(request.form['end_year']))
        db.session.add(dynasty)
        db.session.commit()
        return redirect(url_for('dynasty', dynasty_abbr=dynasty.abbr))

# page edit dynasty
#--------------------------------------------------
@app.route('/dynasty/edit/<int:dynasty_id>', methods=['GET', 'POST'])
@require_admin
def edit_dynasty(dynasty_id):
    if request.method == 'GET':
        dynasty = Dynasty.query.get_or_404(dynasty_id)
        return render_template('dynasty/edit_dynasty.html', dynasty=dynasty)
    else:
        dynasty = Dynasty.query.get_or_404(dynasty_id)
        dynasty.name = request.form['name']
        dynasty.abbr = request.form['abbr']
        dynasty.intro = request.form['intro']
        dynasty.start_year = int(request.form['start_year'])
        dynasty.end_year = int(request.form['end_year'])
        db.session.add(dynasty)
        db.session.commit()
        return redirect(url_for('dynasty', dynasty_abbr=dynasty.abbr))