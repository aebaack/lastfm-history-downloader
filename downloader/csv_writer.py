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
	
	def return_csv_writer(self):
		"""Return csv writer object"""
		access_mode = 'w'
		if os.path.isfile(self.file_path):
			access_mode = 'ab'
			
		with open(self.file_path, access_mode) as csv_file:
			return csv.writer(csv_file)
	
	def write_track_play_to_csv(self, writer, track, play):
		"""Write track play to csv file"""
		formatted_track = self.format_track(track, play)
		writer.writerow(formatted_track)
		
	def write_tracks_to_csv(self, tracks_list):
		"""Write track list to csv file"""
		with open(self.file_path, 'w') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(['Artist', 'Album', 'Song', 'Date', 'UTS'])
			
			for track in tracks_list:
				for play in track.plays:
					self.write_track_play_to_csv(writer, track, play)
				print("Logged " + track.song + " by " +
						track.artist['#text'])
