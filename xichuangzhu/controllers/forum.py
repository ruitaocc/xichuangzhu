#-*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, json, session

from xichuangzhu import app

from xichuangzhu.models.topic_model import Topic
from xichuangzhu.models.node_model import Node
from xichuangzhu.models.comment_model import Comment

import datetime, time

# count the time diff, return a user-friendly format
# dt must be format as 2013-4-1 14:25:10
def time_diff(dt):
	dt = datetime.datetime.strptime(str(dt), "%Y-%m-%d %H:%M:%S")
	today = datetime.datetime.today()

	if dt.year != today.year:
		return str(today.year - dt.year) + "年前"
	elif dt.month != today.month:
		return str(today.month - dt.month) + "个月前"
	elif dt.day != today.day:
		return str(today.day - dt.day) + "天前"
	elif dt.hour != today.hour:
		return str(today.hour - dt.hour) + "小时前"
	elif dt.minite != today.minite:
		return str(today.minite - dt.minite) + "分钟前"
	elif dt.minite == today.minite:
		return "刚刚"

	# or user timedelta
	# s = (today - dt).total_seconds()
	# if day_diff > 365, use year
	# elif day_diff > 30, use month
	# elif hour_diff > 24, use day
	# elif minite_diff > 60, use hour
	# elif second_diff > 60, use minite
	# else use "just now"

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
	comments = Comment.get_comments_by_topic(topic['TopicID'])
	nodes = Node.get_nodes(16)
	return render_template('single_topic.html', topic=topic, comments=comments, nodes=nodes)

# proc - add comment
@app.route('/topic/<int:topic_id>', methods=['POST'])
def add_comment_to_topic(topic_id):
	comment    = request.form['comment']
	replyer_id = session['user_id']
	Comment.add_comment_to_topic(topic_id, replyer_id, 0, comment)
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
		title   = request.form['title']
		content = request.form['content']
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
		title   = request.form['title']
		content = request.form['content']
		new_topic_id = Topic.edit(topic_id, node_id, title, content)
		return redirect(url_for('single_topic', topic_id=topic_id))

# page node
#--------------------------------------------------
@app.route('/node/<node_abbr>')
def node(node_abbr):
	node = Node.get_node_by_abbr(node_abbr)
	nodes = Node.get_nodes(20)
	topcis = Topic.get_topics_by_node(node_abbr)
	return render_template('node.html', node=node, nodes=nodes, topics=topcis)