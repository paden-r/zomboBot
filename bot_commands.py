import random
import os
import discord
from pathlib import Path
from discord.ext import commands
from dotenv import load_dotenv
from constants import (
    IMAGE_FILE,
    VIDEO_FILE,
    VIDEO_INDEX,
    IMAGE_INDEX
)
from utilities import (
    build_list,
    mark_as_used
)


class Zombot(commands.Bot):

    def __init__(self, **kwargs):
        default_commands = commands.DefaultHelpCommand(
            no_category="Common Commands"
        )

        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix=commands.when_mentioned_or('~'),
            description="A Bot for Zombocom",
            help_command=default_commands,
            case_insensitive=True,
            intents=intents,
            kwargs=kwargs
        )
        self.add_command(wednesday)
        self.add_command(dude)
        self.add_command(add_image)
        self.add_command(add_video)


@commands.command(name='dude', help='Responds with a random Wednesday video')
async def dude(ctx):
    videos = build_list(VIDEO_INDEX)
    response = random.choice(videos)
    mark_as_used(VIDEO_INDEX, response)
    await ctx.send(response)


@commands.command(name='wednesday', help='Responds with a Wednesday image')
async def wednesday(ctx):
    images = build_list(IMAGE_INDEX)
    response = random.choice(images)
    mark_as_used(IMAGE_INDEX, response)
    await ctx.send(response)


@commands.command(name='add_image', help='Adds image url to list of Wednesday images.  ~add_image [url to image]')
async def add_image(ctx, url=None):
    if url is not None:
        add_to_file(IMAGE_FILE, url)
        await ctx.send(f"added to the list")


@commands.command(name='add_video', help='Adds video url to list of Wednesday videos.  ~add_video [url to video]')
async def add_video(ctx, url=None):
    if url is not None:
        add_to_file(VIDEO_FILE, url)
        await ctx.send(f"added to the list")


def add_to_file(file_name, item):
    with open(file_name, 'w') as file_handle:
        file_handle.write(f"{item},")


if __name__ == "__main__":
    dotenv_path = Path(".env_secret")
    load_dotenv(dotenv_path=dotenv_path)
    TOKEN = os.getenv("TOKEN")
    bot = Zombot()
    bot.run(TOKEN)
