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
from xichuangzhu.models.work_model import Work, WorkType, WorkTag, WorkImage, WorkReview
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.user_model import User
from xichuangzhu.models.collect_model import CollectWork, CollectWorkImage
from xichuangzhu.form import WorkImageForm
from xichuangzhu.utils import require_login, require_admin

# page - single work image
#--------------------------------------------------
@app.route('/work_image/<int:work_image_id>', methods=['GET'])
def work_image(work_image_id):
    work_image = WorkImage.query.get_or_404(work_image_id)

    if 'user_id' in session:
        is_collected = CollectWorkImage.query.filter(CollectWorkImage.user_id==session['user_id']).filter(CollectWorkImage.work_image_id==work_image_id).count() > 0
    else:
        is_collected = False

    return render_template('work_image/work_image.html', work_image=work_image, is_collected=is_collected)

# proc - delete work image
@app.route('/work_image/<int:work_image_id>/delete', methods=['GET'])
@require_login
def delete_work_image(work_image_id):
    work_image = WorkImage.query.get_or_404(work_image_id)
    if work_image.user_id != session['user_id']:
        abort(404)

    # delete image file
    if os.path.isfile(config.IMAGE_PATH + work_image.filename):
        os.remove(config.IMAGE_PATH + work_image.filename)

    db.session.delete(work_image)
    db.session.commit()

    return redirect(url_for('work', work_id=work_image.work_id))

# proc - collect work image
@app.route('/work_image/<int:work_image_id>/collect', methods=['GET'])
@require_login
def collect_work_image(work_image_id):
    collect = CollectWorkImage(user_id=session['user_id'], work_image_id=work_image_id)
    db.session.add(collect)
    db.session.commit()
    return redirect(url_for('work_image', work_image_id=work_image_id))

# proc - discollect work image
@app.route('/work_image/<int:work_image_id>/discollect', methods=['GET'])
@require_login
def discollect_work_image(work_image_id):
    db.session.query(CollectWorkImage).filter(CollectWorkImage.user_id==session['user_id']).filter(CollectWorkImage.work_image_id==work_image_id).delete()
    db.session.commit()
    return redirect(url_for('work_image', work_image_id=work_image_id))

# page - all work images
#--------------------------------------------------
@app.route('/all_work_images', methods=['GET'])
def all_work_images():
    page = int(request.args.get('page', 1))
    pagination = WorkImage.query.paginate(page, 12)
    return render_template('work_image/all_work_images.html', pagination=pagination)

# page - add work image
#--------------------------------------------------
@app.route('/work/<int:work_id>/add_image', methods=['GET', 'POST'])
@require_login
def add_work_image(work_id):
    work = Work.query.get_or_404(work_id)
    form = WorkImageForm()
    if request.method == 'GET':        
        return render_template('work_image/add_work_image.html', work=work, form=form)
    else:
        if form.validate():
            # Save image
            image = request.files['image']
            image_filename = str(uuid.uuid1()) + '.' + image.filename.split('.')[-1]
            image.save(config.IMAGE_PATH + image_filename)

            work_image = WorkImage(work_id=work_id, user_id=session['user_id'], url=config.IMAGE_URL+image_filename, filename=image_filename)
            db.session.add(work_image)
            db.session.commit()
            return redirect(url_for('work_image', work_image_id=work_image.id))
        else:
            return render_template('work_image/add_work_image.html', work=work, form=form)

# page - edit work image
#--------------------------------------------------
@app.route('/work_image/<int:work_image_id>/edit', methods=['GET', 'POST'])
@require_login
def edit_work_image(work_image_id):
    work_image = WorkImage.query.get_or_404(work_image_id)
    form = WorkImageForm()
    if request.method == 'GET':
        return render_template('work_image/edit_work_image.html', work_image=work_image, form=form)
    else:
        if form.validate():
            # Delete old image
            if os.path.isfile(config.IMAGE_PATH + work_image.filename):
                os.remove(config.IMAGE_PATH + work_image.filename)

            # Save new image
            image = request.files['image']
            image_filename = str(uuid.uuid1()) + '.' + image.filename.split('.')[-1]
            image.save(config.IMAGE_PATH + image_filename)

            # update image info
            work_image.url = config.IMAGE_URL + image_filename
            work_image.filename = image_filename
            db.session.add(work_image)
            db.session.commit()
            return redirect(url_for('work_image', work_image_id=work_image_id))
        else:
            return render_template('work_image/edit_work_image.html', work_image=work_image, form=form)