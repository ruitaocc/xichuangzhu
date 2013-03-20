#-*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, json

from xichuangzhu import app

from xichuangzhu.models.topic_model import Topic
from xichuangzhu.models.node_model import Node

# page forum
#--------------------------------------------------

@app.route('/forum')
def forum():
	topics = Topic.get_topics(15)
	nodes = Node.get_nodes(20)
	hot_topics = Topic.get_hot_topics(10)
	return render_template('topics.html', topics=topics, nodes=nodes, hot_topics=hot_topics)

# page topic
#--------------------------------------------------

@app.route('/topic/<int:topic_id>')
def single_topic(topic_id):
	topic = Topic.get_topic(topic_id)
	nodes = Node.get_nodes(20)
	return render_template('single_topic.html', topic=topic, nodes=nodes)

# page node
#--------------------------------------------------
@app.route('/node/<node_abbr>')
def node(node_abbr):
	node = Node.get_node_by_abbr(node_abbr)
	nodes = Node.get_nodes(20)
	topcis = Topic.get_topics_by_node(node_abbr)
	return render_template('node.html', node=node, nodes=nodes, topics=topcis)