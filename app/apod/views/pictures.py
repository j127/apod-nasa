from flask import Blueprint, render_template, url_for, jsonify
# from ..models.posts import Picture, Video

from ..util.fetcher import fetch_photo


pictures_bp = Blueprint('pictures', __name__, url_prefix='/apod')

@pictures_bp.route('/')
def index():
	pic_data = fetch_photo()
	data = {}
	data['title'] = pic_data['title']
	data['img_url'] = pic_data['url']
	return render_template('pictures/detail.html', data=data)