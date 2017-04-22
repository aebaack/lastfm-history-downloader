from api_wrapper import APIWrapper

username = 'rj'
api_key = input('Enter your API key: ')

scrobbles = APIWrapper(api_key, username)

completed_tracks = []
all_artists = scrobbles.get_all_artists()
for artist in all_artists:
	name = artist['name']
	artist_scrobbles = scrobbles.get_all_artist_scrobbles(name)
	
	form_scrobbles = scrobbles.format_artist_tracks(artist_scrobbles)
	for track in form_scrobbles:
		total_scrob = scrobbles.get_total_track_scrobbles(track)

		play = {
			'uts': '0',
			'#text': '01 Jan 1970, 00:00',
			}
		while len(track.plays) < total_scrob:
			track.add_play(play)
		
		completed_tracks.append(track)
		
		print('Completed ' + track.song + ' by ' + track.artist['#text'])
	break

print(completed_tracks)
