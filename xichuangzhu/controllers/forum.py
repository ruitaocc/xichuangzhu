#-*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, json, session

from xichuangzhu import app

from xichuangzhu.models.topic_model import Topic
from xichuangzhu.models.node_model import Node
from xichuangzhu.models.comment_model import Comment
from xichuangzhu.models.user_model import User
from xichuangzhu.models.inform_model import Inform

from xichuangzhu.utils import time_diff, get_comment_replyee_id, rebuild_comment, build_topic_inform_title

import cgi
import markdown2

# page forum
#--------------------------------------------------

@app.route('/forum')
def forum():
	topics = Topic.get_topics(15)
	for t in topics:
		t['Time'] = time_diff(t['Time'])

	nodes = Node.get_nodes(16)

	hot_topics = Topic.get_hot_topics(10)
	
	node_types = Node.get_types()
	for nt in node_types:
		nt['nodes'] = Node.get_nodes_by_type(nt['TypeID'])

	return render_template('topics.html', topics=topics, nodes=nodes, hot_topics=hot_topics, node_types=node_types)

# page single topic
#--------------------------------------------------

# view
@app.route('/topic/<int:topic_id>')
def single_topic(topic_id):
	topic = Topic.get_topic(topic_id)
	topic['Time'] = time_diff(topic['Time'])
	topic['Content'] = markdown2.markdown(topic['Content'])
	comments = Comment.get_comments_by_topic(topic['TopicID'])
	for c in comments:
		c['Time'] = time_diff(c['Time'])
	Topic.add_click_num(topic_id)
	nodes = Node.get_nodes(16)
	return render_template('single_topic.html', topic=topic, comments=comments, nodes=nodes)

# proc - add comment
@app.route('/topic/<int:topic_id>', methods=['POST'])
def add_comment_to_topic(topic_id):

	replyer_id = session['user_id']
	
	# add comment
	comment = cgi.escape(request.form['comment'])
	replyee_id = get_comment_replyee_id(comment)	# check if @people exist
	if replyee_id != -1:
		comment = rebuild_comment(comment, replyee_id)
	Comment.add_comment_to_topic(topic_id, replyer_id, comment)

	# plus comment num
	Topic.add_comment_num(topic_id)

	# inform
	topic_user_id = Topic.get_topic_by_id(topic_id)['UserID']
	inform_title = build_topic_inform_title(replyer_id, topic_id)
	# if the topic not add by me
	if replyer_id != topic_user_id:
		Inform.add(replyer_id, topic_user_id, inform_title, comment)
	# if replyee exist,
	# and the topic not add by me,
	# and not topic_user_id, because if so, the inform has already been sended above
	if replyee_id != -1 and  replyee_id != replyer_id and replyee_id != topic_user_id:
		Inform.add(replyer_id, replyee_id, inform_title, comment)

	return redirect(url_for('single_topic', topic_id=topic_id))	

# page add topic
#--------------------------------------------------
@app.route('/topic/add', methods=['POST', 'GET'])
def add_topic():
	if request.method == 'GET':
		node_abbr = request.args['node'] if "node" in request.args else "shici"
		node = Node.get_node_by_abbr(node_abbr)
		node_types = Node.get_types()
		for nt in node_types:
			nt['nodes'] = Node.get_nodes_by_type(nt['TypeID'])
		return render_template('add_topic.html', node=node, node_types=node_types)
	elif request.method == 'POST':
		node_id = int(request.form['node-id'])
		title   = cgi.escape(request.form['title'])
		content = cgi.escape(request.form['content'])
		user_id = session['user_id']
		new_topic_id = Topic.add(node_id, title, content, user_id)
		return redirect(url_for('single_topic', topic_id=new_topic_id))

# page edit topic
#--------------------------------------------------
@app.route('/topic/edit/<int:topic_id>', methods=['POST', 'GET'])
def edit_topic(topic_id):
	if request.method == 'GET':
		topic = Topic.get_topic(topic_id)
		node_types = Node.get_types()
		for nt in node_types:
			nt['nodes'] = Node.get_nodes_by_type(nt['TypeID'])
		return render_template('edit_topic.html', topic=topic, node_types=node_types)
	elif request.method == 'POST':
		node_id = int(request.form['node-id'])
		title   = cgi.escape(request.form['title'])
		content = cgi.escape(request.form['content'])
		new_topic_id = Topic.edit(topic_id, node_id, title, content)
		return redirect(url_for('single_topic', topic_id=topic_id))

# page node
#--------------------------------------------------
@app.route('/node/<node_abbr>')
def single_node(node_abbr):
	node = Node.get_node_by_abbr(node_abbr)
	nodes = Node.get_nodes(20)
	topics = Topic.get_topics_by_node(node_abbr)
	for t in topics:
		t['Time'] = time_diff(t['Time'])
	return render_template('single_node.html', node=node, nodes=nodes, topics=topics)