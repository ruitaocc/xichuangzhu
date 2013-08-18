#-*- coding: UTF-8 -*-
import re
from flask import render_template, request, redirect, url_for, json
from xichuangzhu import app
from xichuangzhu.models.work_model import Work
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.review_model import Review
from xichuangzhu.models.topic_model import Topic
from xichuangzhu.models.quote_model import Quote
from xichuangzhu.utils import time_diff, content_clean

# page home
#--------------------------------------------------
@app.route('/')
def index():
    works = Work.get_works_by_random(4)
    for work in works:
        work['Content'] = content_clean(work['Content'])

    work_images = Work.get_images_by_random(9)

    reviews = Review.get_reviews_by_random(4)
    for r in reviews:
        r['Time'] = time_diff(r['Time'])
    
    authors = Author.get_authors_by_random(5)
    for a in authors:
        quote = Quote.get_quote_by_random(a['AuthorID'])
        a['Quote'] = quote['Quote'] if quote else ""
        a['QuoteID'] = quote['QuoteID'] if quote else 0
    
    dynasties = Dynasty.get_dynasties()
    topics = Topic.get_topics(8)
    return render_template('site/index.html', works=works, work_images=work_images, reviews=reviews, authors=authors, dynasties=dynasties, topics=topics)

# json - gene works data for index page
@app.route('/4works', methods=['POST'])
def four_works():
    works = Work.get_works_by_random(4)
    for work in works:
        work['Content'] = content_clean(work['Content'])
    return render_template('widget/index_works.widget', works=works)

# page about
#--------------------------------------------------
@app.route('/about')
def about():
    return render_template('site/about.html')

# page ad
#--------------------------------------------------
@app.route('/ad')
def ad():
    return render_template('site/ad.html')

# page 404
#-------------------------------------------------- 
@app.errorhandler(404)
def page_404(error):
    return render_template('site/404.html'), 404

# page 500
#-------------------------------------------------- 
@app.errorhandler(500)
def page_500(error):
    return render_template('site/500.html'), 500