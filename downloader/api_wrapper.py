import requests

class APIWrapper():
	"""Send API calls for determining scrobbles"""
	
	def __init__(self, api_key, username):
		"""Determine username and API key"""
		self.username = username
		self.api_key = api_key
		self.base_url = 'http://ws.audioscrobbler.com/2.0/?'
		
	def get_all_artists(self):
		"""Get all played artists for account"""		
		
		# Format API call and send request
		request_params = {
			'limit': '1000',
			'method': 'library.getartists',
			'user': self.username,
			}
		response = self.send_api_request(request_params)
		
		artists_list = response['artists']['artist']
		
		# A single request is limited to the first 1000 artists,
		# so additional calls may be needed to populate entire list
		total_info = response['artists']['@attr']
		while int(total_info['page']) < int(total_info['totalPages']):
			request_params['page'] = str(int(total_info['page'])+1)
			response = self.send_api_request(request_params)
			artists_list += response['artists']['artist']
			total_info = response['artists']['@attr']
		
		return artists_list
		
	def get_all_artist_scrobbles(self, artist):
		"""Get all scrobbles for an individual artist"""
		request_params = {
			'artist': artist,
			'method': 'user.getartisttracks',
			'user': self.username,
			}
		response = self.send_api_request(request_params)
		
		tracks_list = response['artisttracks']['track']
		
		while len(response['artisttracks']['track']) > 0:
			current_page = response['artisttracks']['@attr']['page']
			request_params['page'] = str(int(current_page)+1)
			response = self.send_api_request(request_params)
			tracks_list += response['artisttracks']['track']
		
		return tracks_list
		
	def format_api_request(self, params_dict):
		"""Format API request"""
		base_url = ('http://ws.audioscrobbler.com/2.0/?format=json'
					'&api_key=' + self.api_key)
		for param, value in params_dict.items():
			base_url += '&' + param + '=' + value
		return base_url
		
	def send_api_request(self, params_dict):
		"""Send API request with given parameters"""
		request_url = self.format_api_request(params_dict)
		r = requests.get(request_url)
		if r.status_code != 200:
			print("Error with request")
		return r.json()
