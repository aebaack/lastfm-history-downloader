from api_wrapper import APIWrapper

username = 'rj'
api_key = input('Enter your API key: ')

scrobbles = APIWrapper(api_key, username)
test = scrobbles.get_all_artist_scrobbles('Dr. Dre')
