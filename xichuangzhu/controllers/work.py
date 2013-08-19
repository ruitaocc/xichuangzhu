#-*- coding: UTF-8 -*-
from __future__ import division
import os
import re
import math
import markdown2
import uuid
import config
from flask import render_template, request, redirect, url_for, json, session, abort
from xichuangzhu import app
from xichuangzhu.models.work_model import Work
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.review_model import Review
from xichuangzhu.models.collect_model import Collect
from xichuangzhu.models.product_model import Product
from xichuangzhu.models.tag_model import Tag
from xichuangzhu.form import WorkImageForm
from xichuangzhu.utils import time_diff, content_clean, require_login, require_admin, Pagination

# page - work
#--------------------------------------------------
@app.route('/work/<int:work_id>')
def work(work_id):
    work = Work.get_work(work_id)
    if not work:
        abort(404)

    # add comment, split ci, gene paragraph
    work['Content'] = re.sub(r'<([^<^b]+)>', r"<sup title='\1'></sup>", work['Content'])
    work['Content'] = work['Content'].replace('%', "&nbsp;&nbsp;")
    work['Content'] = markdown2.markdown(work['Content'])

    # check if is collected
    if 'user_id' in session:
        is_collected = Collect.check(session['user_id'], work_id)
        tags = Collect.get_tags(session['user_id'], work_id) if is_collected else ""
        my_tags = Tag.get_user_tags(session['user_id'], 20)
        popular_tags = Tag.get_work_tags(work_id, 20)
    else:
        is_collected = False
        tags = ""
        my_tags = []
        popular_tags = []

    reviews = Review.get_reviews_by_work(work_id)
    for r in reviews:
        r['Time'] = time_diff(r['Time'])

    product = Product.get_product_by_random()

    work_images = Work.get_images_by_work(work_id, 9)

    other_works = Work.get_other_works_by_author(work['AuthorID'], work_id, 5)
    for ow in other_works:
        ow['Content'] = content_clean(ow['Content'])

    collectors = Collect.get_users_by_work(work_id, 4)

    return render_template('work/work.html', work=work, tags=tags, my_tags=my_tags, popular_tags=popular_tags, reviews=reviews, is_collected=is_collected, product=product, other_works=other_works, collectors=collectors, work_images=work_images)

# proc - collect work
@app.route('/work/<int:work_id>/collect', methods=['POST'])
@require_login
def collect_work(work_id):
    tags = request.form['tags'].split(' ')

    # remove the empty & repeat item
    new_tags = []
    for t in tags:
        if t != '':
            new_tags.append(t)
    new_tags = list(set(new_tags))

    # collect work
    Collect.add(session['user_id'], work_id, ' '.join(new_tags) + ' ')

    # update user tags & work tags
    for t in new_tags:
        Tag.add_tag(t)
        Tag.add_user_tag(session['user_id'], t)
        Tag.add_work_tag(work_id, t)

    return redirect(url_for('work', work_id=work_id))

# proc - discollect work
@app.route('/work/<int:work_id>/discollect')
@require_login
def discollect_work(work_id):
    Collect.remove(session['user_id'], work_id)
    return redirect(url_for('work', work_id=work_id))

# page - all works
#--------------------------------------------------
@app.route('/works')
def works():
    per_page = 10
    work_type = request.args['type'] if 'type' in request.args else 'all'
    dynasty_abbr = request.args['dynasty'] if 'dynasty' in request.args else 'all'
    page = int(request.args['page'] if 'page' in request.args else 1)

    works = Work.get_works(work_type, dynasty_abbr, page, per_page)
    for work in works:
        work['Content'] = content_clean(work['Content'])

    works_num = Work.get_works_num(work_type, dynasty_abbr)

    pagination = Pagination(page, per_page, works_num)

    work_types = Work.get_types()

    dynasties = Dynasty.get_dynasties()

    return render_template('work/works.html', works=works, works_num=works_num, work_types=work_types, dynasties=dynasties, pagination=pagination, work_type=work_type, dynasty_abbr=dynasty_abbr)

# page - works by tag
#--------------------------------------------------
@app.route('/tag/<tag>')
def works_by_tag(tag):
    per_page = 10
    page = int(request.args['page'] if 'page' in request.args else 1)

    works = Work.get_works_by_tag(tag, page, per_page)
    for work in works:
        work['Content'] = content_clean(work['Content'])

    works_num = Work.get_works_num_by_tag(tag)

    pagination = Pagination(page, per_page, works_num)

    return render_template('work/works_by_tag.html', works=works, tag=tag, pagination=pagination)

# page - add work
#--------------------------------------------------
@app.route('/work/add', methods=['GET', 'POST'])
@require_admin
def add_work():
    if request.method == 'GET':
        work_types = Work.get_types()
        return render_template('work/add_work.html', work_types=work_types)
    else:
        title = request.form['title']
        content = request.form['content']
        foreword = request.form['foreword']
        intro = request.form['introduction']
        authorID = int(request.form['authorID'])
        dynastyID = int(Dynasty.get_dynastyID_by_author(authorID))
        work_type = request.form['type']
        type_name = Work.get_type_name(work_type)
        
        new_work_id = Work.add_work(title, content, foreword, intro, authorID, dynastyID, work_type, type_name)
        return redirect(url_for('work', work_id=new_work_id))

# page - edit work
#--------------------------------------------------
@app.route('/work/<int:work_id>/edit', methods=['GET', 'POST'])
@require_admin
def edit_work(work_id):
    if request.method == 'GET':
        work = Work.get_work(work_id)
        work_types = Work.get_types()
        return render_template('work/edit_work.html', work=work, work_types=work_types)
    else:
        title = request.form['title']
        content = request.form['content']
        foreword = request.form['foreword']
        intro = request.form['introduction']
        author_id = int(request.form['authorID'])
        dynasty_id = int(Dynasty.get_dynastyID_by_author(author_id))
        work_type = request.form['type']
        type_name = Work.get_type_name(work_type)

        Work.edit_work(title, content, foreword, intro ,author_id, dynasty_id, work_type, type_name, work_id)
        return redirect(url_for('work', work_id=work_id))



# page - work image
#--------------------------------------------------
@app.route('/work_image/<int:work_image_id>', methods=['GET'])
def work_image(work_image_id):
    work_image = Work.get_image(work_image_id)
    work = Work.get_work(work_image['work_id'])
    work['Content'] = content_clean(work['Content'])
    return render_template('work/work_image.html', work=work, work_image=work_image)

# page - add work image
#--------------------------------------------------
@app.route('/work/<int:work_id>/add_image', methods=['GET', 'POST'])
@require_login
def add_work_image(work_id):
    work = Work.get_work(work_id)
    form = WorkImageForm()
    if request.method == 'GET':        
        return render_template('work/add_work_image.html', work=work, form=form)
    else:
        if form.validate():
            # Save image
            image = request.files['image']
            image_filename = str(uuid.uuid1()) + '.' + image.filename.split('.')[-1]
            image.save(config.IMAGE_PATH + image_filename)

            image_id = Work.add_image(work_id, session['user_id'], config.IMAGE_URL+image_filename, image_filename)
            return redirect(url_for('work_image', work_image_id=image_id))
        else:
            return render_template('work/add_work_image.html', work=work, form=form)


# page - edit work image
#--------------------------------------------------
@app.route('/work_image/<int:work_image_id>/edit', methods=['GET', 'POST'])
@require_login
def edit_work_image(work_image_id):
    work_image = Work.get_image(work_image_id)
    form = WorkImageForm()
    if request.method == 'GET':
        return render_template('work/edit_work_image.html', work_image=work_image, form=form)
    else:
        if form.validate():
            # Delete old image
            if os.path.isfile(config.IMAGE_PATH + work_image['filename']):
                os.remove(config.IMAGE_PATH + work_image['filename'])

            # Save new image
            image = request.files['image']
            image_filename = str(uuid.uuid1()) + '.' + image.filename.split('.')[-1]
            image.save(config.IMAGE_PATH + image_filename)

            # update image info
            Work.update_image(work_image_id, config.IMAGE_URL+image_filename, image_filename)
            return redirect(url_for('work_image', work_image_id=work_image['id']))
        else:
            return render_template('work/edit_work_image.html', work_image=work_image, form=form)

# proc - delete work image
@app.route('/work_image/<int:work_image_id>/delete', methods=['GET'])
@require_login
def delete_work_image(work_image_id):
    work_image = Work.get_image(work_image_id)
    if not work_image or work_image['user_id'] != session['user_id']:
        abort(404)

    # delete image file
    if os.path.isfile(config.IMAGE_PATH + work_image['filename']):
        os.remove(config.IMAGE_PATH + work_image['filename'])

    Work.delete_image(work_image_id)
    return redirect(url_for('work', work_id=work_image['work_id']))

# json - search authors in page add & edit work
#--------------------------------------------------
@app.route('/work/search_authors', methods=['POST'])
@require_admin
def get_authors_by_name():
    name = request.form['author']
    authors = Author.get_authors_by_name(name)
    return json.dumps(authors)