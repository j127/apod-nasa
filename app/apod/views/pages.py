from flask import Blueprint, render_template, url_for, redirect
# from ..models.posts import Post

pages_bp = Blueprint('pages',__name__)

@pages_bp.route('/')
def index():
	return redirect('apod/astropix.html')