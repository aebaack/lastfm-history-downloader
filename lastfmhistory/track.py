class Track():
	"""A Last.fm track with scrobbling data"""
	
	def __init__(self, artist, album, song, mbid):
		"""Initialize track attributes"""
		self.artist = artist
		self.album = album
		self.song = song
		self.mbid = mbid
		self.plays = []
		
	def add_play(self, play):
		"""Add a new play to the track"""
		self.plays.append(play)
		
	def add_imported_plays(self, amount_to_add):
		"""Add additional plays that have no date"""
		play = {
			'uts': '0',
			'#text': '01 Jan 1970, 00:00',
			}
		
		for _ in range(amount_to_add):
			self.add_play(play)
