# coding: utf-8
from flask import render_template, Blueprint, request, url_for
from ..models import db, Quote
from ..utils import jsonify, absolute_url_for

bp = Blueprint('api', __name__)


@bp.route('/get_random_quote')
@jsonify
def get_random_quote():
    quote = Quote.query.order_by(db.func.random()).first()
    return {
        'quote': quote.quote,
        'author': quote.author.name,
        'work': quote.work.title,
        'url': absolute_url_for('work.view', work_id=quote.work_id)
    }
