from flask import Blueprint, render_template, url_for
# from ..models.posts import Post

pages_bp = Blueprint('pages',__name__)

@pages_bp.route('/')
def index():
	return 'hello world'

