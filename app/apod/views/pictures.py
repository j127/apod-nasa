import json
from flask import Blueprint, render_template, url_for, jsonify
# from ..models.posts import Picture, Video

from ..util.fetcher import fetch_photo


pictures_bp = Blueprint('pictures', __name__, url_prefix='/apod')

@pictures_bp.route('/')
def index():
	pic = fetch_photo()
	pic_json = json.loads(pic)

	return jsonify(pic_json)