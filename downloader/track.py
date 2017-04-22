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
