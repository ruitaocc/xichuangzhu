#-*- coding: UTF-8 -*-
import os
import re
import uuid
from flask import render_template, request, redirect, url_for, json, session, abort
from xichuangzhu import app, db, config
from xichuangzhu.models.work_model import Work, WorkType, WorkTag, WorkImage, WorkReview
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.user_model import User
from xichuangzhu.models.collect_model import CollectWork, CollectWorkImage
from xichuangzhu.form import WorkImageForm
from xichuangzhu.utils import require_login, require_admin

# page - work
#--------------------------------------------------
@app.route('/work/<int:work_id>')
def work(work_id):
    work = Work.query.get_or_404(work_id)

    if 'user_id' in session:
        is_collected = CollectWork.query.filter(CollectWork.work_id==work_id).filter(CollectWork.user_id==session['user_id']).count() > 0
    else:
        is_collected = False

    reviews = work.reviews.order_by(WorkReview.create_time.desc()).filter(WorkReview.is_publish==True).limit(4)
    reviews_num = work.reviews.filter(WorkReview.is_publish==True).count()

    images = work.images.order_by(WorkImage.create_time).limit(9)
    images_num = work.images.count()

    other_works = Work.query.filter(Work.author_id==work.author_id).filter(Work.id!=work_id).limit(5)

    collectors = User.query.join(CollectWork).join(Work).filter(Work.id==work_id).limit(4)

    return render_template('work/work.html', work=work, reviews=reviews, reviews_num=reviews_num, images=images, images_num=images_num, collectors=collectors, is_collected=is_collected, other_works=other_works)

# proc - collect work
@app.route('/work/<int:work_id>/collect', methods=['GET'])
@require_login
def collect_work(work_id):
    collect = CollectWork(user_id=session['user_id'], work_id=work_id)
    db.session.add(collect)
    db.session.commit()
    return redirect(url_for('work', work_id=work_id))

# proc - discollect work
@app.route('/work/<int:work_id>/discollect')
@require_login
def discollect_work(work_id):
    db.session.query(CollectWork).filter(CollectWork.user_id==session['user_id']).filter(CollectWork.work_id==work_id).delete()
    db.session.commit()
    return redirect(url_for('work', work_id=work_id))

# page - all works
#--------------------------------------------------
@app.route('/works')
def works():
    work_type = request.args.get('type', 'all')
    dynasty_abbr = request.args.get('dynasty', 'all')
    page = int(float(request.args.get('page', 1)))

    query = Work.query
    if work_type != 'all':
        query = query.filter(Work.type.has(WorkType.en==work_type))
    if dynasty_abbr != 'all':
        query = query.filter(Work.author.has(Author.dynasty.has(Dynasty.abbr==dynasty_abbr)))
    pagination = query.paginate(page, 10)

    work_types = WorkType.query

    dynasties = Dynasty.query.order_by(Dynasty.start_year)

    return render_template('work/works.html', pagination=pagination, work_type=work_type, dynasty_abbr=dynasty_abbr, work_types=work_types, dynasties=dynasties)

# page - works by tag
#--------------------------------------------------
@app.route('/works_by_tag/<tag>')
def works_by_tag(tag):
    page = int(request.args.get('page', 1))
    pagination = Work.query.filter(Work.tags.any(WorkTag.tag==tag)).paginate(page, 10)
    return render_template('work/works_by_tag.html', tag=tag, pagination=pagination)

# page - add work
#--------------------------------------------------
@app.route('/work/add', methods=['GET', 'POST'])
@require_admin
def add_work():
    if request.method == 'GET':
        if 'author_id' in request.args:
            author = Author.query.get_or_404(request.args['author_id'])
        else:
            author = None
        work_types = WorkType.query
        return render_template('work/add_work.html', work_types=work_types, author=author)
    else:        
        work = Work(title=request.form['title'], content=request.form['content'], foreword=request.form['foreword'], intro=request.form['intro'], author_id = int(request.form['author_id']), type_id=request.form['type_id'])
        db.session.add(work)
        db.session.commit()
        return redirect(url_for('work', work_id=work.id))

# page - edit work
#--------------------------------------------------
@app.route('/work/<int:work_id>/edit', methods=['GET', 'POST'])
@require_admin
def edit_work(work_id):
    work = Work.query.get_or_404(work_id)
    if request.method == 'GET':
        work_types = WorkType.query
        return render_template('work/edit_work.html', work=work, work_types=work_types)
    else:
        work.title = request.form['title']
        work.content = request.form['content']
        work.foreword = request.form['foreword']
        work.intro = request.form['intro']
        work.author_id = int(request.form['author_id'])
        work.type_id = request.form['type_id']
        db.session.add(work)
        db.session.commit()
        return redirect(url_for('work', work_id=work_id))

# page - reviews of this work
#--------------------------------------------------
@app.route('/work/<int:work_id>/reviews')
def work_reviews(work_id):
    work = Work.query.get_or_404(work_id)
    page = int(request.args.get('page', 1))
    pagination = work.reviews.filter(WorkReview.is_publish==True).order_by(WorkReview.create_time.desc()).paginate(page, 10)
    return render_template('work/work_reviews.html', work=work , pagination=pagination)

# page - images of this work
#--------------------------------------------------
@app.route('/work/<int:work_id>/images', methods=['GET'])
def work_images(work_id):
    work = Work.query.get_or_404(work_id)
    page = int(request.args.get('page', 1))
    pagination = work.images.order_by(WorkImage.create_time.desc()).paginate(page, 12)
    return render_template('work/work_images.html', work=work, pagination=pagination)

# json - search authors in page add & edit work
#--------------------------------------------------
@app.route('/work/search_authors', methods=['POST'])
@require_admin
def search_authors():
    author_name = request.form['author_name']
    authors = Author.query.filter(Author.name.like('%%%s%%' % author_name))

    # build json data of authors
    dict_authors = []
    for a in authors:
        dict_authors.append({ 'id': a.id, 'dynasty': a.dynasty.name, 'name': a.name })
    return json.dumps(dict_authors)
