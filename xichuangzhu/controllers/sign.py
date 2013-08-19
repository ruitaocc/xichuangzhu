#-*- coding: UTF-8 -*-
import requests
import smtplib
from email.mime.text import MIMEText
import hashlib
import math
import config
from flask import render_template, request, redirect, url_for, json, session
from xichuangzhu import app
from xichuangzhu.models.user_model import User
from xichuangzhu.utils import require_login
from xichuangzhu.form import EmailForm

# proc - login by douban's oauth2.0 (public)
#--------------------------------------------------
@app.route('/login/douban')
def auth():
    # get current authed userID
    code = request.args['code']
    url = "https://www.douban.com/service/auth2/token"
    data = {
        'client_id': config.DOUBAN_CLIENT_ID,
        'client_secret': config.DOUBAN_SECRET,
        'redirect_uri': config.DOUBAN_REDIRECT_URI,
        'grant_type': 'authorization_code',
        'code': code
    }
    r = requests.post(url, data=data).json()
    user_id = int(r['douban_user_id'])

    # if user exist
    if User.check_exist_by_id(user_id):
        # if user unactive
        if not User.check_active(user_id):
            return redirect(url_for('verify_email_callback', state='unactive', user_id=user_id))
        else:
            # set session
            session.permanent = True
            session['user_id'] = user_id
            session['user_name'] = User.get_name_by_id(user_id)
            session['user_abbr'] = User.get_abbr_by_id(user_id)
            return redirect(url_for('index'))
    # if not exist
    else:
        # get user info
        url = "https://api.douban.com/v2/user/" + str(user_id)
        user_info = requests.get(url).json()

        # add user
        user_id = int(user_info['id'])
        user_name = user_info['name']
        abbr = user_info['uid']
        avatar = user_info['avatar']
        signature = user_info['signature']
        desc = user_info['desc']
        location_id = int(user_info['loc_id']) if 'loc_id' in user_info else 0
        location = user_info['loc_name']
        User.add_user(user_id, user_name, abbr, avatar, signature, desc, location_id, location)

        # redirect to the verify email page
        return redirect(url_for('send_verify_email', user_id=user_id))

# page - send verify email
#--------------------------------------------------
@app.route('/send_verify_email/douban', methods=['GET', 'POST'])
def send_verify_email():
    if request.method == 'GET':
        user_id = int(request.args['user_id'])
        form = EmailForm(user_id=user_id)
        user_name = User.get_name_by_id(user_id)
        return render_template('sign/send_verify_email.html', user_name=user_name, form=form)
    else:
        form = EmailForm(request.form)

        if form.validate():

            # email
            t_addr = form.email.data

            # user info
            user_id = int(form.user_id.data)
            user_name = User.get_name_by_id(user_id)

            # add this email to user
            User.add_email(user_id, t_addr)

            # gene verify url
            verify_code = hashlib.sha1(user_name).hexdigest()
            verify_url = config.SITE_DOMAIN + "verify_email/douban/" + str(user_id) + "/" + verify_code

            # prepare email content
            msgText = '''<h3>点 <a href='%s'>这里</a>，激活你在西窗烛的帐号。</h3>''' % verify_url
            msg = MIMEText(msgText, 'html', 'utf-8')
            msg['From'] = "西窗烛 <" + config.SMTP_FROM + ">"
            msg['To'] = user_name + "<" + t_addr + ">"
            msg['Subject'] = "欢迎来到西窗烛！"

            # send email
            s = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
            s.login(config.SMTP_USER, config.SMTP_PASSWORD)
            s.sendmail(config.SMTP_FROM, t_addr, msg.as_string())

            return redirect(url_for('verify_email_callback', state='send_succ'))
        else:
            user_id = int(form.user_id.data)
            user_name = User.get_name_by_id(user_id)
            return render_template('sign/send_verify_email.html', user_name=user_name, form=form)

# proc - verify the code and active user
#--------------------------------------------------
@app.route('/verify_email/douban/<int:user_id>/<verify_code>')
def verify_email(user_id, verify_code):
    user_name = User.get_name_by_id(user_id)
    user_abbr = User.get_abbr_by_id(user_id)
    if verify_code == hashlib.sha1(user_name).hexdigest():
        User.active_user(user_id)
        session.permanent = True
        session['user_id'] = user_id
        session['user_name'] = user_name
        session['user_abbr'] = user_abbr
        return redirect(url_for('verify_email_callback', state='active_succ'))
    else:
        return redirect(url_for('verify_email_callback', state='active_failed'))

# page - show the state of verify
#--------------------------------------------------
@app.route('/verify_email_callback/douban/')
def verify_email_callback():
    state = request.args['state']
    user_id = int(request.args['user_id']) if 'user_id' in request.args else 0
    return render_template('sign/verify_email_callback.html', state=state, user_id=user_id)

# proc - logout
#--------------------------------------------------
@app.route('/logout')
@require_login
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_abbr', None)
    return redirect(url_for('index'))
