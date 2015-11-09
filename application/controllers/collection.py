# coding: utf-8
from flask import Blueprint, render_template, url_for, redirect
from ..utils.permissions import AdminPermission
from ..models import db, Collection, CollectionKind
from ..forms import CollectionForm

bp = Blueprint('collection', __name__)


@bp.route('/collection/add', methods=['GET', 'POST'])
@AdminPermission()
def add():
    """添加选集"""
    form = CollectionForm()
    form.kind_id.choices = [(c.id, c.name) for c in CollectionKind.query.order_by(CollectionKind.order.asc())]
    if form.validate_on_submit():
        collection = Collection(**form.data)
        collection_kind = CollectionKind.query.get_or_404(form.kind_id.data)
        collection.order = collection_kind.max_collection_order + 1
        db.session.add(collection)
        db.session.commit()
        return redirect(url_for('admin.collection_works', uid=collection.id))
    return render_template('collection/add/add.html', form=form)


@bp.route('/collection/<int:uid>/edit', methods=['GET', 'POST'])
@AdminPermission()
def edit(uid):
    """编辑选集"""
    collection = Collection.query.get_or_404(uid)
    form = CollectionForm(obj=collection)
    form.kind_id.choices = [(c.id, c.name) for c in CollectionKind.query.order_by(CollectionKind.order.asc())]
    if form.validate_on_submit():
        if collection.kind_id != form.kind_id.data:
            collection_kind = CollectionKind.query.get_or_404(form.kind_id.data)
            collection.order = collection_kind.max_collection_order + 1
        form.populate_obj(collection)
        db.session.add(collection)
        db.session.commit()
        return redirect(url_for('admin.collections'))
    return render_template('collection/edit/edit.html', form=form)


@bp.route('/collection/<int:uid>')
def view(uid):
    """选集"""
    collection = Collection.query.get_or_404(uid)
    return render_template('collection/view/view.html', collection=collection)


@bp.route('/collections')
def collections():
    """全部选集"""
    collection_kinds = CollectionKind.query.order_by(CollectionKind.order.asc())
    return render_template('collection/collections/collections.html', collection_kinds=collection_kinds)
