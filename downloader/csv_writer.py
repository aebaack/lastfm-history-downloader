import csv

class CSVWriter():
	"""Write tracks to a CSV file"""
	
	def __init__(self, file_path='./scrobbles.csv'):
		"""Initialize file name where data is saved"""
		self.file_path = file_path
		
	def add_tracks_to_csv(self, tracks_list, access_type):
		"""Append or write track list to csv file"""
		# Track number of successful tracks
		counter = 0
		
		with open(self.file_path, access_type) as csv_file:
			# Create writer object
			writer = csv.writer(csv_file)
			
			# Add column headings
			if access_type == 'w':
				writer.writerow(['Artist', 'Album', 'Album MBID',
								 'Song', 'Date', 'UTS'])

			# Write tracks to file
			for track in tracks_list:
				for play in track.plays:
					self.write_track_play_to_csv(writer, track, play)
					counter += 1
					
		return counter
		
	def override_previous_csv(self):
		"""Override previous files at given path"""
		f = open(self.file_path, 'w')
		f.close()
		
	def format_track(self, track, play):
		"""Format track for csv writing"""
		artist = track.artist['#text']
		album = track.album['#text']
		album_mbid = track.album['mbid']
		song = track.song
		time = play['#text']
		time_unix = play['uts']
		
		return [artist, album, album_mbid, song, time, time_unix]

	def write_track_play_to_csv(self, writer, track, play):
		"""Write track play to csv file"""
		formatted_track = self.format_track(track, play)
		writer.writerow(formatted_track)
