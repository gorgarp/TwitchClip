import twitchio
from twitchio.ext import commands
import requests
import logging

CLIENT_ID = 'your_client_id'
ACCESS_TOKEN = 'your_access_token'
BOT_NICK = 'YourBotName'
BOT_PREFIX = '!'
CHANNELS = ['channel1', 'channel2', 'channel3']
BROADCASTER_IDS = {
    'channel1': 'broadcaster_id1',
    'channel2': 'broadcaster_id2',
    'channel3': 'broadcaster_id3'
}

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=f"oauth:{ACCESS_TOKEN}",
                         client_id=CLIENT_ID,
                         nick=BOT_NICK,
                         prefix=BOT_PREFIX,
                         initial_channels=CHANNELS)
        logger.debug("Bot initialized")

    async def event_ready(self):
        logger.info(f"Logged in as {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return
        await self.handle_commands(message)

    @commands.command(name='clip')
    async def clip(self, ctx):
        clip_url, error_message = self.create_clip(ctx.channel.name)
        if clip_url:
            clip_url = clip_url.replace('/edit', '')
            await ctx.send(f"Clip created: {clip_url}")
        else:
            await ctx.send(f"Error creating clip: {error_message}")

    def create_clip(self, channel_name):
        broadcaster_id = BROADCASTER_IDS.get(channel_name)
        if not broadcaster_id:
            return None, "Invalid channel name."

        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Client-Id': CLIENT_ID,
        }
        response = requests.post(f'https://api.twitch.tv/helix/clips?broadcaster_id={broadcaster_id}', headers=headers)
        
        if response.status_code == 202:
            clip_data = response.json()
            return clip_data['data'][0]['edit_url'], None
        elif response.status_code == 401:
            return None, "Unauthorized. Please check your access token."
        elif response.status_code == 403:
            return None, "Forbidden. The bot may not have permission to create clips for this broadcaster."
        elif response.status_code == 404:
            return None, "Broadcaster not found."
        elif response.status_code == 429:
            return None, "Rate limit exceeded. Please try again later."
        else:
            return None, f"Unexpected error: {response.status_code}. {response.text}"

bot = Bot()
bot.run()
