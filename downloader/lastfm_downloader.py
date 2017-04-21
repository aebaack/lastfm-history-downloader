from api_wrapper import APIWrapper

username = 'rj'
api_key = input('Enter your API key: ')

scrobbles = APIWrapper(username, api_key)
print(scrobbles)
