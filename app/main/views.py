from flask import render_template, url_for, redirect
from flask.templating import render_template_string
from . import main
from ..models import Blog, User, Comment
from .forms import CommentForm, BlogPostForm 

@main.route('/')
def index():
  blog = Blog.get_blogs_content()
  title = 'Blog'
  return render_template('index.html', blogs=blog, title=title)

@main.route('/post/blog', methods=['GET', 'POST',])
def postblog():
  blogform = BlogPostForm()

  if blogform.validate_on_submit():
    title = blogform.title.data
    content = blogform.content.data
    
    newblog = Blog(title=title, content=content)
    newblog.save_blog()
    return redirect(url_for('main.index'))

  return render_template('profile/postblog.html', blogform=blogform)

