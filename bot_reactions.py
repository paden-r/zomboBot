import os
import discord

from pathlib import Path
from dotenv import load_dotenv
from constants import PANIK, AMERICA

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

    this_message = message.content.lower()

    if 'omg' in this_message:
        await message.channel.send(PANIK)

    if 'america' in this_message:
        await message.channel.send(AMERICA)


client.run(TOKEN)
