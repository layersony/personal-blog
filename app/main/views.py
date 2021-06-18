from flask import render_template
from . import main

@main.route('/')
def index():
  heading = 'Working.. Good to go'
  return render_template('index.html', heading=heading)