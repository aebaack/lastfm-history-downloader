import csv
from os import remove
import unittest

from csv_writer import CSVWriter
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
				' from Mars')
		song = 'Five Years'
		mbid = '9c9345d9-a631-484b-b66b-4e78aa776cb3'
		play = {
			'uts': '0',
			'#text': '01 Jan 1970, 00:00',
			}
		
		track_1 = Track(artist, album, song, mbid)
		track_1.add_play(play)
		
		song = 'Soul Love'
		mbid = 'e8afe383-1478-497e-90b1-7885c7f37f6e'
		
		track_2 = Track(artist, album, song, mbid)
		track_2.add_play(play)
		
		self.track_list = [track_1, track_2]
		
		self.file_path = './scrobbles.csv'
		self.writer = CSVWriter(self.file_path)

	def test_write_tracks_to_csv(self):
		"""Test write_tracks_to_csv method"""
		logged_tracks = self.writer.write_tracks_to_csv(self.track_list)
		
		self.assertEqual(2, logged_tracks)
		
		with open(self.file_path, 'r') as csv_file:
			reader = csv.reader(csv_file)
			
			next(reader)
			first_track = next(reader)
			second_track = next(reader)
			
		self.assertIn('Five Years', first_track)
		self.assertIn('Soul Love', second_track)
			
		self.assertEqual(3, reader.line_num)
		
		remove(self.file_path)

unittest.main()
