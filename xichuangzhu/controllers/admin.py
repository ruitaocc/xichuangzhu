# coding: utf-8
from flask import render_template, Blueprint
from ..models import Work, Author
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
    paginator = Work.query.filter(Work.highlight == True).paginate(page, 15)
    return render_template('admin/highlight_works.html', paginator=paginator)