from flask import Blueprint, render_template, url_for, jsonify, redirect, abort
from ..models.pictures import Picture
from ..util.api_client.client import fetch_photo
from ..util.helpers import pic2data, add_year_prefix
import time
import json
import datetime

pictures_bp = Blueprint('pictures', __name__, url_prefix='/apod')


@pictures_bp.route('/')
def redirect_to_current_day():
    """Redirects to the homepage at apod/astropix.html."""
    return redirect('apod/astropix.html')


@pictures_bp.route('/astropix.html')
def pictures_index():
    """This is the homepage of the site."""
    split_date = time.strftime('%y,%m,%d').split(',')
    pic_data = fetch_photo(split_date[0], split_date[1], split_date[2])
    data = pic2data(pic_data)
    data['is_today'] = True

    # split_date = [int(date_str[i:i + 2]) for i in range(0, len(date_str), 2)]
    todays_date = datetime.datetime(int(add_year_prefix(split_date[0])), int(split_date[1]), int(split_date[2]))
    yesterdays_date = todays_date - datetime.timedelta(days=1)

    data['previous_date'] = yesterdays_date.strftime('%y%m%d')

    return render_template('pictures/detail.html', data=data)

# @pictures_bp.route('/ap<picture_date>.html')
# def picture_detail(picture_date):
#     date_str = str(picture_date)
#     if len(date_str) != 6:
#         return abort(404)
#     split_date = [date_str[i:i + 2] for i in range(0, len(date_str), 2)]
#     pic_data = fetch_photo(split_date[0], split_date[1], split_date[2])
#     data = pic2data(pic_data)
#     return render_template('pictures/detail.html', data=data)
#     return "<h1>" + str(picture_date) + "</h1>"

@pictures_bp.route('/ap<picture_date>.html')
def picture_detail(picture_date):
    """This renders a detail view for a picture of the day."""

    # Check length of date string
    date_str = str(picture_date)
    if len(date_str) != 6:
        return abort(404)

    # Split date into a list, e.g., ['13', '12', '07']
    split_date = [int(date_str[i:i + 2]) for i in range(0, len(date_str), 2)]
    todays_date = datetime.datetime(int(add_year_prefix(split_date[0])), split_date[1], split_date[2])
    tomorrows_date = todays_date + datetime.timedelta(days=1)
    yesterdays_date = todays_date - datetime.timedelta(days=1)
    pic_from_db = Picture.objects(__raw__={'apod_date': {'$gte': todays_date, '$lt': tomorrows_date}})

    if len(pic_from_db) < 1:
        # If no results in database, use API.
        pic_data = fetch_photo(split_date[0], split_date[1], split_date[2])
        data = pic2data(pic_data)
    else:
        # Use database results.
        current_pic = json.loads(pic_from_db[0].to_json())['api_record'][0]
        data = pic2data(current_pic)

    # Get the latest picture
    last_picture = Picture.objects().only('apod_date').order_by('-apod_date').first()
    last_date_raw = last_picture.apod_date
    
    two_digit_year = getattr(last_date_raw,'year')
    four_digit_year = add_year_prefix(two_digit_year)
    
    last_date_day = getattr(last_date_raw, 'day')
    last_date_month = getattr(last_date_raw, 'month')
    last_date_year = int(four_digit_year)
    last_date_complete = datetime.datetime(last_date_year, last_date_month, last_date_month)
    
    if todays_date.date() == last_date_complete.date():
        data['is_today'] = True
    elif todays_date.date() == datetime.datetime(1996,6,16).date():
        data['is_beginning_date'] = True

    data['next_date'] = tomorrows_date.strftime('%y%m%d')
    data['previous_date'] = yesterdays_date.strftime('%y%m%d')
    return render_template('pictures/detail.html', data=data)

@pictures_bp.route('/archivepix.html')
def archive_home():
    """Renders the main archive page."""
    data_array = []
    for picture in Picture.objects():
        title = picture.api_record[0].title

        iso_date = picture.apod_date
        year, month, day = iso_date.strftime('%y-%m-%d').split('-')
        four_digit_year = add_year_prefix(year)
        pre_date = datetime.datetime(int(year),int(month),int(day))
        date_str = pre_date.strftime('%Y %B %d')
        
        url = '/apod/ap{}{}{}.html'.format(year,month,day)
        
        data_array.append({'title': title, 'url': url, 'date_str': date_str})

    # output = json.dumps(data_array, indent=4, sort_keys=True)
    data = {}
    data['pictures'] = data_array
    data['title'] = 'Astronomy Picture Of The Day Archive'

    return render_template('pictures/archive.html', data=data)