import requests
import json

class LastDownloader():
	"""A listening history downloader for Last.fm"""
	
	def __init__(self, username):
		"""Determine username and API key"""
		self.username = username
		self.api_key = input('Enter your API key: ')
		self.base_url = 'http://ws.audioscrobbler.com/2.0/?'
		
	def get_all_artists(self):
		"""Get all artists artists for account"""
		
		# Format API call
		request_params = {
			'limit': '1000',
			'method': 'library.getartists',
			'user': self.username,
			}
		request_url = self.format_api_request(request_params)
		
		# Send request
		r = requests.get(request_url)
		if r.status_code != 200:
			print("Error with request")
		response = r.json()
		
		# Display response
		print(json.dumps(response, indent=4, sort_keys=True))
		artists_list = response['artists']['artist']
		print(len(artists_list))
		
	def format_api_request(self, params_dict):
		"""Format API request"""
		base_url = ('http://ws.audioscrobbler.com/2.0/?format=json'
					'&api_key=' + self.api_key)
		for param, value in params_dict.items():
			base_url += '&' + param + '=' + value
		return base_url
		
download_user = LastDownloader('***REMOVED***')
download_user.get_all_artists()
