from api_wrapper import APIWrapper
from csv_writer import CSVWriter

# Determine credentials
username = 'rj'
api_key = input('Enter your API key: ')

# Create new instance of APIWrapper
scrobbles = APIWrapper(api_key, username)

# Traverse list of artists for user and create list of tracks
completed_tracks = []
all_artists = scrobbles.get_all_artists()
for artist in all_artists:
	counter = counter + 1
	# Get all scrobbles for individual artist
	name = artist['name']
	artist_scrobbles = scrobbles.get_all_artist_scrobbles(name)
	
	# Traverse list of formatted scrobbles
	form_scrobbles = scrobbles.format_artist_tracks(artist_scrobbles)
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
		
		print('Completed ' + track.song + ' by ' + track.artist['#text'])
	break

# Write completed tracks to csv
writer = CSVWriter()
writer.write_tracks_to_csv(completed_tracks)
