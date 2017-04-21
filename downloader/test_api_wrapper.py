import unittest

from api_wrapper import APIWrapper

class APIWrapperTestCase(unittest.TestCase):
	"""Tests for api_wrapper.py"""
	
	def setUp(self):
		"""Setup username and API key"""
		self.username = 'rj'
		self.api_key = api_key
		self.lastfm_api = APIWrapper(self.api_key, self.username)
	
	def test_get_all_artists(self):
		"""Test get_all_artists method"""
		artists_list = self.lastfm_api.get_all_artists()
		first_artist = artists_list[0]

		self.assertTrue(len(artists_list) >= 10735)
		self.assertIn('name', first_artist)
		self.assertIn('playcount', first_artist)
		
	def test_get_all_artist_scrobbles(self):
		"""Test get_all_artist_scrobbles method"""
		track_list = self.lastfm_api.get_all_artist_scrobbles('Dr. Dre')
		first_track = track_list[0]
		
		self.assertTrue(len(track_list) >= 748)
		self.assertIn('name', first_track)
		self.assertIn('date', first_track)
		self.assertIn('artist', first_track)
		
		
api_key = input('Enter your API key: ')
print("These tests can take awhile, since the tested user"
		" has a lot of data...")

unittest.main()
