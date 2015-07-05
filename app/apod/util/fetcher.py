import requests

def fetch_photo():
	# api_key = app.config['NASA_API_KEY']
	api_key = 'ldWyF16dCc1uyXUTWpRAC2O3QGOzZRuINM7Mjo08'
	url = 'https://api.nasa.gov/planetary/apod?concept_tags=True&api_key={}'.format(api_key)

	res = requests.get(url)
	return res.text