from api_wrapper import APIWrapper
from csv_writer import CSVWriter

def determine_credentials():
	"""Determine user credentials"""
	username = input(' Enter your last.fm username: ')
	api_key = input(' Enter your API key: ')
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
	
	return completed_tracks

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
