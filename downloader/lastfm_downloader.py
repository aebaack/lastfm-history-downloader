from api_wrapper import APIWrapper
from csv_writer import CSVWriter

# Display information
print('\n =============== LAST.FM HISTORY DOWNLOADER ===============')
print(' == https://github.com/aebaack/lastfm-history-downloader ==')
print(' ==========================================================\n')

# Determine credentials
username = input(' Enter your last.fm username: ')
api_key = input(' Enter your API key: ')

# Create new instance of APIWrapper
scrobbles = APIWrapper(api_key, username)

print('\n - Searching for all artists in ' + username + "'s library")

# Traverse list of artists for user and create list of tracks
completed_tracks = []
all_artists = scrobbles.get_all_artists()
for artist in all_artists:
	# Get all scrobbles for individual artist
	name = artist['name']
	print('\n ' + name + ' -------------------------------------------')
	print(' - Searching for all songs by ' + name)
	artist_scrobbles = scrobbles.get_all_artist_scrobbles(name)
	
	# Traverse list of formatted scrobbles
	form_scrobbles = scrobbles.format_artist_tracks(artist_scrobbles)
	print(' - Searching for scrobble data for ' + 
			str(len(form_scrobbles)) + ' tracks')
	for track in form_scrobbles:
		# Get total scrobbles for track
		total_scrob = scrobbles.get_total_track_scrobbles(track)

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
		
# Write completed tracks to csv
print(' - Writing scrobbles to file')
writer = CSVWriter()
writer.write_tracks_to_csv(completed_tracks)
