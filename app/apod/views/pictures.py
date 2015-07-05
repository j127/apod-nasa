from flask import Blueprint, render_template, url_for, jsonify, redirect
# from ..models.posts import Picture, Video

from ..util.fetcher import fetch_photo


pictures_bp = Blueprint('pictures', __name__, url_prefix='/apod')

@pictures_bp.route('/')
def redirect_to_current_day():
	return redirect('apod/astropix.html')


@pictures_bp.route('/astropix.html')
def pictures_index():
	pic_data = fetch_photo()
	data = {}
	data['title'] = pic_data['title']
	data['img_url'] = pic_data['url']
	data['explanation'] = pic_data['explanation']
	return render_template('pictures/detail.html', data=data)