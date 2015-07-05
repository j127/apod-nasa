from flask import Blueprint, render_template, url_for
# from ..models.posts import Picture, Video

pictures_bp = Blueprint('pictures', __name__, url_prefix='/apod')

@pictures_bp.route('/')
def index():
	return 'hello from pictures'