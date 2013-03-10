#-*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, json

from xichuangzhu import app

from xichuangzhu.models.work_model import Work
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.review_model import Review

import re

# Home Controller
#--------------------------------------------------

# page home
@app.route('/')
def index():
	# shi = Work.get_work_by_random('shi')
	# shi['type'] = '诗'

	# wen = Work.get_work_by_random('wen')
	# wen['type'] = '文'

	# ge = Work.get_work_by_random('ge')
	# ge['type'] = '歌'

	# ci = Work.get_work_by_random('ci')
	# ci['type'] = '词'

	# works = (shi, wen, ge, ci)
	# for work in works:
	# 	work['Content'] = re.sub(r'<([^<]+)>', '', work['Content'])
	# 	work['Content'] = work['Content'].replace('%', '').replace('/', '')
	
	works = Work.get_works_by_random(4)
	for work in works:
		work['Content'] = re.sub(r'<([^<]+)>', '', work['Content'])
		work['Content'] = work['Content'].replace('%', '').replace('/', '')

	reviews = Review.get_reviews_by_random(5)
	authors = Author.get_authors_by_random(5)
	dynasties = Dynasty.get_dynasties()
	return render_template('index.html', works=works, reviews=reviews, authors=authors, dynasties=dynasties)

# json - gene 4 works of different type
@app.route('/4works', methods=['POST'])
def four_works():
	# shi = Work.get_work_by_random('shi')
	# shi['type'] = '诗'

	# wen = Work.get_work_by_random('wen')
	# wen['type'] = '文'

	# ge = Work.get_work_by_random('ge')
	# ge['type'] = '歌'

	# ci = Work.get_work_by_random('ci')
	# ci['type'] = '词'

	# works = (shi, wen, ge, ci)
	# for work in works:
	# 	work['Content'] = re.sub(r'<([^<]+)>', '', work['Content'])
	# 	work['Content'] = work['Content'].replace('%', '').replace('/', '')

	works = Work.get_works_by_random(4)
	for work in works:
		work['Content'] = re.sub(r'<([^<]+)>', '', work['Content'])
		work['Content'] = work['Content'].replace('%', '').replace('/', '')
	return render_template('four_works.widget', works=works)