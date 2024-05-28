# Twitch Clip Bot

This bot allows users to create clips on specified Twitch channels via chat commands. It uses the Twitch API to capture and create clips and can be configured for multiple channels.

## Features
- Create clips via chat command `!clip`
- Supports multiple Twitch channels

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

### 5. Find the Broadcaster ID
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

### 6. Create a Systemd Service
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

### 7. Enable and Start the Service
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
