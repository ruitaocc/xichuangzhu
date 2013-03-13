#-*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, json

from xichuangzhu import app

from xichuangzhu.models.topic_model import Topic

# page forum
#--------------------------------------------------

@app.route('/forum')
def forum():
	topics = Topic.get_topics(15)
	return render_template('topics.html', topics=topics)