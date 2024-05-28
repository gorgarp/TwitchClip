import twitchio
from twitchio.ext import commands
import requests

# Configuration variables
CLIENT_ID = 'your_client_id'
ACCESS_TOKEN = 'your_access_token'
BOT_NICK = 'your_bot_username'
BOT_PREFIX = '!'
CHANNELS = ['channel1', 'channel2']  # List of channels
BROADCASTER_IDS = {
    'channel1': 'broadcaster_id1',
    'channel2': 'broadcaster_id2',
}

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=f"oauth:{ACCESS_TOKEN}",
                         client_id=CLIENT_ID,
                         nick=BOT_NICK,
                         prefix=BOT_PREFIX,
                         initial_channels=CHANNELS)

    async def event_ready(self):
        print(f"Logged in as {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return
        await self.handle_commands(message)

    @commands.command(name='clip')
    async def clip(self, ctx):
        channel = ctx.channel.name
        clip_url = self.create_clip(channel)
        if "Error" not in clip_url:
            clip_url = clip_url.replace('/edit', '')
            await ctx.send(f"Clip created: {clip_url}")
        else:
            await ctx.send(clip_url)

    def create_clip(self, channel):
        broadcaster_id = BROADCASTER_IDS.get(channel)
        if not broadcaster_id:
            return "Error: Unknown channel"

        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Client-Id': CLIENT_ID,
        }
        response = requests.post(f'https://api.twitch.tv/helix/clips?broadcaster_id={broadcaster_id}', headers=headers)
        if response.status_code == 202:
            clip_data = response.json()
            return clip_data['data'][0]['edit_url']
        else:
            return f"Error creating clip: {response.text}"

bot = Bot()
bot.run()
