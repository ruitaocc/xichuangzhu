# coding: utf-8
from flask import render_template, redirect, url_for, session, abort, Blueprint
from ..models import db, Topic, TopicComment
from ..forms import TopicForm, TopicCommentForm
from ..utils import require_login


bp = Blueprint('topic', __name__)


@bp.route('/topic/<int:topic_id>', methods=['POST', 'GET'])
def view(topic_id):
    """话题"""
    form = TopicCommentForm()
    topic = Topic.query.get_or_404(topic_id)
    topic.click_num += 1
    db.session.add(topic)
    db.session.commit()
    if form.validate_on_submit():
        comment = TopicComment(user_id=session['user_id'], **form.data)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.view', topic_id=topic_id) + "#" + str(comment.id))
    return render_template('topic/topic.html', topic=topic, form=form)

@bp.route('/topics', defaults={'page': 1})
@bp.route('/topics/<int:page>')
def topics(page):
    """全部话题"""
    paginator = Topic.query.order_by(Topic.create_time).paginate(page, 10)
    return render_template('topic/topics.html', paginator=paginator)


@bp.route('/add', methods=['POST', 'GET'])
@require_login
def add():
    """添加话题"""
    form = TopicForm()
    if form.validate_on_submit():
        topic = Topic(user_id=session['user_id'], **form.data)
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('.view', topic_id=topic.id))
    return render_template('topic/add.html', form=form)


@bp.route('/topic/<int:topic_id>/edit', methods=['POST', 'GET'])
@require_login
def edit(topic_id):
    """编辑话题"""
    topic = Topic.query.get_or_404(topic_id)
    if topic.user_id != session['user_id']:
        abort(404)
    form = TopicForm(obj=topic)
    if form.validate_on_submit():
        form.populate_obj(topic)
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('.view', topic_id=topic_id))
    return render_template('topic/edit.html', topic=topic, form=form)


@bp.route('/topic/<int:topic_id>/delete')
@require_login
def delete(topic_id):
    """删除话题"""
    topic = Topic.query.get_or_404(topic_id)
    if topic.user_id != session['user_id']:
        abort(404)
    db.session.delete(topic)
    db.session.commit()
    return redirect(url_for('.topics'))