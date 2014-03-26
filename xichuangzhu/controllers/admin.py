# coding: utf-8
from flask import render_template, Blueprint, request
from ..models import Work, Author, Dynasty, WorkType
from ..permissions import admin_permission

bp = Blueprint('admin', __name__)


@bp.route('/authors', methods=['GET', 'POST'])
@admin_permission
def authors():
    """管理文学家"""
    authors = Author.query
    return render_template('admin/authors.html', authors=authors)


@bp.route('/works', defaults={'page': 1})
@bp.route('/works/page/<int:page>', methods=['GET', 'POST'])
@admin_permission
def works(page):
    """管理作品"""
    paginator = Work.query.paginate(page, 15)
    return render_template('admin/works.html', paginator=paginator)


@bp.route('/highlight_works', defaults={'page': 1})
@bp.route('/highlight_works/page/<int:page>', methods=['GET', 'POST'])
@admin_permission
def highlight_works(page):
    """全部加精作品"""
    work_type = request.args.get('type', 'all')
    dynasty_abbr = request.args.get('dynasty', 'all')
    works = Work.query.filter(Work.highlight == True)
    if work_type != 'all':
        works = works.filter(Work.type.has(WorkType.en == work_type))
    if dynasty_abbr != 'all':
        works = works.filter(Work.author.has(Author.dynasty.has(Dynasty.abbr == dynasty_abbr)))
    paginator = works.paginate(page, 15)
    work_types = WorkType.query
    dynasties = Dynasty.query.order_by(Dynasty.start_year.asc())
    return render_template('admin/highlight_works.html', paginator=paginator, work_type=work_type,
                           dynasty_abbr=dynasty_abbr, work_types=work_types, dynasties=dynasties)
