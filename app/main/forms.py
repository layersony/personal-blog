from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import Required

class BlogPostForm(FlaskForm):
  title = StringField('Blog Title', validators=[Required()])
  content =  TextAreaField('Blog Content',validators=[Required()])
  submit = SubmitField('Submit Post')

class CommentForm(FlaskForm):
  comment = TextAreaField('.')
  submit = SubmitField('Submit')
  
   