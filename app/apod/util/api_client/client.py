import requests
import json
from time import sleep
import datetime

def fetch_photo(year, month, day):
	# api_key = app.config['NASA_API_KEY']
	if int(year) > 40:
		year = '19' + year
	else:
		year = '20' + year

	constructed_date = '{}-{}-{}'.format(year,month, day)
	api_key = 'ldWyF16dCc1uyXUTWpRAC2O3QGOzZRuINM7Mjo08'
	base_url = 'https://api.nasa.gov/planetary/apod'
	url = '{base_url}?concept_tags=True&date={date}&api_key={key}'.format(base_url=base_url, date=constructed_date, key=api_key)

	res = requests.get(url)
	picture_dict = json.loads(res.text)
	
	return picture_dict

def fetch_photos(dates, delay=4):
	photos_data = []
	for d in dates:
		sleep(delay)
		year = d[0]
		month = d[1]
		day = d[2]
		photos_data.append(fetch_photo(year, month, day))
	print(photos_data)

def generate_dates(n):
	numdays = n
	formatted_dates = []
	base = datetime.datetime.today()
	date_list = [base - datetime.timedelta(days=x) for x in range(0,numdays)]
	for d in date_list:
		formatted_dates.append(d.strftime('%y-%m-%d').split('-'))
	return formatted_dates

if __name__ == '__main__':
	fetch_photos(generate_dates(5))
	