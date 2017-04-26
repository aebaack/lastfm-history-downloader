from lastfmhistory.api_wrapper import APIWrapper
from lastfmhistory.csv_writer import CSVWriter
from lastfmhistory.track import Track

def determine_credentials():
	"""Determine user credentials"""
	api_key = '9a5bb0d39039d14b7f3cfb2fafbabc73'

	username = input(' Enter your last.fm username: ')
	save_location = input(' Enter a file save location or press enter' +
		' for current directory: ')

	return {
		'api_key': api_key,
		'save_location': save_location,
		'username': username,
		}

def display_current_artist(artist_name):
	"""Display progress for current artist"""
	print('\n ' + artist_name + ' ' + '-'*(55 - len(artist_name)))

def display_introduction():
	"""Display opening instructions to the terminal"""
	print('\n =============== LAST.FM HISTORY DOWNLOADER =============')
	print(' = https://github.com/aebaack/lastfm-history-downloader =')
	print(' ========================================================\n')

def find_artist_songs(api_wrapper, artist):
	"""Search for songs by given artist and pull additional info"""
	# Display artist information
	name = artist['name']
	display_current_artist(name)
	print(' - Determining scrobbled tracks')
	
	# Determine scrobbling information for given artist
	artist_scrobbles = api_wrapper.get_all_artist_scrobbles(name)
	form_scrob = api_wrapper.format_artist_tracks(artist_scrobbles)
	
	# Display number of tracks to search for
	print(' - Searching for total scrobble count for ' + 
			str(len(form_scrob)) + ' tracks')
	
	# Traverse list of formatted scrobbles and total track play count
	completed_tracks = []
	for track in form_scrob:
		# Get total scrobbles for track
		total_scrob = api_wrapper.get_total_track_scrobbles(track)
		
		# Add additional plays until list of recent scrobbles is as
		# long as the list of total scrobbles
		# This ensures that imported scrobbles are not ignored
		play = {
			'uts': '0',
			'#text': '01 Jan 1970, 00:00',
			}
		while len(track.plays) < total_scrob:
			track.add_play(play)
		
		completed_tracks.append(track)
	
	# Search through top 100 for any missed tracks
	missed = search_artist_top_100(api_wrapper, completed_tracks, name)
	completed_tracks += missed
	
	return completed_tracks
	
def search_artist_top_100(api_wrapper, comp_tracks, artist):
	"""Search top 100 tracks by artist to find additional scrobbles"""
	# Determine total artist scrobbles to compare against logged amount
	total_art_scrob = api_wrapper.get_total_artist_scrobbles(artist)
	
	# Determine total completed scrobbles for the artist
	comp_count = 0
	for track in comp_tracks:
		comp_count += len(track.plays)
	
	# If logged amount is less than total, search through top tracks to
	# find additional missed scrobbles
	new_tracks = []
	if comp_count < total_art_scrob:
		print(' - Searching through top 100 songs to find any missed' +
				' tracks')
		top_tracks = api_wrapper.get_all_songs_by_artist(artist)
		
		counter = 0
		for track in top_tracks:
			track_already_completed = False
			
			for comp_track in comp_tracks:
				if track['name'] == comp_track.song:
					track_already_completed = True
					
			if not track_already_completed:
				new_track = Track({'#text': artist}, 'test', track['name'], '')
				total = api_wrapper.get_total_track_scrobbles(new_track)
				print(total)
				
				if total > 0:
					play = {
						'uts': '0',
						'#text': '01 Jan 1970, 00:00',
						}
					while len(new_track.plays) < total_scrob:
						new_track.add_play(play)
						counter += 1
						
					new_tracks.append(new_track)
		print(' - Found ' + str(counter) + ' plays out of the ' +
				'missing ' + str(total_art_scrob - comp_count))
	return new_tracks
			

def main():
	"""Download listening history for input user"""
	display_introduction()
	
	# Create new instance of APIWrapper
	user = determine_credentials()
	scrobbles = APIWrapper(user['api_key'], user['username'])
	
	# Determine list of all scrobbled artists for the user
	print('\n - Searching for all artists for ' + user['username'])
	all_artists = scrobbles.get_all_artists()
	print(' - Found ' + str(len(all_artists)) + ' artists')
	
	# Create new CSVWriter
	if user['save_location']:
		writer = CSVWriter(user['save_location'])
	else:
		writer = CSVWriter('./' + user['username'] + '.csv')
	writer.override_previous_csv()
	
	# Determine total listening history for each track
	all_tracks = []
	for artist in all_artists:
		artist_tracks = find_artist_songs(scrobbles, artist)
		writer.add_tracks_to_csv(artist_tracks, 'a')
		print(' - Writing ' + str(len(artist_tracks)) + ' scrobbles ' +
				'to ' + writer.file_path)

if __name__ == '__main__':
	main()
