# coding: utf-8
from flask import render_template, request
from xichuangzhu import app
from ..models import Work, Author
from ..utils import require_admin


@app.route('/admin_authors', methods=['GET', 'POST'])
@require_admin
def admin_authors():
    """管理文学家"""
    authors = Author.query
    return render_template('admin/admin_authors.html', authors=authors)


@app.route('/admin_works', methods=['GET', 'POST'])
@require_admin
def admin_works():
    """管理作品"""
    page = int(request.args.get('page', 1))
    paginator = Work.query.paginate(page, 15)
    return render_template('admin/admin_works.html', paginator=paginator)