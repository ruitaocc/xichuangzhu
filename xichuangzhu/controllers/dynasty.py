# coding: utf-8
from flask import render_template, redirect, url_for, Blueprint
from ..models import db, Dynasty, Author
from ..forms import DynastyForm
from ..permissions import AdminPermission

bp = Blueprint('dynasty', __name__)


@bp.route('/<dynasty_abbr>')
def view(dynasty_abbr):
    """朝代"""
    dynasties = Dynasty.query.order_by(Dynasty.start_year.asc())
    dynasty = Dynasty.query.filter(Dynasty.abbr == dynasty_abbr).first_or_404()
    authors = Author.query.filter(Author.dynasty_id == dynasty.id).order_by(db.func.random()) \
        .limit(5)
    return render_template('dynasty/dynasty.html', dynasty=dynasty, authors=authors,
                           dynasties=dynasties)


@bp.route('/add', methods=['GET', 'POST'])
@AdminPermission()
def add():
    """添加朝代"""
    form = DynastyForm()
    if form.validate_on_submit():
        dynasty = Dynasty(**form.data)
        db.session.add(dynasty)
        db.session.commit()
        return redirect(url_for('.view', dynasty_abbr=dynasty.abbr))
    return render_template('dynasty/add.html', form=form)


@bp.route('/<int:dynasty_id>/edit', methods=['GET', 'POST'])
@AdminPermission()
def edit(dynasty_id):
    """编辑朝代"""
    dynasty = Dynasty.query.get_or_404(dynasty_id)
    form = DynastyForm(obj=dynasty)
    if form.validate_on_submit():
        form.populate_obj(dynasty)
        db.session.add(dynasty)
        db.session.commit()
        return redirect(url_for('.view', dynasty_abbr=dynasty.abbr))
    return render_template('dynasty/edit.html', dynasty=dynasty, form=form)