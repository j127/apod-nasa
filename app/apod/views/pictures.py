from flask import Blueprint, render_template, url_for, jsonify, redirect, abort
from ..models.pictures import Picture

from ..util.api_client.client import fetch_photo
from ..util.helpers import pic2data
import time
import json
import datetime


pictures_bp = Blueprint('pictures', __name__, url_prefix='/apod')


@pictures_bp.route('/')
def redirect_to_current_day():
    return redirect('apod/astropix.html')


@pictures_bp.route('/astropix.html')
def pictures_index():
    split_date = time.strftime('%y,%m,%d').split(',')
    pic_data = fetch_photo(split_date[0], split_date[1], split_date[2])
    data = pic2data(pic_data)
    data['is_today'] = True
    return render_template('pictures/detail.html', data=data)


@pictures_bp.route('/ap<picture_date>.html')
def picture_detail(picture_date):
    date_str = str(picture_date)
    if len(date_str) != 6:
        return abort(404)
    split_date = [date_str[i:i + 2] for i in range(0, len(date_str), 2)]
    pic_data = fetch_photo(split_date[0], split_date[1], split_date[2])
    data = pic2data(pic_data)
    return render_template('pictures/detail.html', data=data)

@pictures_bp.route('/2/ap<picture_date>.html')
def picture_detail2(picture_date):
    date_str = str(picture_date)
    if len(date_str) != 6:
        return abort(404)
    split_date = [int(date_str[i:i + 2]) for i in range(0, len(date_str), 2)]
    todays_date = datetime.datetime(split_date[0], split_date[1], split_date[2])
    tomorrows_date = datetime.datetime(split_date[0], split_date[1], split_date[2]+1)
    pic_from_db = Picture.objects(__raw__={'apod_date': {'$gte': todays_date, '$lt': tomorrows_date}})
    if len(pic_from_db) < 1:
        # If no results in database, use API.
        pic_data = fetch_photo(split_date[0], split_date[1], split_date[2])
        data = pic2data(pic_data)
    else:
        # Use database results.
        current_pic = json.loads(pic_from_db[0].to_json())['api_record'][0]
        data = pic2data(current_pic)
    
    return render_template('pictures/detail.html', data=data)

@pictures_bp.route('/archivepix.html')
def archive_home():
    # pictures = Picture.objects() #.order_by('-apod_date')
    # pre_json = pictures[0].to_json() #.to_json())['api_record'][0][0]
    # json_to_dict = json.loads(pre_json)
    # jsonify(pre_json)

    q = Picture.objects()
    j = q[0].to_json()
    d = json.loads(j)
    output = d['api_record'] #[0]['title']
    jsonify(output)
    # jsonify(json.loads(Pictures.objects()[0].to_json())['api_record'][0]['title'])