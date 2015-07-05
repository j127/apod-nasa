from flask import Blueprint, render_template, url_for
# from ..models.posts import Post

pages_bp = Blueprint('pages',__name__)

@pages_bp.route('/')
def index():
	data = {'title': 'Welcome to APOD'}
	return render_template('pages/index.html', data=data)

