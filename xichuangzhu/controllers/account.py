# coding: utf-8
import requests
import smtplib
import hashlib
from email.mime.text import MIMEText
from flask import render_template, request, redirect, url_for, Blueprint, flash, abort, g
from .. import config
from ..models import db, User
from ..utils import signin_user, signout_user
from ..forms import SignupForm, SettingsForm
from ..roles import NewUserRole, BanUserRole, UserRole
from ..permissions import require_visitor, new_user_permission

bp = Blueprint('account', __name__)


@bp.route('/signin')
@require_visitor
def signin():
    """通过豆瓣OAuth登陆"""
    # get current authed user id
    code = request.args.get('code')
    if not code:
        abort(500)
    url = "https://www.douban.com/service/auth2/token"
    data = {
        'client_id': config.DOUBAN_CLIENT_ID,
        'client_secret': config.DOUBAN_SECRET,
        'redirect_uri': config.DOUBAN_REDIRECT_URI,
        'grant_type': 'authorization_code',
        'code': code
    }
    res = requests.post(url, data=data).json()
    user_id = int(res['douban_user_id'])

    user = User.query.get(user_id)
    if user:
        if user.role == BanUserRole:
            flash('账户已被禁用')
            return redirect(url_for('site.index'))
        if user.role == NewUserRole:
            flash('账户尚未激活，请登陆邮箱激活账户')
        signin_user(user, True)
        return redirect(url_for('site.index'))
    return redirect(url_for('.signup', user_id=user_id))


@bp.route('/signup/<int:user_id>', methods=['GET', 'POST'])
@require_visitor
def signup(user_id):
    """发送激活邮件"""
    # Get user info from douban
    url = "https://api.douban.com/v2/user/%d" % user_id
    user_info = requests.get(url).json()
    form = SignupForm()
    if form.validate_on_submit():
        to_addr = form.email.data
        user = User(id=user_id, name=user_info['name'], abbr=user_info['uid'],
                    avatar=user_info['large_avatar'], signature=user_info['signature'],
                    email=to_addr)
        db.session.add(user)
        db.session.commit()
        signin_user(user, True)

        # send active email
        token = hashlib.sha1(user.name).hexdigest()
        url = config.SITE_DOMAIN + url_for('.activate', user_id=user_id, token=token)

        msg = '''<h3>点 <a href='%s'>这里</a>，激活你在西窗烛的帐号。</h3>''' % url
        msg = MIMEText(msg, 'html', 'utf-8')
        msg['From'] = "西窗烛 <%s>" % config.SMTP_USER
        msg['To'] = "%s <%s>" % (user.name, to_addr)
        msg['Subject'] = "欢迎来到西窗烛！"

        s = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
        s.login(config.SMTP_USER, config.SMTP_PASSWORD)
        try:
            s.sendmail(config.SMTP_USER, to_addr, msg.as_string())
        except:
            flash('邮件发送失败，请稍后尝试')
        else:
            flash('激活邮件已发送到你的邮箱，请查收')
        return redirect(url_for('site.index'))
    return render_template('account/signup.html', user_info=user_info, form=form)


@bp.route('/activate/<int:user_id>/<token>')
def activate(user_id, token):
    """激活用户"""
    user = User.query.get_or_404(user_id)
    if token == hashlib.sha1(user.name).hexdigest():
        user.role = UserRole
        db.session.add(user)
        db.session.commit()
        signin_user(user, True)
        flash('账号激活成功！')
        return redirect(url_for('site.index'))
    flash('无效的激活链接')
    return redirect(url_for('site.index'))


@bp.route('/signout')
def signout():
    """登出"""
    signout_user()
    return redirect(url_for('site.index'))


@bp.route('/settings', methods=['GET', 'POST'])
@new_user_permission
def settings():
    """个人设置"""
    form = SettingsForm(signature=g.user.signature)
    if form.validate_on_submit():
        g.user.signature = form.signature.data
        db.session.add(g.user)
        db.session.commit()
        flash('设置已保存')
        return redirect(url_for('.settings'))
    return render_template('account/settings.html', form=form)


@bp.route('/resend_activate_mail')
@new_user_permission
def resend_activate_mail():
    if g.user_role != NewUserRole:
        abort(403)