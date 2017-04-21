import unittest

from api_wrapper import APIWrapper

class APIWrapperTestCase(unittest.TestCase):
	"""Tests for api_wrapper.py"""
	
	def setUp(self):
		"""Setup username and API key"""
		username = 'rj'
		api_key = input('Enter your API key: ')
		self.lastfm_api = APIWrapper(api_key, username)
	
	def test_get_all_artists(self):
		"""Test get_all_artists method"""
		artists_list = self.lastfm_api.get_all_artists()
		first_artist = artists_list[0]

		self.assertTrue(len(artists_list) >= 10735)
		self.assertIn('name', first_artist)
		self.assertIn('playcount', first_artist)
		
unittest.main()
