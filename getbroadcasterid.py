import requests

CLIENT_ID = 'your_client_id'
ACCESS_TOKEN = 'your_access_token'
USERNAME = 'streamer_name'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Client-Id': CLIENT_ID,
}

params = {
    'login': USERNAME
}

response = requests.get('https://api.twitch.tv/helix/users', headers=headers, params=params)
user_info = response.json()
print(user_info['data'][0]['id'])
