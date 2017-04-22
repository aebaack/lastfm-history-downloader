import unittest

#from csv_writer import CSVWriter
from track import Track

class CSVWriterTestCase(unittest.TestCase):
	"""Tests for csv_writer.py"""
	
	def setUp(self):
		"""Setup track to write to csv file"""
		artist = {
			'#text': 'David Bowie',
			'mbid': '5441c29d-3602-4898-b1a1-b77fa23b8e50',
			}
		album = ('The Rise and Fall of Ziggy Stardust and the Spiders'
				'from Mars')
		song = 'Five Years'
		mbid = '9c9345d9-a631-484b-b66b-4e78aa776cb3'
		
		self.track = Track(artist, album, song, mbid)
