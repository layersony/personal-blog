from flask import render_template
from . import main
from ..models import Blog, User, Comment
from .forms import CommentForm, BlogPostForm 

@main.route('/')
def index():
  blog = Blog.get_blogs_content()
  title = 'Blog'
  return render_template('index.html', blogs=blog, title=title)

