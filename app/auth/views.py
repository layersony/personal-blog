from flask import render_template, redirect, url_for, flash, request
from . import auth
from . forms import LoginForm, Registration
from ..models import User
from .. import db
from flask_login import login_user, login_required, logout_user, current_user
from ..request import get_quotes

@auth.route('/login', methods=['GET', 'POST'])
def login():
  login_form = LoginForm()

  if login_form.validate_on_submit():
    user = User.query.filter_by(email = login_form.email.data).first()
    if user is not None and user.verify_password(login_form.password.data):
      login_user(user, login_form.remember.data)
      return redirect(request.args.get('next') or url_for('main.profile', uname=current_user.username))
    flash('Invalid username or password')
  title = 'Login'
  quote = get_quotes()
  return render_template('/auth/login.html', loginform = login_form, title=title, quote=quote)

@auth.route('/register', methods=['GET', 'POST'])
def register():
  form = Registration()
  if form.validate_on_submit():
    user = User(fname = form.fname.data, sname = form.sname.data, username = form.username.data, email = form.email.data, password = form.password.data)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('auth.login'))

  title = 'New Account'
  quote = get_quotes()

  return render_template('auth/register.html', registrationform = form, title=title, quote=quote)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('main.index'))