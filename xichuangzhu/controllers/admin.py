# coding: utf-8
from flask import render_template, request, Blueprint
from ..models import Work, Author
from ..utils import require_admin

bp = Blueprint('admin', __name__)


@bp.route('/authors', methods=['GET', 'POST'])
@require_admin
def authors():
    """管理文学家"""
    authors = Author.query
    return render_template('admin/authors.html', authors=authors)


@bp.route('/works', defaults={'page': 1})
@bp.route('/works/<int:page>', methods=['GET', 'POST'])
@require_admin
def works(page):
    """管理作品"""
    paginator = Work.query.paginate(page, 15)
    return render_template('admin/works.html', paginator=paginator)