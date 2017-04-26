import unittest

from lastfmhistory.api_wrapper import APIWrapper
from lastfmhistory.track import Track

class APIWrapperTestCase(unittest.TestCase):
	"""Tests for api_wrapper.py"""
	
	def setUp(self):
		"""Setup username and API key"""
		self.api_key = '9a5bb0d39039d14b7f3cfb2fafbabc73'
		self.username = 'rj'
		self.lastfm_api = APIWrapper(self.api_key, self.username)
	
	def test_get_all_artists(self):
		"""Test get_all_artists method"""
		# Get all artists for user and test properties of first artist
		artists_list = self.lastfm_api.get_all_artists()
		first_artist = artists_list[0]

		self.assertTrue(len(artists_list) >= 10735)
		self.assertIn('name', first_artist)
		self.assertIn('playcount', first_artist)
		
	def test_get_all_artist_scrobbles(self):
		"""Test get_all_artist_scrobbles method"""
		# Get all scrobbles by artist and test properties of first track
		track_list = self.lastfm_api.get_all_artist_scrobbles(
		'Dr. Dre')
		first_track = track_list[0]
		
		self.assertTrue(len(track_list) >= 748)
		self.assertIn('name', first_track)
		self.assertIn('date', first_track)
		self.assertIn('artist', first_track)
		
	def test_get_all_songs_by_artist(self):
		"""Test get_all_songs_by_artist method"""
		artist = 'Kanye West'
		top_tracks = self.lastfm_api.get_all_songs_by_artist(artist)
		
		first_track = top_tracks[0]
		second_track = top_tracks[1]
		
		self.assertTrue(first_track['name'] == 'Stronger')
		self.assertTrue(second_track['name'] == 'Heartless')
		
	def test_get_total_artist_scrobbles(self):
		"""Test get_total_artist_scrobbles method"""
		total = self.lastfm_api.get_total_artist_scrobbles('Metallica')
		
		self.assertTrue(total >= 878)
		
	def test_get_total_track_scrobbles(self):
		"""Test get_total_track_scrobbles method"""
		# Create a new track and test scrobble count
		artist = {
			'#text': 'David Bowie',
			'mbid': '5441c29d-3602-4898-b1a1-b77fa23b8e50',
			}
		album = ('The Rise and Fall of Ziggy Stardust and the Spiders'
				' from Mars')
		song = 'Five Years'
		mbid = '9c9345d9-a631-484b-b66b-4e78aa776cb3'
		
		track = Track(artist, album, song, mbid)
		total = self.lastfm_api.get_total_track_scrobbles(track)
		
		self.assertTrue(total >= 1)
		
	def test_format_api_request(self):
		"""Test format_api_request method"""
		request_params = {
			'album': 'Test && Test',
			'artist': 'Test & test ! Test',
			'limit': '200',
			}
		
		request = self.lastfm_api.format_api_request(request_params)
		
		# Test percent encoding
		self.assertIn('&album=Test%20%26%26%20Test', request)
		self.assertIn('&artist=Test%20%26%20test%20%21%20Test', request)
		
		# Test normal parameter
		self.assertIn('&limit=200', request)
		
	def test_format_artist_tracks(self):
		"""Test format_artist_tracks method"""
		track_list = self.lastfm_api.get_all_artist_scrobbles('Dr. Dre')
		track_objs = self.lastfm_api.format_artist_tracks(track_list)
		
		total_track_count = 0
		for track in track_objs:
			total_track_count += len(track.plays)
		
		self.assertEqual(total_track_count, len(track_list))
		
print("These tests can take awhile, since the tested user"
		" has a lot of data...")

unittest.main()
