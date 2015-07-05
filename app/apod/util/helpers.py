def pic2data(pic_data):
	data = {}
	data['title'] = pic_data['title']
	data['media_url'] = pic_data['url']
	data['media_type'] = pic_data['media_type']
	data['explanation'] = pic_data['explanation']
	return data