from flask import Blueprint, render_template, url_for, jsonify, redirect, abort
# from ..models.posts import Picture, Video

from ..util.fetcher import fetch_photo
from ..util.helpers import pic2data


pictures_bp = Blueprint('pictures', __name__, url_prefix='/apod')

@pictures_bp.route('/')
def redirect_to_current_day():
	return redirect('apod/astropix.html')


@pictures_bp.route('/astropix.html')
def pictures_index():
	pic_data = fetch_photo()
	data = pic2data(pic_data)
	return render_template('pictures/detail.html', data=data)


@pictures_bp.route('/ap<int:picture_date>.html')
def picture_detail(picture_date):
	date_str = str(picture_date)
	if len(date_str) != 6:
		return abort(404)
	split_date = [date_str[i:i+2] for i in range(0, len(date_str), 2)]
	pic_data = fetch_photo(split_date[0], split_date[1], split_date[2])
	data = pic2data(pic_data)
	return render_template('pictures/detail.html', data=data)

