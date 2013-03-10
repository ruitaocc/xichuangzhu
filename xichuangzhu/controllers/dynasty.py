from flask import render_template, request, redirect, url_for, json, render_template_string

from xichuangzhu import app

from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.author_model import Author

import markdown2

# page single dynasty
#--------------------------------------------------

@app.route('/dynasty/<dynasty_abbr>')
def single_dynasty(dynasty_abbr):
	dynasty = Dynasty.get_dynasty_by_abbr(dynasty_abbr)
	dynasty['History'] = markdown2.markdown(dynasty['History'])

	authors = Author.get_authors_by_dynasty(dynasty['DynastyID'], 5)
	authors_num = Author.get_authors_num_by_dynasty(dynasty['DynastyID'])
	
	dynasties = Dynasty.get_dynasties()
	
	return render_template('single_dynasty.html', dynasty=dynasty, authors=authors, authors_num=authors_num, dynasties=dynasties)

# page add dynasty
#--------------------------------------------------
@app.route('/dynasty/add', methods=['GET', 'POST'])
def add_dynasty():
	if request.method == 'GET':
		return render_template('add_dynasty.html')
	elif request.method == 'POST':
		dynasty      = request.form['dynasty']
		abbr         = request.form['abbr']
		introduction = request.form['introduction']
		startYear    = int(request.form['startYear'])
		endYear      = int(request.form['endYear'])
		Dynasty.add_dynasty(dynasty, abbr, introduction, startYear, endYear)
		return redirect(url_for('single_dynasty', dynasty_abbr=abbr))

# page edit dynasty
#--------------------------------------------------
@app.route('/dynasty/edit/<int:dynasty_id>', methods=['GET', 'POST'])
def edit_dynasty(dynasty_id):
	if request.method == 'GET':
		dynasty = Dynasty.get_dynasty(dynasty_id)
		return render_template('edit_dynasty.html', dynasty=dynasty)
	elif request.method == 'POST':
		dynasty      = request.form['dynasty']
		abbr         = request.form['abbr']
		introduction = request.form['introduction']
		history      = request.form['history']
		startYear    = int(request.form['startYear'])
		endYear      = int(request.form['endYear'])
		Dynasty.edit_dynasty(dynasty, abbr, introduction, history, startYear, endYear, dynasty_id)
		return redirect(url_for('single_dynasty', dynasty_abbr=abbr))

# json - get single dynasty info
#--------------------------------------------------
@app.route('/dynasty/json', methods=['POST'])
def get_dynasty_by_json():
	dynasty_id = int(request.form['dynasty_id'])
	dynasty = Dynasty.get_dynasty(dynasty_id)
	authors = Author.get_authors_by_dynasty(dynasty_id)
	return render_template('single_dynasty.widget', dynasty=dynasty, authors=authors)
