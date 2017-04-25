import csv
from os import remove
import unittest

from lastfmhistory.csv_writer import CSVWriter
from lastfmhistory.track import Track

class CSVWriterTestCase(unittest.TestCase):
	"""Tests for csv_writer.py"""
	
	def setUp(self):
		"""Setup track to write to csv file"""
		# Create a track and add a play
		artist = {
			'#text': 'David Bowie',
			'mbid': '5441c29d-3602-4898-b1a1-b77fa23b8e50',
			}
		album = {
			'#text': ('The Rise and Fall of Ziggy Stardust and the'
						' Spiders from Mars'),
			'mbid': '6c9ae3dd-32ad-472c-96be-69d0a3536261',
			}
		song = 'Five Years'
		mbid = '9c9345d9-a631-484b-b66b-4e78aa776cb3'
		play = {
			'uts': '0',
			'#text': '01 Jan 1970, 00:00',
			}
		
		track_1 = Track(artist, album, song, mbid)
		track_1.add_play(play)
		
		# Create another track and add two plays
		song = 'Soul Love'
		mbid = 'e8afe383-1478-497e-90b1-7885c7f37f6e'
		
		track_2 = Track(artist, album, song, mbid)
		track_2.add_play(play)
		track_2.add_play(play)
		
		# Create track for appending
		song = 'Moonage Daydream'
		mbid = 'c0f27bed-7986-4c88-a9c6-1d16ebc9817b'
		
		self.track_3 = Track(artist, album, song, mbid)
		self.track_3.add_play(play)
		
		# Create track list and file writer
		self.track_list = [track_1, track_2]
		
		self.file_path = './scrobbles.csv'
		self.writer = CSVWriter(self.file_path)

	def test_append_tracks_to_csv(self):
		"""Test add_tracks_to_csv method with append access"""
		# Write previous tracks to file
		self.writer.add_tracks_to_csv(self.track_list, 'w')
		
		# Append new track to file
		self.writer.add_tracks_to_csv([self.track_3], 'a')
		
		# Read file to ensure data was written
		with open(self.file_path, 'r') as csv_file:
			reader = csv.reader(csv_file)
			
			next(reader)
			first_track = next(reader)
			second_track = next(reader)
			third_track = next(reader)
			fourth_track = next(reader)
			
		self.assertIn('Five Years', first_track)
		self.assertIn('Soul Love', second_track)
		self.assertIn('Soul Love', third_track)
		self.assertIn('Moonage Daydream', fourth_track)

	def test_write_single_track_to_csv(self):
		"""Test writing a single track"""
		# Log tracks to csv file
		track = self.writer.add_tracks_to_csv([self.track_list[0]], 'w')
		self.assertEqual(1, track)
		
		# Read file to ensure data was written
		with open(self.file_path, 'r') as csv_file:
			reader = csv.reader(csv_file)
			
			next(reader)
			first_track = next(reader)
		
		self.assertIn('Five Years', first_track)
		
		# Delete created file
		remove(self.file_path)

	def test_write_tracks_to_csv(self):
		"""Test add_tracks_to_csv method with write access"""
		# Log tracks to csv file
		log_tracks = self.writer.add_tracks_to_csv(self.track_list, 'w')
		self.assertEqual(3, log_tracks)
		
		# Read file to ensure data was written
		with open(self.file_path, 'r') as csv_file:
			reader = csv.reader(csv_file)
			
			next(reader)
			first_track = next(reader)
			second_track = next(reader)
			third_track = next(reader)
		
		self.assertIn('Five Years', first_track)
		self.assertIn('Soul Love', second_track)
		self.assertIn('Soul Love', third_track)
		
		# Delete created file
		remove(self.file_path)

unittest.main()
