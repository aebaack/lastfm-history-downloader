import requests

from track import Track

class APIWrapper():
	"""Send API calls for determining scrobbles"""
	
	def __init__(self, api_key, username):
		"""Initialize API credentials and URL"""
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
		
		# Format API call and send request
		request_params = {
			'limit': '200',
			'artist': artist,
			'method': 'user.getartisttracks',
			'user': self.username,
			}
		response = self.send_api_request(request_params)
		
		tracks_list = response['artisttracks']['track']
		
		# A single request is limited to the first 200 tracks,
		# so additional calls may be needed to populate entire list
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
		
	def format_artist_tracks(self, unform_list):
		"""Format tracks to a dictionary with a list of plays"""
		form_list = []
		
		for track_info in unform_list:
			
			# Find track in list or None if not found
			name = track_info['name']
			track = next((x for x in form_list if x.song == name), None)		
			if track:
				track.add_play(track_info['date'])
			else:
				# Create a new instance of Track and add to list
				artist = track_info['artist']
				album = track_info['album']
				mbid = track_info['mbid']
				song = track_info['name']
				
				new_track = Track(artist, album, song, mbid)
				new_track.add_play(track_info['date'])
				
				form_list.append(new_track)
				
		return form_list
		
	def send_api_request(self, params_dict):
		"""Send API request with given parameters"""
		request_url = self.format_api_request(params_dict)
		r = requests.get(request_url)
		if r.status_code != 200:
			print("Error with request")
		return r.json()
