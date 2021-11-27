import os
import random
import os
from pathlib import Path
from discord.ext import commands
from dotenv import load_dotenv
from constants import WEDNESDAY, IMAGES, IMAGE_FILE, VIDEO_FILE
dotenv_path = Path(".env_secret")
load_dotenv(dotenv_path=dotenv_path)
TOKEN = os.getenv("TOKEN")
channel_id = int(os.getenv("CHANNEL_ALPY"))

default_commands = commands.DefaultHelpCommand(
    no_category = "Common Commands"
)

bot = commands.Bot(
    command_prefix = commands.when_mentioned_or('~'),
    description="A Bot for Zombocom",
    help_command=default_commands
)

@bot.command(name='dude', help='Responds with a random Wednesday video')
async def dude(ctx):
    videos = build_video_list()
    response = random.choice(videos)
    await ctx.send(response)

@bot.command(name='wednesday', help='Responds with a Wednesday image')
async def wednesday(ctx):
    images = build_image_list()
    response = random.choice(images)
    await ctx.send(response)

@bot.command(name='add_image', help='Adds image url to list of Wednesday images.  ~add_image [url to image]')
async def add_image(ctx, url=None):
    if url is not None:
        add_to_file(IMAGE_FILE, url)
        await ctx.send(f"added to the list")

@bot.command(name='add_video', help='Adds video url to list of Wednesday videos.  ~add_video [url to video]')
async def add_video(ctx, url=None):
    if url is not None:
        add_to_file(VIDEO_FILE, url)
        await ctx.send(f"added to the list")

def add_to_file(file_name, item):
    with open(file_name, 'w') as file_handle:
        file_handle.write(f"{item},")

def build_image_list():
    image_list = IMAGES
    additional_images = None
    try:
        with open(IMAGE_FILE, 'r') as file_handle:
           additional_images = file_handle.read()
    except FileNotFoundError:
        pass
    if additional_images:
        image_list.extend([x for x in additional_images.split(',') if x])
    print(image_list)
    return image_list

def build_video_list():
    video_list = WEDNESDAY
    additional_videos = None
    try:
        with open(VIDEO_FILE, 'r') as file_handle:
            additional_videos = file_handle.read()
    except FileNotFoundError:
        pass
    if additional_videos:
        video_list.extend([x for x in additional_videos.split(',') if x])
    return video_list

bot.run(TOKEN)