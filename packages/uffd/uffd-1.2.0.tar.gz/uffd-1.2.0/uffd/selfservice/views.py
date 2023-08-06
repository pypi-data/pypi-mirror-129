import datetime
import secrets

from flask import Blueprint, render_template, request, url_for, redirect, flash, current_app, session, abort
from flask_babel import gettext as _, lazy_gettext

from uffd.navbar import register_navbar
from uffd.csrf import csrf_protect
from uffd.user.models import User
from uffd.session import login_required
from uffd.selfservice.models import PasswordToken, MailToken
from uffd.sendmail import sendmail
from uffd.role.models import Role
from uffd.database import db
from uffd.ldap import ldap
from uffd.ratelimit import host_ratelimit, Ratelimit, format_delay

bp = Blueprint("selfservice", __name__, template_folder='templates', url_prefix='/self/')

reset_ratelimit = Ratelimit('passwordreset', 1*60*60, 3)

def selfservice_acl_check():
	return request.user and request.user.is_in_group(current_app.config['ACL_SELFSERVICE_GROUP'])

@bp.route("/")
@register_navbar(0, lazy_gettext('Selfservice'), icon='portrait', blueprint=bp, visible=selfservice_acl_check)
@login_required(selfservice_acl_check)
def index():
	return render_template('selfservice/self.html', user=request.user)

@bp.route("/updateprofile", methods=(['POST']))
@csrf_protect(blueprint=bp)
@login_required(selfservice_acl_check)
def update_profile():
	user = request.user
	if request.values['displayname'] != user.displayname:
		if user.set_displayname(request.values['displayname']):
			flash(_('Display name changed.'))
		else:
			flash(_('Display name is not valid.'))
	if request.values['mail'] != user.mail:
		send_mail_verification(user.loginname, request.values['mail'])
		flash(_('We sent you an email, please verify your mail address.'))
	ldap.session.commit()
	return redirect(url_for('selfservice.index'))

@bp.route("/changepassword", methods=(['POST']))
@csrf_protect(blueprint=bp)
@login_required(selfservice_acl_check)
def change_password():
	password_changed = False
	user = request.user
	if not request.values['password1'] == request.values['password2']:
		flash(_('Passwords do not match'))
	else:
		if user.set_password(request.values['password1']):
			flash(_('Password changed'))
			password_changed = True
		else:
			flash(_('Invalid password'))
	ldap.session.commit()
	# When using a user_connection, update the connection on password-change
	if password_changed and current_app.config['LDAP_SERVICE_USER_BIND']:
		session['user_pw'] = request.values['password1']
	return redirect(url_for('selfservice.index'))

@bp.route("/passwordreset", methods=(['GET', 'POST']))
def forgot_password():
	if request.method == 'GET':
		return render_template('selfservice/forgot_password.html')

	loginname = request.values['loginname'].lower()
	mail = request.values['mail']
	reset_delay = reset_ratelimit.get_delay(loginname+'/'+mail)
	host_delay = host_ratelimit.get_delay()
	if reset_delay or host_delay:
		if reset_delay > host_delay:
			flash(_('We received too many password reset requests for this user! Please wait at least %(delay)s.', delay=format_delay(reset_delay)))
		else:
			flash(_('We received too many requests from your ip address/network! Please wait at least %(delay)s.', delay=format_delay(host_delay)))
		return redirect(url_for('.forgot_password'))
	reset_ratelimit.log(loginname+'/'+mail)
	host_ratelimit.log()
	flash(_("We sent a mail to this user's mail address if you entered the correct mail and login name combination"))
	user = User.query.filter_by(loginname=loginname).one_or_none()
	if user and user.mail == mail and user.is_in_group(current_app.config['ACL_SELFSERVICE_GROUP']):
		send_passwordreset(user)
	return redirect(url_for('session.login'))

# Deprecated
@bp.route('/token/password/<token>')
def token_password_legacy(token):
	matching_token = None
	filter_expr = PasswordToken.created >= (datetime.datetime.now() - datetime.timedelta(days=2))
	for dbtoken in PasswordToken.query.filter(filter_expr):
		if secrets.compare_digest(dbtoken.token, token):
			matching_token = dbtoken
	if not matching_token:
		flash(_('Token expired, please try again.'))
		return redirect(url_for('session.login'))
	return redirect(url_for('token_password', token_id=matching_token.id, token=token))

@bp.route("/token/password/<int:token_id>/<token>", methods=(['POST', 'GET']))
def token_password(token_id, token):
	dbtoken = PasswordToken.query.get(token_id)
	if not dbtoken or not secrets.compare_digest(dbtoken.token, token) or \
			dbtoken.created < (datetime.datetime.now() - datetime.timedelta(days=2)):
		flash(_('Token expired, please try again.'))
		if dbtoken:
			db.session.delete(dbtoken)
			db.session.commit()
		return redirect(url_for('session.login'))
	if request.method == 'GET':
		return render_template('selfservice/set_password.html', token=dbtoken)
	if not request.values['password1']:
		flash(_('You need to set a password, please try again.'))
		return render_template('selfservice/set_password.html', token=dbtoken)
	if not request.values['password1'] == request.values['password2']:
		flash(_('Passwords do not match, please try again.'))
		return render_template('selfservice/set_password.html', token=dbtoken)
	user = User.query.filter_by(loginname=dbtoken.loginname).one()
	if not user.is_in_group(current_app.config['ACL_SELFSERVICE_GROUP']):
		abort(403)
	if not user.set_password(request.values['password1']):
		flash(_('Password ist not valid, please try again.'))
		return render_template('selfservice/set_password.html', token=dbtoken)
	db.session.delete(dbtoken)
	flash(_('New password set'))
	ldap.session.commit()
	db.session.commit()
	return redirect(url_for('session.login'))

# Deprecated
@bp.route("/token/mail_verification/<token>")
def token_mail_legacy(token):
	matching_token = None
	filter_expr = MailToken.created >= (datetime.datetime.now() - datetime.timedelta(days=2))
	for dbtoken in MailToken.query.filter(filter_expr):
		if secrets.compare_digest(dbtoken.token, token):
			matching_token = dbtoken
	if not matching_token:
		flash(_('Token expired, please try again.'))
		return redirect(url_for('session.login'))
	return redirect(url_for('mail_password', token_id=matching_token.id, token=token))

@bp.route("/token/mail_verification/<int:token_id>/<token>")
@login_required(selfservice_acl_check)
def token_mail(token_id, token):
	dbtoken = MailToken.query.get(token_id)
	if not dbtoken or not secrets.compare_digest(dbtoken.token, token) or \
			dbtoken.created < (datetime.datetime.now() - datetime.timedelta(days=2)):
		flash(_('Token expired, please try again.'))
		if dbtoken:
			db.session.delete(dbtoken)
			db.session.commit()
		return redirect(url_for('selfservice.index'))
	user = User.query.filter_by(loginname=dbtoken.loginname).one()
	if user != request.user:
		abort(403, description=_('This link was generated for another user. Login as the correct user to continue.'))
	user.set_mail(dbtoken.newmail)
	flash(_('New mail set'))
	db.session.delete(dbtoken)
	ldap.session.commit()
	db.session.commit()
	return redirect(url_for('selfservice.index'))

@bp.route("/leaverole/<int:roleid>", methods=(['POST']))
@csrf_protect(blueprint=bp)
@login_required(selfservice_acl_check)
def leave_role(roleid):
	if not current_app.config['ENABLE_ROLESELFSERVICE']:
		flash(_('Leaving roles is disabled'))
		return redirect(url_for('selfservice.index'))
	role = Role.query.get_or_404(roleid)
	role.members.discard(request.user)
	request.user.update_groups()
	ldap.session.commit()
	db.session.commit()
	flash(_('You left role %(role_name)s', role_name=role.name))
	return redirect(url_for('selfservice.index'))

def send_mail_verification(loginname, newmail):
	expired_tokens = MailToken.query.filter(MailToken.created < (datetime.datetime.now() - datetime.timedelta(days=2))).all()
	duplicate_tokens = MailToken.query.filter(MailToken.loginname == loginname).all()
	for i in expired_tokens + duplicate_tokens:
		db.session.delete(i)
	token = MailToken()
	token.loginname = loginname
	token.newmail = newmail
	db.session.add(token)
	db.session.commit()

	user = User.query.filter_by(loginname=loginname).one()

	if not sendmail(newmail, 'Mail verification', 'selfservice/mailverification.mail.txt', user=user, token=token):
		flash(_('Mail to "%(mail_address)s" could not be sent!', mail_address=newmail))

def send_passwordreset(user, new=False):
	expired_tokens = PasswordToken.query.filter(PasswordToken.created < (datetime.datetime.now() - datetime.timedelta(days=2))).all()
	duplicate_tokens = PasswordToken.query.filter(PasswordToken.loginname == user.loginname).all()
	for i in expired_tokens + duplicate_tokens:
		db.session.delete(i)
	token = PasswordToken()
	token.loginname = user.loginname
	db.session.add(token)
	db.session.commit()

	if new:
		template = 'selfservice/newuser.mail.txt'
		subject = 'Welcome to the %s infrastructure'%current_app.config.get('ORGANISATION_NAME', '')
	else:
		template = 'selfservice/passwordreset.mail.txt'
		subject = 'Password reset'

	if not sendmail(user.mail, subject, template, user=user, token=token):
		flash(_('Mail to "%(mail_address)s" could not be sent!', mail_address=user.mail))
