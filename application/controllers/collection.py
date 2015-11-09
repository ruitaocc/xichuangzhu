# coding: utf-8
from flask import Blueprint, render_template
from ..utils.permissions import AdminPermission

bp = Blueprint('collection', __name__)


@bp.route('/collection/add', methods=['GET', 'POST'])
@AdminPermission()
def add():
    return render_template('collection/add/add.html')


@bp.route('/collection/edit', methods=['GET', 'POST'])
@AdminPermission()
def edit():
    return render_template('collection/edit/edit.html')


@bp.route('/collection/view')
def view():
    return render_template('collection/view/view.html')


@bp.route('/collections')
def collections():
    return render_template('collection/collections/collections.html')
