from api_wrapper import APIWrapper

username = 'rj'
api_key = input('Enter your API key: ')

scrobbles = APIWrapper(api_key, username)

test = scrobbles.get_all_artist_scrobbles('David Bowie')
formatted = scrobbles.format_artist_tracks(test)

test = scrobbles.get_total_track_scrobbles(track=formatted[0].song, artist=formatted[0].artist['#text'])
print(test)
