# coding: utf-8
import cgi
from flask import render_template, request, redirect, url_for, session, abort
from xichuangzhu import app, db
from xichuangzhu.models.topic import Topic, TopicComment
from xichuangzhu.form import TopicForm, CommentForm
from xichuangzhu.utils import require_login


@app.route('/topics')
def topics():
    """全部话题"""
    page = int(request.args.get('page', 1))
    pagination = Topic.query.order_by(Topic.create_time).paginate(page, 10)
    return render_template('topic/topics.html', pagination=pagination)


@app.route('/topic/<int:topic_id>')
def topic(topic_id):
    """话题"""
    form = CommentForm()
    topic = Topic.query.get_or_404(topic_id)
    topic.click_num += 1
    db.session.add(topic)
    db.session.commit()
    return render_template('topic/topic.html', topic=topic, form=form)


@app.route('/topic/<int:topic_id>/comment', methods=['POST'])
@require_login
def comment_topic(topic_id):
    """添加评论"""
    form = CommentForm(request.form)
    if form.validate():
        comment = TopicComment(content=cgi.escape(form.content.data), topic_id=topic_id, user_id=session['user_id'])
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('topic', topic_id=topic_id) + "#" + str(comment.id))
    return redirect(url_for('topic', topic_id=topic_id))


@app.route('/topic/add', methods=['POST', 'GET'])
@require_login
def add_topic():
    """添加话题"""
    if request.method == 'GET':
        form = TopicForm()
        return render_template('topic/add_topic.html', form=form)
    form = TopicForm(request.form)
    if form.validate():
        topic = Topic(title=cgi.escape(form.title.data), content=cgi.escape(form.content.data),
                      user_id=session['user_id'])
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('topic', topic_id=topic.id))
    return render_template('topic/add_topic.html', form=form)


@app.route('/topic/edit/<int:topic_id>', methods=['POST', 'GET'])
@require_login
def edit_topic(topic_id):
    """编辑话题"""
    topic = Topic.query.get_or_404(topic_id)
    if topic.user_id != session['user_id']:
        abort(404)

    if request.method == 'GET':
        form = TopicForm(title=topic.title, content=topic.content)
        return render_template('topic/edit_topic.html', topic=topic, form=form)
    form = TopicForm(request.form)
    if form.validate():
        topic.title = cgi.escape(form.title.data)
        topic.content = cgi.escape(form.content.data)
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('topic', topic_id=topic_id))
    return render_template('topic/edit_topic.html', topic=topic, form=form)