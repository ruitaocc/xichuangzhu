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