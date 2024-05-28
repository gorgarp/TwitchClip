# Twitch Clip Bot

This bot allows users to create clips on specified Twitch channels via chat commands. It uses the Twitch API to capture and create clips and can be configured for multiple channels.

There are obviously other services that do this, but they are rate limited. If you host your own, you can do unlimited clipping (within reason).

## Features
- Create clips via chat command `!clip`
- Supports multiple Twitch channels
- Provides error messages if clip creation fails.

## Requirements
- Python 3.7+
- Twitch Developer account
- Access Token with the `clips:edit` scope

## Setup

### 1. Clone the Repository
```sh
git clone https://github.com/gorgarp/twitchclip.git
cd twitchclip
```

### 2. Create and Activate a Virtual Environment
```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```sh
pip install twitchio requests
```

### 4. Configure the Bot
Update the `clippy.py` script with your details:
- `CLIENT_ID`
- `ACCESS_TOKEN`
- `BOT_NICK`
- `CHANNELS`
- `BROADCASTER_IDS`

### 5. Obtain the Access Token

#### Register Your Application
1. Go to the [Twitch Developer Console](https://dev.twitch.tv/console/apps) and register a new application.
2. Set the OAuth Redirect URL to `https://oauth-redirect.cloudapp.net/` or any other valid redirect URL you control.
3. Note down your `Client ID` and `Client Secret`.

#### Generate the Access Token
1. Open the following URL in your browser, replacing `YOUR_CLIENT_ID` with your actual Client ID:
```
https://id.twitch.tv/oauth2/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=https://oauth-redirect.cloudapp.net/&response_type=token&scope=clips:edit
```
2. Authorize the application to access your Twitch account.
3. Copy the access token from the URL fragment (`#access_token=YOUR_ACCESS_TOKEN`).

### 6. Find the Broadcaster ID
Use the following script to find the broadcaster ID:
```python
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
```

### 7. Create a Systemd Service
Create a service file `/etc/systemd/system/clippy.service`:
```ini
[Unit]
Description=Twitch Clip Bot
After=network.target

[Service]
ExecStart=/path/to/venv/bin/python /path/to/twitchclip/clippy.py
WorkingDirectory=/path/to/twitchclip
StandardOutput=file:/var/log/clippy.log
StandardError=file:/var/log/clippy.err.log
Restart=always
User=root
Group=root

[Install]
WantedBy=multi-user.target
```

### 8. Enable and Start the Service
```sh
sudo systemctl daemon-reload
sudo systemctl start clippy.service
sudo systemctl enable clippy.service
sudo systemctl status clippy.service
```

## Usage
Once the bot is running, users can create clips by typing `!clip` in the configured Twitch channels. The bot will respond with a link to the created clip.

## Logs
- Standard output: `/var/log/clippy.log`
- Standard error: `/var/log/clippy.err.log`

## License
This project is licensed under the MIT License.

