# coding: utf-8
from flask import render_template, request, redirect, url_for, Blueprint
from xichuangzhu import db
from ..models import Dynasty
from ..utils import require_admin

bp = Blueprint('dynasty', __name__)


@bp.route('/<dynasty_abbr>')
def view(dynasty_abbr):
    """朝代信息"""
    dynasties = Dynasty.query.order_by(Dynasty.start_year)
    dynasty = Dynasty.query.filter(Dynasty.abbr == dynasty_abbr).first_or_404()
    authors = dynasty.authors.order_by(db.func.rand()).limit(5)
    authors_num = dynasty.authors.count()
    return render_template('dynasty/dynasty.html', dynasty=dynasty, authors=authors, authors_num=authors_num,
                           dynasties=dynasties)


@bp.route('/add', methods=['GET', 'POST'])
@require_admin
def add():
    """添加朝代"""
    if request.method == 'GET':
        return render_template('dynasty/add.html')
    dynasty = Dynasty(name=request.form['name'], abbr=request.form['abbr'], intro=request.form['intro'],
                      start_year=int(request.form['start_year']), end_year=int(request.form['end_year']))
    db.session.add(dynasty)
    db.session.commit()
    return redirect(url_for('.view', dynasty_abbr=dynasty.abbr))


@bp.route('/<int:dynasty_id>/edit', methods=['GET', 'POST'])
@require_admin
def edit(dynasty_id):
    """编辑朝代信息"""
    if request.method == 'GET':
        dynasty = Dynasty.query.get_or_404(dynasty_id)
        return render_template('dynasty/edit.html', dynasty=dynasty)
    else:
        dynasty = Dynasty.query.get_or_404(dynasty_id)
        dynasty.name = request.form['name']
        dynasty.abbr = request.form['abbr']
        dynasty.intro = request.form['intro']
        dynasty.start_year = int(request.form['start_year'])
        dynasty.end_year = int(request.form['end_year'])
        db.session.add(dynasty)
        db.session.commit()
        return redirect(url_for('.view', dynasty_abbr=dynasty.abbr))