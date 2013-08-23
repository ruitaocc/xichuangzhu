#-*- coding: UTF-8 -*-
from __future__ import division
import os
import re
import math
import uuid
import config
from flask import render_template, request, redirect, url_for, json, session, abort
from xichuangzhu import app
from xichuangzhu import db
from xichuangzhu.models.work_model import Work, WorkType, WorkTag
from xichuangzhu.models.work_image import WorkImage
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.review_model import WorkReview
from xichuangzhu.models.review_model import Review
from xichuangzhu.models.collect_model import Collect
from xichuangzhu.models.user_model import User
from xichuangzhu.models.collect import CollectWork, CollectWorkImage
from xichuangzhu.models.tag_model import Tag
from xichuangzhu.form import WorkImageForm
from xichuangzhu.utils import time_diff, require_login, require_admin

# page - single work image
#--------------------------------------------------
@app.route('/work_image/<int:work_image_id>', methods=['GET'])
def work_image(work_image_id):
    work_image = Work.get_image(work_image_id)
    work = Work.get_work(work_image['work_id'])
    work['Content'] = content_clean(work['Content'])

    if 'user_id' in session:
        is_collected = Collect.check_collect_work_image(session['user_id'], work_image_id)
    else:
        is_collected = False

    return render_template('work/work_image.html', work=work, work_image=work_image, is_collected=is_collected)

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

# proc - collect work image
@app.route('/work_image/<int:work_image_id>/collect', methods=['GET'])
@require_login
def collect_work_image(work_image_id):
    Collect.collect_work_image(session['user_id'], work_image_id)
    return redirect(url_for('work_image', work_image_id=work_image_id))

# proc - discollect work image
@app.route('/work_image/<int:work_image_id>/discollect', methods=['GET'])
@require_login
def discollect_work_image(work_image_id):
    Collect.discollect_work_image(session['user_id'], work_image_id)
    return redirect(url_for('work_image', work_image_id=work_image_id))

# page - all work images
#--------------------------------------------------
@app.route('/all_work_images', methods=['GET'])
def all_work_images():
    # pagination
    per_page = 9
    page = int(request.args['page'] if 'page' in request.args else 1)

    work_images = Work.get_images(page, per_page)
    work_images_num = Work.get_images_num()

    pagination = Pagination(page, per_page, work_images_num)

    return render_template('work/all_work_images.html', work_images=work_images, work_images_num=work_images_num, pagination=pagination)

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