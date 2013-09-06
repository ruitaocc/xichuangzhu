#-*- coding: UTF-8 -*-
import re
from flask import render_template, request, redirect, url_for, json, abort, session
from xichuangzhu import app, db
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.work_model import Work
from xichuangzhu.utils import require_admin

# page admin authors
#--------------------------------------------------
@app.route('/admin_authors', methods=['GET', 'POST'])
@require_admin
def admin_authors():
    authors = Author.query
    return render_template('admin/admin_authors.html', authors=authors)

# page admin works
#--------------------------------------------------
@app.route('/admin_works', methods=['GET', 'POST'])
@require_admin
def admin_works():
    works = Work.query
    return render_template('admin/admin_works.html', works=works)