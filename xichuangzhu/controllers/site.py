# coding: utf-8
from flask import render_template, Blueprint
from xichuangzhu import db
from ..models import Work, WorkImage, WorkReview, Author, Dynasty

bp = Blueprint('site', __name__)


@bp.route('/')
def index():
    """首页"""
    works = Work.query.order_by(db.func.rand()).limit(4)
    work_images = WorkImage.query.order_by(WorkImage.create_time.desc()).limit(18)
    work_reviews = WorkReview.query.filter(WorkReview.is_publish == True).order_by(WorkReview.create_time.desc()).limit(
        4)
    authors = Author.query.order_by(db.func.rand()).limit(5)
    dynasties = Dynasty.query.order_by(Dynasty.start_year)
    return render_template('site/index.html', works=works, work_images=work_images, work_reviews=work_reviews,
                           authors=authors, dynasties=dynasties)


@bp.route('/works', methods=['POST'])
def works():
    """生成首页需要的作品json数据"""
    works = Work.query.order_by(db.func.rand()).limit(4)
    return render_template('macro/index_works.html', works=works)


@bp.route('/about')
def about():
    """关于页"""
    return render_template('site/about.html')


@bp.errorhandler(404)
def page_404(error):
    """404错误页"""
    return render_template('site/404.html'), 404


@bp.errorhandler(500)
def page_500(error):
    """500错误页"""
    return render_template('site/500.html'), 500