import requests
import json

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