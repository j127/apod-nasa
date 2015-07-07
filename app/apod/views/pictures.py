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
    return "<h1>" + str(picture_date) + "</h1>"

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
    data_array = []
    for picture in Picture.objects():
        title = picture.api_record[0].title

        iso_date = picture.apod_date
        url_date = iso_date.strftime('%y%m%d')
        date_str = iso_date.strftime('%Y %B %d')
        
        url = '/apod/ap' + url_date + '.html'
        
        data_array.append({'title': title, 'url': url, 'date_str': date_str})

    output = json.dumps(data_array, indent=4, sort_keys=True)
    data = {}
    data['pictures'] = data_array

    data['title'] = 'Astronomy Picture Of The Day Archive'

    return render_template('pictures/archive.html', data=data)