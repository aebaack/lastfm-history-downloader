import csv
import os.path

class CSVWriter():
	"""Write tracks to a CSV file"""
	
	def __init__(self, file_path='./scrobbles.csv'):
		"""Initialize file name where data is saved"""
		self.file_path = file_path
	
	def return_csv_writer(self):
		"""Return csv writer object"""
		access_mode = 'wb'
		if os.path.isfile(self.file_path):
			access_mode = 'ab'
			
		with open(self.file_path, access_mode) as csv_file:
			return csv.writer(csv_file)
	
	#def write_track_to_csv(self, track):
		
writer = CSVWriter()
