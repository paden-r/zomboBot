import os
import discord

from pathlib import Path
from dotenv import load_dotenv
from constants import PANIK

dotenv_path = Path(".env_secret")
load_dotenv(dotenv_path=dotenv_path)
TOKEN = os.getenv('TOKEN')
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'omg' in message.content.lower():
        await message.channel.send(PANIK)


client.run(TOKEN)
