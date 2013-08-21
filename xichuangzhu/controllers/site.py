#-*- coding: UTF-8 -*-
import re
from flask import render_template, request, redirect, url_for, json
from xichuangzhu import app
from xichuangzhu.models.work_model import Work
from xichuangzhu.models.work_image import WorkImage
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.author_quote import AuthorQuote
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.review_model import WorkReview
from xichuangzhu.models.topic_model import Topic
from xichuangzhu.models.quote_model import Quote
from xichuangzhu.utils import time_diff
from sqlalchemy import func

# page home
#--------------------------------------------------
@app.route('/')
def index():
    # need to be random
    works = Work.query.order_by(func.rand()).limit(4)

    # work_images = Work.get_images_by_random(9)
    work_images = WorkImage.query.order_by(func.rand()).limit(9)

    # reviews = Review.get_reviews_by_random(4)
    # for r in reviews:
    #     r['Time'] = time_diff(r['Time'])

    work_reviews = WorkReview.query.filter(WorkReview.is_publish == True).order_by(func.rand()).limit(4)

    authors = Author.query.order_by(func.rand()).limit(5).all()

    dynasties = Dynasty.query.all()

    return render_template('site/index.html', works=works, work_images=work_images, work_reviews=work_reviews, authors=authors, dynasties=dynasties)

# json - gene works data for index page
@app.route('/4works', methods=['POST'])
def four_works():
    works = Work.query.order_by(func.rand()).limit(4)
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