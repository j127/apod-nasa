import requests
import json
from time import sleep
import datetime
import mongoengine as me
from ...models.pictures import Picture, APIRecord


def fetch_photo(year, month, day):
    # api_key = app.config['NASA_API_KEY']
    if int(year) > 40:
        year = '19' + str(year).zfill(2)
    else:
        year = '20' + str(year).zfill(2)

    constructed_date = '{}-{}-{}'.format(year, month, day)
    api_key = 'ldWyF16dCc1uyXUTWpRAC2O3QGOzZRuINM7Mjo08'
    base_url = 'https://api.nasa.gov/planetary/apod'
    url = '{base_url}?concept_tags=True&date={date}&api_key={key}'.format(base_url=base_url, date=constructed_date,
                                                                          key=api_key)

    res = requests.get(url)
    picture_dict = json.loads(res.text)

    return picture_dict


def fetch_photos(dates, delay=4):
    photos_data = []
    for d in dates:
        year = d[0]
        month = d[1]
        day = d[2]
        current_photo = fetch_photo(year,month,day)
        photos_data.append(current_photo)
        save_picture(current_photo, urldate_to_date(d))
        sleep(delay)
    print(photos_data)

def urldate_to_date(date_list):
    '''Takes a date in the format of ['yy', 'mm', 'dd'] and returns a python date object.'''
    new_date = datetime.datetime(int(date_list[0]),int(date_list[1]),int(date_list[2]))
    print(date_list,new_date)
    return new_date

def generate_dates(n):
    numdays = n
    formatted_dates = []
    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
    for d in date_list:
        formatted_dates.append(d.strftime('%y-%m-%d').split('-'))
    return formatted_dates


def save_picture(pic, pic_date):
    print(pic, pic_date)
    current_api_record = APIRecord(
        title=pic['title'],
        explanation=pic['explanation'],
        url=pic['url'],
        media_type=pic['media_type'],
        concepts=pic['concepts']
        # requested_date=datetime.datetime.now
    )
    current_pic = Picture(apod_date=pic_date, published=True)
    current_pic.api_record.append(current_api_record)
    current_pic.save()

if __name__ == '__main__':
    fetch_photos(generate_dates(200),1)
