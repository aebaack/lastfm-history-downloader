import csv

class CSVWriter():
	"""Write tracks to a CSV file"""
	
	def __init__(self, file_path='./scrobbles.csv'):
		"""Initialize file name where data is saved"""
		self.file_path = file_path
		
	def format_track(self, track, play):
		"""Format track for csv writing"""
		artist = track.artist['#text']
		album = track.album
		song = track.song
		time = play['#text']
		time_unix = play['uts']
		
		return [artist, album, song, time, time_unix]

	def write_track_play_to_csv(self, writer, track, play):
		"""Write track play to csv file"""
		formatted_track = self.format_track(track, play)
		writer.writerow(formatted_track)
		
	def write_tracks_to_csv(self, tracks_list):
		"""Write track list to csv file"""
		# Track number of successful tracks
		counter = 0

		# Write track information to csv at provided file path
		with open(self.file_path, 'w') as csv_file:
			# Create writer object and add column headings
			writer = csv.writer(csv_file)
			writer.writerow(['Artist', 'Album', 'Song', 'Date', 'UTS'])
			
			for track in tracks_list:
				for play in track.plays:
					self.write_track_play_to_csv(writer, track, play)
					counter += 1
				
				# Log progress
				print("Logged " + track.song + " by " +
						track.artist['#text'])
				
		return counter
