# coding: utf-8
import requests
import smtplib
import hashlib
from email.mime.text import MIMEText
from flask import render_template, request, redirect, url_for, session, Blueprint
from xichuangzhu import db, config
from ..models import User
from ..utils import require_login
from ..forms import EmailForm

bp = Blueprint('account', __name__)


@bp.route('/signin')
def signin():
    """通过豆瓣OAuth登陆"""
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
    if User.query.get(user_id):
        # if user unactive
        if User.query.filter(User.is_active == False).filter(User.id == user_id).first():
            return redirect(url_for('active_state', state='unactive', user_id=user_id))
        else:
            # set session
            session.permanent = True
            user = User.query.get_or_404(user_id)
            session['user_id'] = user_id
            session['user_name'] = user.name
            session['user_abbr'] = user.abbr
            return redirect(url_for('index'))
    # if not exist
    else:
        # get user info
        url = "https://api.douban.com/v2/user/" + str(user_id)
        user_info = requests.get(url).json()

        user = User(id=user_id, name=user_info['name'], abbr=user_info['uid'], avatar=user_info['avatar'],
                    signature=user_info['signature'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('send_active_email', user_id=user_id))


@bp.route('/send_active_email/<int:user_id>', methods=['GET', 'POST'])
def send_active_email(user_id):
    """发送激活邮件"""
    user = User.query.get_or_404(user_id)
    if request.method == 'GET':
        form = EmailForm(user_id=user_id)
        return render_template('account/send_active_email.html', user=user, form=form)
    else:
        form = EmailForm(request.form)

        if form.validate():
            to_addr = form.email.data

            # update user email
            user.email = to_addr
            db.session.add(user)
            db.session.commit()

            # gene active url
            active_code = hashlib.sha1(user.name).hexdigest()
            active_url = config.SITE_DOMAIN + "active_user/" + str(user_id) + "/" + active_code

            # prepare email content
            msgText = '''<h3>点 <a href='%s'>这里</a>，激活你在西窗烛的帐号。</h3>''' % active_url
            msg = MIMEText(msgText, 'html', 'utf-8')
            msg['From'] = "西窗烛 <" + config.SMTP_USER + ">"
            msg['To'] = user.name + "<" + to_addr + ">"
            msg['Subject'] = "欢迎来到西窗烛！"

            # send email
            s = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
            s.login(config.SMTP_USER, config.SMTP_PASSWORD)
            try:
                s.sendmail(config.SMTP_USER, to_addr, msg.as_string())
            except:
                return redirect(url_for('active_state', state='send_failed'))
            else:
                return redirect(url_for('active_state', state='send_succ'))
        else:
            return render_template('account/send_active_email.html', user=user, form=form)


@bp.route('/active/<int:user_id>/<active_code>')
def active(user_id, active_code):
    """激活用户"""
    user = User.query.get_or_404(user_id)
    if active_code == hashlib.sha1(user.name).hexdigest():
        # active user
        user.is_active = True
        db.session.add(user)
        db.session.commit()

        session.permanent = True
        session['user_id'] = user_id
        session['user_name'] = user.name
        session['user_abbr'] = user.abbr
        return redirect(url_for('active_state', state='active_succ'))
    return redirect(url_for('active_state', state='active_failed'))


@bp.route('/active_state')
def active_state():
    """显示激活状态"""
    state = request.args['state']
    user_id = int(request.args.get('user_id', 0))
    return render_template('account/active_state.html', state=state, user_id=user_id)


@bp.route('/signout')
@require_login
def signout():
    """登出"""
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_abbr', None)
    return redirect(url_for('index'))
