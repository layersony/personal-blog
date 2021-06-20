from flask import render_template, url_for, redirect, abort, request
from . import main
from .. import db
from ..models import Blog, User, Comment, Subscribe
from .forms import CommentForm, BlogPostForm 
from flask_login import login_required, current_user
from ..request import get_quotes
from ..email import mail_message
import time


@main.route('/')
def index():
  blog = Blog.get_blogs_content()
  title = 'Blog'
  blog.reverse()
  quote = get_quotes() 
  return render_template('index.html', blogs=blog, title=title, quote=quote)

@main.route('/post/blog', methods=['GET', 'POST',])
@login_required
def postblog():
  blogform = BlogPostForm()

  if blogform.validate_on_submit():
    title = blogform.title.data
    content = blogform.content.data
    
    newblog = Blog(title=title, content=content, user_id=current_user.id)
    newblog.save_blog()

    for i in Subscribe.query.all():
      mail_message("New Blog Is Out", "email/update_subscriber", i.email, newblog=newblog)

    return redirect(url_for('main.profile', uname=current_user.username))

  quote = get_quotes()
  return render_template('profile/postblog.html', blogform=blogform, quote=quote)

@main.route('/user/<uname>')
@login_required
def profile(uname):
  user = User.query.filter_by(username = uname).first()

  
  if user is None:
    abort(404)
  else:
    blog = Blog.query.filter_by(user_id=current_user.id).all()
    quote = get_quotes()
    return render_template('profile/profile.html', user = user, blog = blog, quote=quote)

@main.route('/comment/<id>', methods=['GET', 'POST'])
@login_required
def comment(id):
  form = CommentForm()
  blog = Blog.query.filter_by(id=id).first()

  if form.validate_on_submit():
    comment = form.comment.data
    new_comment = Comment(comment = comment, user_id = current_user.id, blog_id = id)

    new_comment.save_comment()
    return redirect(url_for('main.index'))
  
  blogcomment = Comment.query.filter_by(blog_id=id).all()
  quote = get_quotes()

  return render_template('profile/comment.html', comment=form, blog=blog, blogcomment = blogcomment, quote=quote)

@main.route('/post/<id>/comments', methods=['GET'])
def viewcomments(id):
  allcomments = Comment.query.filter_by(blog_id=id).all()
  quote = get_quotes()
  return render_template('profile/viewcomment.html', allcomments=allcomments, quote=quote)

@main.route('/post/<id>/delete', methods = ['GET', 'POST'])
def deletePost(id):
  todele = Blog.query.filter_by(id=id).first()
  db.session.delete(todele)
  db.session.commit()
  return redirect(url_for('main.profile', uname=current_user.username))

@main.route('/post/<id>/comment/delete', methods = ['GET', 'POST'])
def deleteComment(id):
  todele = Comment.query.filter_by(id=id).first()
  db.session.delete(todele)
  db.session.commit()
  return redirect(url_for('main.profile', uname=current_user.username))

@main.route('/post/<id>', methods=['POST', 'GET'])
def fullblog(id):
  blogdetail = Blog.query.filter_by(id=id).first()
  quote = get_quotes()
  return render_template('fullblog.html', blogdetail=blogdetail,   quote = quote)

@main.route('/subscribe', methods=['POST'])
def subscribe():
        email = request.form.get('subscriber')
        new_sub = Subscribe(email=email)
        new_sub.save_subscriber()
        mail_message("Subscribed to Maingi Blog","email/welcome_subscriber", email)

        return redirect(url_for('main.index'))
 