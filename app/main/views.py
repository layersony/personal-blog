from flask import render_template, url_for, redirect, abort
from . import main
from ..models import Blog, User, Comment
from .forms import CommentForm, BlogPostForm 
from flask_login import login_required, current_user

@main.route('/')
def index():
  blog = Blog.get_blogs_content()
  title = 'Blog'
  return render_template('index.html', blogs=blog, title=title)

@main.route('/post/blog', methods=['GET', 'POST',])
@login_required
def postblog():
  blogform = BlogPostForm()

  if blogform.validate_on_submit():
    title = blogform.title.data
    content = blogform.content.data
    
    newblog = Blog(title=title, content=content, user_id=current_user.id)
    newblog.save_blog()
    return redirect(url_for('main.profile', uname=current_user.username))

  return render_template('profile/postblog.html', blogform=blogform)

@main.route('/user/<uname>')
@login_required
def profile(uname):
  user = User.query.filter_by(username = uname).first()

  
  if user is None:
    abort(404)
  else:
    blog = Blog.query.filter_by(user_id=current_user.id).all()
    print(blog)
    return render_template('profile/profile.html', user = user, blog = blog)

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
  return render_template('profile/comment.html', comment=form, blog=blog, blogcomment = blogcomment)

@main.route('/post/<id>/comments', methods=['GET'])
def viewcomments(id):
  allcomments = Comment.query.filter_by(blog_id=id).all()
  print(allcomments)
  return render_template('profile/viewcomment.html', allcomments=allcomments)
